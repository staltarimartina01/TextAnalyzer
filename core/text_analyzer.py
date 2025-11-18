#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextAnalyzer Core Engine
Facade principale per analisi testuale AI vs Human
"""

import sys
import os
sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

# Import analyzers
from analyzers import (
    create_default_ensemble,
    create_analyzer,
    list_available_analyzers,
    DEFAULT_WEIGHTS
)

# Import utils
from utils.input_validator import InputValidator
from utils.confidence_metrics import ConfidenceMetrics


@dataclass
class AnalysisResult:
    """Risultato di un'analisi testuale"""
    classification: str
    ai_probability: float
    human_probability: float
    confidence: float
    certainty_level: str
    recommendation: str
    individual_results: Dict[str, Any]
    ensemble_result: Dict[str, Any]
    confidence_analysis: Dict[str, Any]
    input_validation: Dict[str, Any]
    processing_time_ms: float
    timestamp: str


class TextAnalyzer:
    """
    Facade principale per TextAnalyzer.

    Combina:
    - Input validation
    - Ensemble analysis (5 analyzers)
    - Confidence metrics
    - Calibrated predictions

    Usage:
        analyzer = TextAnalyzer()
        result = analyzer.analyze("Il tuo testo qui")
        print(result.classification)
        print(f"AI Probability: {result.ai_probability:.4f}")
    """

    def __init__(self,
                 auto_calibrate: bool = False,
                 enable_cache: bool = True,
                 debug: bool = False):
        """
        Inizializza TextAnalyzer.

        Args:
            auto_calibrate: Se True, calibra automaticamente al primo uso
            enable_cache: Se True, abilita caching risultati
            debug: Se True, abilita logging debug
        """
        # Components
        self.validator = InputValidator()
        self.confidence_metrics = ConfidenceMetrics()

        # Ensemble
        from core.ensemble_engine import EnsembleEngine
        self.ensemble = EnsembleEngine()

        # Config
        self.auto_calibrate = auto_calibrate
        self.enable_cache = enable_cache
        self.debug = debug

        # State
        self.is_calibrated = False
        self.calibration_threshold = 0.5
        self.cache = {} if enable_cache else None

        # Stats
        self.stats = {
            'total_analyses': 0,
            'avg_processing_time': 0.0,
            'avg_confidence': 0.0
        }

        if self.debug:
            print(f"✅ TextAnalyzer initialized")
            print(f"   Ensemble: {len(self.ensemble.analyzers)} analyzers")
            print(f"   Cache: {'Enabled' if enable_cache else 'Disabled'}")

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analizza un testo e determina se è AI o umano.

        Args:
            text: Testo da analizzare (min 10 caratteri)

        Returns:
            AnalysisResult con tutti i dettagli

        Raises:
            ValueError: Se testo non valido
        """
        start_time = datetime.now()

        # Check cache
        cache_key = self._get_cache_key(text)
        if self.cache and cache_key in self.cache:
            if self.debug:
                print("📦 Returning cached result")
            return self.cache[cache_key]

        # Validate input
        validation = self.validator.validate_text(text)
        if not validation['valid']:
            raise ValueError(f"Invalid input: {validation['errors']}")

        # Ensemble analysis
        ensemble_result = self.ensemble.analyze(text)

        # Confidence metrics
        uncertainty = self.confidence_metrics.prediction_uncertainty(ensemble_result)

        # Apply calibration if available
        if self.is_calibrated:
            ai_prob = ensemble_result['ensemble_result']['ai_probability']
            if ai_prob >= self.calibration_threshold:
                calibrated_classification = "Probabilmente AI"
                calibrated_confidence = ai_prob
            else:
                calibrated_classification = "Probabilmente Umano"
                calibrated_confidence = 1.0 - ai_prob
        else:
            # Use ensemble classification
            calibrated_classification = ensemble_result['ensemble_result']['classification']
            calibrated_confidence = uncertainty['prediction_certainty']

        # Build result
        result = AnalysisResult(
            classification=calibrated_classification,
            ai_probability=round(ensemble_result['ensemble_result']['ai_probability'], 4),
            human_probability=round(ensemble_result['ensemble_result']['human_probability'], 4),
            confidence=round(uncertainty['prediction_certainty'], 4),
            certainty_level=uncertainty['certainty_level'],
            recommendation=uncertainty['recommendation'],
            individual_results=ensemble_result['individual_results'],
            ensemble_result=ensemble_result['ensemble_result'],
            confidence_analysis=uncertainty,
            input_validation=validation,
            processing_time_ms=round(
                (datetime.now() - start_time).total_seconds() * 1000, 2
            ),
            timestamp=datetime.now().isoformat()
        )

        # Update stats
        self._update_stats(result)

        # Cache
        if self.cache:
            self.cache[cache_key] = result

        return result

    def analyze_batch(self, texts: List[str]) -> List[AnalysisResult]:
        """
        Analizza una lista di testi.

        Args:
            texts: Lista di testi da analizzare

        Returns:
            Lista di AnalysisResult
        """
        results = []
        for i, text in enumerate(texts, 1):
            if self.debug:
                print(f"🔄 Analyzing {i}/{len(texts)}...")
            try:
                result = self.analyze(text)
                results.append(result)
            except Exception as e:
                if self.debug:
                    print(f"⚠️ Error analyzing text {i}: {e}")
                # Create error result
                error_result = AnalysisResult(
                    classification="Errore",
                    ai_probability=0.5,
                    human_probability=0.5,
                    confidence=0.0,
                    certainty_level="N/A",
                    recommendation=f"Errore: {str(e)}",
                    individual_results={},
                    ensemble_result={},
                    confidence_analysis={},
                    input_validation={'error': str(e)},
                    processing_time_ms=0.0,
                    timestamp=datetime.now().isoformat()
                )
                results.append(error_result)

        return results

    def calibrate(self, dataset_path: str = "data/validation_dataset.json"):
        """
        Calibra il sistema su un dataset.

        Args:
            dataset_path: Path al dataset JSON

        Returns:
            Dict con risultati calibrazione
        """
        try:
            from utils.calibration_engine import CalibrationEngine

            calibrator = CalibrationEngine(self.ensemble)
            result = calibrator.calibrate_on_dataset(dataset_path)

            self.is_calibrated = True
            self.calibration_threshold = result.best_thresholds.get('ai_threshold', 0.5)

            if self.debug:
                print(f"✅ Calibration complete")
                print(f"   Threshold: {self.calibration_threshold:.4f}")
                print(f"   F1-Score: {result.best_f1_score:.4f}")
                print(f"   ROC AUC: {result.roc_auc:.4f}")

            return {
                'success': True,
                'threshold': self.calibration_threshold,
                'f1_score': result.best_f1_score,
                'roc_auc': result.roc_auc
            }

        except Exception as e:
            if self.debug:
                print(f"❌ Calibration failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_available_analyzers(self) -> Dict[str, str]:
        """
        Ottiene lista analyzers disponibili.

        Returns:
            Dict nome -> descrizione
        """
        return list_available_analyzers()

    def get_stats(self) -> Dict[str, Any]:
        """
        Ottiene statistiche di utilizzo.

        Returns:
            Dict con statistiche
        """
        return {
            **self.stats,
            'is_calibrated': self.is_calibrated,
            'calibration_threshold': self.calibration_threshold,
            'cache_size': len(self.cache) if self.cache else 0,
            'available_analyzers': list(self.get_available_analyzers().keys())
        }

    def clear_cache(self):
        """Pulisce la cache."""
        if self.cache:
            self.cache.clear()
            if self.debug:
                print("🧹 Cache cleared")

    def export_result(self, result: AnalysisResult, filepath: str):
        """
        Esporta risultato in file JSON.

        Args:
            result: AnalysisResult da esportare
            filepath: Path del file di output
        """
        # Convert dataclass to dict
        result_dict = {
            'classification': result.classification,
            'ai_probability': result.ai_probability,
            'human_probability': result.human_probability,
            'confidence': result.confidence,
            'certainty_level': result.certainty_level,
            'recommendation': result.recommendation,
            'individual_results': result.individual_results,
            'ensemble_result': result.ensemble_result,
            'confidence_analysis': result.confidence_analysis,
            'input_validation': result.input_validation,
            'processing_time_ms': result.processing_time_ms,
            'timestamp': result.timestamp
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False, default=str)

        if self.debug:
            print(f"💾 Result exported to {filepath}")

    def _get_cache_key(self, text: str) -> str:
        """Genera chiave cache per un testo."""
        # Simple hash based on first/last 100 chars and length
        text_sample = text[:100] + text[-100:] if len(text) > 200 else text
        return f"{len(text)}:{hash(text_sample)}"

    def _update_stats(self, result: AnalysisResult):
        """Aggiorna statistiche interne."""
        self.stats['total_analyses'] += 1

        # Average processing time
        n = self.stats['total_analyses']
        old_avg_time = self.stats['avg_processing_time']
        new_time = result.processing_time_ms
        self.stats['avg_processing_time'] = (
            (old_avg_time * (n - 1) + new_time) / n
        )

        # Average confidence
        old_avg_conf = self.stats['avg_confidence']
        new_conf = result.confidence
        self.stats['avg_confidence'] = (
            (old_avg_conf * (n - 1) + new_conf) / n
        )

    def __repr__(self) -> str:
        return (
            f"<TextAnalyzer("
            f"analyzers={len(self.ensemble.analyzers)}, "
            f"calibrated={self.is_calibrated}, "
            f"analyses={self.stats['total_analyses']}"
            f")>"
        )
