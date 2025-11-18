#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syntactic Analyzer per TextAnalyzer
Analizzatore specializzato in metriche sintattiche
"""

from typing import Dict, Any, Tuple
from collections import Counter
import re
import statistics
from .base_analyzer import BaseAnalyzer


class SyntacticAnalyzer(BaseAnalyzer):
    """
    Analizzatore specializzato in metriche sintattiche.

    Metriche calcolate:
    - Avg Sentence Length: lunghezza media frasi
    - Sentence Variability: variabilità lunghezza frasi
    - Pattern Repetitiveness: ripetitività pattern sintattici
    - Sentence Count: numero totale frasi
    """

    def __init__(self):
        super().__init__()
        self.name = "SyntacticAnalyzer"
        self.description = "Analizzatore metriche sintattiche (Variabilità frasi, Pattern)"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi sintattica dettagliata"""
        self._validate_input(text)

        # Lunghezza frasi
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        sentence_lengths = [len(s.split()) for s in sentences]

        # Variabilità lunghezza frasi
        if len(sentence_lengths) > 1:
            avg_length = statistics.mean(sentence_lengths)
            std_length = statistics.stdev(sentence_lengths)
            variability = std_length / avg_length if avg_length > 0 else 0
        else:
            variability = 0.0
            avg_length = sentence_lengths[0] if sentence_lengths else 0

        # Min/Max sentence length
        min_length = min(sentence_lengths) if sentence_lengths else 0
        max_length = max(sentence_lengths) if sentence_lengths else 0

        # Pattern ripetitivi (frasi con struttura simile)
        pattern_scores = []
        for sent in sentences[:10]:  # Analizza max 10 frasi
            words = sent.lower().split()
            if len(words) > 3:
                # Similitudine pattern (primo, ultimo, medio)
                pattern = (words[0], words[-1], words[len(words)//2])
                pattern_scores.append(pattern)

        # Rileva pattern ripetitivi
        pattern_counter = Counter(pattern_scores)
        repetitions = sum(1 for count in pattern_counter.values() if count > 1)
        pattern_repetitiveness = repetitions / len(pattern_scores) if pattern_scores else 0

        # Average words per sentence
        total_words = sum(sentence_lengths)
        avg_words_per_sentence = self._safe_divide(total_words, len(sentences))

        metrics = {
            'avg_sentence_length': round(avg_length, 2),
            'min_sentence_length': min_length,
            'max_sentence_length': max_length,
            'sentence_variability': round(variability, 4),
            'pattern_repetitiveness': round(pattern_repetitiveness, 4),
            'sentence_count': len(sentences),
            'total_words': total_words,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2)
        }

        # Confidence basata su variabilità
        confidence = min(0.9, 0.5 + variability * 0.4)
        metrics['confidence'] = round(confidence, 4)

        return metrics

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """Prediction basata su sintassi"""
        variability = metrics.get('sentence_variability', 0.5)
        repetitiveness = metrics.get('pattern_repetitiveness', 0.1)

        ai_score = 0.0

        # Variabilità bassa indica AI
        if variability < 0.2:
            ai_score += 0.4

        # Pattern troppo ripetitivi o troppo vari indicano AI
        if repetitiveness < 0.001:
            ai_score += 0.3
        elif repetitiveness > 0.5:
            ai_score += 0.2

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob
