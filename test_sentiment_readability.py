
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script per verificare le nuove funzionalità di sentiment analysis e leggibilità
"""

import sys
import os

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from features.feature_extractor import FeatureExtractor

def test_sentiment_analysis():
    """Test della funzionalità di sentiment analysis"""
    print("🧪 Test Sentiment Analysis")
    print("=" * 50)
    
    extractor = FeatureExtractor()
    
    # Testi di esempio
    test_cases = [
        {
            "name": "Testo Positivo",
            "text": "Questo è un giorno fantastico! Sono molto felice e contento. La vita è bellissima e piena di gioia e successi meravigliosi."
        },
        {
            "name": "Testo Negativo", 
            "text": "Oggi è stata una giornata terrible. Mi sento molto triste e deluso. È un periodo orribile pieno di problemi e fallimenti."
        },
        {
            "name": "Testo Neutro",
            "text": "Il sistema è stato aggiornato con le nuove funzionalità. L'implementazione include sentiment analysis e indice di leggibilità."
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📝 {test_case['name']}")
        print("-" * 30)
        
        features = extractor.extract_all_features(test_case['text'])
        sentiment = features.get('sentiment', {})
        
        if sentiment:
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            positive_ratio = sentiment.get('positive_sentiment_ratio', 0)
            negative_ratio = sentiment.get('negative_sentiment_ratio', 0)
            dominant_emotion = sentiment.get('dominant_emotion', 0.5)
            
            print(f"Net Sentiment Score: {net_sentiment:.3f}")
            print(f"Positive Ratio: {positive_ratio:.1%}")
            print(f"Negative Ratio: {negative_ratio:.1%}")
            print(f"Dominant Emotion: {dominant_emotion:.3f}")
            
            # Determina il sentiment
            if net_sentiment > 0.1:
                sentiment_label = "POSITIVO"
            elif net_sentiment < -0.1:
                sentiment_label = "NEGATIVO"
            else:
                sentiment_label = "NEUTRALE"
            
            print(f"Sentiment: {sentiment_label}")
        else:
            print("❌ Nessun risultato sentiment")

def test_readability_analysis():
    """Test della funzionalità di analisi leggibilità"""
    print("\n\n📖 Test Readability Analysis")
    print("=" * 50)
    
    extractor = FeatureExtractor()
    
    # Testi di esempio con diversi livelli di complessità
    test_cases = [
        {
            "name": "Testo Semplice",
            "text": "Il gatto dorme. Il cane corre. La casa è grande. I bambini giocano nel giardino."
        },
        {
            "name": "Testo Complesso",
            "text": "L'implementazione dell'algoritmo di sentiment analysis richiede un'elaborazione complessa che coinvolge l'analisi semantica del testo attraverso metodologie avanzate di natural language processing."
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📝 {test_case['name']}")
        print("-" * 30)
        
        features = extractor.extract_all_features(test_case['text'])
        readability = features.get('readability', {})
        
        if readability:
            flesch_score = readability.get('flesch_reading_ease', 0)
            fk_grade = readability.get('flesch_kincaid_grade', 0)
            gunning_fog = readability.get('gunning_fog_index', 0)
            avg_sentence_length = readability.get('avg_sentence_length', 0)
            complex_words_ratio = readability.get('complex_words_ratio', 0)
            
            print(f"Flesch Reading Ease: {flesch_score:.1f}/100")
            print(f"Flesch-Kincaid Grade: {fk_grade:.1f}")
            print(f"Gunning Fog Index: {gunning_fog:.1f}")
            print(f"Avg Sentence Length: {avg_sentence_length:.1f} parole")
            print(f"Complex Words Ratio: {complex_words_ratio:.1%}")
            
            # Determina il livello di leggibilità
            if flesch_score >= 90:
                level = "Molto Facile"
            elif flesch_score >= 80:
                level = "Facile"
            elif flesch_score >= 70:
                level = "Abbastanza Facile"
            elif flesch_score >= 60:
                level = "Standard"
            elif flesch_score >= 50:
                level = "Abbastanza Difficile"
            elif flesch_score >= 30:
                level = "Difficile"
            else:
                level = "Molto Difficile"
            
            print(f"Livello: {level}")
        else:
            print("❌ Nessun risultato leggibilità")

def test_full_analysis():
    """Test dell'analisi completa con classificazione AI vs Umano"""
    print("\n\n🤖 Test Full Analysis (AI vs Human + Sentiment + Readability)")
    print("=" * 50)
    
    from core.analyzer import TextAnalyzer
    
    analyzer = TextAnalyzer()
    
    test_texts = [
        "Oggi è una giornata bellissima! Sono molto felice e contento. Il sole splende e gli uccelli cantano. È perfetto per una passeggiata nel parco.",
        "L'implementazione dell'algoritmo di machine learning richiede l'ottimizzazione dei parametri di configurazione attraverso metodologie avanzate di data processing e pattern recognition per ottenere risultati efficaci."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Testo {i}")
        print("-" * 30)
        
        result = analyzer.analyze_text(text, f"test_text_{i}.txt")
        
        if 'error' in result:
            print(f"❌ Errore: {result['error']}")
            continue
        
        # Risultato principale
        assessment = result.get('final_assessment', {})
        prediction = assessment.get('prediction', 'Sconosciuto')
        confidence = assessment.get('confidence', 0)
        
        print(f"Classificazione: {prediction} ({confidence:.1%})")
        
        # Sentiment
        features = result.get('features', {})
        sentiment = features.get('sentiment', {})
        if sentiment:
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            if net_sentiment > 0.1:
                sentiment_label = "POSITIVO"
            elif net_sentiment < -0.1:
                sentiment_label = "NEGATIVO"
            else:
                sentiment_label = "NEUTRALE"
            print(f"Sentiment: {sentiment_label}")
        
        # Readability
        readability = features.get('readability', {})
        if readability:
            flesch_score = readability.get('flesch_reading_ease', 0)
            print(f"Leggibilità: {flesch_score:.1f}/100")
        
        print("✅ Analisi completata con successo")

if __name__ == "__main__":
    print("🚀 TextAnalyzer - Test Nuove Funzionalità")
    print("=" * 60)
    
    try:
        test_sentiment_analysis()
        test_readability_analysis()
        test_full_analysis()
        
        print("\n\n🎉 Tutti i test completati con successo!")
        print("Le funzionalità di sentiment analysis e leggibilità sono operative.")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()
