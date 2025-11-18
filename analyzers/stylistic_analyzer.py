#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stylistic Analyzer per TextAnalyzer
Analizzatore specializzato in metriche stilistiche
"""

from typing import Dict, Any, Tuple
from collections import Counter
import re
import statistics
from .base_analyzer import BaseAnalyzer


class StylisticAnalyzer(BaseAnalyzer):
    """
    Analizzatore specializzato in metriche stilistiche.

    Metriche calcolate:
    - Punctuation Density: densità punteggiatura
    - Capital Ratio: rapporto maiuscole
    - Punctuation Variability: variabilità punteggiatura
    - Phrase Repetitiveness: ripetitività frasi
    """

    def __init__(self):
        super().__init__()
        self.name = "StylisticAnalyzer"
        self.description = "Analizzatore metriche stilistiche (Punteggiatura, Maiuscole)"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi stilistica (punteggiatura, maiuscole, ecc.)"""
        self._validate_input(text)

        # Uso punteggiatura
        total_chars = len(text)
        punct_chars = len(re.findall(r'[.,;:!?()"\']', text))
        punct_density = punct_chars / total_chars if total_chars > 0 else 0

        # Maiuscole
        upper_chars = len(re.findall(r'[A-Z]', text))
        upper_ratio = upper_chars / total_chars if total_chars > 0 else 0

        # Pattern di punteggiatura
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Variazione punteggiatura nelle frasi
        punct_per_sentence = [len(re.findall(r'[.,;:!?]', s)) for s in sentences]
        if len(punct_per_sentence) > 1:
            punct_variability = statistics.stdev(punct_per_sentence)
        else:
            punct_variability = 0

        # Ripetitività espressioni
        common_phrases = re.findall(r'\b\w+\s+\w+\s+\w+\b', text.lower())
        phrase_counter = Counter(common_phrases)
        max_phrase_freq = max(phrase_counter.values()) if phrase_counter else 0
        phrase_repetitiveness = max_phrase_freq / len(common_phrases) if common_phrases else 0

        # Paragraph structure
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        avg_paragraph_length = statistics.mean([len(p.split()) for p in paragraphs]) if paragraphs else 0

        # Exclamation and question marks
        exclamations = text.count('!')
        questions = text.count('?')
        total_punct = punct_chars

        # Use of ellipsis
        ellipsis = text.count('...')

        # Quotation marks
        quotes = text.count('"') + text.count("'")

        metrics = {
            'punctuation_density': round(punct_density, 4),
            'capital_ratio': round(upper_ratio, 4),
            'punct_variability': round(punct_variability, 3),
            'phrase_repetitiveness': round(phrase_repetitiveness, 4),
            'exclamation_count': exclamations,
            'question_count': questions,
            'ellipsis_count': ellipsis,
            'quote_count': quotes,
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': round(avg_paragraph_length, 2),
            'avg_punct_per_sentence': round(statistics.mean(punct_per_sentence), 2) if punct_per_sentence else 0
        }

        # Confidence basata su variabilità punteggiatura
        confidence = min(0.9, 0.5 + punct_variability * 0.3)
        metrics['confidence'] = round(confidence, 4)

        return metrics

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """Prediction basata su stile"""
        punct_density = metrics.get('punctuation_density', 0.05)
        upper_ratio = metrics.get('capital_ratio', 0.05)
        punct_variability = metrics.get('punct_variability', 1.0)
        phrase_repet = metrics.get('phrase_repetitiveness', 0.1)

        ai_score = 0.0

        # Punteggiatura troppo uniforme indica AI
        if punct_variability < 0.5:
            ai_score += 0.3

        # Maiuscole troppo rare
        if upper_ratio < 0.02:
            ai_score += 0.2

        # Ripetitività frasi
        if phrase_repet > 0.3:
            ai_score += 0.3

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob
