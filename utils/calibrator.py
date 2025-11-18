#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calibratore Automatico per TextAnalyzer
Calibra soglie e parametri del sistema ensemble usando il dataset di validazione
Include: Grid Search, ROC Analysis, Optimizzazione F1-Score
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import itertools
from dataclasses import dataclass
from sklearn.metrics import roc_curve, auc, precision_recall_curve, f1_score, accuracy_score
import os

@dataclass
class CalibrationResult:
    """Risultati della calibrazione"""
    best_thresholds: Dict[str, float]
    best_f1_score: float
    best_accuracy: float
    roc_auc: float
    pr_auc: float
    confusion_matrix: Dict[str, int]
    detailed_metrics: Dict[str, Any]
    timestamp: str


class EnsembleCalibrator:
    """Calibratore per sistemi ensemble"""

    def __init__(self, ensemble_analyzer):
        self.ensemble = ensemble_analyzer
        self.calibration_results = []
        self.best_parameters = None

    def calibrate_on_dataset(self, dataset_path: str = "data/validation_dataset.json",
                           method: str = "grid_search") -> CalibrationResult:
        """
        Calibra i parametri dell'ensemble su un dataset

        Args:
            dataset_path: Percorso al dataset JSON
            method: Metodo di calibrazione ('grid_search', 'roc_optimization')

        Returns:
            CalibrationResult con parametri ottimali
        """
        print(f"🎯 Starting calibration with method: {method}")
        print(f"📊 Loading dataset: {dataset_path}")

        # Carica dataset
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        print(f"✅ Loaded {len(dataset)} samples")
        print(f"   Human: {sum(1 for d in dataset if d['label'] == 'human')}")
        print(f"   AI: {sum(1 for d in dataset if d['label'] == 'ai')}")

        # Esegui analisi su tutto il dataset
        print("\n🔄 Running ensemble analysis on dataset...")
        predictions = []
        for item in dataset:
            text = item['text']
            true_label = 1 if item['label'] == 'ai' else 0  # 1=AI, 0=Human

            result = self.ensemble.analyze(text)
            ai_prob = result['ensemble_result']['ai_probability']

            predictions.append({
                'true_label': true_label,
                'ai_probability': ai_prob,
                'confidence': result['overall_confidence'],
                'text_id': item['id'],
                'text_length': item['length']
            })

        print(f"✅ Analysis complete: {len(predictions)} predictions")

        # Calibra in base al metodo scelto
        if method == "grid_search":
            result = self._grid_search_calibration(predictions)
        elif method == "roc_optimization":
            result = self._roc_optimization(predictions)
        else:
            raise ValueError(f"Unknown calibration method: {method}")

        self.calibration_results.append(result)
        self.best_parameters = result.best_thresholds

        print(f"\n✅ Calibration complete!")
        print(f"   Best F1-Score: {result.best_f1_score:.4f}")
        print(f"   Best Accuracy: {result.best_accuracy:.4f}")
        print(f"   ROC AUC: {result.roc_auc:.4f}")

        return result

    def _grid_search_calibration(self, predictions: List[Dict[str, Any]]) -> CalibrationResult:
        """Grid search per trovare soglie ottimali"""
        print("\n🔍 Running Grid Search...")

        # Estrai true labels e probabilities
        y_true = np.array([p['true_label'] for p in predictions])
        y_scores = np.array([p['ai_probability'] for p in predictions])

        # Crea griglia di soglie da testare
        thresholds = np.arange(0.1, 0.9, 0.05)
        best_f1 = 0
        best_thresholds = {}
        best_metrics = {}

        print(f"   Testing {len(thresholds)} threshold values...")

        for threshold in thresholds:
            # Applica soglia
            y_pred = (y_scores >= threshold).astype(int)

            # Calcola metriche
            f1 = f1_score(y_true, y_pred)
            acc = accuracy_score(y_true, y_pred)

            # Traccia best
            if f1 > best_f1:
                best_f1 = f1
                best_thresholds = {'ai_threshold': threshold}
                best_metrics = {
                    'f1_score': f1,
                    'accuracy': acc,
                    'threshold': threshold,
                    'predictions_count': len(y_pred),
                    'positive_predictions': sum(y_pred),
                    'true_positives': sum((y_true == 1) & (y_pred == 1))
                }

        # Calcola metriche avanzate
        fpr, tpr, roc_thresholds = roc_curve(y_true, y_scores)
        roc_auc_score = auc(fpr, tpr)

        precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores)
        pr_auc_score = auc(recall, precision)

        # Confusion matrix finale
        final_pred = (y_scores >= best_thresholds['ai_threshold']).astype(int)
        tp = sum((y_true == 1) & (final_pred == 1))
        fp = sum((y_true == 0) & (final_pred == 1))
        tn = sum((y_true == 0) & (final_pred == 0))
        fn = sum((y_true == 1) & (final_pred == 0))

        return CalibrationResult(
            best_thresholds=best_thresholds,
            best_f1_score=best_f1,
            best_accuracy=best_metrics['accuracy'],
            roc_auc=roc_auc_score,
            pr_auc=pr_auc_score,
            confusion_matrix={
                'true_positive': int(tp),
                'false_positive': int(fp),
                'true_negative': int(tn),
                'false_negative': int(fn)
            },
            detailed_metrics={
                'grid_search_results': best_metrics,
                'roc_curve': {
                    'fpr': fpr.tolist(),
                    'tpr': tpr.tolist(),
                    'thresholds': roc_thresholds.tolist()
                },
                'precision_recall': {
                    'precision': precision.tolist(),
                    'recall': recall.tolist(),
                    'thresholds': pr_thresholds.tolist()
                }
            },
            timestamp=datetime.now().isoformat()
        )

    def _roc_optimization(self, predictions: List[Dict[str, Any]]) -> CalibrationResult:
        """Calibrazione usando ROC curve"""
        print("\n📈 Running ROC-based Optimization...")

        y_true = np.array([p['true_label'] for p in predictions])
        y_scores = np.array([p['ai_probability'] for p in predictions])

        # Calcola ROC curve
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)

        # Trova soglia ottimale (Youden's J statistic)
        j_scores = tpr - fpr
        best_idx = np.argmax(j_scores)
        optimal_threshold = thresholds[best_idx]

        # Applica soglia ottimale
        y_pred = (y_scores >= optimal_threshold).astype(int)

        best_f1 = f1_score(y_true, y_pred)
        best_acc = accuracy_score(y_true, y_pred)

        # Confusion matrix
        tp = sum((y_true == 1) & (y_pred == 1))
        fp = sum((y_true == 0) & (y_pred == 1))
        tn = sum((y_true == 0) & (y_pred == 0))
        fn = sum((y_true == 1) & (y_pred == 0))

        # Precision-Recall AUC
        precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores)
        pr_auc = auc(recall, precision)

        return CalibrationResult(
            best_thresholds={'ai_threshold': float(optimal_threshold)},
            best_f1_score=best_f1,
            best_accuracy=best_acc,
            roc_auc=roc_auc,
            pr_auc=pr_auc,
            confusion_matrix={
                'true_positive': int(tp),
                'false_positive': int(fp),
                'true_negative': int(tn),
                'false_negative': int(fn)
            },
            detailed_metrics={
                'roc_auc': float(roc_auc),
                'optimal_threshold': float(optimal_threshold),
                'youden_index': float(j_scores[best_idx]),
                'precision': float(precision[1]) if len(precision) > 1 else 0.0,
                'recall': float(recall[1]) if len(recall) > 1 else 0.0,
                'specificity': float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0,
                'sensitivity': float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
            },
            timestamp=datetime.now().isoformat()
        )

    def apply_calibration(self, text: str) -> Dict[str, Any]:
        """Applica parametri calibrati a una nuova prediction"""
        if not self.best_parameters:
            raise ValueError("No calibration parameters available. Run calibrate_on_dataset first.")

        result = self.ensemble.analyze(text)

        # Applica soglia calibrata
        calibrated_threshold = self.best_parameters.get('ai_threshold', 0.5)
        ai_prob = result['ensemble_result']['ai_probability']

        # Re-classifica con soglia calibrata
        if ai_prob >= calibrated_threshold:
            calibrated_classification = "AI (Calibrated)"
            calibrated_confidence = ai_prob
        else:
            calibrated_classification = "Human (Calibrated)"
            calibrated_confidence = 1.0 - ai_prob

        # Aggiungi metadati calibrazione
        result['calibration'] = {
            'applied': True,
            'calibrated_threshold': calibrated_threshold,
            'original_classification': result['ensemble_result']['classification'],
            'calibrated_classification': calibrated_classification,
            'calibrated_confidence': calibrated_confidence,
            'calibration_improvement': abs(ai_prob - 0.5)  # Quanto siamo lontani dalla soglia
        }

        return result

    def cross_validate(self, dataset_path: str = "data/validation_dataset.json",
                      folds: int = 5) -> Dict[str, Any]:
        """Cross-validation per validare robustezza"""
        print(f"\n🔄 Running {folds}-fold Cross-Validation...")

        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)

        # Shuffle dataset
        np.random.seed(42)
        indices = np.random.permutation(len(dataset))

        fold_size = len(dataset) // folds
        cv_scores = {
            'f1_scores': [],
            'accuracies': [],
            'roc_aucs': []
        }

        for fold in range(folds):
            # Split train/test
            start = fold * fold_size
            end = start + fold_size if fold < folds - 1 else len(dataset)
            test_indices = indices[start:end]
            train_indices = np.concatenate([indices[:start], indices[end:]])

            train_set = [dataset[i] for i in train_indices]
            test_set = [dataset[i] for i in test_indices]

            # Analizza test set
            y_true = []
            y_scores = []

            for item in test_set:
                result = self.ensemble.analyze(item['text'])
                y_true.append(1 if item['label'] == 'ai' else 0)
                y_scores.append(result['ensemble_result']['ai_probability'])

            # Calcola metriche
            threshold = self.best_parameters.get('ai_threshold', 0.5) if self.best_parameters else 0.5
            y_pred = (np.array(y_scores) >= threshold).astype(int)

            fold_f1 = f1_score(y_true, y_pred)
            fold_acc = accuracy_score(y_true, y_pred)

            # ROC AUC
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            fold_auc = auc(fpr, tpr)

            cv_scores['f1_scores'].append(fold_f1)
            cv_scores['accuracies'].append(fold_acc)
            cv_scores['roc_aucs'].append(fold_auc)

            print(f"   Fold {fold+1}: F1={fold_f1:.4f}, Acc={fold_acc:.4f}, AUC={fold_auc:.4f}")

        # Statistiche finali
        cv_summary = {
            'mean_f1': np.mean(cv_scores['f1_scores']),
            'std_f1': np.std(cv_scores['f1_scores']),
            'mean_accuracy': np.mean(cv_scores['accuracies']),
            'std_accuracy': np.std(cv_scores['accuracies']),
            'mean_auc': np.mean(cv_scores['roc_aucs']),
            'std_auc': np.std(cv_scores['roc_aucs']),
            'per_fold_scores': cv_scores
        }

        print(f"\n✅ Cross-Validation Results:")
        print(f"   F1-Score: {cv_summary['mean_f1']:.4f} ± {cv_summary['std_f1']:.4f}")
        print(f"   Accuracy: {cv_summary['mean_accuracy']:.4f} ± {cv_summary['std_accuracy']:.4f}")
        print(f"   ROC AUC: {cv_summary['mean_auc']:.4f} ± {cv_summary['std_auc']:.4f}")

        return cv_summary

    def export_calibration_report(self, filename: str = "calibration_report.json"):
        """Esporta report completo della calibrazione"""
        if not self.calibration_results:
            raise ValueError("No calibration results to export")

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_calibrations': len(self.calibration_results),
            'best_result': {
                'f1_score': self.calibration_results[-1].best_f1_score,
                'accuracy': self.calibration_results[-1].best_accuracy,
                'roc_auc': self.calibration_results[-1].roc_auc,
                'thresholds': self.calibration_results[-1].best_thresholds
            },
            'all_results': [
                {
                    'timestamp': r.timestamp,
                    'f1_score': r.best_f1_score,
                    'accuracy': r.best_accuracy,
                    'thresholds': r.best_thresholds
                }
                for r in self.calibration_results
            ]
        }

        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 Calibration report saved to: {filepath}")
        return filepath


# Test
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

    from core.ensemble_analyzer import EnsembleAnalyzer

    # Crea ensemble
    ensemble = EnsembleAnalyzer()

    # Crea calibratore
    calibrator = EnsembleCalibrator(ensemble)

    # Calibra
    result = calibrator.calibrate_on_dataset(method="grid_search")

    # Cross-validate
    cv_results = calibrator.cross_validate()

    # Esporta report
    calibrator.export_calibration_report()

    print("\n🎉 Calibration complete!")
