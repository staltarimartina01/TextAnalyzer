#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Analyzer Class per TextAnalyzer
Classe base astratta per tutti gli analizzatori specializzati
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
import statistics
import re


class BaseAnalyzer(ABC):
    """
    Classe base astratta per tutti gli analizzatori.

    Ogni analyzer specializzato deve ereditare da questa classe
    e implementare i metodi abstract: analyze() e predict()
    """

    def __init__(self):
        """Inizializza l'analyzer con metadati base."""
        self.name = self.__class__.__name__
        self.description = "Base analyzer - implementare in subclass"
        self.version = "1.0"

    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analizza il testo e calcola metriche specifiche.

        Args:
            text: Testo da analizzare (stringa non vuota)

        Returns:
            Dict con metriche calcolate e 'confidence' score (0-1)

        Raises:
            ValueError: Se testo è vuoto o non valido
            Exception: Per errori durante l'analisi
        """
        pass

    @abstractmethod
    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """
        Predice probabilità AI vs Human basata sulle metriche.

        Args:
            metrics: Dizionario con metriche da analyze()

        Returns:
            Tuple (ai_probability, human_probability)
            - ai_probability: 0.0 = sicuramente umano, 1.0 = sicuramente AI
            - human_probability: 1.0 - ai_probability
        """
        pass

    def _validate_input(self, text: str) -> None:
        """
        Valida input testuale.

        Args:
            text: Testo da validare

        Raises:
            ValueError: Se input non valido
        """
        if not isinstance(text, str):
            raise ValueError(f"Input must be string, got {type(text).__name__}")

        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        if len(text.strip()) < 10:
            raise ValueError("Input text too short (min 10 characters)")

    def _calculate_confidence(self, metrics: Dict[str, Any],
                            base_confidence: float = 0.5) -> float:
        """
        Calcola confidence score per questo analyzer.

        Args:
            metrics: Metriche calcolate
            base_confidence: Confidenza di base (0.5)

        Returns:
            Confidence score normalizzato (0.0 - 1.0)
        """
        # Fattori che aumentano confidence
        factors = []

        # 1. Validità delle metriche
        if isinstance(metrics, dict) and len(metrics) > 0:
            factors.append(0.1)

        # 2. Range delle metriche ragionevoli
        numeric_values = [v for v in metrics.values()
                         if isinstance(v, (int, float))]
        if numeric_values:
            # Calcola varianza per vedere se le metriche hanno dispersione
            if len(numeric_values) > 1:
                var = statistics.variance(numeric_values)
                if var > 0.001:  # Se c'è variazione, è più affidabile
                    factors.append(0.1)

        # 3. Confidence esplicito nelle metriche
        if 'confidence' in metrics:
            factors.append(metrics['confidence'] * 0.3)

        # Calcola confidence finale
        bonus = sum(factors)
        confidence = min(1.0, base_confidence + bonus)

        return round(confidence, 4)

    def _safe_divide(self, numerator: float, denominator: float,
                    default: float = 0.0) -> float:
        """
        Divisione sicura che evita ZeroDivisionError.

        Args:
            numerator: Numeratore
            denominator: Denominatore
            default: Valore di default se divisione per zero

        Returns:
            Risultato della divisione o default
        """
        if denominator == 0 or denominator is None:
            return default
        return numerator / denominator

    def _normalize_score(self, value: float, min_val: float,
                        max_val: float) -> float:
        """
        Normalizza uno score in range [0, 1].

        Args:
            value: Valore da normalizzare
            min_val: Valore minimo del range
            max_val: Valore massimo del range

        Returns:
            Valore normalizzato in [0, 1]
        """
        if max_val == min_val:
            return 0.5  # Default se range è punto

        normalized = (value - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))

    def _get_word_count(self, text: str) -> int:
        """Conta parole in un testo."""
        return len(re.findall(r'\b\w+\b', text))

    def _get_sentence_count(self, text: str) -> int:
        """Conta frasi in un testo."""
        sentences = re.findall(r'[.!?]+', text)
        return len(sentences)

    def _get_paragraph_count(self, text: str) -> int:
        """Conta paragrafi in un testo."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return len(paragraphs)

    def get_info(self) -> Dict[str, Any]:
        """
        Ritorna informazioni sull'analyzer.

        Returns:
            Dict con metadata dell'analyzer
        """
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'type': self.__class__.__bases__[0].__name__
        }

    def __repr__(self) -> str:
        """Rappresentazione stringa dell'analyzer."""
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class EnsembleAnalyzer(BaseAnalyzer):
    """
    Analyzer specializzato per operazioni ensemble.
    Combina risultati di più analyzers.
    """

    def __init__(self, analyzers: list):
        """
        Inizializza ensemble analyzer.

        Args:
            analyzers: Lista di analyzer da combinare
        """
        super().__init__()
        self.analyzers = analyzers
        self.description = f"Ensemble of {len(analyzers)} analyzers"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Esegue analisi con tutti gli analyzers."""
        self._validate_input(text)

        individual_results = {}
        all_metrics = {}

        # Esegui analisi con ogni analyzer
        for analyzer in self.analyzers:
            try:
                metrics = analyzer.analyze(text)
                ai_prob, human_prob = analyzer.predict(metrics)

                individual_results[analyzer.name] = {
                    'metrics': metrics,
                    'ai_probability': ai_prob,
                    'human_probability': human_prob,
                    'confidence': metrics.get('confidence', 0.5)
                }

                # Aggrega metriche
                all_metrics.update(metrics)

            except Exception as e:
                individual_results[analyzer.name] = {
                    'error': str(e),
                    'ai_probability': 0.5,
                    'human_probability': 0.5,
                    'confidence': 0.0
                }

        # Calcola ensemble result (weighted average)
        weighted_ai = 0
        weight_sum = 0

        for result in individual_results.values():
            if 'error' not in result:
                weight = result['confidence']
                weighted_ai += result['ai_probability'] * weight
                weight_sum += weight

        if weight_sum > 0:
            ensemble_ai = weighted_ai / weight_sum
        else:
            ensemble_ai = 0.5

        # Calcola agreement (varianza tra ai_probabilities)
        ai_probs = [r['ai_probability'] for r in individual_results.values()
                   if 'error' not in r]
        if len(ai_probs) > 1:
            agreement = 1.0 - min(1.0, statistics.variance(ai_probs))
        else:
            agreement = 1.0

        result = {
            'individual_results': individual_results,
            'ensemble_result': {
                'ai_probability': round(ensemble_ai, 4),
                'human_probability': round(1.0 - ensemble_ai, 4),
                'agreement_score': round(agreement, 3)
            },
            'aggregated_metrics': all_metrics,
            'analyzer_count': len(self.analyzers)
        }

        # Confidence basata su agreement e numero di analyzers
        base_conf = len(ai_probs) / 5.0  # Max confidence con 5 analyzers
        confidence = self._calculate_confidence(result, base_conf)
        result['overall_confidence'] = confidence

        return result

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """
        Prediction non applicabile per ensemble (già aggregato).
        """
        ensemble_result = metrics.get('ensemble_result', {})
        ai_prob = ensemble_result.get('ai_probability', 0.5)
        return ai_prob, 1.0 - ai_prob
