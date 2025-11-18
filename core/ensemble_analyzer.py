#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble Analyzer per TextAnalyzer
Sistema di ensemble learning con 5 analizzatori specializzati
Include: Majority Voting, Weighted Voting, Confidence Aggregation
"""

import statistics
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter
import json
import os
from datetime import datetime

# Import degli analizzatori base (disponibili nel progetto)
# Il sistema ensemble è autonomo e non dipende da altri analyzer


class LexicalAnalyzer:
    """Analizzatore specializzato in metriche lessicali"""

    def __init__(self):
        self.name = "LexicalAnalyzer"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi lessicale dettagliata"""
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

        return {
            'ttr': ttr,
            'ttr_variation': ttr_variation,
            'burstiness': burstiness,
            'unique_words_ratio': len(unique_words) / len(words) if words else 0,
            'confidence': min(0.9, 0.6 + abs(ttr - 0.5) * 0.6)  # Confidence basata su certezza TTR
        }

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


class SyntacticAnalyzer:
    """Analizzatore specializzato in metriche sintattiche"""

    def __init__(self):
        self.name = "SyntacticAnalyzer"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi sintattica dettagliata"""
        import re

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

        return {
            'avg_sentence_length': avg_length,
            'sentence_variability': variability,
            'pattern_repetitiveness': pattern_repetitiveness,
            'sentence_count': len(sentences),
            'confidence': min(0.9, 0.5 + variability * 0.4)
        }

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


class SemanticAnalyzer:
    """Analizzatore specializzato in metriche semantiche"""

    def __init__(self):
        self.name = "SemanticAnalyzer"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi semantica basilare (coerenza, temi)"""
        import re

        # Soggettività/Oggettività (proxy tramite presenza aggettivi/avverbi)
        words = text.lower().split()
        adjectives_adverbs = len([w for w in words if w.endswith('ly') or w.endswith('ous')])
        subjectivity = adjectives_adverbs / len(words) if words else 0.5

        # Complessità concettuale (parole lunghe/complesse)
        complex_words = len([w for w in words if len(w) > 7])
        conceptual_density = complex_words / len(words) if words else 0

        # Coerenza tematica (condivisione parole tra frasi)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        sentence_word_sets = [set(s.lower().split()) for s in sentences]
        overlaps = []
        for i in range(len(sentence_word_sets) - 1):
            overlap = len(sentence_word_sets[i] & sentence_word_sets[i+1])
            overlaps.append(overlap)

        avg_overlap = statistics.mean(overlaps) if overlaps else 0

        return {
            'subjectivity': subjectivity,
            'conceptual_density': conceptual_density,
            'thematic_coherence': avg_overlap,
            'confidence': min(0.9, 0.4 + conceptual_density * 0.5)
        }

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


class StylisticAnalyzer:
    """Analizzatore specializzato in metriche stilistiche"""

    def __init__(self):
        self.name = "StylisticAnalyzer"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi stilistica (punteggiatura, maiuscole, ecc.)"""
        import re

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

        return {
            'punctuation_density': punct_density,
            'capital_ratio': upper_ratio,
            'punct_variability': punct_variability,
            'phrase_repetitiveness': phrase_repetitiveness,
            'confidence': min(0.9, 0.5 + punct_variability * 0.3)
        }

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


class AdvancedMLAnalyzer:
    """Analizzatore basato su pattern complessi (proxy ML)"""

    def __init__(self):
        self.name = "AdvancedMLAnalyzer"

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi con pattern complessi"""
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

        # Complexity score
        complexity = (normalized_entropy + transition_diversity) / 2

        return {
            'entropy': normalized_entropy,
            'transition_diversity': transition_diversity,
            'complexity_score': complexity,
            'confidence': min(0.95, 0.6 + complexity * 0.3)
        }

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

        ai_prob = min(1.0, ai_score)
        human_prob = 1.0 - ai_prob

        return ai_prob, human_prob


