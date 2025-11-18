#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML Analyzer per TextAnalyzer
Analizzatore basato su pattern complessi (proxy ML)
"""

from typing import Dict, Any, Tuple
from collections import Counter
import numpy as np
from .base_analyzer import BaseAnalyzer


class MLAnalyzer(BaseAnalyzer):
    """
    Analizzatore basato su pattern complessi (proxy ML).

    Metriche calcolate:
    - Entropy: entropia caratteri (prevedibilità)
    - Transition Diversity: diversità transizioni parole
    - Complexity Score: score complessità combinato
    """

    def __init__(self):
        super().__init__()
        self.name = "MLAnalyzer"
        self.description = "Analizzatore pattern complessi (Entropia, Transizioni, ML)"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi con pattern complessi"""
        self._validate_input(text)

        words = text.split()
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]

        # Entropia del testo (prevedibilità)
        char_freq = Counter(text.lower())
        total_chars = sum(char_freq.values())
        entropy = 0
        for count in char_freq.values():
            p = count / total_chars
            if p > 0:
                entropy -= p * np.log2(p)

        # Normalizza entropia (0-1)
        max_entropy = np.log2(len(char_freq)) if len(char_freq) > 0 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.5

        # Transition patterns (pattern tra parole consecutive)
        word_pairs = [(words[i], words[i+1]) for i in range(len(words)-1)]
        pair_counter = Counter(word_pairs)
        unique_pairs = len(pair_counter)
        total_pairs = len(word_pairs)

        transition_diversity = unique_pairs / total_pairs if total_pairs > 0 else 0

        # Character transition entropy
        char_pairs = [(text[i], text[i+1]) for i in range(len(text)-1)]
        char_pair_counter = Counter(char_pairs)
        char_transition_diversity = len(char_pair_counter) / len(char_pairs) if char_pairs else 0

        # Word length distribution
        word_lengths = [len(w) for w in words]
        if word_lengths:
            length_entropy = 0
            length_counts = Counter(word_lengths)
            for count in length_counts.values():
                p = count / len(word_lengths)
                if p > 0:
                    length_entropy -= p * np.log2(p)

            # Normalize
            max_length_entropy = np.log2(len(length_counts))
            normalized_length_entropy = length_entropy / max_length_entropy if max_length_entropy > 0 else 0.5
        else:
            normalized_length_entropy = 0

        # Complexity score combinato
        complexity = (normalized_entropy + transition_diversity + char_transition_diversity) / 3

        # Repeating patterns
        max_repeat_count = max(pair_counter.values()) if pair_counter else 1
        max_repeat_ratio = max_repeat_count / total_pairs if total_pairs > 0 else 0

        metrics = {
            'entropy': round(normalized_entropy, 4),
            'length_entropy': round(normalized_length_entropy, 4),
            'transition_diversity': round(transition_diversity, 4),
            'char_transition_diversity': round(char_transition_diversity, 4),
            'complexity_score': round(complexity, 4),
            'max_repeat_ratio': round(max_repeat_ratio, 4),
            'unique_word_pairs': unique_pairs,
            'total_word_pairs': total_pairs,
            'unique_char_pairs': len(char_pair_counter),
            'vocabulary_size': len(set(words)),
            'avg_word_length': round(np.mean(word_lengths), 2) if word_lengths else 0
        }

        # Confidence basata su complexity
        confidence = min(0.95, 0.6 + complexity * 0.3)
        metrics['confidence'] = round(confidence, 4)

        return metrics

    def predict(self, metrics: Dict[str, Any]) -> Tuple[float, float]:
        """Prediction basata su pattern complessi"""
        entropy = metrics.get('entropy', 0.5)
        transition_div = metrics.get('transition_diversity', 0.5)
        complexity = metrics.get('complexity_score', 0.5)

        ai_score = 0.0

        # Entropia troppo bassa o alta indica AI
        if entropy < 0.3 or entropy > 0.8:
            ai_score += 0.3

        # Transition diversity troppo uniforme
        if transition_div < 0.4:
            ai_score += 0.3

        # Max repeat ratio alto indica ripetitività (AI)
        max_repeat = metrics.get('max_repeat_ratio', 0)
        if max_repeat > 0.1:
            ai_score += 0.2

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob
