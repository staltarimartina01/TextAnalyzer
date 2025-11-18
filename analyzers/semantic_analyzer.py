#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Analyzer per TextAnalyzer
Analizzatore specializzato in metriche semantiche
"""

from typing import Dict, Any, Tuple
import re
import statistics
from .base_analyzer import BaseAnalyzer


class SemanticAnalyzer(BaseAnalyzer):
    """
    Analizzatore specializzato in metriche semantiche.

    Metriche calcolate:
    - Subjectivity: soggettività/oggettività del testo
    - Conceptual Density: densità concettuale (parole complesse)
    - Thematic Coherence: coerenza tematica tra frasi
    """

    def __init__(self):
        super().__init__()
        self.name = "SemanticAnalyzer"
        self.description = "Analizzatore metriche semantiche (Coerenza, Densità concettuale)"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi semantica basilare (coerenza, temi)"""
        self._validate_input(text)

        words = text.lower().split()

        # Soggettività/Oggettività (proxy tramite presenza aggettivi/avverbi)
        adjectives_adverbs = len([w for w in words if w.endswith('ly') or w.endswith('ous')])
        subjectivity = adjectives_adverbs / len(words) if words else 0.5

        # Complessità concettuale (parole lunghe/complesse)
        complex_words = len([w for w in words if len(w) > 7])
        conceptual_density = complex_words / len(words) if words else 0

        # Unique concept density (parole uniche di contenuto)
        content_words = [w for w in words if len(w) > 4]  #跳过短词
        unique_concepts = len(set(content_words))
        concept_diversity = unique_concepts / len(content_words) if content_words else 0

        # Coerenza tematica (condivisione parole tra frasi)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        sentence_word_sets = [set(s.lower().split()) for s in sentences]
        overlaps = []
        for i in range(len(sentence_word_sets) - 1):
            overlap = len(sentence_word_sets[i] & sentence_word_sets[i+1])
            overlaps.append(overlap)

        avg_overlap = statistics.mean(overlaps) if overlaps else 0
        max_overlap = max(overlaps) if overlaps else 0

        # Topic consistency (variazione overlap)
        if len(overlaps) > 1:
            overlap_variability = statistics.stdev(overlaps)
        else:
            overlap_variability = 0

        metrics = {
            'subjectivity': round(subjectivity, 4),
            'conceptual_density': round(conceptual_density, 4),
            'concept_diversity': round(concept_diversity, 4),
            'thematic_coherence': round(avg_overlap, 2),
            'max_thematic_overlap': max_overlap,
            'overlap_variability': round(overlap_variability, 3),
            'complex_words_count': complex_words,
            'adverbs_count': len([w for w in words if w.endswith('ly')])
        }

        # Confidence basata su densità concettuale
        confidence = min(0.9, 0.4 + conceptual_density * 0.5)
        metrics['confidence'] = round(confidence, 4)

        return metrics

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """Prediction basata su semantica"""
        subjectivity = metrics.get('subjectivity', 0.5)
        conceptual_density = metrics.get('conceptual_density', 0.3)
        coherence = metrics.get('thematic_coherence', 5)

        ai_score = 0.0

        # Oggettività eccessiva indica AI
        if subjectivity < 0.1:
            ai_score += 0.3

        # Densità concettuale uniforme indica AI
        if 0.15 < conceptual_density < 0.25:
            ai_score += 0.2

        # Coerenza troppo perfetta indica AI
        if coherence > 8:
            ai_score += 0.3

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob
