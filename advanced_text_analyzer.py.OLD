#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced TextAnalyzer - Sistema Completo e Affidabile
Integra: Ensemble Learning, Calibrazione Automatica, Confidence Metrics, ROC Analysis

Autore: TextAnalyzer Advanced System
Versione: 3.0 - Professional Edition
Data: 2025
"""

import sys
import os
sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import dei moduli avanzati
from core.ensemble_analyzer import EnsembleAnalyzer
from utils.input_validator import InputValidator
from utils.calibrator import EnsembleCalibrator
from utils.confidence_metrics import ConfidenceMetrics
from utils.roc_analyzer import ROCAnalyzer

class AdvancedTextAnalyzerSystem:
    """
    Sistema completo di analisi testuale avanzata
    Combina ensemble learning, calibrazione e metriche di confidenza
    """

    def __init__(self, auto_calibrate: bool = True):
        # Inizializza componenti
        self.validator = InputValidator()
        self.ensemble = EnsembleAnalyzer()
        self.confidence_metrics = ConfidenceMetrics()
        self.roc_analyzer = ROCAnalyzer()
        self.calibrator = EnsembleCalibrator(self.ensemble)

        # Stato del sistema
        self.is_calibrated = False
        self.calibration_result = None
        self.system_stats = {
            'total_analyses': 0,
            'avg_confidence': 0.0,
            'reliability_score': 0.0
        }

        print("🚀 Advanced TextAnalyzer System v3.0")
        print("=" * 60)
        print("✅ Input Validator: Ready")
        print("✅ Ensemble Analyzer: Ready (5 specialized analyzers)")
        print("✅ Confidence Metrics: Ready")
        print("✅ ROC Analyzer: Ready")

        # Auto-calibrazione
        if auto_calibrate:
            self.auto_calibrate()

    def auto_calibrate(self):
        """Auto-calibrazione del sistema"""
        print("\n🎯 Starting auto-calibration...")

        try:
            self.calibration_result = self.calibrator.calibrate_on_dataset(
                method="grid_search"
            )
            self.is_calibrated = True

            print(f"\n✅ Calibration Complete!")
            print(f"   Best F1-Score: {self.calibration_result.best_f1_score:.4f}")
            print(f"   Best Accuracy: {self.calibration_result.best_accuracy:.4f}")
            print(f"   ROC AUC: {self.calibration_result.roc_auc:.4f}")
            print(f"   Calibrated Threshold: {self.calibration_result.best_thresholds.get('ai_threshold', 0.5):.4f}")

        except Exception as e:
            print(f"⚠️ Calibration failed: {e}")
            print("   Using default parameters...")

    def analyze_text(self, text: str, return_full_report: bool = False) -> Dict[str, Any]:
        """
        Analisi completa di un testo con tutte le metriche

        Args:
            text: Testo da analizzare
            return_full_report: Se True, restituisce report completo

        Returns:
            Dict con risultati dell'analisi
        """
        start_time = datetime.now()

        # 1. Validazione input
        validation = self.validator.validate_text(text)
        if not validation['valid']:
            return {
                'error': 'Invalid input',
                'validation_errors': validation['errors'],
                'validation_warnings': validation['warnings']
            }

        sanitized_text = validation['sanitized_text']

        # 2. Analisi ensemble
        ensemble_result = self.ensemble.analyze(sanitized_text)

        # 3. Metriche di confidenza
        uncertainty = self.confidence_metrics.prediction_uncertainty(ensemble_result)

        # 4. Applica calibrazione se disponibile
        if self.is_calibrated and self.calibration_result:
            calibrated_result = self.calibrator.apply_calibration(sanitized_text)
            # Unisci risultati
            ensemble_result.update(calibrated_result)

        # 5. Calcola tempo di elaborazione
        processing_time = (datetime.now() - start_time).total_seconds()

        # 6. Compila risultato finale
        result = {
            'timestamp': datetime.now().isoformat(),
            'processing_time_ms': round(processing_time * 1000, 2),
            'input_validation': {
                'valid': validation['valid'],
                'quality_score': validation['quality_score'],
                'warnings': validation['warnings']
            },
            'ensemble_analysis': ensemble_result,
            'confidence_analysis': {
                'prediction_certainty': uncertainty['prediction_certainty'],
                'certainty_level': uncertainty['certainty_level'],
                'uncertainty_breakdown': uncertainty['uncertainty_breakdown'],
                'recommendation': uncertainty['recommendation']
            },
            'system_info': {
                'is_calibrated': self.is_calibrated,
                'calibration_threshold': self.calibration_result.best_thresholds.get('ai_threshold') if self.calibration_result else None,
                'ensemble_analyzers_count': len(self.ensemble.analyzers)
            }
        }

        # Aggiorna statistiche sistema
        self.system_stats['total_analyses'] += 1
        self._update_system_stats(result)

        # Report completo se richiesto
        if return_full_report:
            result['full_report'] = self._generate_full_report(result)

        return result

    def batch_analyze(self, texts: List[str], return_reports: bool = False) -> List[Dict[str, Any]]:
        """Analizza un batch di testi"""
        print(f"\n🔄 Batch Analysis: {len(texts)} texts")

        results = []
        for i, text in enumerate(texts, 1):
            print(f"   Analyzing {i}/{len(texts)}...", end='\r')
            result = self.analyze_text(text, return_full_report=return_reports)
            results.append(result)

        print(f"\n✅ Batch complete: {len(results)} analyses")

        # Statistiche batch
        avg_confidence = sum(r.get('confidence_analysis', {}).get('prediction_certainty', 0)
                           for r in results) / len(results)

        print(f"   Average Confidence: {avg_confidence:.3f}")
        print(f"   Reliability: {self.system_stats['reliability_score']:.3f}")

        return results

    def evaluate_system_reliability(self) -> Dict[str, Any]:
        """Valuta affidabilità complessiva del sistema"""
        # Carica dati di validazione
        try:
            with open('data/validation_dataset.json', 'r') as f:
                dataset = json.load(f)

            # Analizza tutto il dataset
            predictions = []
            for item in dataset:
                result = self.analyze_text(item['text'])
                if 'error' not in result:
                    predictions.append(result)

            # Calcola metriche di affidabilità
            reliability = self.confidence_metrics.model_reliability(predictions)

            # ROC Analysis
            y_true = [1 if item['label'] == 'ai' else 0 for item in dataset]
            y_scores = [r['ensemble_analysis']['ensemble_result']['ai_probability']
                       for r in predictions]

            roc_result = self.roc_analyzer.analyze_model_performance(
                y_true, y_scores, "AdvancedTextAnalyzer"
            )

            return {
                'reliability_assessment': reliability,
                'roc_analysis': {
                    'auc': roc_result['roc_analysis']['auc'],
                    'auc_interpretation': roc_result['roc_analysis']['auc_interpretation'],
                    'pr_auc': roc_result['pr_analysis']['auc_pr'],
                    'best_f1': max(p.get('f1_score', 0) for p in roc_result['threshold_performance'].values())
                },
                'system_stats': self.system_stats,
                'is_calibrated': self.is_calibrated
            }

        except Exception as e:
            return {'error': f'Reliability evaluation failed: {str(e)}'}

    def _update_system_stats(self, result: Dict[str, Any]):
        """Aggiorna statistiche del sistema"""
        # Media mobile per confidenza
        curr_conf = result.get('confidence_analysis', {}).get('prediction_certainty', 0)
        n = self.system_stats['total_analyses']

        if n == 1:
            self.system_stats['avg_confidence'] = curr_conf
        else:
            self.system_stats['avg_confidence'] = (
                (self.system_stats['avg_confidence'] * (n - 1) + curr_conf) / n
            )

        # Affidabilità (semplificata)
        if curr_conf > 0.7:
            self.system_stats['reliability_score'] = min(1.0, self.system_stats['reliability_score'] + 0.01)
        else:
            self.system_stats['reliability_score'] = max(0.0, self.system_stats['reliability_score'] - 0.005)

    def _generate_full_report(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Genera report completo dell'analisi"""
        return {
            'input_statistics': result['input_validation']['input_stats'] if 'input_stats' in result['input_validation'] else {},
            'ensemble_details': {
                'individual_analyzer_results': result['ensemble_analysis']['individual_results'],
                'agreement_score': result['ensemble_analysis']['ensemble_result']['agreement_score'],
                'weighted_confidence': result['ensemble_analysis']['ensemble_result']['weighted_confidence']
            },
            'confidence_details': result['confidence_analysis'],
            'recommendations': self._generate_comprehensive_recommendations(result),
            'technical_metrics': {
                'processing_time_ms': result['processing_time_ms'],
                'input_quality': result['input_validation']['quality_score'],
                'system_reliability': self.system_stats['reliability_score']
            }
        }

    def _generate_comprehensive_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """Genera raccomandazioni complete"""
        recommendations = []

        # Raccomandazioni basate su confidenza
        certainty = result['confidence_analysis']['prediction_certainty']
        if certainty < 0.5:
            recommendations.append(
                "⚠️ Bassa certezza nella prediction. Si raccomanda revisione manuale."
            )
        elif certainty > 0.8:
            recommendations.append(
                "✅ Alta certezza nella prediction. Risultato molto affidabile."
            )

        # Raccomandazioni basate su calibrazione
        if not self.is_calibrated:
            recommendations.append(
                "🔧 Sistema non calibrato. Calibrazione raccomandata per migliori risultati."
            )

        # Raccomandazioni basate su qualità input
        input_quality = result['input_validation']['quality_score']
        if input_quality < 0.6:
            recommendations.append(
                "📝 Qualità input bassa. Considera revisione o pulizia del testo."
            )

        return recommendations

    def export_system_report(self, filename: str = "advanced_analyzer_report.json"):
        """Esporta report completo del sistema"""
        reliability = self.evaluate_system_reliability()

        report = {
            'system_info': {
                'version': '3.0',
                'timestamp': datetime.now().isoformat(),
                'components': {
                    'input_validator': 'Advanced validation with quality scoring',
                    'ensemble_analyzer': f'{len(self.ensemble.analyzers)} specialized analyzers',
                    'calibration': 'Grid search with cross-validation',
                    'confidence_metrics': 'Bootstrap, Bayesian, Uncertainty quantification',
                    'roc_analysis': 'Complete ROC/PR analysis'
                }
            },
            'calibration_status': {
                'is_calibrated': self.is_calibrated,
                'calibration_result': self.calibration_result.__dict__ if self.calibration_result else None
            },
            'system_performance': reliability,
            'statistics': self.system_stats
        }

        os.makedirs('data', exist_ok=True)
        filepath = f'data/{filename}'

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n💾 System report exported to: {filepath}")
        return filepath

    def get_system_status(self) -> Dict[str, Any]:
        """Stato corrente del sistema"""
        return {
            'version': '3.0 Professional',
            'status': 'Ready',
            'components': {
                'input_validator': '✅ Active',
                'ensemble_analyzer': f'✅ Active ({len(self.ensemble.analyzers)} analyzers)',
                'calibrator': f'{"✅ Calibrated" if self.is_calibrated else "⚠️ Not calibrated"}',
                'confidence_metrics': '✅ Active',
                'roc_analyzer': '✅ Active'
            },
            'statistics': self.system_stats,
            'uptime': datetime.now().isoformat()
        }


def main():
    """Demo del sistema avanzato"""
    print("🎯 Advanced TextAnalyzer System Demo\n")

    # Crea sistema
    analyzer = AdvancedTextAnalyzerSystem()

    # Test texts
    test_texts = [
        # Testo umano
        "It was the best of times, it was the worst of times. We lived in an age of wisdom and foolishness, of belief and incredulity. The world had its light and dark sides.",
        # Testo AI
        "Artificial intelligence represents a revolutionary advancement in modern technology. This field encompasses machine learning, natural language processing, and complex algorithmic systems designed to simulate human cognitive functions.",
    ]

    # Analizza testi
    print("\n" + "=" * 60)
    print("📊 TESTING WITH SAMPLE TEXTS")
    print("=" * 60)

    for i, text in enumerate(test_texts, 1):
        label = "HUMAN" if i == 1 else "AI"
        print(f"\n{label} TEXT:")
        print("-" * 60)

        result = analyzer.analyze_text(text)

        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            ensemble = result['ensemble_analysis']['ensemble_result']
            confidence = result['confidence_analysis']

            print(f"🤖 Classification: {ensemble['classification']}")
            print(f"📊 AI Probability: {ensemble['ai_probability']:.4f}")
            print(f"🎯 Confidence: {confidence['prediction_certainty']:.4f}")
            print(f"📈 Certainty Level: {confidence['certainty_level']}")
            print(f"⚡ Processing Time: {result['processing_time_ms']:.2f}ms")
            print(f"\n💡 Recommendation: {confidence['recommendation']}")

    # Valuta affidabilità sistema
    print("\n" + "=" * 60)
    print("🔍 SYSTEM RELIABILITY EVALUATION")
    print("=" * 60)

    reliability = analyzer.evaluate_system_reliability()

    if 'error' not in reliability:
        print(f"\n📈 ROC AUC: {reliability['roc_analysis']['auc']:.4f}")
        print(f"   → {reliability['roc_analysis']['auc_interpretation']}")
        print(f"\n🎯 Best F1-Score: {reliability['roc_analysis']['best_f1']:.4f}")
        print(f"\n🏆 Reliability Grade: {reliability['reliability_assessment'].get('reliability_grade', 'N/A')}")
        print(f"   → {reliability['reliability_assessment'].get('recommendation', 'N/A')}")

    # Esporta report
    analyzer.export_system_report()

    print("\n" + "=" * 60)
    print("✅ ADVANCED ANALYZER DEMO COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
