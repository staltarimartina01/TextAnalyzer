# -*- coding: utf-8 -*-
"""
Test Suite - Test automatizzati per AI vs Human Text Analyzer
Suite di test per verificare il corretto funzionamento del sistema
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.text_processor import TextProcessor
from features.feature_extractor import FeatureExtractor
from core.analyzer import TextAnalyzer
from utils.data_loader import DataLoader


class TestTextProcessor(unittest.TestCase):
    """Test per il TextProcessor"""
    
    def setUp(self):
        self.processor = TextProcessor()
    
    def test_normalize_text(self):
        """Test normalizzazione testo"""
        text = "  Questo    è un    test!  "
        normalized = self.processor.normalize_text(text)
        self.assertNotIn("  ", normalized)
        self.assertIn("test", normalized)
    
    def test_tokenize(self):
        """Test tokenizzazione"""
        text = "Ciao mondo! Come stai?"
        tokens = self.processor.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
    
    def test_split_sentences(self):
        """Test divisione frasi"""
        text = "Prima frase. Seconda frase! Terza frase?"
        sentences = self.processor.split_sentences(text)
        self.assertEqual(len(sentences), 3)
    
    def test_get_text_stats(self):
        """Test statistiche testo"""
        text = "Questo è un test di analisi del testo. Contiene diverse frasi."
        stats = self.processor.get_text_stats(text)
        
        self.assertIn('char_count', stats)
        self.assertIn('word_count', stats)
        self.assertIn('sentence_count', stats)
        self.assertGreater(stats['word_count'], 0)


class TestFeatureExtractor(unittest.TestCase):
    """Test per il FeatureExtractor"""
    
    def setUp(self):
        self.extractor = FeatureExtractor()
    
    def test_extract_lexical_features(self):
        """Test estrazione features lessicali"""
        text = "Questo è un testo di test con parole diverse e variegate. Contiene molte parole diverse."
        features = self.extractor.extract_lexical_features(text)
        
        self.assertIn('avg_word_length', features)
        self.assertIn('lexical_diversity', features)
        self.assertIn('type_token_ratio', features)
        self.assertGreaterEqual(features['lexical_diversity'], 0)
        self.assertLessEqual(features['lexical_diversity'], 1)
    
    def test_extract_syntactic_features(self):
        """Test estrazione features sintattiche"""
        text = "Questo è un test. Questo è un altro test. E questo è un terzo test molto più lungo e complesso."
        features = self.extractor.extract_syntactic_features(text)
        
        self.assertIn('avg_sentence_length', features)
        self.assertIn('punctuation_density', features)
        self.assertGreater(features['avg_sentence_length'], 0)
    
    def test_extract_style_features(self):
        """Test estrazione features stilistiche"""
        text = "Questo è un TESTO con MAIUSCOLE e 123 numeri! E anche... punteggiatura."
        features = self.extractor.extract_style_features(text)
        
        self.assertIn('uppercase_ratio', features)
        self.assertIn('numbers_ratio', features)
        self.assertGreaterEqual(features['uppercase_ratio'], 0)
    
    def test_extract_semantic_features(self):
        """Test estrazione features semantiche"""
        text = "Per esempio, poiché questo è un test, quindi possiamo concludere che funziona bene."
        features = self.extractor.extract_semantic_features(text)
        
        # Verifica che almeno alcune features semantiche siano presenti
        self.assertGreater(len(features), 0)
    
    def test_extract_all_features(self):
        """Test estrazione completa features"""
        text = "Questo è un test completo per verificare l'estrazione di tutte le features."
        all_features = self.extractor.extract_all_features(text)
        
        self.assertIn('metadata', all_features)
        self.assertIn('lexical', all_features)
        self.assertIn('syntactic', all_features)
        self.assertIn('style', all_features)
        self.assertIn('semantic', all_features)
        self.assertIn('all_features', all_features)


class TestDataLoader(unittest.TestCase):
    """Test per il DataLoader"""
    
    def setUp(self):
        self.loader = DataLoader()
        
        # Crea file temporanei per i test
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test.txt")
        
        with open(self.temp_file, 'w', encoding='utf-8') as f:
            f.write("Questo è un file di test per verificare il caricamento dei dati.")
    
    def tearDown(self):
        # Pulizia file temporanei
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_load_text_file(self):
        """Test caricamento file di testo"""
        content = self.loader.load_text_file(self.temp_file)
        self.assertIsInstance(content, str)
        self.assertIn("file di test", content)
    
    def test_load_files_from_directory(self):
        """Test caricamento file da directory"""
        files = self.loader.load_files_from_directory(self.temp_dir, "*.txt")
        self.assertIn(self.temp_file, files)
    
    def test_validate_file(self):
        """Test validazione file"""
        validation = self.loader.validate_file(self.temp_file)
        self.assertTrue(validation['valid'])
        self.assertIn('file_info', validation)


class TestAnalyzer(unittest.TestCase):
    """Test per l'Analyzer principale"""
    
    def setUp(self):
        self.analyzer = TextAnalyzer()
        
        # Crea file temporanei
        self.temp_dir = tempfile.mkdtemp()
        self.ai_file = os.path.join(self.temp_dir, "ai_test.txt")
        self.human_file = os.path.join(self.temp_dir, "human_test.txt")
        
        # Testo AI-like (strutturato, vario)
        ai_text = """L'intelligenza artificiale rappresenta una tecnologia rivoluzionaria. 
        Attraverso algoritmi complessi e apprendimento automatico, i sistemi AI elaborano 
        enormi quantità di dati identificando pattern nascosti. Questa capacità supera 
        significativamente le possibilità umane tradizionali in termini di velocità e precisione."""
        
        # Testo umano-like (più naturale, imperfetto)
        human_text = """Beh, non so se è proprio così. Ieri parlavo con mio fratello e 
        lui diceva che l'AI è utile ma che forse ci stiamo esagerando un po'. Boh, 
        secondo me è complicato da capire. Però, che ne so, magari ha ragione lui."""
        
        with open(self.ai_file, 'w', encoding='utf-8') as f:
            f.write(ai_text)
        
        with open(self.human_file, 'w', encoding='utf-8') as f:
            f.write(human_text)
    
    def tearDown(self):
        # Pulizia file temporanei
        for file_path in [self.ai_file, self.human_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_analyze_text(self):
        """Test analisi testo diretto"""
        text = "Questo è un test di analisi del testo generato da AI."
        result = self.analyzer.analyze_text(text, "test.txt")
        
        self.assertIn('final_assessment', result)
        self.assertIn('prediction', result['final_assessment'])
        self.assertIn('confidence', result['final_assessment'])
    
    def test_analyze_file(self):
        """Test analisi file"""
        result = self.analyzer.analyze_file(self.ai_file)
        
        self.assertNotIn('error', result)
        self.assertIn('final_assessment', result)
        self.assertIn('features', result)
    
    def test_batch_analyze(self):
        """Test analisi batch"""
        results = self.analyzer.batch_analyze(self.temp_dir, "*.txt")
        
        self.assertEqual(len(results), 2)
        
        for result in results:
            self.assertNotIn('error', result)
            self.assertIn('final_assessment', result)
    
    def test_confidence_calculation(self):
        """Test calcolo confidence"""
        text = "Questo è un test con parole diverse e variegate che dovrebbe avere alta diversità lessicale."
        result = self.analyzer.analyze_text(text)
        
        confidence = result.get('final_assessment', {}).get('confidence', 0)
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 1)


