#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble Engine per TextAnalyzer
Gestisce l'ensemble di analyzers con voting strategico
"""

import statistics
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import json
import os

from analyzers import DEFAULT_WEIGHTS, create_analyzer


class EnsembleEngine:
    """
    Engine per ensemble analysis con weighted voting.

    Combina risultati di più analyzers specializzati usando
    weighted voting strategico con confidence aggregation.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Inizializza ensemble engine.

        Args:
            weights: Dizionario {analyzer_name: weight} per custom weights
        """
        # Initialize all analyzers
        self.analyzers = [
            create_analyzer('lexical'),
            create_analyzer('syntactic'),
            create_analyzer('semantic'),
            create_analyzer('stylistic'),
            create_analyzer('ml')
        ]

        # Set weights
        if weights:
            self.weights = weights
        else:
            self.weights = DEFAULT_WEIGHTS.copy()

        self.name = "EnsembleEngine"
        self.prediction_history = []

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Esegue analisi ensemble completa.

        Args:
            text: Testo da analizzare

        Returns:
            Dict con risultati ensemble e individuali
        """
        individual_results = {}
        predictions = []

        # Run analysis with each analyzer
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

        # Aggregate results
        ensemble_result = self._aggregate_predictions(predictions)

        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(predictions)

        # Save to history
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

        agreement_scores = []

        for pred in predictions:
            # Get weight for this analyzer
            analyzer_name = pred['analyzer']
            weight = self.weights.get(analyzer_name, 0.2) * pred['confidence']

            weighted_ai_sum += pred['ai_prob'] * weight
            weighted_human_sum += pred['human_prob'] * weight
            weight_sum += weight
            confidence_weighted_sum += pred['confidence'] * self.weights.get(analyzer_name, 0.2)

            agreement_scores.append(pred['ai_prob'])

        if weight_sum > 0:
            ai_prob = weighted_ai_sum / weight_sum
            human_prob = weighted_human_sum / weight_sum
        else:
            ai_prob = 0.5
            human_prob = 0.5

        # Agreement score (1 - variance)
        if agreement_scores:
            agreement_variance = statistics.variance(agreement_scores)
            agreement_score = 1.0 - min(1.0, agreement_variance)
        else:
            agreement_score = 0.0

        # Classification
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

        if not predictions:
            return 0.0

        # Average individual confidence
        avg_individual_conf = statistics.mean([p['confidence'] for p in predictions])

        # Agreement between analyzers
        ai_probs = [p['ai_prob'] for p in predictions]
        if len(ai_probs) > 1:
            prob_variance = statistics.variance(ai_probs)
            agreement = 1.0 - min(1.0, prob_variance)
        else:
            agreement = 1.0

        # Distance from decision threshold (0.5)
        avg_ai_prob = statistics.mean(ai_probs)
        certainty = abs(avg_ai_prob - 0.5) * 2

        # Combine factors
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
            'history': self.prediction_history[-100:]  # Last 100
        }

        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 Predictions exported to: {filepath}")
        return filepath

    def set_weights(self, weights: Dict[str, float]):
        """Aggiorna pesi ensemble"""
        self.weights = weights

    def add_analyzer(self, analyzer_name: str, weight: float = 0.2):
        """Aggiunge analyzer all'ensemble"""
        try:
            analyzer = create_analyzer(analyzer_name)
            self.analyzers.append(analyzer)
            self.weights[analyzer_name] = weight
            return True
        except Exception as e:
            print(f"Error adding analyzer: {e}")
            return False

    def __repr__(self) -> str:
        return f"<EnsembleEngine(analyzers={len(self.analyzers)})>"
