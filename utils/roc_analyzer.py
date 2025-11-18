#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROC Analyzer per TextAnalyzer
Analisi completa ROC e Precision-Recall per valutazione modelli
Include: ROC Curves, AUC, Optimal Threshold, Model Comparison
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, average_precision_score,
    f1_score, accuracy_score, precision_score, recall_score,
    confusion_matrix, roc_auc_score
)
from datetime import datetime
import json
import os


class ROCAnalyzer:
    """Analizzatore ROC per valutazione modelli AI detection"""

    def __init__(self):
        self.name = "ROCAnalyzer"
        self.analysis_history = []

    def analyze_model_performance(self, y_true: List[int], y_scores: List[float],
                                model_name: str = "Model") -> Dict[str, Any]:
        """
        Analisi completa delle performance del modello

        Args:
            y_true: True labels (0=human, 1=ai)
            y_scores: Predicted probabilities for AI class
            model_name: Nome del modello

        Returns:
            Dict completo con tutte le metriche
        """
        y_true = np.array(y_true)
        y_scores = np.array(y_scores)

        # 1. ROC Curve Analysis
        fpr, tpr, roc_thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)

        # 2. Precision-Recall Analysis
        precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores)
        pr_auc = average_precision_score(y_true, y_scores)

        # 3. Trova soglie ottimali con diversi criteri
        optimal_thresholds = self._find_optimal_thresholds(
            fpr, tpr, roc_thresholds, precision, recall, pr_thresholds
        )

        # 4. Valuta performance a diverse soglie
        threshold_evaluations = self._evaluate_thresholds(
            y_true, y_scores, optimal_thresholds
        )

        # 5. Calcola metriche complete
        performance_summary = {
            'model_name': model_name,
            'total_samples': len(y_true),
            'ai_samples': sum(y_true),
            'human_samples': len(y_true) - sum(y_true),
            'ai_ratio': sum(y_true) / len(y_true)
        }

        # 6. ROC Metrics
        roc_metrics = {
            'auc': roc_auc,
            'auc_interpretation': self._interpret_auc(roc_auc),
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'thresholds': roc_thresholds.tolist()
        }

        # 7. PR Metrics
        pr_metrics = {
            'auc_pr': pr_auc,
            'auc_pr_interpretation': self._interpret_pr_auc(pr_auc),
            'precision': precision.tolist(),
            'recall': recall.tolist(),
            'pr_thresholds': pr_thresholds.tolist()
        }

        # 8. Best thresholds
        thresholds = {
            'youden_index': optimal_thresholds['youden'],
            'f1_optimal': optimal_thresholds['f1'],
            'precision_recall_optimal': optimal_thresholds['pr'],
            'balanced_accuracy': optimal_thresholds['balanced_acc']
        }

        # 9. Performance a soglie ottimali
        performance_at_thresholds = threshold_evaluations

        # 10. Distributional analysis
        distribution = self._analyze_score_distribution(y_true, y_scores)

        # Combina tutto
        result = {
            'timestamp': datetime.now().isoformat(),
            'summary': performance_summary,
            'roc_analysis': roc_metrics,
            'pr_analysis': pr_metrics,
            'optimal_thresholds': thresholds,
            'threshold_performance': performance_at_thresholds,
            'distribution_analysis': distribution,
            'recommendations': self._generate_recommendations(
                roc_auc, pr_auc, performance_at_thresholds
            )
        }

        self.analysis_history.append(result)
        return result

    def _find_optimal_thresholds(self, fpr: np.ndarray, tpr: np.ndarray,
                                roc_thresholds: np.ndarray,
                                precision: np.ndarray, recall: np.ndarray,
                                pr_thresholds: np.ndarray) -> Dict[str, float]:
        """Trova soglie ottimali con diversi criteri"""

        # 1. Youden's J Statistic (TPR - FPR)
        j_scores = tpr - fpr
        youden_idx = np.argmax(j_scores)
        youden_threshold = roc_thresholds[youden_idx]

        # 2. F1-Score ottimale
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
        f1_idx = np.argmax(f1_scores)
        f1_threshold = pr_thresholds[f1_idx]
        f1_max = f1_scores[f1_idx]

        # 3. Balanced Accuracy ottimale
        balanced_accs = []
        for thresh in roc_thresholds:
            y_pred = (y_scores >= thresh).astype(int)
            acc = accuracy_score(y_true, y_pred)
            balanced_accs.append(acc)

        bal_idx = np.argmax(balanced_accs)
        bal_threshold = roc_thresholds[bal_idx]

        # 4. Precision-Recall optimal (F0.5 score)
        f05_scores = (1 + 0.5**2) * (precision * recall) / (0.5**2 * precision + recall + 1e-10)
        pr_idx = np.argmax(f05_scores)
        pr_threshold = pr_thresholds[pr_idx]

        return {
            'youden': float(youden_threshold),
            'f1': float(f1_threshold),
            'pr': float(pr_threshold),
            'balanced_acc': float(bal_threshold),
            'f1_max': float(f1_max)
        }

    def _evaluate_thresholds(self, y_true: np.ndarray, y_scores: np.ndarray,
                           thresholds: Dict[str, float]) -> Dict[str, Any]:
        """Valuta performance a soglie specifiche"""
        results = {}

        for criterion, thresh_val in thresholds.items():
            if criterion == 'f1_max':
                continue

            # Crea predictions usando la soglia
            # Nota: questa è una versione semplificata
            # In pratica dovresti passare anche la soglia specifica
            # Per ora usiamo una stima basata sui valori
            pred_score = np.mean(y_scores)  # Score medio come proxy
            y_pred = (pred_score >= thresh_val).astype(int)

            # Per il test, creiamo dati dummy per le metriche
            if criterion == 'youden':
                y_pred = (y_scores >= thresh_val).astype(int)
            elif criterion == 'f1':
                y_pred = (y_scores >= thresh_val).astype(int)
            elif criterion == 'balanced_acc':
                y_pred = (y_scores >= thresh_val).astype(int)
            elif criterion == 'pr':
                y_pred = (y_scores >= thresh_val).astype(int)

            metrics = {
                'threshold': float(thresh_val),
                'accuracy': accuracy_score(y_true, y_pred),
                'precision': precision_score(y_true, y_pred),
                'recall': recall_score(y_true, y_pred),
                'f1_score': f1_score(y_true, y_pred),
                'specificity': self._calculate_specificity(y_true, y_pred),
                'sensitivity': recall_score(y_true, y_pred),
                'tn': int(sum((y_true == 0) & (y_pred == 0))),
                'fp': int(sum((y_true == 0) & (y_pred == 1))),
                'fn': int(sum((y_true == 1) & (y_pred == 0))),
                'tp': int(sum((y_true == 1) & (y_pred == 1)))
            }

            results[criterion] = metrics

        return results

    def _calculate_specificity(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calcola specificity (TNR)"""
        tn = sum((y_true == 0) & (y_pred == 0))
        fp = sum((y_true == 0) & (y_pred == 1))
        return tn / (tn + fp) if (tn + fp) > 0 else 0

    def _analyze_score_distribution(self, y_true: np.ndarray,
                                  y_scores: np.ndarray) -> Dict[str, Any]:
        """Analizza distribuzione degli score"""

        ai_scores = y_scores[y_true == 1]
        human_scores = y_scores[y_true == 0]

        return {
            'ai_scores': {
                'mean': float(np.mean(ai_scores)),
                'std': float(np.std(ai_scores)),
                'min': float(np.min(ai_scores)),
                'max': float(np.max(ai_scores)),
                'median': float(np.median(ai_scores)),
                'q25': float(np.percentile(ai_scores, 25)),
                'q75': float(np.percentile(ai_scores, 75))
            },
            'human_scores': {
                'mean': float(np.mean(human_scores)),
                'std': float(np.std(human_scores)),
                'min': float(np.min(human_scores)),
                'max': float(np.max(human_scores)),
                'median': float(np.median(human_scores)),
                'q25': float(np.percentile(human_scores, 25)),
                'q75': float(np.percentile(human_scores, 75))
            },
            'separation': {
                'mean_difference': float(np.mean(ai_scores) - np.mean(human_scores)),
                'overlap': self._calculate_overlap(ai_scores, human_scores)
            }
        }

    def _calculate_overlap(self, ai_scores: np.ndarray,
                         human_scores: np.ndarray) -> float:
        """Calcola overlap tra distribuzioni (approssimazione)"""
        # Semplice stima di overlap basata su deviazioni standard
        ai_mean, ai_std = np.mean(ai_scores), np.std(ai_scores)
        human_mean, human_std = np.mean(human_scores), np.std(human_scores)

        # Sovrapposizione approssimativa
        overlap = 0.5 * (
            (human_mean - ai_mean) / np.sqrt(0.5 * (ai_std**2 + human_std**2)) + 1
        )
        return max(0.0, min(1.0, overlap))

    def _interpret_auc(self, auc_value: float) -> str:
        """Interpreta valore AUC"""
        if auc_value >= 0.95:
            return "Eccellente (Quasi perfetto)"
        elif auc_value >= 0.9:
            return "Ottimo"
        elif auc_value >= 0.8:
            return "Buono"
        elif auc_value >= 0.7:
            return "Discreto"
        elif auc_value >= 0.6:
            return "Scarso"
        else:
            return "Molto scarso (Vicino al caso)"

    def _interpret_pr_auc(self, pr_auc: float) -> str:
        """Interpreta PR AUC"""
        if pr_auc >= 0.9:
            return "Eccellente"
        elif pr_auc >= 0.8:
            return "Buono"
        elif pr_auc >= 0.7:
            return "Discreto"
        elif pr_auc >= 0.6:
            return "Scarso"
        else:
            return "Molto scarso"

    def _generate_recommendations(self, roc_auc: float, pr_auc: float,
                                performance: Dict[str, Any]) -> List[str]:
        """Genera raccomandazioni basate su performance"""
        recommendations = []

        # ROC AUC recommendations
        if roc_auc < 0.7:
            recommendations.append(
                "ROC AUC basso. Considera: feature engineering, ensemble methods, o diverso algoritmo."
            )
        elif roc_auc > 0.9:
            recommendations.append(
                "ROC AUC eccellente! Il modello ha ottima discriminazione."
            )

        # PR AUC recommendations
        if pr_auc < 0.6:
            recommendations.append(
                "PR AUC basso. Il modello fatica con classe AI. Bilanciamento dataset raccomandato."
            )
        elif pr_auc > 0.8:
            recommendations.append(
                "PR AUC molto buono. Ottima performance su classe AI."
            )

        # Balanced Accuracy
        best_balanced = None
        for p in performance.values():
            if isinstance(p, dict) and 'balanced_accuracy' in p:
                if best_balanced is None or p['balanced_accuracy'] > best_balanced:
                    best_balanced = p['balanced_accuracy']

        if best_balanced is not None and best_balanced < 0.7:
            recommendations.append(
                "Balanced Accuracy bassa. Soglia non ottimale o problema di bias."
            )

        # Default recommendation
        recommendations.append(
            "Continua a monitorare precisione e recall per evitare bias."
        )

        return recommendations

    def compare_models(self, model_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Confronta più modelli"""
        if len(model_results) < 2:
            return {'error': 'Need at least 2 models to compare'}

        comparison = {
            'models': [],
            'ranking': {
                'by_auc': [],
                'by_f1': [],
                'by_accuracy': []
            },
            'best_model': {},
            'insights': []
        }

        for result in model_results:
            model_name = result['summary']['model_name']

            # Estrai metriche principali
            roc_auc = result['roc_analysis']['auc']
            best_f1 = max(
                p.get('f1_score', 0) for p in result['threshold_performance'].values()
            )
            best_acc = max(
                p.get('accuracy', 0) for p in result['threshold_performance'].values()
            )

            comparison['models'].append({
                'name': model_name,
                'auc': roc_auc,
                'best_f1': best_f1,
                'best_accuracy': best_acc
            })

        # Crea rankings
        comparison['ranking']['by_auc'] = sorted(
            comparison['models'], key=lambda x: x['auc'], reverse=True
        )
        comparison['ranking']['by_f1'] = sorted(
            comparison['models'], key=lambda x: x['best_f1'], reverse=True
        )
        comparison['ranking']['by_accuracy'] = sorted(
            comparison['models'], key=lambda x: x['best_accuracy'], reverse=True
        )

        # Best overall (media dei ranking)
        scores = {}
        for model in comparison['models']:
            name = model['name']
            auc_rank = next(i for i, m in enumerate(comparison['ranking']['by_auc']) if m['name'] == name)
            f1_rank = next(i for i, m in enumerate(comparison['ranking']['by_f1']) if m['name'] == name)
            acc_rank = next(i for i, m in enumerate(comparison['ranking']['by_accuracy']) if m['name'] == name)

            # Score più basso = migliore
            scores[name] = auc_rank + f1_rank + acc_rank

        best_model_name = min(scores.keys(), key=lambda x: scores[x])
        comparison['best_model'] = {
            'name': best_model_name,
            'rank_score': scores[best_model_name]
        }

        return comparison

    def export_roc_report(self, result: Dict[str, Any],
                         filename: str = "roc_analysis.json"):
        """Esporta report ROC completo"""
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"💾 ROC analysis saved to: {filepath}")
        return filepath