class TestIntegration(unittest.TestCase):
    """Test di integrazione del sistema completo"""
    
    def setUp(self):
        self.analyzer = TextAnalyzer()
        self.loader = DataLoader()
        
        # Crea directory di test
        self.test_dir = tempfile.mkdtemp()
        
        # Crea file di esempio
        self.loader.create_sample_data(self.test_dir, 6)
    
    def tearDown(self):
        # Rimuovi tutti i file creati
        for file_name in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file_name))
        os.rmdir(self.test_dir)
    
    def test_full_workflow(self):
        """Test del workflow completo"""
        # 1. Carica file
        files = self.loader.load_files_from_directory(self.test_dir, "*.txt")
        self.assertGreater(len(files), 0)
        
        # 2. Analizza ogni file
        results = []
        for file_path in files:
            result = self.analyzer.analyze_file(file_path)
            results.append(result)
            self.assertNotIn('error', result)
        
        # 3. Genera report
        report = self.analyzer.generate_report(results, None)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)
        
        # 4. Verifica che ci siano risultati coerenti
        for result in results:
            assessment = result.get('final_assessment', {})
            self.assertIn('prediction', assessment)
            self.assertIn(assessment['prediction'], ['AI', 'UMANO'])


def run_performance_test():
    """Esegue test di performance"""
    print("\n🧪 ESEGUENDO TEST DI PERFORMANCE...")
    
    analyzer = TextAnalyzer()
    
    # Test con testo di diverse dimensioni
    test_sizes = [100, 500, 1000, 2000]
    
    for size in test_sizes:
        # Crea testo di test
        text = "Questo è un test di performance. " * (size // 30)
        
        import time
        start_time = time.time()
        
        result = analyzer.analyze_text(text, f"perf_test_{size}.txt")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        confidence = result.get('final_assessment', {}).get('confidence', 0)
        
        print(f"  📊 {size} caratteri: {processing_time:.3f}s, confidence: {confidence:.1%}")


def run_sample_analysis():
    """Esegue analisi sui file di esempio esistenti"""
    print("\n🔍 ESEGUENDO ANALISI SUI FILE ESISTENTI...")
    
    analyzer = TextAnalyzer()
    
    # Controlla se esistono file di esempio
    test_dir = "/home/martina/TESI/TextAnalyzer/testi"
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith('.txt')]
        
        if files:
            print(f"📁 Trovati {len(files)} file di esempio")
            results = analyzer.batch_analyze(test_dir)
            
            # Mostra risultati
            for result in results:
                file_name = result.get('file_name', 'sconosciuto')
                assessment = result.get('final_assessment', {})
                prediction = assessment.get('prediction', 'Sconosciuto')
                confidence = assessment.get('confidence', 0)
                
                print(f"  📄 {file_name}: {prediction} ({confidence:.1%})")
        else:
            print("❌ Nessun file .txt trovato in testi/")
    else:
        print("❌ Directory testi/ non trovata")


def main():
    """Esegue tutti i test"""
    print("🤖 AI vs HUMAN TEXT ANALYZER - TEST SUITE")
    print("=" * 60)
    
    # Test unitari
    print("\n🧪 ESEGUENDO TEST UNITARI...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Test di performance
    try:
        run_performance_test()
    except Exception as e:
        print(f"⚠️ Test performance fallito: {e}")
    
    # Test su file esistenti
    try:
        run_sample_analysis()
    except Exception as e:
        print(f"⚠️ Analisi esempi fallita: {e}")
    
    print("\n✅ Test completati!")


if __name__ == "__main__":
    main()