class EnsembleAnalyzer:
    """Ensemble di analizzatori con voting strategico"""

    def __init__(self):
        # Inizializza analizzatori
        self.analyzers = [
            LexicalAnalyzer(),
            SyntacticAnalyzer(),
            SemanticAnalyzer(),
            StylisticAnalyzer(),
            AdvancedMLAnalyzer()
        ]

        # Pesi per voting (possono essere calibrati)
        self.weights = [0.25, 0.25, 0.20, 0.15, 0.15]

        self.name = "EnsembleAnalyzer"
        self.prediction_history = []

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analisi ensemble completa"""
        individual_results = {}
        predictions = []

        # Esegui analisi con ogni analizzatore
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

                predictions.append({
                    'analyzer': analyzer.name,
                    'ai_prob': ai_prob,
                    'human_prob': human_prob,
                    'confidence': metrics.get('confidence', 0.5)
                })

            except Exception as e:
                individual_results[analyzer.name] = {
                    'error': str(e),
                    'ai_probability': 0.5,
                    'human_probability': 0.5,
                    'confidence': 0.0
                }

        # Aggrega risultati
        ensemble_result = self._aggregate_predictions(predictions)

        # Calcola confidenza complessiva
        overall_confidence = self._calculate_overall_confidence(predictions)

        # Salva in history
        self.prediction_history.append({
            'timestamp': datetime.now().isoformat(),
            'ensemble_result': ensemble_result,
            'overall_confidence': overall_confidence
        })

        return {
            'individual_results': individual_results,
            'ensemble_result': ensemble_result,
            'overall_confidence': overall_confidence,
            'prediction_method': 'weighted_voting',
            'analyzer_count': len(self.analyzers)
        }

    def _aggregate_predictions(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggrega predictions con weighted voting"""

        # Weighted average
        weighted_ai_sum = 0
        weighted_human_sum = 0
        weight_sum = 0
        confidence_weighted_sum = 0

        agreement_scores = []  # Per misurare accordo tra analizzatori

        for i, pred in enumerate(predictions):
            weight = self.weights[i] * pred['confidence']  # Pesato per confidenza
            weighted_ai_sum += pred['ai_prob'] * weight
            weighted_human_sum += pred['human_prob'] * weight
            weight_sum += weight
            confidence_weighted_sum += pred['confidence'] * self.weights[i]

            agreement_scores.append(pred['ai_prob'])

        if weight_sum > 0:
            ai_prob = weighted_ai_sum / weight_sum
            human_prob = weighted_human_sum / weight_sum
        else:
            ai_prob = 0.5
            human_prob = 0.5

        # Misura accordo (varianza bassa = alto accordo)
        if agreement_scores:
            agreement_variance = statistics.variance(agreement_scores)
            agreement_score = 1.0 - min(1.0, agreement_variance)
        else:
            agreement_score = 0.0

        # Classificazione
        if ai_prob > 0.6:
            classification = "Probabilmente AI"
            confidence_level = "Alta" if ai_prob > 0.75 else "Media"
        elif ai_prob < 0.4:
            classification = "Probabilmente Umano"
            confidence_level = "Alta" if human_prob > 0.75 else "Media"
        else:
            classification = "Indeterminato"
            confidence_level = "Bassa"

        return {
            'ai_probability': round(ai_prob, 4),
            'human_probability': round(human_prob, 4),
            'classification': classification,
            'confidence_level': confidence_level,
            'agreement_score': round(agreement_score, 3),
            'weighted_confidence': round(confidence_weighted_sum, 3)
        }

    def _calculate_overall_confidence(self, predictions: List[Dict[str, Any]]) -> float:
        """Calcola confidenza complessiva dell'ensemble"""

        # Fattori di confidenza:
        # 1. Media delle confidenze individuali
        avg_individual_conf = statistics.mean([p['confidence'] for p in predictions])

        # 2. Accordo tra analizzatori
        ai_probs = [p['ai_prob'] for p in predictions]
        if len(ai_probs) > 1:
            prob_variance = statistics.variance(ai_probs)
            agreement = 1.0 - min(1.0, prob_variance)
        else:
            agreement = 1.0

        # 3. Distanza dalla soglia decisionale (0.5)
        avg_ai_prob = statistics.mean(ai_probs)
        certainty = abs(avg_ai_prob - 0.5) * 2  # 0-1, più alto = più certi

        # Combina fattori
        overall_conf = (avg_individual_conf * 0.4 +
                       agreement * 0.3 +
                       certainty * 0.3)

        return round(min(1.0, overall_conf), 3)

    def get_prediction_statistics(self) -> Dict[str, Any]:
        """Statistiche sulle predictions"""
        if not self.prediction_history:
            return {'message': 'No predictions yet'}

        confidences = [p['overall_confidence'] for p in self.prediction_history]
        ai_probs = [p['ensemble_result']['ai_probability'] for p in self.prediction_history]

        return {
            'total_predictions': len(self.prediction_history),
            'avg_confidence': round(statistics.mean(confidences), 3),
            'min_confidence': round(min(confidences), 3),
            'max_confidence': round(max(confidences), 3),
            'avg_ai_probability': round(statistics.mean(ai_probs), 3),
            'prediction_variance': round(statistics.variance(ai_probs), 4)
        }

    def export_predictions(self, filename: str = "ensemble_predictions.json"):
        """Esporta history predictions"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'analyzer_count': len(self.analyzers),
            'weights': self.weights,
            'statistics': self.get_prediction_statistics(),
            'history': self.prediction_history[-100:]  # Ultime 100
        }

        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 Predictions exported to: {filepath}")
        return filepath


# Test
if __name__ == "__main__":
    ensemble = EnsembleAnalyzer()

    # Test con testo umano
    human_text = "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions."

    print("Testing ensemble with human text:")
    result = ensemble.analyze(human_text)
    print(f"  Classification: {result['ensemble_result']['classification']}")
    print(f"  AI Probability: {result['ensemble_result']['ai_probability']}")
    print(f"  Overall Confidence: {result['overall_confidence']}")
    print(f"  Agreement: {result['ensemble_result']['agreement_score']}")

    # Test con testo AI
    ai_text = "Artificial intelligence represents a revolutionary advancement in modern technology. This field encompasses machine learning, natural language processing, and complex algorithmic systems designed to simulate human cognitive functions. AI has the potential to transform various industries, including healthcare, transportation, and education."

    print("\nTesting ensemble with AI text:")
    result = ensemble.analyze(ai_text)
    print(f"  Classification: {result['ensemble_result']['classification']}")
    print(f"  AI Probability: {result['ensemble_result']['ai_probability']}")
    print(f"  Overall Confidence: {result['overall_confidence']}")

    print("\nPrediction Statistics:")
    print(ensemble.get_prediction_statistics())
