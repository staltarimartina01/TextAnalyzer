# -*- coding: utf-8 -*-
"""
Analyzer - Analizzatore principale per testi AI vs Umano
Modulo di orchestrazione per l'analisi completa dei testi
"""

import os
import json
import pickle
import statistics
from typing import Dict, List, Any, Tuple
from datetime import datetime

from core.text_processor import TextProcessor
from features.feature_extractor import FeatureExtractor
from utils.data_loader import DataLoader
from utils.evaluator import ModelEvaluator


class TextAnalyzer:
    """Analizzatore principale per classificazione testi AI vs umani"""
    
    def __init__(self, model_path: str = None):
        self.text_processor = TextProcessor()
        self.feature_extractor = FeatureExtractor()
        self.data_loader = DataLoader()
        self.evaluator = ModelEvaluator()
        
        # Inizializza modello (se disponibile)
        self.model = None
        self.scaler = None
        self.feature_names = []
        
        if model_path and os.path.exists(model_path):
            self._load_model(model_path)
        
        # Database delle caratteristiche conosciute
        self.known_patterns = {
            'ai_indicators': {
                'high_lexical_diversity': 0.85,  # AI tende ad avere alta diversità lessicale
                'low_stylistic_consistency': 0.3,  # AI ha pattern meno consistenti
                'high_complexity_ratio': 0.7,  # AI usa costruzioni complesse
                'low_repetition_ratio': 0.2,  # AI ripete meno
                'structured_paragraphs': 0.8  # AI organizza meglio i paragrafi
            },
            'human_indicators': {
                'low_lexical_diversity': 0.4,  # Umani hanno diversità più bassa
                'high_stylistic_consistency': 0.7,  # Umani hanno stile più consistente
                'natural_variations': 0.6,  # Variazioni naturali nel testo
                'emotional_markers': 0.5,  # Indicatori emotivi
                'conversational_tone': 0.4  # Tono più conversazionale
            }
        }

    def analyze_text(self, text: str, file_name: str = None) -> Dict[str, Any]:
        """Analizza un testo e restituisce risultati dettagliati"""
        if not text or len(text.strip()) < 10:
            return {
                'error': 'Testo troppo corto per l\'analisi (minimo 10 caratteri)',
                'text_preview': text[:100] + '...' if len(text) > 100 else text
            }
        
        try:
            # Estrazione features
            features = self.feature_extractor.extract_all_features(text)
            
            # Calcola confidence score basato su pattern conosciuti
            confidence = self._calculate_confidence(features['all_features'])
            
            # Se modello ML disponibile, usa predizione
            prediction = None
            probability = None
            if self.model:
                prediction, probability = self._ml_predict(features['all_features'])
            
            # Classificazione rule-based
            rule_based_prediction = self._rule_based_classification(features['all_features'])
            
            # Combina risultati
            result = {
                'file_name': file_name,
                'analysis_timestamp': datetime.now().isoformat(),
                'text_stats': self.text_processor.get_text_stats(text),
                'features': features,
                'confidence_score': confidence,
                'rule_based_prediction': rule_based_prediction,
                'ml_prediction': prediction,
                'ml_probability': probability,
                'final_assessment': self._combine_predictions(rule_based_prediction, prediction, confidence, probability)
            }
            
            return result
            
        except Exception as e:
            return {
                'error': f'Errore durante l\'analisi: {str(e)}',
                'text_preview': text[:100] + '...' if len(text) > 100 else text
            }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analizza un file di testo"""
        if not os.path.exists(file_path):
            return {'error': f'File non trovato: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return self.analyze_text(text, os.path.basename(file_path))
            
        except Exception as e:
            return {'error': f'Errore nella lettura del file: {str(e)}'}

    def batch_analyze(self, directory: str, file_pattern: str = "*.txt") -> List[Dict[str, Any]]:
        """Analizza multiple files in una directory"""
        results = []
        files = self.data_loader.load_files_from_directory(directory, file_pattern)
        
        for file_path in files:
            result = self.analyze_file(file_path)
            result['file_path'] = file_path
            results.append(result)
        
        return results

    def generate_report(self, results: List[Dict[str, Any]], output_path: str = None) -> str:
        """Genera un report dettagliato dell'analisi"""
        if not results:
            return "Nessun risultato da analizzare."
        
        report = []
        report.append("=" * 80)
        report.append("REPORT ANALISI TESTI AI vs UMANI")
        report.append("=" * 80)
        report.append(f"Data analisi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Numero di testi analizzati: {len(results)}")
        report.append("")
        
        # Statistiche generali
        ai_count = sum(1 for r in results if r.get('final_assessment', {}).get('prediction') == 'AI')
        human_count = sum(1 for r in results if r.get('final_assessment', {}).get('prediction') == 'UMANO')
        
        report.append("STATISTICHE GENERALI:")
        report.append(f"  Testi identificati come AI: {ai_count} ({ai_count/len(results)*100:.1f}%)")
        report.append(f"  Testi identificati come Umani: {human_count} ({human_count/len(results)*100:.1f}%)")
        report.append("")
        
        # Dettagli per ogni testo
        report.append("DETTAGLI ANALISI:")
        report.append("-" * 80)
        
        for i, result in enumerate(results, 1):
            report.append(f"\n{i}. {result.get('file_name', 'File sconosciuto')}")
            
            if 'error' in result:
                report.append(f"   ERRORE: {result['error']}")
                continue
            
            assessment = result.get('final_assessment', {})
            prediction = assessment.get('prediction', 'Sconosciuto')
            confidence = assessment.get('confidence', 0)
            
            report.append(f"   Classificazione: {prediction}")
            report.append(f"   Confidenza: {confidence:.1%}")
            
            # Metriche chiave
            features = result.get('features', {})
            lexical = features.get('lexical', {})
            syntactic = features.get('syntactic', {})
            
            report.append(f"   Diversità lessicale: {lexical.get('lexical_diversity', 0):.3f}")
            report.append(f"   Lunghezza media frase: {syntactic.get('avg_sentence_length', 0):.1f} parole")
            report.append(f"   Consistenza stilistica: {features.get('style', {}).get('stylistic_consistency', 0):.3f}")
        
        # Analisi comparativa
        if len(results) > 1:
            report.append("\n" + "=" * 80)
            report.append("ANALISI COMPARATIVA")
            report.append("=" * 80)
            
            self._add_comparative_analysis(report, results)
        
        report_text = "\n".join(report)
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"Report salvato in: {output_path}")
            except Exception as e:
                print(f"Errore nel salvataggio del report: {e}")
        
        return report_text

    def _calculate_confidence(self, features: Dict[str, float]) -> float:
        """Calcola il confidence score basato su features"""
        ai_score = 0
        human_score = 0
        evaluated_features = 0
        
        # Features chiave da valutare (soglie aggiustate)
        key_features = [
            ('lexical_lexical_diversity', 0.95, 'ai'),  # Molto alta diversità -> AI
            ('style_stylistic_consistency', 0.7, 'human'),  # Molto alta consistenza -> Umano
            ('syntactic_complex_sentences_ratio', 0.5, 'ai'),  # Molte frasi complesse -> AI
            ('style_word_repetition_ratio', 0.1, 'human'),  # Alcune ripetizioni -> Umano
            ('lexical_type_token_ratio', 0.95, 'ai'),  # TTR molto alto -> AI
            ('style_stylistic_consistency', 0.2, 'ai'),  # Molto bassa consistenza -> AI
        ]
        
        for feature_name, threshold, prediction_type in key_features:
            if feature_name in features:
                evaluated_features += 1
                value = features[feature_name]
                
                if prediction_type == 'ai':
                    if value > threshold:
                        ai_score += 1
                    else:
                        human_score += 1
                else:  # human
                    if value > threshold:
                        human_score += 1
                    else:
                        ai_score += 1
        
        if evaluated_features == 0:
            return 0.5
        
        # Confidenza basata su features valutate
        confidence = max(ai_score, human_score) / evaluated_features
        
        # Bonus se molte features concordano
        total_score = ai_score + human_score
        if total_score > 0:
            agreement_bonus = (max(ai_score, human_score) / total_score - 0.5) * 0.3
            confidence = min(confidence + agreement_bonus, 0.95)
        
        return confidence

    def _rule_based_classification(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Classificazione basata su regole predefinite"""
        ai_score = 0
        human_score = 0
        
        # Regole per AI (soglie più realistiche)
        if features.get('lexical_lexical_diversity', 0) > 0.9:
            ai_score += 2
        if features.get('lexical_type_token_ratio', 0) > 0.9:
            ai_score += 2
        if features.get('style_stylistic_consistency', 0) < 0.3:
            ai_score += 1
        if features.get('syntactic_avg_sentence_length', 0) > 15:  # Frasi lunghe
            ai_score += 1
        
        # Regole per Umani (più flessibili)
        if features.get('lexical_lexical_diversity', 0) < 0.85:  # Non perfetta diversità
            human_score += 2
        if features.get('style_stylistic_consistency', 0) > 0.2:  # Almeno un po' di consistenza
            human_score += 2
        if features.get('style_word_repetition_ratio', 0) > 0.05:  # Alcune ripetizioni
            human_score += 1
        if features.get('style_contractions_ratio', 0) > 0.05:  # Contrazioni (naturale)
            human_score += 1
        
        prediction = 'AI' if ai_score > human_score else 'UMANO'
        confidence = max(ai_score, human_score) / (ai_score + human_score) if (ai_score + human_score) > 0 else 0.5
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'ai_score': ai_score,
            'human_score': human_score
        }

    def _ml_predict(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Predizione usando modello ML (se disponibile)"""
        if not self.model or not self.scaler:
            return None, None
        
        try:
            # Prepara il vettore delle features
            feature_vector = [features.get(name, 0.0) for name in self.feature_names]
            
            # Scala le features
            scaled_features = self.scaler.transform([feature_vector])
            
            # Predizione
            prediction = self.model.predict(scaled_features)[0]
            probabilities = self.model.predict_proba(scaled_features)[0]
            
            return prediction, max(probabilities)
            
        except Exception:
            return None, None

    def _combine_predictions(self, rule_based: Dict, ml_pred: str, rule_confidence: float, ml_probability: float) -> Dict[str, Any]:
        """Combina le predizioni rule-based e ML"""
        final_prediction = None
        final_confidence = 0
        
        if ml_pred and ml_probability:
            # Combina con pesi
            if rule_confidence > 0.7 and ml_probability > 0.7:
                # Entrambi concordano e sono confident
                if rule_based['prediction'] == ml_pred:
                    final_prediction = ml_pred
                    final_confidence = (rule_confidence + ml_probability) / 2
                else:
                    # Disaccordo - scegli il più confident
                    if rule_confidence > ml_probability:
                        final_prediction = rule_based['prediction']
                        final_confidence = rule_confidence
                    else:
                        final_prediction = ml_pred
                        final_confidence = ml_probability
            else:
                # Usa quello più confident
                if rule_confidence > ml_probability:
                    final_prediction = rule_based['prediction']
                    final_confidence = rule_confidence
                else:
                    final_prediction = ml_pred
                    final_confidence = ml_probability
        else:
            # Solo rule-based disponibile
            final_prediction = rule_based['prediction']
            final_confidence = rule_confidence
        
        return {
            'prediction': final_prediction,
            'confidence': final_confidence,
            'rule_based_used': True,
            'ml_used': ml_pred is not None
        }

    def _add_comparative_analysis(self, report: List[str], results: List[Dict[str, Any]]):
        """Aggiunge analisi comparativa al report"""
        # Raccogli features per analisi
        all_features = {}
        for result in results:
            if 'error' not in result:
                features = result.get('features', {})
                for category, feature_dict in features.items():
                    if isinstance(feature_dict, dict):
                        for name, value in feature_dict.items():
                            if name not in all_features:
                                all_features[name] = []
                            all_features[name].append(value)
        
        # Statistiche comparative
        report.append("METRICHE COMPARATIVE:")
        for feature_name, values in all_features.items():
            if len(values) > 1:
                mean_val = statistics.mean(values)
                std_val = statistics.stdev(values) if len(values) > 1 else 0
                report.append(f"  {feature_name}: μ={mean_val:.3f}, σ={std_val:.3f}")
        
        # Identificazione outlier
        report.append("\nOUTLIER IDENTIFICATI:")
        for result in results:
            if 'error' not in result:
                assessment = result.get('final_assessment', {})
                confidence = assessment.get('confidence', 0)
                if confidence < 0.6:  # Bassa confidence
                    report.append(f"  - {result.get('file_name', 'File sconosciuto')}: confidence {confidence:.1%}")

    def _load_model(self, model_path: str):
        """Carica modello ML salvato"""
        try:
            with open(f"{model_path}/model.pkl", 'rb') as f:
                self.model = pickle.load(f)
            with open(f"{model_path}/scaler.pkl", 'rb') as f:
                self.scaler = pickle.load(f)
            with open(f"{model_path}/feature_names.txt", 'r') as f:
                self.feature_names = [line.strip() for line in f]
        except Exception as e:
            print(f"Errore nel caricamento del modello: {e}")
            self.model = None
            self.scaler = None
            self.feature_names = []
