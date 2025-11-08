# -*- coding: utf-8 -*-
"""
Text Processor - Preprocessing avanzato per analisi testuale
Modulo per la pulizia e preparazione del testo
"""

import re
import string
import unicodedata
from typing import List, Dict, Any


class TextProcessor:
    """Processore di testo per analisi avanzate"""
    
    def __init__(self):
        # Pattern per la pulizia del testo
        self.cleaning_patterns = {
            'multiple_spaces': re.compile(r'\s+'),
            'multiple_newlines': re.compile(r'\n\s*\n'),
            'special_chars': re.compile(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\']'),
            'urls': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'emails': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        }
        
        # Stop words comuni in italiano
        self.stop_words = {
            'il', 'la', 'le', 'i', 'lo', 'gli', 'un', 'una', 'di', 'da', 'in', 'con', 
            'su', 'per', 'tra', 'fra', 'a', 'e', 'o', 'ma', 'se', 'che', 'chi', 'cui', 
            'come', 'dove', 'quando', 'perché', 'quindi', 'però', 'anzi', 'bensì',
            'del', 'della', 'dello', 'dei', 'delle', 'al', 'allo', 'alla', 'ai', 'alle',
            'nel', 'nello', 'nella', 'nei', 'nelle', 'sul', 'sullo', 'sulla', 'sui', 'sulle',
            'questo', 'questa', 'questi', 'quelle', 'quel', 'quello', 'quelli', 'quelle',
            'che', 'chi', 'cui', 'quale', 'quali', 'quanto', 'quanta', 'quanti', 'quante'
        }

    def normalize_text(self, text: str) -> str:
        """Normalizza il testo rimuovendo caratteri speciali e normalizzando unicode"""
        if not text:
            return ""
        
        # Normalizza unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Rimuovi URLs e email
        text = self.cleaning_patterns['urls'].sub(' ', text)
        text = self.cleaning_patterns['emails'].sub(' ', text)
        
        # Rimuovi caratteri speciali ma mantieni punteggiatura base
        text = self.cleaning_patterns['special_chars'].sub(' ', text)
        
        # Normalizza spazi
        text = self.cleaning_patterns['multiple_spaces'].sub(' ', text)
        text = self.cleaning_patterns['multiple_newlines'].sub('\n', text)
        
        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        """Tokenizza il testo in parole"""
        text = self.normalize_text(text.lower())
        
        # Rimuovi punteggiatura per tokenizzazione
        translator = str.maketrans('', '', string.punctuation)
        words = text.translate(translator).split()
        
        # Filtra parole troppo corte e stop words
        return [word for word in words if len(word) > 2 and word not in self.stop_words]

    def split_sentences(self, text: str) -> List[str]:
        """Divide il testo in frasi"""
        text = self.normalize_text(text)
        
        # Pattern per dividere in frasi (migliorato)
        sentence_endings = r'[.!?]+\s+'
        sentences = re.split(sentence_endings, text)
        
        # Pulisci le frasi
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 5:  # Solo frasi con più di 5 caratteri
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences

    def extract_paragraphs(self, text: str) -> List[str]:
        """Estrae paragrafi dal testo"""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]

    def get_text_stats(self, text: str) -> Dict[str, Any]:
        """Calcola statistiche base del testo"""
        sentences = self.split_sentences(text)
        words = self.tokenize(text)
        paragraphs = self.extract_paragraphs(text)
        
        return {
            'char_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            'unique_words': len(set(words)),
            'lexical_diversity': len(set(words)) / len(words) if words else 0
        }
