#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Validator per TextAnalyzer
Sistema di validazione robusto per gli input testuali
Include: sanitizzazione, rilevamento anomalie, controlli di qualità
"""

import re
import sys
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import warnings

class InputValidator:
    """
    Validatore di input con controlli multi-livello
    Garantisce qualità e consistenza dei testi in ingresso
    """

    # Pattern sospetti che indicano possibile contenuto non valido
    SUSPICIOUS_PATTERNS = {
        'lorem_ipsum': r'\b(lorem ipsum|amet, consectetur|adipiscing elit)\b',
        'template_text': r'\b(TODO|FIXME|placeholder|sample text|copy and paste)\b',
        'nonsense': r'^([a-z]{1,2}\s*){30,}$',  # Sequenze casuali di caratteri
        'binary_data': r'[\x00-\x08\x0E-\x1F]',  # Caratteri di controllo
        'excessive_caps': r'[A-Z]{20,}',  # Troppi caratteri maiuscoli consecutivi
        'excessive_punct': r'[.!?]{5,}',  # Troppi segni di punteggiatura
    }

    # Range accettabili per metriche
    VALIDATION_RANGES = {
        'min_length': 10,      # Minimo 10 parole
        'max_length': 5000,    # Massimo 5000 parole
        'max_char_length': 50000,  # Massimo 50000 caratteri
        'min_sentences': 1,    # Minimo 1 frase
        'max_sentences': 200,  # Massimo 200 frasi
    }

    def __init__(self):
        self.validation_log = []

    def validate_text(self, text: str, strict_mode: bool = False) -> Dict[str, Any]:
        """
        Valida un testo con controlli multi-livello

        Args:
            text: Testo da validare
            strict_mode: Se True, applica controlli più severi

        Returns:
            Dict con risultati validazione
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'quality_score': 0.0,
            'sanitized_text': None,
            'stats': {},
            'timestamp': datetime.now().isoformat()
        }

        try:
            # 1. Validazione base
            base_validation = self._validate_base(text)
            result['errors'].extend(base_validation['errors'])
            result['warnings'].extend(base_validation['warnings'])

            # 2. Controlli di sicurezza
            security_check = self._validate_security(text)
            result['errors'].extend(security_check['errors'])

            # 3. Rilevamento pattern sospetti
            suspicion_check = self._validate_suspicious_patterns(text, strict_mode)
            result['warnings'].extend(suspicion_check['warnings'])

            # 4. Analisi qualità del testo
            quality_check = self._analyze_quality(text)
            result['quality_score'] = quality_check['score']
            result['stats'] = quality_check['stats']
            result['warnings'].extend(quality_check['warnings'])

            # 5. Sanitizzazione
            result['sanitized_text'] = self._sanitize_text(text)

            # 6. Verifica finale
            result['valid'] = len(result['errors']) == 0

            # Log
            self.validation_log.append({
                'timestamp': result['timestamp'],
                'valid': result['valid'],
                'errors_count': len(result['errors']),
                'warnings_count': len(result['warnings']),
                'quality_score': result['quality_score']
            })

        except Exception as e:
            result['errors'].append(f"Validation failed: {str(e)}")
            result['valid'] = False

        return result

    def _validate_base(self, text: str) -> Dict[str, List[str]]:
        """Validazione base: tipo, lunghezza, encoding"""
        errors = []
        warnings = []

        # Controllo tipo
        if not isinstance(text, str):
            errors.append("Input must be a string")
            return {'errors': errors, 'warnings': warnings}

        # Controllo encoding
        try:
            text.encode('utf-8').decode('utf-8')
        except UnicodeError:
            errors.append("Invalid UTF-8 encoding")

        # Controllo lunghezza caratteri
        char_length = len(text)
        if char_length == 0:
            errors.append("Empty text")
        elif char_length > self.VALIDATION_RANGES['max_char_length']:
            errors.append(f"Text too long: {char_length} chars (max: {self.VALIDATION_RANGES['max_char_length']})")

        # Controllo numero parole
        words = text.split()
        word_count = len(words)
        if word_count < self.VALIDATION_RANGES['min_length']:
            warnings.append(f"Very short text: {word_count} words (min recommended: {self.VALIDATION_RANGES['min_length']})")
        elif word_count > self.VALIDATION_RANGES['max_length']:
            errors.append(f"Text too long: {word_count} words (max: {self.VALIDATION_RANGES['max_length']})")

        # Controllo numero frasi
        sentences = re.findall(r'[.!?]+', text)
        sentence_count = len(sentences)
        if sentence_count < self.VALIDATION_RANGES['min_sentences']:
            warnings.append(f"No clear sentence structure detected")

        return {'errors': errors, 'warnings': warnings}

    def _validate_security(self, text: str) -> Dict[str, List[str]]:
        """Controlli di sicurezza: injection, script, ecc."""
        errors = []

        # Rileva caratteri di controllo (possibile injection)
        if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', text):
            errors.append("Contains control characters (potential security risk)")

        # Rileva pattern SQL injection comuni
        sql_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)',
            r'(\b(UNION|OR|AND)\s+\d+\s*=\s*\d+)',
            r"('|(\\x27|'))",
        ]
        for pattern in sql_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append("Contains suspicious SQL-like patterns")

        # Rileva pattern XSS comuni
        xss_patterns = [
            r'<script',
            r'javascript:',
            r'on\w+\s*=',
        ]
        for pattern in xss_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append("Contains potential XSS patterns")

        return {'errors': errors}

    def _validate_suspicious_patterns(self, text: str, strict: bool) -> Dict[str, List[str]]:
        """Rileva pattern sospetti o non naturali"""
        warnings = []

        for pattern_name, pattern in self.SUSPICIOUS_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                severity = 'High' if strict else 'Medium'
                warnings.append(f"Suspicious pattern '{pattern_name}' detected (severity: {severity})")

        # Controllo ripetitività eccessiva
        words = text.lower().split()
        unique_words = set(words)
        if len(words) > 10:  # Solo per testi sufficientemente lunghi
            repetition_ratio = (len(words) - len(unique_words)) / len(words)
            if repetition_ratio > 0.5:  # Più del 50% parole ripetute
                warnings.append(f"High word repetition: {repetition_ratio:.2%}")

        return {'warnings': warnings}

    def _analyze_quality(self, text: str) -> Dict[str, Any]:
        """Analizza qualità generale del testo"""
        warnings = []

        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Statistiche base
        word_count = len(words)
        sentence_count = len(sentences)
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

        # Calcola quality score (0-1)
        score = 1.0

        # Penalità per lunghezza inappropriata
        if word_count < 20:
            score -= 0.3
        elif word_count > 1000:
            score -= 0.2

        # Penalità per frasi troppo lunghe o corte
        if avg_words_per_sentence > 40:
            score -= 0.2
            warnings.append("Very long sentences detected")
        elif avg_words_per_sentence < 5:
            score -= 0.1
            warnings.append("Very short sentences detected")

        # Bonus per diversità lessicale
        unique_words = set(w.lower() for w in words)
        lexical_diversity = len(unique_words) / word_count if word_count > 0 else 0
        if lexical_diversity > 0.7:
            score += 0.1
        elif lexical_diversity < 0.3:
            score -= 0.2
            warnings.append("Low lexical diversity")

        # Normalizza score
        score = max(0.0, min(1.0, score))

        stats = {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'lexical_diversity': round(lexical_diversity, 3),
            'unique_word_count': len(unique_words)
        }

        return {
            'score': score,
            'warnings': warnings,
            'stats': stats
        }

    def _sanitize_text(self, text: str) -> str:
        """Sanitizza il testo rimuovendo caratteri problematici"""
        # Rimuovi caratteri di controllo (eccetto newline e tab)
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

        # Normalizza whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)

        # Rimuovi spazi iniziali/finali
        sanitized = sanitized.strip()

        return sanitized

    def batch_validate(self, texts: List[str], strict_mode: bool = False) -> List[Dict[str, Any]]:
        """Valida un batch di testi"""
        results = []
        for i, text in enumerate(texts):
            result = self.validate_text(text, strict_mode)
            result['batch_index'] = i
            results.append(result)
        return results

    def get_validation_summary(self) -> Dict[str, Any]:
        """Riepilogo delle validazioni effettuate"""
        if not self.validation_log:
            return {'message': 'No validations performed yet'}

        total = len(self.validation_log)
        valid_count = sum(1 for log in self.validation_log if log['valid'])
        invalid_count = total - valid_count

        avg_quality = sum(log['quality_score'] for log in self.validation_log) / total

        return {
            'total_validations': total,
            'valid_count': valid_count,
            'invalid_count': invalid_count,
            'validation_rate': valid_count / total,
            'average_quality_score': round(avg_quality, 3),
            'recent_logs': self.validation_log[-5:]  # Ultimi 5
        }


# Test
if __name__ == "__main__":
    validator = InputValidator()

    # Test con testo valido
    valid_text = "This is a well-structured sentence with proper punctuation. It contains multiple words and demonstrates normal human writing patterns."
    result = validator.validate_text(valid_text)
    print("Valid text test:")
    print(f"  Valid: {result['valid']}")
    print(f"  Quality score: {result['quality_score']}")
    print(f"  Errors: {result['errors']}")
    print(f"  Warnings: {result['warnings']}")

    # Test con testo sospetto
    suspicious_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet."
    result = validator.validate_text(suspicious_text, strict_mode=True)
    print("\nSuspicious text test:")
    print(f"  Valid: {result['valid']}")
    print(f"  Warnings: {result['warnings']}")

    # Summary
    print("\nValidation Summary:")
    print(validator.get_validation_summary())
