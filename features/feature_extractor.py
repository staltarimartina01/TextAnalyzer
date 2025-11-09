# -*- coding: utf-8 -*-
"""
Feature Extractor - Estrazione features avanzate per classificazione AI vs Umano
Modulo per l'estrazione di caratteristiche linguistiche e stilistiche
"""

import re
import math
import string
from collections import Counter
from typing import Dict, List, Any, Tuple
from datetime import datetime

from core.text_processor import TextProcessor


class FeatureExtractor:
    """Estrae features avanzate per la classificazione di testi AI vs umani"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        
        # Pattern per analisi avanzate
        self.patterns = {
            'repeated_punctuation': re.compile(r'([!?.]){2,}'),
            'capital_words': re.compile(r'\b[A-Z]{3,}\b'),
            'numbers': re.compile(r'\b\d+[\.,]?\d*\b'),
            'foreign_words': re.compile(r'\b[a-zA-ZÀ-ÿ]+(?:\s+[a-zA-ZÀ-ÿ]+)*\b'),
            'complex_sentences': re.compile(r'\b(?:poiché|pertanto|quindi|tuttavia|conseguentemente|perciò)\b'),
            'questions': re.compile(r'\?+'),
            'exclamations': re.compile(r'!+')
        }
        
        # Parole chiave per analisi semantica
        self.academic_indicators = {
            'conclusioni': ['concludendo', 'in conclusione', 'pertanto', 'quindi', 'dunque'],
            'analisi': ['analizzando', 'esaminando', 'valutando', 'considerando', 'studiando'],
            'confronto': ['invece', 'tuttavia', 'confronto', 'diversamente', 'al contrario'],
            'esempi': ['ad esempio', 'ad esempio', 'per esempio', 'come', 'tipo', 'qualche'],
            'certezza': ['sicuramente', 'ovviamente', 'chiaramente', 'indubbiamente', 'certamente'],
            'incertezza': ['probabilmente', 'forse', 'possibilmente', 'presumibilmente', 'verosimilmente']
        }

    def extract_lexical_features(self, text: str) -> Dict[str, float]:
        """Estrae features lessicali avanzate"""
        words = self.text_processor.tokenize(text)
        total_words = len(words)
        
        if total_words == 0:
            return self._empty_lexical_features()
        
        # Calcolo word frequency
        word_freq = Counter(words)
        most_common = word_freq.most_common(10)
        
        # Calcolo metriche lessicali
        lexical_features = {
            'avg_word_length': sum(len(w) for w in words) / total_words,
            'lexical_diversity': len(set(words)) / total_words,
            'hapax_legomena_ratio': sum(1 for count in word_freq.values() if count == 1) / total_words,
            'type_token_ratio': len(set(words)) / total_words,
            'most_common_word_ratio': most_common[0][1] / total_words if most_common else 0,
            'top5_words_ratio': sum(count for _, count in most_common[:5]) / total_words,
            'long_words_ratio': sum(1 for w in words if len(w) > 6) / total_words,
            'very_long_words_ratio': sum(1 for w in words if len(w) > 10) / total_words,
            'short_words_ratio': sum(1 for w in words if len(w) < 4) / total_words,
        }
        
        # Calcolo entropia del testo
        entropy = -sum((count/total_words) * math.log2(count/total_words) 
                      for count in word_freq.values())
        lexical_features['text_entropy'] = entropy / math.log2(len(word_freq)) if len(word_freq) > 1 else 0
        
        return lexical_features

    def extract_syntactic_features(self, text: str) -> Dict[str, float]:
        """Estrae features sintattiche (simulate senza spaCy)"""
        sentences = self.text_processor.split_sentences(text)
        total_sentences = len(sentences)
        total_words = len(self.text_processor.tokenize(text))
        
        if total_sentences == 0 or total_words == 0:
            return self._empty_syntactic_features()
        
        # Analisi punteggiatura
        punct_chars = sum(1 for c in text if c in string.punctuation)
        
        # Pattern complessi
        complex_sentences = sum(1 for sentence in sentences 
                              if len(re.findall(r'\b(?:poiché|pertanto|quindi|tuttavia|conseguentemente|perciò)\b', sentence)) > 0)
        
        # Analisi lunghezza frasi
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        
        # Analisi subordinazione (simulata)
        subordinate_indicators = sum(1 for word in self.text_processor.tokenize(text) 
                                   if word in ['che', 'qualora', 'benché', 'sebbene', 'purché'])
        
        syntactic_features = {
            'avg_sentence_length': sum(sentence_lengths) / len(sentence_lengths),
            'sentence_length_variance': self._variance(sentence_lengths),
            'punctuation_density': punct_chars / len(text),
            'complex_sentences_ratio': complex_sentences / total_sentences,
            'subordination_ratio': subordinate_indicators / total_words,
            'question_ratio': len(self.patterns['questions'].findall(text)) / total_sentences if total_sentences > 0 else 0,
            'exclamation_ratio': len(self.patterns['exclamations'].findall(text)) / total_sentences if total_sentences > 0 else 0,
            'paragraph_count': len(self.text_processor.extract_paragraphs(text)),
            'avg_words_per_paragraph': total_words / len(self.text_processor.extract_paragraphs(text)) if self.text_processor.extract_paragraphs(text) else 0
        }
        
        return syntactic_features

    def extract_style_features(self, text: str) -> Dict[str, float]:
        """Estrae features stilistiche"""
        words = self.text_processor.tokenize(text)
        sentences = self.text_processor.split_sentences(text)
        
        if not words or not sentences:
            return self._empty_style_features()
        
        # Analisi maiuscole/minuscole
        uppercase_chars = sum(1 for c in text if c.isupper())
        total_chars = len(text)
        
        # Pattern ripetitivi
        repeated_punct = len(self.patterns['repeated_punctuation'].findall(text))
        
        # Analisi numeri
        numbers = self.patterns['numbers'].findall(text)
        foreign_words = self.patterns['foreign_words'].findall(text)
        
        # Analisi variabilità sintattica
        sentence_variety = self._calculate_sentence_variety(sentences)
        
        style_features = {
            'uppercase_ratio': uppercase_chars / total_chars if total_chars > 0 else 0,
            'repeated_punctuation_ratio': repeated_punct / len(sentences) if sentences else 0,
            'numbers_ratio': len(numbers) / len(words) if words else 0,
            'foreign_words_ratio': len(foreign_words) / len(words) if words else 0,
            'sentence_variety_index': sentence_variety,
            'contractions_ratio': self._count_contractions(text) / len(words) if words else 0,
            'word_repetition_ratio': self._calculate_word_repetition(words),
            'stylistic_consistency': self._calculate_stylistic_consistency(text)
        }
        
        return style_features

    def extract_semantic_features(self, text: str) -> Dict[str, float]:
        """Estrae features semantiche e di contenuto"""
        words = self.text_processor.tokenize(text)
        sentences = self.text_processor.split_sentences(text)
        
        if not words or not sentences:
            return self._empty_semantic_features()
        
        # Analisi indicatori accademici
        academic_presence = {}
        for category, indicators in self.academic_indicators.items():
            count = sum(1 for word in words if any(ind in word for ind in indicators))
            academic_presence[f'{category}_ratio'] = count / len(words)
        
        # Analisi coerenza semantica (semplificata)
        coherence_indicators = {
            'repeated_concepts_ratio': self._calculate_concept_repetition(words),
            'topic_consistency': self._calculate_topic_consistency(words),
            'argumentation_indicators': self._count_argumentation_markers(sentences)
        }
        
        semantic_features = {**academic_presence, **coherence_indicators}
        return semantic_features

    def extract_all_features(self, text: str) -> Dict[str, Any]:
        """Estrae tutte le features e le organizza"""
        timestamp = datetime.now().isoformat()
        
        features = {
            'metadata': {
                'timestamp': timestamp,
                'text_length': len(text),
                'processing_time': datetime.now().timestamp()
            },
            'lexical': self.extract_lexical_features(text),
            'syntactic': self.extract_syntactic_features(text),
            'style': self.extract_style_features(text),
            'semantic': self.extract_semantic_features(text),
            'sentiment': self.extract_sentiment_features(text),
            'readability': self.extract_readability_features(text)
        }
        
        # Combina tutte le features in un vettore unico
        all_features = {}
        for category, feature_dict in features.items():
            if isinstance(feature_dict, dict):
                for feature_name, value in feature_dict.items():
                    all_features[f"{category}_{feature_name}"] = value
            else:
                all_features[category] = feature_dict
        
        features['all_features'] = all_features
        return features

    # Metodi di utilità privati
    def _variance(self, values: List[float]) -> float:
        """Calcola la varianza di una lista di valori"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    def _calculate_sentence_variety(self, sentences: List[str]) -> float:
        """Calcola l'indice di varietà delle frasi"""
        if not sentences:
            return 0
        
        sentence_lengths = [len(s.split()) for s in sentences]
        return self._variance(sentence_lengths) / (sum(sentence_lengths) / len(sentences)) if sentence_lengths else 0

    def _count_contractions(self, text: str) -> int:
        """Conta le contrazioni nel testo"""
        contraction_patterns = [
            r"\b[d|l]'[aeiou]",  # dell', dell', d'
            r"\b[s]'[a-z]",      # s'
            r"\b[nm]?'[a-z]",    # m', n'
        ]
        
        count = 0
        for pattern in contraction_patterns:
            count += len(re.findall(pattern, text.lower()))
        
        return count

    def _calculate_word_repetition(self, words: List[str]) -> float:
        """Calcola il ratio di ripetizione delle parole"""
        if not words:
            return 0
        
        word_freq = Counter(words)
        repeated_words = sum(1 for count in word_freq.values() if count > 1)
        return repeated_words / len(word_freq)

    def _calculate_stylistic_consistency(self, text: str) -> float:
        """Calcola la consistenza stilistica (basata su pattern ricorrenti)"""
        sentences = self.text_processor.split_sentences(text)
        if len(sentences) < 2:
            return 1.0
        
        # Calcola similarità di pattern tra frasi
        sentence_patterns = []
        for sentence in sentences:
            pattern = re.sub(r'\w+', 'W', sentence)  # Sostituisci parole con 'W'
            pattern = re.sub(r'\d+', 'N', pattern)  # Sostituisci numeri con 'N'
            sentence_patterns.append(pattern)
        
        # Calcola pattern ricorrenti
        pattern_freq = Counter(sentence_patterns)
        recurring_patterns = sum(1 for count in pattern_freq.values() if count > 1)
        
        return recurring_patterns / len(sentence_patterns)

    def _calculate_concept_repetition(self, words: List[str]) -> float:
        """Calcola la ripetizione di concetti (semplificata)"""
        if not words:
            return 0
        
        # Raggruppa parole simili (stessa radice)
        word_stems = {}
        for word in words:
            stem = word[:4] if len(word) > 4 else word  # Radice semplificata
            if stem not in word_stems:
                word_stems[stem] = 0
            word_stems[stem] += 1
        
        concept_repetitions = sum(1 for count in word_stems.values() if count > 2)
        return concept_repetitions / len(word_stems)

    def _calculate_topic_consistency(self, words: List[str]) -> float:
        """Calcola la consistenza del topic (semplificata)"""
        if len(words) < 10:
            return 1.0
        
        # Dividi in parti e calcola diversità
        part_size = len(words) // 3
        parts = [words[i:i+part_size] for i in range(0, len(words), part_size)]
        
        consistency_scores = []
        for i, part1 in enumerate(parts):
            for j, part2 in enumerate(parts[i+1:], i+1):
                # Calcola overlap tra le parti
                overlap = len(set(part1) & set(part2))
                similarity = overlap / min(len(set(part1)), len(set(part2))) if min(len(set(part1)), len(set(part2))) > 0 else 0
                consistency_scores.append(similarity)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0

    def _count_argumentation_markers(self, sentences: List[str]) -> float:
        """Conta gli indicatori di argomentazione"""
        markers = ['perché', 'poiché', 'infatti', 'quindi', 'pertanto', 'conseguentemente', 
                  'tuttavia', 'invece', 'd\'altro canto', 'però', 'tuttavia']
        
        marker_count = 0
        total_sentences = len(sentences)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for marker in markers:
                if marker in sentence_lower:
                    marker_count += 1
                    break
        
        return marker_count / total_sentences if total_sentences > 0 else 0

    # Metodi per valori vuoti
    def _empty_lexical_features(self) -> Dict[str, float]:
        return {key: 0.0 for key in [
            'avg_word_length', 'lexical_diversity', 'hapax_legomena_ratio', 
            'type_token_ratio', 'most_common_word_ratio', 'top5_words_ratio',
            'long_words_ratio', 'very_long_words_ratio', 'short_words_ratio', 'text_entropy'
        ]}

    def _empty_syntactic_features(self) -> Dict[str, float]:
        return {key: 0.0 for key in [
            'avg_sentence_length', 'sentence_length_variance', 'punctuation_density',
            'complex_sentences_ratio', 'subordination_ratio', 'question_ratio',
            'exclamation_ratio', 'paragraph_count', 'avg_words_per_paragraph'
        ]}

    def _empty_style_features(self) -> Dict[str, float]:
        return {key: 0.0 for key in [
            'uppercase_ratio', 'repeated_punctuation_ratio', 'numbers_ratio',
            'foreign_words_ratio', 'sentence_variety_index', 'contractions_ratio',
            'word_repetition_ratio', 'stylistic_consistency'
        ]}

    def _empty_semantic_features(self) -> Dict[str, float]:
        semantic_keys = []
        for category in self.academic_indicators.keys():
            semantic_keys.append(f'{category}_ratio')
        semantic_keys.extend(['repeated_concepts_ratio', 'topic_consistency', 'argumentation_indicators'])
        
        return {key: 0.0 for key in semantic_keys}

    # =============================================================================
    # SENTIMENT ANALYSIS
    # =============================================================================
    
    def extract_sentiment_features(self, text: str) -> Dict[str, float]:
        """Estrae features per l'analisi del sentiment"""
        words = self.text_processor.tokenize(text)
        sentences = self.text_processor.split_sentences(text)
        
        if not words or not sentences:
            return self._empty_sentiment_features()
        
        # Dizionari per sentiment (parole positive, negative, neutro)
        positive_words = {
            'ottimo', 'eccellente', 'fantastico', 'meraviglioso', 'straordinario', 'formidabile',
            'positivo', 'bene', 'buono', 'grandioso', 'magnifico', 'splendido', 'brillante',
            'felice', 'contento', 'gioioso', 'allegro', 'entusiasta', 'motivato', 'ispirato',
            'amore', 'amicizia', 'affetto', 'caro', 'adorabile', 'delizioso', 'piacevole',
            'successo', 'vittoria', 'trionfo', 'eccellente', 'superbo', 'impressionante',
            'creatività', 'innovativo', 'geniale', 'intelligente', 'brillante', 'talento',
            'pace', 'tranquillità', 'serenità', 'armonia', 'benessere', 'salute', 'prosperità',
            'speranza', 'fiducia', 'ottimismo', 'entusiasmo', 'energia', 'vitalità',
            'qualità', 'perfezione', 'eleganza', 'bellezza', 'attrattiva', 'fascino'
        }
        
        negative_words = {
            'terribile', 'orribile', 'brutto', 'pessimo', 'orribile', 'deplorevole', 'disgusto',
            'negativo', 'cattivo', 'pessimo', 'orribile', 'disastroso', 'catastrofico', 'lamentabile',
            'triste', 'mesto', 'malinconico', 'depresso', 'avvilito', 'sconsolato', 'rammaricato',
            'odio', 'antipatia', 'avversione', 'sdegno', 'disprezzo', 'insofferenza', 'irritazione',
            'fallimento', 'sconfitta', 'sconfitta', 'insuccesso', 'frustrazione', 'delusione',
            'stupidità', 'ignoranza', 'incompetenza', 'incapacità', 'mancanza', 'deficienza',
            'conflitto', 'guerra', 'lotta', 'guerriglio', 'pericolo', 'minaccia', 'paura',
            'disperazione', 'disgrazia', 'miseria', 'dolore', 'sofferenza', 'angoscia', 'agonia',
            'corruzione', 'ingiustizia', 'inefficienza', 'burocrazia', 'inemprobabilità',
            'mediocrità', 'banalità', 'noia', 'monotonia', 'repetitività'
        }
        
        # Conteggio sentiment
        positive_count = sum(1 for word in words if word.lower() in positive_words)
        negative_count = sum(1 for word in words if word.lower() in negative_words)
        total_sentiment_words = len(words)
        
        # Calcolo sentiment score
        positive_ratio = positive_count / total_sentiment_words if total_sentiment_words > 0 else 0
        negative_ratio = negative_count / total_sentiment_words if total_sentiment_words > 0 else 0
        net_sentiment = positive_ratio - negative_ratio
        
        # Intensità emotiva (basata su punteggiatura e maiuscole)
        intensity_indicators = 0
        intensity_indicators += len(self.patterns['exclamations'].findall(text)) * 0.1
        intensity_indicators += len(self.patterns['questions'].findall(text)) * 0.05
        intensity_indicators += sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Emozioni specifiche
        emotion_indicators = {
            'joy_indicators': sum(1 for word in words if word.lower() in {'felice', 'contento', 'gioioso', 'allegro', 'lieto'}),
            'sadness_indicators': sum(1 for word in words if word.lower() in {'triste', 'mesto', 'addolorato', 'piangere', 'lacrime'}),
            'anger_indicators': sum(1 for word in words if word.lower() in {'arrabbiato', 'furioso', 'irritato', 'indignato', 'sdegno'}),
            'fear_indicators': sum(1 for word in words if word.lower() in {'paura', 'terrore', 'panico', 'spavento', 'inquietudine'}),
            'surprise_indicators': sum(1 for word in words if word.lower() in {'sorpresa', 'stupore', 'incredulo', 'meravigliato', 'sorpreso'})
        }
        
        # Sentiment analysis features
        sentiment_features = {
            'positive_sentiment_ratio': positive_ratio,
            'negative_sentiment_ratio': negative_ratio,
            'net_sentiment_score': net_sentiment,
            'sentiment_intensity': min(intensity_indicators, 1.0),  # Normalizzato
            'emotional_clarity': abs(net_sentiment),  # Chiarezza emotiva
            'sentiment_variance': self._calculate_sentiment_variance(text),
            'joy_indicators_ratio': emotion_indicators['joy_indicators'] / total_sentiment_words if total_sentiment_words > 0 else 0,
            'sadness_indicators_ratio': emotion_indicators['sadness_indicators'] / total_sentiment_words if total_sentiment_words > 0 else 0,
            'anger_indicators_ratio': emotion_indicators['anger_indicators'] / total_sentiment_words if total_sentiment_words > 0 else 0,
            'fear_indicators_ratio': emotion_indicators['fear_indicators'] / total_sentiment_words if total_sentiment_words > 0 else 0,
            'surprise_indicators_ratio': emotion_indicators['surprise_indicators'] / total_sentiment_words if total_sentiment_words > 0 else 0,
            'dominant_emotion': self._identify_dominant_emotion(emotion_indicators),
            'emotional_consistency': self._calculate_emotional_consistency(sentences)
        }
        
        return sentiment_features
    
    def _calculate_sentiment_variance(self, text: str) -> float:
        """Calcola la varianza del sentiment nel testo"""
        sentences = self.text_processor.split_sentences(text)
        if len(sentences) < 2:
            return 0.0
        
        sentence_sentiments = []
        for sentence in sentences:
            words = self.text_processor.tokenize(sentence)
            if words:
                # Calcola sentiment per ogni frase
                positive_words = {'bene', 'buono', 'ottimo', 'felice', 'positivo', 'bellissimo', 'fantastico'}
                negative_words = {'male', 'cattivo', 'terribile', 'triste', 'negativo', 'orribile', 'pessimo'}
                
                pos_count = sum(1 for word in words if word.lower() in positive_words)
                neg_count = sum(1 for word in words if word.lower() in negative_words)
                
                sentiment_score = (pos_count - neg_count) / len(words) if words else 0
                sentence_sentiments.append(sentiment_score)
        
        if not sentence_sentiments:
            return 0.0
        
        mean_sentiment = sum(sentence_sentiments) / len(sentence_sentiments)
        variance = sum((s - mean_sentiment) ** 2 for s in sentence_sentiments) / len(sentence_sentiments)
        return variance
    
    def _identify_dominant_emotion(self, emotion_indicators: Dict[str, int]) -> float:
        """Identifica l'emozione dominante (0=sadness, 0.5=neutral, 1=joy)"""
        max_emotion = max(emotion_indicators.values())
        if max_emotion == 0:
            return 0.5  # Neutro
        
        dominant_emotions = {
            'joy_indicators': 1.0,
            'surprise_indicators': 0.7,
            'anger_indicators': 0.2,
            'sadness_indicators': 0.0,
            'fear_indicators': 0.1
        }
        
        for emotion, value in emotion_indicators.items():
            if value == max_emotion:
                return dominant_emotions.get(emotion, 0.5)
        
        return 0.5
    
    def _calculate_emotional_consistency(self, sentences: List[str]) -> float:
        """Calcola la consistenza emotiva tra le frasi"""
        if len(sentences) < 2:
            return 1.0
        
        sentence_sentiments = []
        for sentence in sentences:
            words = self.text_processor.tokenize(sentence)
            if words:
                # Mappatura semplificata del sentiment
                positive_patterns = ['bene', 'buono', 'felice', 'ottimo', 'contento', 'positivo', 'bellissimo']
                negative_patterns = ['male', 'cattivo', 'triste', 'terribile', 'negativo', 'pessimo', 'orribile']
                
                pos_score = sum(1 for word in words if word.lower() in positive_patterns)
                neg_score = sum(1 for word in words if word.lower() in negative_patterns)
                
                if pos_score > neg_score:
                    sentence_sentiments.append(1.0)  # Positivo
                elif neg_score > pos_score:
                    sentence_sentiments.append(-1.0)  # Negativo
                else:
                    sentence_sentiments.append(0.0)  # Neutro
        
        if not sentence_sentiments:
            return 1.0
        
        # Calcola consistenza (quante frasi hanno lo stesso sentiment)
        consistency_scores = []
        for i in range(len(sentence_sentiments)):
            for j in range(i + 1, len(sentence_sentiments)):
                if sentence_sentiments[i] == sentence_sentiments[j]:
                    consistency_scores.append(1.0)
                else:
                    consistency_scores.append(0.0)
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0
    
    def _empty_sentiment_features(self) -> Dict[str, float]:
        return {key: 0.0 for key in [
            'positive_sentiment_ratio', 'negative_sentiment_ratio', 'net_sentiment_score',
            'sentiment_intensity', 'emotional_clarity', 'sentiment_variance',
            'joy_indicators_ratio', 'sadness_indicators_ratio', 'anger_indicators_ratio',
            'fear_indicators_ratio', 'surprise_indicators_ratio', 'dominant_emotion',
            'emotional_consistency'
        ]}

    # =============================================================================
    # READABILITY ANALYSIS
    # =============================================================================
    
    def extract_readability_features(self, text: str) -> Dict[str, float]:
        """Estrae features per l'indice di leggibilità"""
        words = self.text_processor.tokenize(text)
        sentences = self.text_processor.split_sentences(text)
        
        if not words or not sentences:
            return self._empty_readability_features()
        
        total_sentences = len(sentences)
        total_words = len(words)
        total_syllables = self._count_syllables_in_text(text)
        
        # Calcolo metriche base
        avg_sentence_length = total_words / total_sentences
        avg_syllables_per_word = total_syllables / total_words if total_words > 0 else 0
        
        # Indici di leggibilità
        readability_scores = {
            'flesch_reading_ease': self._calculate_flesch_reading_ease(avg_sentence_length, avg_syllables_per_word),
            'flesch_kincaid_grade': self._calculate_flesch_kincaid_grade(avg_sentence_length, avg_syllables_per_word),
            'gunning_fog_index': self._calculate_gunning_fog_index(text, avg_sentence_length),
            'automated_readability_index': self._calculate_automated_readability_index(text, words),
            'coleman_liau_index': self._calculate_coleman_liau_index(text),
            'smog_index': self._calculate_smog_index(text, total_sentences)
        }
        
        # Metriche di complessità linguistica
        complexity_features = {
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables_per_word': avg_syllables_per_word,
            'long_sentences_ratio': sum(1 for sentence in sentences if len(sentence.split()) > 20) / total_sentences,
            'very_long_sentences_ratio': sum(1 for sentence in sentences if len(sentence.split()) > 30) / total_sentences,
            'short_sentences_ratio': sum(1 for sentence in sentences if len(sentence.split()) < 8) / total_sentences,
            'complex_words_ratio': self._calculate_complex_words_ratio(words, total_syllables),
            'polysyllabic_words_ratio': self._calculate_polysyllabic_words_ratio(words),
            'technical_terms_ratio': self._calculate_technical_terms_ratio(words)
        }
        
        # Struttura del testo
        structural_features = {
            'paragraph_count': len(self.text_processor.extract_paragraphs(text)),
            'avg_sentence_length_variance': self._calculate_sentence_length_variance(sentences),
            'connectors_ratio': self._calculate_connectors_ratio(words),
            'subordination_ratio': self._calculate_subordination_ratio(text)
        }
        
        # Combina tutte le features
        readability_features = {**readability_scores, **complexity_features, **structural_features}
        return readability_features
    
    def _count_syllables_in_text(self, text: str) -> int:
        """Conta le sillabe totali nel testo"""
        words = self.text_processor.tokenize(text)
        return sum(self._count_syllables(word) for word in words)
    
    def _count_syllables(self, word: str) -> int:
        """Conta le sillabe in una parola (approssimazione)"""
        word = word.lower()
        vowels = 'aeiouyàèéìíòóùú'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Aggiusta per parole che finiscono con silenti
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)  # Almeno una sillaba per parola
    
    def _calculate_flesch_reading_ease(self, avg_sentence_length: float, avg_syllables_per_word: float) -> float:
        """Calcola l'indice di leggibilità Flesch Reading Ease"""
        if avg_sentence_length <= 0 or avg_syllables_per_word <= 0:
            return 0.0
        
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return max(0, min(100, score))  # Range 0-100
    
    def _calculate_flesch_kincaid_grade(self, avg_sentence_length: float, avg_syllables_per_word: float) -> float:
        """Calcola l'indice Flesch-Kincaid Grade Level"""
        if avg_sentence_length <= 0 or avg_syllables_per_word <= 0:
            return 0.0
        
        score = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        return max(0, score)
    
    def _calculate_gunning_fog_index(self, text: str, avg_sentence_length: float) -> float:
        """Calcola l'indice Gunning Fog"""
        words = self.text_processor.tokenize(text)
        if not words or avg_sentence_length <= 0:
            return 0.0
        
        complex_words = sum(1 for word in words if self._count_syllables(word) >= 3)
        complex_words_ratio = complex_words / len(words)
        
        score = 0.4 * (avg_sentence_length + (complex_words_ratio * 100))
        return max(0, score)
    
    def _calculate_automated_readability_index(self, text: str, words: List[str]) -> float:
        """Calcola l'Automated Readability Index"""
        if not words or len(text) == 0:
            return 0.0
        
        characters = sum(1 for char in text if char.isalnum())
        avg_characters_per_word = characters / len(words)
        
        sentences = self.text_processor.split_sentences(text)
        if not sentences:
            return 0.0
        
        score = (4.71 * avg_characters_per_word) + (0.5 * len(words) / len(sentences)) - 21.43
        return max(0, score)
    
    def _calculate_coleman_liau_index(self, text: str) -> float:
        """Calcola l'indice Coleman-Liau"""
        if not text:
            return 0.0
        
        letters = sum(1 for char in text if char.isalpha())
        words = self.text_processor.tokenize(text)
        sentences = self.text_processor.split_sentences(text)
        
        if not words or not sentences:
            return 0.0
        
        letters_per_100_words = (letters / len(words)) * 100
        sentences_per_100_words = (len(sentences) / len(words)) * 100
        
        score = (0.0588 * letters_per_100_words) - (0.296 * sentences_per_100_words) - 15.8
        return max(0, score)
    
    def _calculate_smog_index(self, text: str, total_sentences: int) -> float:
        """Calcola l'indice SMOG (Simple Measure of Gobbledygook)"""
        if total_sentences < 1:
            return 0.0
        
        words = self.text_processor.tokenize(text)
        polysyllabic_words = sum(1 for word in words if self._count_syllables(word) >= 3)
        
        if polysyllabic_words == 0:
            return 0.0
        
        score = 1.0430 * (polysyllabic_words * (30 / total_sentences)) + 3.1291
        return max(0, score)
    
    def _calculate_complex_words_ratio(self, words: List[str], total_syllables: int) -> float:
        """Calcola il rapporto di parole complesse (3+ sillabe)"""
        if not words:
            return 0.0
        
        complex_words = sum(1 for word in words if self._count_syllables(word) >= 3)
        return complex_words / len(words)
    
    def _calculate_polysyllabic_words_ratio(self, words: List[str]) -> float:
        """Calcola il rapporto di parole polisillabiche (4+ sillabe)"""
        if not words:
            return 0.0
        
        polysyllabic_words = sum(1 for word in words if self._count_syllables(word) >= 4)
        return polysyllabic_words / len(words)
    
    def _calculate_technical_terms_ratio(self, words: List[str]) -> float:
        """Calcola il rapporto di termini tecnici (parole lunghe e complesse)"""
        if not words:
            return 0.0
        
        technical_indicators = [
            # Suffissi tipici di termini tecnici
            'izzazione', 'ificazione', 'izzazione', 'ologia', 'grafia', 'metria', 'scopia',
            'sintesi', 'analisi', 'metodologia', 'filosofia', 'teoria', 'prassi', 'pratiche',
            'processo', 'procedimento', 'sistema', 'apparato', 'meccanismo', 'funzionamento',
            'struttura', 'organizzazione', 'architettura', 'configurazione', 'implementazione'
        ]
        
        technical_terms = sum(1 for word in words 
                            if len(word) > 8 and 
                            any(suffix in word.lower() for suffix in technical_indicators))
        
        return technical_terms / len(words)
    
    def _calculate_sentence_length_variance(self, sentences: List[str]) -> float:
        """Calcola la varianza della lunghezza delle frasi"""
        if len(sentences) < 2:
            return 0.0
        
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
        return variance
    
    def _calculate_connectors_ratio(self, words: List[str]) -> float:
        """Calcola il rapporto di connettivi logici"""
        connectors = {
            'invece', 'tuttavia', 'pertanto', 'conseguentemente', 'quindi', 'dunque', 'dato che',
            'poiché', 'perché', 'sebbene', 'benché', 'qualora', 'purché', 'mentre', 'durante',
            'pertanto', 'infatti', 'ovviamente', 'certamente', 'indubbiamente', 'presumibilmente',
            'd\'altro canto', 'altresì', 'peraltro', 'sicuramente', 'probabilmente', 'possibilmente'
        }
        
        if not words:
            return 0.0
        
        connector_count = sum(1 for word in words if word.lower() in connectors)
        return connector_count / len(words)
    
    def _calculate_subordination_ratio(self, text: str) -> float:
        """Calcola il rapporto di subordinazione (frasi complesse)"""
        sentences = self.text_processor.split_sentences(text)
        if not sentences:
            return 0.0
        
        subordinate_indicators = [
            'che', 'qualora', 'benché', 'sebbene', 'purché', 'affinché', 'perché', 'dato che',
            'poiché', 'mentre', 'quando', 'se', 'qualora', 'qualora', 'nonostante', 'malgrado'
        ]
        
        complex_sentences = 0
        for sentence in sentences:
            sentence_words = self.text_processor.tokenize(sentence)
            subordinate_count = sum(1 for word in sentence_words if word.lower() in subordinate_indicators)
            if subordinate_count > 0:
                complex_sentences += 1
        
        return complex_sentences / len(sentences)
    
    def _empty_readability_features(self) -> Dict[str, float]:
        return {key: 0.0 for key in [
            'flesch_reading_ease', 'flesch_kincaid_grade', 'gunning_fog_index',
            'automated_readability_index', 'coleman_liau_index', 'smog_index',
            'avg_sentence_length', 'avg_syllables_per_word', 'long_sentences_ratio',
            'very_long_sentences_ratio', 'short_sentences_ratio', 'complex_words_ratio',
            'polysyllabic_words_ratio', 'technical_terms_ratio', 'paragraph_count',
            'avg_sentence_length_variance', 'connectors_ratio', 'subordination_ratio'
        ]}
