# -*- coding: utf-8 -*-
"""
Model Evaluator - Valutazione e metriche del modello
Modulo per la valutazione delle performance del sistema di classificazione
"""

import math
from typing import Dict, List, Any, Tuple
from collections import Counter
import statistics


class ModelEvaluator:
    """Evaluator per il modello di classificazione AI vs Umano"""
    
    def __init__(self):
        self.confusion_matrix = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    
    def evaluate_predictions(self, predictions: List[Dict[str, Any]], ground_truth: List[str] = None) -> Dict[str, Any]:
        """Valuta le predizioni contro la verità di base"""
        if ground_truth and len(predictions) != len(ground_truth):
            raise ValueError("Numero di predizioni e verità di base non corrispondono")
        
        if not ground_truth:
            # Valutazione senza verità di base (analisi descrittiva)
            return self._descriptive_evaluation(predictions)
        
        # Valutazione supervisionata
        return self._supervised_evaluation(predictions, ground_truth)
    
    def _descriptive_evaluation(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Valutazione descrittiva senza verità di base"""
        total = len(predictions)
        if total == 0:
            return {'error': 'Nessuna predizione da valutare'}
        
        # Conta predizioni
        pred_counts = Counter()
        confidence_scores = []
        features_analysis = {}
        
        valid_predictions = [p for p in predictions if 'error' not in p]
        
        for pred in valid_predictions:
            assessment = pred.get('final_assessment', {})
            prediction = assessment.get('prediction', 'Sconosciuto')
            confidence = assessment.get('confidence', 0)
            
            pred_counts[prediction] += 1
            confidence_scores.append(confidence)
            
            # Analisi features
            features = pred.get('features', {})
            for category, feature_dict in features.items():
                if isinstance(feature_dict, dict):
                    if category not in features_analysis:
                        features_analysis[category] = {}
                    for name, value in feature_dict.items():
                        key = f"{category}_{name}"
                        if key not in features_analysis:
                            features_analysis[key] = []
                        features_analysis[key].append(value)
        
        # Calcola statistiche
        descriptive_stats = {
            'total_predictions': total,
            'valid_predictions': len(valid_predictions),
            'errors': total - len(valid_predictions),
            'prediction_distribution': dict(pred_counts),
            'confidence_stats': {
                'mean': statistics.mean(confidence_scores) if confidence_scores else 0,
                'median': statistics.median(confidence_scores) if confidence_scores else 0,
                'min': min(confidence_scores) if confidence_scores else 0,
                'max': max(confidence_scores) if confidence_scores else 0,
                'std': statistics.stdev(confidence_scores) if len(confidence_scores) > 1 else 0
            }
        }
        
        # Statistiche features
        features_stats = {}
        for feature_name, values in features_analysis.items():
            if values:
                features_stats[feature_name] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std': statistics.stdev(values) if len(values) > 1 else 0,
                    'min': min(values),
                    'max': max(values)
                }
        
        descriptive_stats['features_statistics'] = features_stats
        
        return descriptive_stats
    
    def _supervised_evaluation(self, predictions: List[Dict[str, Any]], ground_truth: List[str]) -> Dict[str, Any]:
        """Valutazione supervisionata con verità di base"""
        # Prepara dati
        y_true = []
        y_pred = []
        confidences = []
        
        for pred, truth in zip(predictions, ground_truth):
            if 'error' not in pred:
                assessment = pred.get('final_assessment', {})
                prediction = assessment.get('prediction', 'Sconosciuto')
                confidence = assessment.get('confidence', 0)
                
                y_true.append(truth)
                y_pred.append(prediction)
                confidences.append(confidence)
        
        # Calcola metriche
        accuracy = self._calculate_accuracy(y_true, y_pred)
        precision, recall, f1 = self._calculate_precision_recall_f1(y_true, y_pred)
        
        # Confidence analysis
        high_conf_mask = [c > 0.7 for c in confidences]
        high_conf_accuracy = self._calculate_accuracy(
            [y_true[i] for i, mask in enumerate(high_conf_mask) if mask],
            [y_pred[i] for i, mask in enumerate(high_conf_mask) if mask]
        ) if any(high_conf_mask) else 0
        
        return {
            'total_samples': len(predictions),
            'valid_predictions': len(y_true),
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'high_confidence_accuracy': high_conf_accuracy,
            'confidence_threshold': 0.7,
            'confusion_matrix': self._create_confusion_matrix(y_true, y_pred),
            'confidence_stats': {
                'mean': statistics.mean(confidences) if confidences else 0,
                'median': statistics.median(confidences) if confidences else 0,
                'std': statistics.stdev(confidences) if len(confidences) > 1 else 0
            },
            'per_class_metrics': self._calculate_per_class_metrics(y_true, y_pred)
        }
    
    def _calculate_accuracy(self, y_true: List[str], y_pred: List[str]) -> float:
        """Calcola l'accuratezza"""
        if not y_true:
            return 0.0
        correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        return correct / len(y_true)
    
    def _calculate_precision_recall_f1(self, y_true: List[str], y_pred: List[str]) -> Tuple[float, float, float]:
        """Calcola precision, recall e F1-score"""
        if not y_true:
            return 0.0, 0.0, 0.0
        
        # Calcola per classe (AI vs UMANO)
        classes = set(y_true + y_pred)
        metrics = {}
        
        for cls in classes:
            tp = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred == cls)
            fp = sum(1 for true, pred in zip(y_true, y_pred) if true != cls and pred == cls)
            fn = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred != cls)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            metrics[cls] = {'precision': precision, 'recall': recall, 'f1': f1}
        
        # Media pesata (basata su supporto)
        total_support = len(y_true)
        weighted_precision = sum(metrics[cls]['precision'] * sum(1 for t in y_true if t == cls) for cls in classes) / total_support
        weighted_recall = sum(metrics[cls]['recall'] * sum(1 for t in y_true if t == cls) for cls in classes) / total_support
        weighted_f1 = 2 * weighted_precision * weighted_recall / (weighted_precision + weighted_recall) if (weighted_precision + weighted_recall) > 0 else 0
        
        return weighted_precision, weighted_recall, weighted_f1
    
    def _create_confusion_matrix(self, y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, int]]:
        """Crea confusion matrix"""
        classes = sorted(set(y_true + y_pred))
        matrix = {}
        
        for true_class in classes:
            matrix[true_class] = {}
            for pred_class in classes:
                count = sum(1 for true, pred in zip(y_true, y_pred) if true == true_class and pred == pred_class)
                matrix[true_class][pred_class] = count
        
        return matrix
    
    def _calculate_per_class_metrics(self, y_true: List[str], y_pred: List[str]) -> Dict[str, Dict[str, float]]:
        """Calcola metriche per classe"""
        classes = set(y_true + y_pred)
        class_metrics = {}
        
        for cls in classes:
            tp = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred == cls)
            fp = sum(1 for true, pred in zip(y_true, y_pred) if true != cls and pred == cls)
            fn = sum(1 for true, pred in zip(y_true, y_pred) if true == cls and pred != cls)
            tn = sum(1 for true, pred in zip(y_true, y_pred) if true != cls and pred != cls)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            class_metrics[cls] = {
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'support': sum(1 for true in y_true if true == cls)
            }
        
        return class_metrics
    
    def generate_evaluation_report(self, evaluation_results: Dict[str, Any], output_path: str = None) -> str:
        """Genera un report dettagliato della valutazione"""
        report = []
        report.append("=" * 80)
        report.append("REPORT VALUTAZIONE MODELLO AI vs UMANO")
        report.append("=" * 80)
        report.append(f"Data valutazione: {statistics.median([0])}")  # Placeholder timestamp
        report.append("")
        
        if 'error' in evaluation_results:
            report.append(f"ERRORE: {evaluation_results['error']}")
            return "\n".join(report)
        
        # Metriche generali
        report.append("METRICHE GENERALI:")
        report.append(f"  Campioni totali: {evaluation_results.get('total_samples', 0)}")
        report.append(f"  Predizioni valide: {evaluation_results.get('valid_predictions', 0)}")
        report.append("")
        
        # Se supervisionato
        if 'accuracy' in evaluation_results:
            report.append("METRICHE SUPERVISIONATE:")
            report.append(f"  Accuracy: {evaluation_results['accuracy']:.3f}")
            report.append(f"  Precision: {evaluation_results['precision']:.3f}")
            report.append(f"  Recall: {evaluation_results['recall']:.3f}")
            report.append(f"  F1-Score: {evaluation_results['f1_score']:.3f}")
            report.append(f"  High-confidence Accuracy (>0.7): {evaluation_results.get('high_confidence_accuracy', 0):.3f}")
            report.append("")
            
            # Confusion Matrix
            if 'confusion_matrix' in evaluation_results:
                report.append("CONFUSION MATRIX:")
                cm = evaluation_results['confusion_matrix']
                classes = list(cm.keys())
                
                # Header
                report.append("Predicted ->")
                header = "Actual \\/".ljust(15)
                for cls in classes:
                    header += cls.ljust(12)
                report.append(header)
                report.append("-" * len(header))
                
                # Matrix rows
                for true_cls in classes:
                    row = true_cls.ljust(15)
                    for pred_cls in classes:
                        row += str(cm[true_cls][pred_cls]).ljust(12)
                    report.append(row)
                report.append("")
            
            # Per-class metrics
            if 'per_class_metrics' in evaluation_results:
                report.append("METRICHE PER CLASSE:")
                for class_name, metrics in evaluation_results['per_class_metrics'].items():
                    report.append(f"  {class_name}:")
                    report.append(f"    Precision: {metrics['precision']:.3f}")
                    report.append(f"    Recall: {metrics['recall']:.3f}")
                    report.append(f"    F1-Score: {metrics['f1']:.3f}")
                    report.append(f"    Support: {metrics['support']}")
                report.append("")
        
        # Confidence analysis
        if 'confidence_stats' in evaluation_results:
            conf_stats = evaluation_results['confidence_stats']
            report.append("ANALISI CONFIDENCE:")
            report.append(f"  Media: {conf_stats.get('mean', 0):.3f}")
            report.append(f"  Mediana: {conf_stats.get('median', 0):.3f}")
            report.append(f"  Deviazione standard: {conf_stats.get('std', 0):.3f}")
            report.append("")
        
        # Features analysis (se disponibile)
        if 'features_statistics' in evaluation_results:
            report.append("STATISTICHE FEATURES:")
            for feature_name, stats in evaluation_results['features_statistics'].items():
                if 'semantic_' not in feature_name:  # Focus su features principali
                    report.append(f"  {feature_name}: μ={stats['mean']:.3f}, σ={stats['std']:.3f}")
            report.append("")
        
        # Raccomandazioni
        report.append("RACCOMANDAZIONI:")
        if 'accuracy' in evaluation_results:
            acc = evaluation_results['accuracy']
            if acc > 0.8:
                report.append("  ✓ Modello performante - Accuracy > 80%")
            elif acc > 0.6:
                report.append("  ⚠ Modello moderatamente performante - Considera ottimizzazioni")
            else:
                report.append("  ✗ Modello da migliorare - Accuracy < 60%")
            
            if evaluation_results.get('high_confidence_accuracy', 0) > evaluation_results.get('accuracy', 0):
                report.append("  ✓ Confidence calata bene - Predizioni confident sono più accurate")
            else:
                report.append("  ⚠ Confidence non ben calibrata - Rivedere thresholds")
        
        report_text = "\n".join(report)
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"Report valutazione salvato in: {output_path}")
            except Exception as e:
                print(f"Errore nel salvataggio del report: {e}")
        
        return report_text