# Test
if __name__ == "__main__":
    # Genera dati di test
    np.random.seed(42)
    y_true = np.random.binomial(1, 0.5, 100)  # 50% AI, 50% Human
    y_scores = np.random.beta(
        y_true * 3 + 1,  # Bias verso classe corretta
        (1 - y_true) * 3 + 1,
        100
    )

    analyzer = ROCAnalyzer()

    # Analizza
    result = analyzer.analyze_model_performance(y_true, y_scores, "TestModel")

    print("ROC Analysis Results:")
    print(f"  AUC: {result['roc_analysis']['auc']:.4f}")
    print(f"  AUC Interpretation: {result['roc_analysis']['auc_interpretation']}")
    print(f"  PR AUC: {result['pr_analysis']['auc_pr']:.4f}")

    print("\nOptimal Thresholds:")
    for name, thresh in result['optimal_thresholds'].items():
        if name != 'f1_max':
            print(f"  {name}: {thresh:.4f}")

    print("\nPerformance at thresholds:")
    for name, perf in result['threshold_performance'].items():
        print(f"  {name}:")
        print(f"    Accuracy: {perf['accuracy']:.4f}")
        print(f"    F1-Score: {perf['f1_score']:.4f}")
        print(f"    Precision: {perf['precision']:.4f}")
        print(f"    Recall: {perf['recall']:.4f}")

    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")

    analyzer.export_roc_report(result)
    print("\n✅ ROC analysis complete!")
