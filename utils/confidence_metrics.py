#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Confidence Metrics per TextAnalyzer
Sistema avanzato di metriche di confidenza statistica
Include: Intervalli di confidenza, Bootstrap, Bayesian Inference, Uncertainty Quantification
"""

import numpy as np
import statistics
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import json
import os
from scipy import stats


class ConfidenceMetrics:
    """Calcolo metriche di confidenza avanzate"""

    def __init__(self):
        self.name = "ConfidenceMetrics"

    def calculate_confidence_intervals(self, predictions: List[float],
                                     confidence_level: float = 0.95,
                                     method: str = "bootstrap") -> Dict[str, Any]:
        """
        Calcola intervalli di confidenza per le predictions

        Args:
            predictions: Lista di probabilità AI
            confidence_level: Livello di confidenza (0.95 = 95%)
            method: Metodo ('bootstrap', 'wilson', 'normal')

        Returns:
            Dict con intervalli di confidenza
        """
        predictions = np.array(predictions)
        n = len(predictions)
        mean_pred = np.mean(predictions)

        result = {
            'mean': float(mean_pred),
            'std': float(np.std(predictions)),
            'confidence_level': confidence_level,
            'n_samples': n,
            'method': method
        }

        if method == "bootstrap":
            # Bootstrap resampling
            n_bootstrap = 1000
            bootstrap_means = []

            for _ in range(n_bootstrap):
                # Resample con sostituzione
                sample = np.random.choice(predictions, size=n, replace=True)
                bootstrap_means.append(np.mean(sample))

            # Calcola intervallo di confidenza
            alpha = 1 - confidence_level
            lower_percentile = (alpha / 2) * 100
            upper_percentile = (1 - alpha / 2) * 100

            ci_lower = np.percentile(bootstrap_means, lower_percentile)
            ci_upper = np.percentile(bootstrap_means, upper_percentile)

            result['ci_lower'] = float(ci_lower)
            result['ci_upper'] = float(ci_upper)
            result['margin_of_error'] = float((ci_upper - ci_lower) / 2)
            result['bootstrap_stdev'] = float(np.std(bootstrap_means))

        elif method == "normal":
            # Approssimazione normale (assumendo distribuzione normale)
            z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
            std_error = np.std(predictions) / np.sqrt(n)

            ci_lower = mean_pred - z_score * std_error
            ci_upper = mean_pred + z_score * std_error

            result['ci_lower'] = float(ci_lower)
            result['ci_upper'] = float(ci_upper)
            result['margin_of_error'] = float(z_score * std_error)
            result['std_error'] = float(std_error)

        elif method == "wilson":
            # Wilson score interval (per proporzioni)
            # Approssimazione per Bernoulli (0 o 1)
            binary_preds = (predictions > 0.5).astype(float)
            p = np.mean(binary_preds)

            z = stats.norm.ppf(1 - (1 - confidence_level) / 2)
            denominator = 1 + z**2 / n
            center = (p + z**2 / (2 * n)) / denominator
            margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denominator

            result['wilson_score'] = float(p)
            result['ci_lower'] = float(center - margin)
            result['ci_upper'] = float(center + margin)
            result['margin_of_error'] = float(margin)

        return result

    def bootstrap_ensemble_predictions(self, ensemble_results: List[Dict[str, Any]],
                                     n_bootstrap: int = 1000) -> Dict[str, Any]:
        """
        Bootstrap sulle predictions dell'ensemble per stimare incertezza

        Args:
            ensemble_results: Lista di risultati ensemble
            n_bootstrap: Numero di campioni bootstrap

        Returns:
            Statistiche bootstrap
        """
        if not ensemble_results:
            return {'error': 'No ensemble results provided'}

        ai_probs = [r['ensemble_result']['ai_probability'] for r in ensemble_results]
        confidences = [r['overall_confidence'] for r in ensemble_results]

        ai_probs = np.array(ai_probs)
        confidences = np.array(confidences)

        bootstrap_ai = []
        bootstrap_conf = []

        for _ in range(n_bootstrap):
            # Resample con sostituzione
            indices = np.random.choice(len(ai_probs), size=len(ai_probs), replace=True)

            bootstrap_ai.append(np.mean(ai_probs[indices]))
            bootstrap_conf.append(np.mean(confidences[indices]))

        bootstrap_ai = np.array(bootstrap_ai)
        bootstrap_conf = np.array(bootstrap_conf)

        # Statistiche bootstrap
        return {
            'ai_probability': {
                'mean': float(np.mean(bootstrap_ai)),
                'std': float(np.std(bootstrap_ai)),
                'ci_95': [float(np.percentile(bootstrap_ai, 2.5)),
                         float(np.percentile(bootstrap_ai, 97.5))],
                'median': float(np.median(bootstrap_ai)),
                'min': float(np.min(bootstrap_ai)),
                'max': float(np.max(bootstrap_ai))
            },
            'confidence': {
                'mean': float(np.mean(bootstrap_conf)),
                'std': float(np.std(bootstrap_conf)),
                'ci_95': [float(np.percentile(bootstrap_conf, 2.5)),
                         float(np.percentile(bootstrap_conf, 97.5))],
                'median': float(np.median(bootstrap_conf)),
                'min': float(np.min(bootstrap_conf)),
                'max': float(np.max(bootstrap_conf))
            },
            'n_bootstrap': n_bootstrap,
            'original_samples': len(ensemble_results)
        }

    def bayesian_credible_interval(self, ai_probabilities: List[float],
                                  prior_alpha: float = 1.0,
                                  prior_beta: float = 1.0,
                                  credibility_level: float = 0.95) -> Dict[str, Any]:
        """
        Calcola intervalli credibili bayesiani
        Usa Beta-Binomial conjugate prior

        Args:
            ai_probabilities: Probabilità AI (0-1)
            prior_alpha, prior_beta: Parametri prior Beta
            credibility_level: Livello di credibilità

        Returns:
            Intervalli credibili bayesiani
        """
        if not ai_probabilities:
            return {'error': 'No probabilities provided'}

        # Converti a successi (1 se prob > 0.5)
        successes = sum(1 for p in ai_probabilities if p > 0.5)
        trials = len(ai_probabilities)

        # Posterior parameters (Beta distribution)
        posterior_alpha = prior_alpha + successes
        posterior_beta = prior_beta + trials - successes

        # Calcola intervallo credibile
        alpha_level = (1 - credibility_level) / 2
        ci_lower = stats.beta.ppf(alpha_level, posterior_alpha, posterior_beta)
        ci_upper = stats.beta.ppf(1 - alpha_level, posterior_alpha, posterior_beta)

        # Posterior mean
        posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)

        # Posterior mode
        mode = (posterior_alpha - 1) / (posterior_alpha + posterior_beta - 2) if posterior_alpha > 1 and posterior_beta > 1 else posterior_mean

        return {
            'credibility_level': credibility_level,
            'posterior_mean': float(posterior_mean),
            'posterior_mode': float(mode),
            'credible_interval': [float(ci_lower), float(ci_upper)],
            'prior': {
                'alpha': prior_alpha,
                'beta': prior_beta
            },
            'posterior': {
                'alpha': posterior_alpha,
                'beta': posterior_beta
            },
            'effective_sample_size': float(posterior_alpha + posterior_beta)
        }

    def prediction_uncertainty(self, ensemble_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Quantifica incertezza di una singola prediction
        Basata su: accordo tra analizzatori, distanza dalla soglia, confidenza

        Args:
            ensemble_result: Risultato ensemble

        Returns:
            Metriche di incertezza
        """
        individual = ensemble_result.get('individual_results', {})
        ensemble = ensemble_result.get('ensemble_result', {})

        if not individual or not ensemble:
            return {'error': 'Invalid ensemble result'}

        # 1. Disaccordo tra analizzatori
        ai_probs = [r['ai_probability'] for r in individual.values()
                   if 'ai_probability' in r and isinstance(r['ai_probability'], (int, float))]

        disagreement = 0.0
        if len(ai_probs) > 1:
            disagreement = float(np.std(ai_probs))  # Standard deviation come misura di disaccordo

        # 2. Vicinanza alla soglia decisionale
        ai_prob = ensemble.get('ai_probability', 0.5)
        threshold_distance = abs(ai_prob - 0.5) * 2  # 0-1, più alto = più lontano dalla soglia

        # 3. Accordo tra analizzatori (già calcolato nell'ensemble)
        agreement_score = ensemble.get('agreement_score', 0.5)

        # 4. Confidenza ponderata
        weighted_confidence = ensemble.get('weighted_confidence', 0.5)

        # Combina in incertezza totale
        uncertainty_factors = {
            'disagreement': disagreement,  # Alto = più incerto
            'threshold_proximity': 1.0 - threshold_distance,  # Alto = più incerto
            'low_agreement': 1.0 - agreement_score,  # Alto = più incerto
            'low_confidence': 1.0 - weighted_confidence  # Alto = più incerto
        }

        # Incertezza totale (0-1, più alto = più incerto)
        total_uncertainty = np.mean(list(uncertainty_factors.values()))

        # Incertezza specifica (0-1, più alto = più certo)
        prediction_certainty = 1.0 - total_uncertainty

        # Classificazione incertezza
        if prediction_certainty > 0.8:
            certainty_level = "Molto Alta"
        elif prediction_certainty > 0.6:
            certainty_level = "Alta"
        elif prediction_certainty > 0.4:
            certainty_level = "Media"
        elif prediction_certainty > 0.2:
            certainty_level = "Bassa"
        else:
            certainty_level = "Molto Bassa"

        return {
            'prediction_certainty': round(prediction_certainty, 4),
            'total_uncertainty': round(total_uncertainty, 4),
            'certainty_level': certainty_level,
            'uncertainty_breakdown': {k: round(v, 4) for k, v in uncertainty_factors.items()},
            'threshold_distance': round(threshold_distance, 4),
            'recommendation': self._get_recommendation(prediction_certainty, ai_prob),
            'factors': {
                'analyzer_count': len(ai_probs),
                'ai_probability': ai_prob,
                'agreement_score': agreement_score,
                'weighted_confidence': weighted_confidence
            }
        }

    def _get_recommendation(self, certainty: float, ai_prob: float) -> str:
        """Genera raccomandazione basata su certezza e probabilità"""
        if certainty > 0.8 and (ai_prob > 0.8 or ai_prob < 0.2):
            return "Prediction molto affidabile. Alta confidenza nella classificazione."
        elif certainty > 0.6:
            return "Prediction affidabile. Classificazione credibile."
        elif certainty > 0.4:
            return "Prediction moderatamente affidabile. Considera fattori aggiuntivi."
        else:
            return "Prediction incerta. Si raccomanda analisi manuale o dati aggiuntivi."

    def model_reliability(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Valuta affidabilità complessiva del modello

        Args:
            predictions: Lista di risultati ensemble

        Returns:
            Metriche di affidabilità
        """
        if not predictions:
            return {'error': 'No predictions provided'}

        confidences = [p['overall_confidence'] for p in predictions]
        ai_probs = [p['ensemble_result']['ai_probability'] for p in predictions]

        # Statistiche di base
        stats = {
            'mean_confidence': statistics.mean(confidences),
            'std_confidence': statistics.stdev(confidences) if len(confidences) > 1 else 0,
            'mean_ai_prob': statistics.mean(ai_probs),
            'std_ai_prob': statistics.stdev(ai_probs) if len(ai_probs) > 1 else 0,
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'total_predictions': len(predictions)
        }

        # Affidabilità basata su confidenza
        high_conf_predictions = sum(1 for c in confidences if c > 0.7)
        reliability_score = high_conf_predictions / len(predictions)

        # Stabilità delle predictions
        predictions_stability = 1.0 - (stats['std_ai_prob'] / 0.5)  # Normalizzato
        predictions_stability = max(0.0, min(1.0, predictions_stability))

        # Diversità delle predictions
        entropy = 0
        unique_probs = list(set([round(p, 2) for p in ai_probs]))
        for prob in unique_probs:
            count = sum(1 for p in ai_probs if round(p, 2) == prob)
            p_normalized = count / len(ai_probs)
            if p_normalized > 0:
                entropy -= p_normalized * np.log2(p_normalized)

        diversity_score = entropy / np.log2(len(unique_probs)) if len(unique_probs) > 1 else 0

        # Affidabilità finale (0-1)
        final_reliability = (reliability_score * 0.5 +
                           predictions_stability * 0.3 +
                           diversity_score * 0.2)

        return {
            'reliability_score': round(final_reliability, 4),
            'reliability_grade': self._grade_reliability(final_reliability),
            'confidence_statistics': {
                'mean': round(stats['mean_confidence'], 4),
                'std': round(stats['std_confidence'], 4),
                'high_confidence_ratio': round(high_conf_predictions / len(predictions), 4)
            },
            'prediction_statistics': {
                'mean_ai_probability': round(stats['mean_ai_prob'], 4),
                'std_ai_probability': round(stats['std_ai_prob'], 4),
                'stability_score': round(predictions_stability, 4),
                'diversity_score': round(diversity_score, 4)
            },
            'total_predictions': stats['total_predictions'],
            'recommendation': self._get_reliability_recommendation(final_reliability)
        }

    def _grade_reliability(self, score: float) -> str:
        """Converte score in voto letterale"""
        if score >= 0.9:
            return "A+ (Eccellente)"
        elif score >= 0.8:
            return "A (Molto Buono)"
        elif score >= 0.7:
            return "B+ (Buono)"
        elif score >= 0.6:
            return "B (Discreto)"
        elif score >= 0.5:
            return "C (Sufficiente)"
        else:
            return "D (Insufficiente)"

    def _get_reliability_recommendation(self, score: float) -> str:
        """Raccomandazione basata su affidabilità"""
        if score >= 0.8:
            return "Modello molto affidabile. Può essere usato per decisioni critiche."
        elif score >= 0.6:
            return "Modello affidabile. Adatto per la maggior parte delle applicazioni."
        elif score >= 0.4:
            return "Affidabilità moderata. Considera miglioramenti o validazione aggiuntiva."
        else:
            return "Affidabilità bassa. Si raccomanda revisione del modello."

    def export_confidence_report(self, results: Dict[str, Any],
                               filename: str = "confidence_report.json"):
        """Esporta report completo di confidenza"""
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"💾 Confidence report saved to: {filepath}")
        return filepath


# Test
if __name__ == "__main__":
    # Simula risultati ensemble
    test_predictions = [
        {'ensemble_result': {'ai_probability': 0.7}, 'overall_confidence': 0.8},
        {'ensemble_result': {'ai_probability': 0.6}, 'overall_confidence': 0.7},
        {'ensemble_result': {'ai_probability': 0.8}, 'overall_confidence': 0.9},
    ]

    metrics = ConfidenceMetrics()

    # Test confidence intervals
    ai_probs = [p['ensemble_result']['ai_probability'] for p in test_predictions]
    ci = metrics.calculate_confidence_intervals(ai_probs)
    print("Confidence Intervals:")
    print(f"  Mean: {ci['mean']:.4f}")
    print(f"  CI 95%: [{ci['ci_lower']:.4f}, {ci['ci_upper']:.4f}]")

    # Test bootstrap
    bootstrap = metrics.bootstrap_ensemble_predictions(test_predictions)
    print("\nBootstrap Analysis:")
    print(f"  AI Prob Mean: {bootstrap['ai_probability']['mean']:.4f}")
    print(f"  CI 95%: [{bootstrap['ai_probability']['ci_95'][0]:.4f}, {bootstrap['ai_probability']['ci_95'][1]:.4f}]")

    # Test Bayesian
    bayesian = metrics.bayesian_credible_interval(ai_probs)
    print("\nBayesian Credible Interval:")
    print(f"  Posterior Mean: {bayesian['posterior_mean']:.4f}")
    print(f"  Credible Interval: [{bayesian['credible_interval'][0]:.4f}, {bayesian['credible_interval'][1]:.4f}]")

    # Test single prediction uncertainty
    full_test_result = {
        'individual_results': {
            'Analyzer1': {'ai_probability': 0.7},
            'Analyzer2': {'ai_probability': 0.6},
            'Analyzer3': {'ai_probability': 0.8}
        },
        'ensemble_result': {
            'ai_probability': 0.7,
            'agreement_score': 0.9,
            'weighted_confidence': 0.8
        },
        'overall_confidence': 0.8
    }

    uncertainty = metrics.prediction_uncertainty(full_test_result)
    print("\nPrediction Uncertainty:")
    print(f"  Certainty: {uncertainty['prediction_certainty']:.4f}")
    print(f"  Level: {uncertainty['certainty_level']}")
    print(f"  Recommendation: {uncertainty['recommendation']}")

    print("\n✅ Confidence metrics test complete!")
