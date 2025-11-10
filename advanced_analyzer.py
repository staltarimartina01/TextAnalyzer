# -*- coding: utf-8 -*-
"""
Advanced Text Analyzer per Tesi "LLM vs Autore Umano"
Sistema completo di analisi testuale avanzato con metriche lessicali, sintattiche, semantiche e stilistiche

Implementazione per analisi comparativa avanzata
Versione: 1.0
Data: 2025-11-10
"""

import nltk
import statistics
import re
import json
from collections import Counter
from typing import Dict, List, Any, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    from textblob import TextBlob
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError as e:
    print(f"⚠️ Avviso: Alcune librerie avanzate non disponibili: {e}")
    TextBlob = None
    TfidfVectorizer = None
    np = None

# Download NLTK data se necessario
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True) 
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

class AdvancedTextAnalyzer:
    """
    Analyzer avanzato per testi in inglese
    Include metriche per rilevamento AI vs umano
    """
    
    def __init__(self):
        # Stop words
        self.stop_words = set()
        try:
            if nltk.corpus.stopwords._fileids:
                self.stop_words = set(nltk.corpus.stopwords.words('english'))
        except:
            # Fallback stop words se NLTK fallisce
            self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # VADER sentiment analyzer
        self.vader_analyzer = None
        try:
            from nltk.sentiment import VADER
            self.vader_analyzer = VADER()
        except ImportError:
            try:
                # Metodo alternativo per accedere a VADER
                from nltk.sentiment.vader import SentimentIntensityAnalyzer
                self.vader_analyzer = SentimentIntensityAnalyzer()
            except:
                pass
        
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisi completa del testo con tutte le metriche
        
        Args:
            text: Testo in inglese (stringa)
            
        Returns:
            Dizionario JSON con tutte le metriche
        """
        try:
            if not text or not text.strip():
                return {"error": "Testo vuoto o non valido"}
            
            text = text.strip()
            results = {}
            
            # Inizializza risultati base
            results['text_info'] = {
                'word_count': len(text.split()),
                'character_count': len(text),
                'sentence_count': len(re.findall(r'[.!?]+', text))
            }
            
            # Metriche lessicali
            results['metriche_lessicali'] = self._lexical_analysis(text)
            
            # Metriche sintattiche  
            results['metriche_sintattiche'] = self._syntactic_analysis(text)
            
            # Metriche semantiche
            results['metriche_semantiche'] = self._semantic_analysis(text)
            
            # Metriche stilistiche
            results['metriche_stilistiche'] = self._stylistic_analysis(text)
            
            # Summary con score AI/Human detection
            results['ai_detection_score'] = self._calculate_ai_score(results)
            
            return results
            
        except Exception as e:
            return {"error": f"Analisi fallita: {str(e)}"}

    def _lexical_analysis(self, text: str) -> Dict[str, Any]:
        """Analisi lessicale completa"""
        try:
            words = re.findall(r'\b\w+\b', text.lower())
            if not words:
                return {}
            
            # Type-Token Ratio (TTR) Base
            unique_words = set(words)
            ttr_base = len(unique_words) / len(words)
            
            # TTR Progressivo (variazione nel tempo)
            ttr_progressive = []
            seen_words = set()
            for i, word in enumerate(words, 1):
                seen_words.add(word)
                ttr_progressive.append(len(seen_words) / i)
            
            ttr_variation = statistics.stdev(ttr_progressive) if len(ttr_progressive) > 1 else 0
            
            # Burstiness (creatività lessicale)
            freq = Counter(words)
            frequencies = list(freq.values())
            mean_freq = statistics.mean(frequencies)
            std_freq = statistics.stdev(frequencies) if len(frequencies) > 1 else 0
            burstiness = (std_freq - mean_freq) / (std_freq + mean_freq) if (std_freq + mean_freq) != 0 else 0
            
            # Densità lessicale (parole di contenuto vs strutturali)
            content_words = [w for w in words if w not in self.stop_words]
            content_density = len(content_words) / len(words) if words else 0
            
            # Ricchezza vocabolario per categoria
            word_categories = self._categorize_words(words)
            
            # Complex words (more than 6 characters)
            complex_words = [w for w in words if len(w) > 6]
            complex_ratio = len(complex_words) / len(words) if words else 0
            
            return {
                'ttr_base': round(ttr_base, 3),
                'ttr_variation': round(ttr_variation, 3),
                'burstiness': round(burstiness, 3),
                'densita_lessicale': round(content_density, 3),
                'parole_uniche': len(unique_words),
                'frequenza_media_parole': round(mean_freq, 2),
                'complessita_lessicale': round(complex_ratio, 3),
                'ricchezza_vocabulario': round(len(unique_words) / len(words), 3),
                'categorie_parole': word_categories
            }
            
        except Exception as e:
            return {'error_lexical': str(e)}

    def _syntactic_analysis(self, text: str) -> Dict[str, Any]:
        """Analisi sintattica del testo"""
        try:
            # Pulisci e dividi in frasi
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) < 2:
                return {'error': 'Testo troppo corto per analisi sintattica'}
            
            # Lunghezza frasi
            sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
            avg_sentence_length = statistics.mean(sentence_lengths)
            sentence_length_std = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
            sentence_variability = sentence_length_std / avg_sentence_length if avg_sentence_length > 0 else 0
            
            # Pattern ripetitivi (sequenze di 3 parole)
            words = re.findall(r'\b\w+\b', text.lower())
            repetitive_patterns_score = 0
            if len(words) >= 3:
                patterns = Counter()
                for i in range(len(words) - 2):
                    pattern = ' '.join(words[i:i+3])
                    patterns[pattern] += 1
                # Score basato su pattern che si ripetono più di una volta
                repetitive_patterns_score = sum(1 for count in patterns.values() if count > 1) / len(words)
            
            # Complessità strutturale
            complex_sentences = sum(1 for length in sentence_lengths if length > 20)  # frasi > 20 parole
            complex_ratio = complex_sentences / len(sentences) * 100
            
            # Punteggiatura varietà
            punctuation_types = len(re.findall(r'[,;:"()\-\[\]{}]', text))
            
            return {
                'numero_frasi': len(sentences),
                'lunghezza_media_frasi': round(avg_sentence_length, 1),
                'deviazione_standard_frasi': round(sentence_length_std, 2),
                'variabilita_lunghezza': round(sentence_variability, 3),
                'pattern_ripetitivi': round(repetitive_patterns_score, 4),
                'percentuale_frasi_complesse': round(complex_ratio, 1),
                'variazione_punteggiatura': punctuation_types
            }
            
        except Exception as e:
            return {'error_syntactic': str(e)}

    def _semantic_analysis(self, text: str) -> Dict[str, Any]:
        """Analisi semantica del testo"""
        try:
            result = {}
            
            # Sentiment Analysis con TextBlob
            if TextBlob:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                # Classificazione sentiment
                if polarity > 0.1:
                    sentiment_label = 'positive'
                elif polarity < -0.1:
                    sentiment_label = 'negative'
                else:
                    sentiment_label = 'neutral'
                
                result['sentiment_polarity'] = round(polarity, 3)
                result['sentiment_subjectivity'] = round(subjectivity, 3)
                result['sentiment_label'] = sentiment_label
            
            # VADER Sentiment (più accurato per testo inglese)
            if self.vader_analyzer:
                vader_scores = self.vader_analyzer.polarity_scores(text)
                result['vader_compound'] = round(vader_scores['compound'], 3)
                result['vader_positive'] = round(vader_scores['pos'], 3)
                result['vader_negative'] = round(vader_scores['neg'], 3)
                result['vader_neutral'] = round(vader_scores['neu'], 3)
            
            # Coerenza tematica con TF-IDF
            if TfidfVectorizer and np:
                thematic_coherence = self._calculate_thematic_coherence(text)
                result['coerenza_tematica'] = round(thematic_coherence, 3)
            
            # Transizioni emotive
            sentiment_transitions = self._calculate_sentiment_transitions(text)
            if sentiment_transitions:
                result['transizioni_emotive'] = round(statistics.mean(sentiment_transitions), 3)
                result['volatilita_emotiva'] = round(statistics.stdev(sentiment_transitions), 3)
            
            return result
            
        except Exception as e:
            return {'error_semantic': str(e)}

    def _stylistic_analysis(self, text: str) -> Dict[str, Any]:
        """Analisi stilistica del testo"""
        try:
            text_lower = text.lower()
            
            # Figure retoriche
            similes = len(re.findall(r'\b(as|like)\s+\w+\s+(?:a|an|the)?\s*\w*', text_lower))
            metaphors = len(re.findall(r'\b(\w+)\s+(?:is|are|was|were|seems|appears)\s+(\w+)', text_lower))
            
            # Connettivi logici
            connectives = re.findall(r'\b(however|therefore|moreover|thus|hence|consequently|nevertheless|although|while|whereas|since|because)\b', text_lower)
            
            # Originalità linguistica
            unusual_patterns = self._detect_unusual_patterns(text)
            
            # Coesione testuale
            cohesive_devices = re.findall(r'\b(furthermore|in addition|moving on|conversely|on the other hand|in contrast|similarly|likewise|in the same way)\b', text_lower)
            
            # Ripetizioni e anaphora
            repetitive_structures = self._detect_repetitive_structures(text)
            
            return {
                'figure_retoriche': {
                    'similitudini': similes,
                    'metafore': metaphors,
                    'totale_figure': similes + metaphors
                },
                'connettivi_logici': {
                    'count': len(connectives),
                    'tipi': list(set(connectives))
                },
                'originalita_linguistica': unusual_patterns,
                'coesione_testuale': {
                    'device_count': len(cohesive_devices),
                    'coesione_score': round(len(cohesive_devices) / max(len(re.findall(r'\b\w+\b', text)) / 100, 1), 3)
                },
                'strutture_ripetitive': repetitive_structures
            }
            
        except Exception as e:
            return {'error_stylistic': str(e)}

    def _calculate_thematic_coherence(self, text: str) -> float:
        """Calcola la coerenza tematica del testo"""
        try:
            # Dividi il testo in 4 segmenti
            words = re.findall(r'\b\w+\b', text.lower())
            if len(words) < 50:
                return 0.0
            
            segment_length = len(words) // 4
            segments = []
            for i in range(4):
                start = i * segment_length
                end = start + segment_length if i < 3 else len(words)
                segment_text = ' '.join(words[start:end])
                segments.append(segment_text)
            
            # Calcola TF-IDF e similarità
            vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(segments)
            
            # Calcola similarità media tra tutti i segmenti
            similarities = []
            for i in range(len(segments)):
                for j in range(i+1, len(segments)):
                    sim = cosine_similarity(tfidf_matrix[i:i+1], tfidf_matrix[j:j+1])[0][0]
                    similarities.append(sim)
            
            return statistics.mean(similarities) if similarities else 0.0
            
        except:
            return 0.0

    def _calculate_sentiment_transitions(self, text: str) -> List[float]:
        """Calcola le transizioni emotive tra frasi"""
        try:
            if not TextBlob:
                return []
            
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) < 2:
                return []
            
            transitions = []
            for i in range(1, len(sentences)):
                prev_sentiment = TextBlob(sentences[i-1]).sentiment.polarity
                curr_sentiment = TextBlob(sentences[i]).sentiment.polarity
                transition = abs(curr_sentiment - prev_sentiment)
                transitions.append(transition)
            
            return transitions
            
        except:
            return []

    def _categorize_words(self, words: List[str]) -> Dict[str, int]:
        """Categorizza le parole per tipo"""
        categories = {
            'nouns': 0,
            'verbs': 0, 
            'adjectives': 0,
            'adverbs': 0,
            'prepositions': 0,
            'determinants': 0,
            'other': 0
        }
        
        # Liste semplificate per categorizzazione
        prepositions = {'in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further'}
        determinants = {'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        for word in words:
            if word in prepositions:
                categories['prepositions'] += 1
            elif word in determinants:
                categories['determinants'] += 1
            else:
                # Semplificazione: categorizzazione basata su suffissi
                if word.endswith(('tion', 'sion', 'ness', 'ment', 'ity', 'ism', 'er', 'or')):
                    categories['nouns'] += 1
                elif word.endswith(('ing', 'ed', 'er')):
                    categories['verbs'] += 1
                elif word.endswith(('ly')):
                    categories['adverbs'] += 1
                elif word.endswith(('ous', 'ful', 'less', 'able', 'ible', 'al', 'ic', 'ive')):
                    categories['adjectives'] += 1
                else:
                    categories['other'] += 1
        
        return categories

    def _detect_unusual_patterns(self, text: str) -> Dict[str, Any]:
        """Rileva pattern linguistici insoliti"""
        try:
            patterns = {}
            
            # Parolacce o linguaggio informale (semplificato)
            informal_indicators = re.findall(r'\b(gonna|wanna|gotta|kinda|sorta|ain\'t|y\'all|yo|bro|dude)\b', text.lower())
            patterns['indicatori_informali'] = len(informal_indicators)
            
            # Eccesso di punteggiatura
            excess_punctuation = re.findall(r'[!?]{2,}', text)
            patterns['punteggiatura_eccessiva'] = len(excess_punctuation)
            
            # Parentesi frequenti
            parentheses = len(re.findall(r'[\(\)]', text))
            patterns['uso_parentesi'] = parentheses
            
            # Maiuscolo eccessivo
            caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
            patterns['maiuscolo_eccessivo'] = len(caps_words)
            
            return patterns
            
        except:
            return {}

    def _detect_repetitive_structures(self, text: str) -> Dict[str, Any]:
        """Rileva strutture ripetitive"""
        try:
            structures = {}
            
            # Ripetizione di parole consecutive
            words = re.findall(r'\b\w+\b', text.lower())
            word_repetitions = []
            for i in range(len(words) - 1):
                if words[i] == words[i+1]:
                    word_repetitions.append(words[i])
            
            structures['ripetizioni_consecutive'] = len(word_repetitions)
            
            # Inizio di frasi simili
            sentences = re.split(r'[.!?]+', text)
            sentence_starts = [re.findall(r'\b\w+\b', s.lower())[0] if re.findall(r'\b\w+\b', s.lower()) else '' for s in sentences if s.strip()]
            start_counts = Counter(sentence_starts)
            repeated_starts = sum(1 for count in start_counts.values() if count > 1)
            
            structures['inizi_frasi_simil'] = repeated_starts
            
            return structures
            
        except:
            return {}

    def _calculate_ai_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcola un punteggio di probabilità AI vs umano"""
        try:
            score = 0
            confidence = 0
            
            # Metriche lessicali per AI detection
            lexical = results.get('metriche_lessicali', {})
            
            # TTR molto alto o molto basso può indicare AI
            ttr = lexical.get('ttr_base', 0.5)
            if ttr > 0.8 or ttr < 0.3:
                score += 0.2
                confidence += 0.1
            
            # Burstiness molto basso può indicare pattern AI
            burstiness = lexical.get('burstiness', 0)
            if burstiness < 0.1:
                score += 0.3
                confidence += 0.2
            
            # Densità lessicale molto alta può indicare AI
            density = lexical.get('densita_lessicale', 0.5)
            if density > 0.8:
                score += 0.2
                confidence += 0.1
            
            # Metriche sintattiche
            syntactic = results.get('metriche_sintattiche', {})
            
            # Variabilità lunghezza frasi molto bassa indica AI
            variability = syntactic.get('variabilita_lunghezza', 0.5)
            if variability < 0.2:
                score += 0.3
                confidence += 0.2
            
            # Pattern ripetitivi molto bassi indicano AI
            patterns = syntactic.get('pattern_ripetitivi', 0.1)
            if patterns < 0.001:
                score += 0.2
                confidence += 0.1
            
            # Normalizza il punteggio
            ai_probability = min(score, 1.0)
            human_probability = 1.0 - ai_probability
            
            # Classificazione
            if ai_probability > 0.7:
                classification = "Probabilmente AI"
            elif ai_probability > 0.4:
                classification = "Indeterminato"
            else:
                classification = "Probabilmente Umano"
            
            return {
                'ai_probability': round(ai_probability, 3),
                'human_probability': round(human_probability, 3),
                'confidence': round(min(confidence, 1.0), 3),
                'classification': classification
            }
            
        except Exception as e:
            return {'error': str(e)}

    def export_results(self, results: Dict[str, Any], filename: str = "analysis_results.json"):
        """Esporta i risultati in formato JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Risultati salvati in: {filename}")
        except Exception as e:
            print(f"❌ Errore salvataggio: {e}")

# USAGE EXAMPLE
if __name__ == "__main__":
    # Test del sistema
    analyzer = AdvancedTextAnalyzer()
    
    # Esempio di testo umano vs AI
    human_text = """
    I walked through the old forest yesterday. The trees were tall and ancient, 
    their branches reaching toward the cloudy sky like gnarled fingers. 
    I felt a sense of peace among the natural beauty, though I couldn't shake 
    the feeling that something was watching me from the shadows.
    """
    
    ai_text = """
    The implementation of advanced natural language processing systems has revolutionized 
    the field of computational linguistics. These sophisticated algorithms demonstrate 
    remarkable capabilities in understanding and generating human-like text. Furthermore, 
    the continuous improvement of machine learning models enables increasingly accurate 
    analysis of linguistic patterns and semantic structures.
    """
    
    print("=== ANALISI TESTO UMANO ===")
    human_results = analyzer.analyze_text(human_text)
    print(json.dumps(human_results, indent=2))
    
    print("\n=== ANALISI TESTO AI ===")
    ai_results = analyzer.analyze_text(ai_text)
    print(json.dumps(ai_results, indent=2))
