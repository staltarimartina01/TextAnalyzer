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
            'semantic': self.extract_semantic_features(text)
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
