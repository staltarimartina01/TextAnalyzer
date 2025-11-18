#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lexical Analyzer per TextAnalyzer
Analizzatore specializzato in metriche lessicali
"""

from typing import Dict, Any, Tuple
from collections import Counter
import statistics
from .base_analyzer import BaseAnalyzer


class LexicalAnalyzer(BaseAnalyzer):
    """
    Analizzatore specializzato in metriche lessicali.

    Metriche calcolate:
    - Type-Token Ratio (TTR): diversità lessicale
    - TTR Variazione: variazione TTR nel tempo
    - Burstiness: creatività/variazione frequenze
    - Unique Words Ratio: percentuale parole uniche
    """

    def __init__(self):
        super().__init__()
        self.name = "LexicalAnalyzer"
        self.description = "Analizzatore metriche lessicali (TTR, Burstiness, Diversità)"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi lessicale dettagliata"""
        self._validate_input(text)

        words = text.lower().split()
        unique_words = set(words)

        # Metriche lessicali principali
        ttr = len(unique_words) / len(words) if words else 0

        # TTR progressivo (variazione nel tempo)
        ttr_progressive = []
        seen = set()
        for i, word in enumerate(words, 1):
            seen.add(word)
            ttr_progressive.append(len(seen) / i)

        ttr_variation = statistics.stdev(ttr_progressive) if len(ttr_progressive) > 1 else 0

        # Frequenze per burstiness
        freq = Counter(words)
        frequencies = list(freq.values())
        mean_freq = statistics.mean(frequencies) if frequencies else 0
        std_freq = statistics.stdev(frequencies) if len(frequencies) > 1 else 0

        burstiness = 0
        if mean_freq > 0:
            burstiness = (std_freq - mean_freq) / (std_freq + mean_freq)

        # Altre metriche lessicali
        unique_words_ratio = len(unique_words) / len(words) if words else 0
        vocabulary_richness = len(unique_words) / len(words) if words else 0

        # Complex words (more than 6 characters)
        complex_words = [w for w in words if len(w) > 6]
        complex_ratio = len(complex_words) / len(words) if words else 0

        # Long words (more than 7 characters)
        long_words = [w for w in words if len(w) > 7]
        long_ratio = len(long_words) / len(words) if words else 0

        # Calculate confidence
        metrics = {
            'ttr': round(ttr, 4),
            'ttr_variation': round(ttr_variation, 4),
            'burstiness': round(burstiness, 4),
            'unique_words_ratio': round(unique_words_ratio, 4),
            'vocabulary_richness': round(vocabulary_richness, 4),
            'complex_words_ratio': round(complex_ratio, 4),
            'long_words_ratio': round(long_ratio, 4),
            'total_words': len(words),
            'unique_words': len(unique_words),
            'most_common_word': freq.most_common(1)[0][0] if freq else '',
            'most_common_freq': freq.most_common(1)[0][1] if freq else 0
        }

        # Confidence basata su certezza TTR
        confidence = min(0.9, 0.6 + abs(ttr - 0.5) * 0.6)
        metrics['confidence'] = round(confidence, 4)

        return metrics

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """Prediction AI vs Human basata su metriche lessicali"""
        ttr = metrics.get('ttr', 0.5)
        burstiness = metrics.get('burstiness', 0.0)
        unique_ratio = metrics.get('unique_words_ratio', 0.5)

        # Regole basate su ricerca
        ai_score = 0.0

        # TTR anomalo indica AI
        if ttr > 0.8:
            ai_score += 0.4
        elif ttr < 0.3:
            ai_score += 0.3

        # Burstiness basso indica AI (scrittura più uniforme)
        if burstiness < 0.1:
            ai_score += 0.3

        # Troppa diversità lessicale può indicare AI
        if unique_ratio > 0.9:
            ai_score += 0.2

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob
