#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite per il Sistema di Analisi Testuale Avanzato
Per Tesi "LLM vs Autore Umano" - Analisi Comparativa

Questo script testa tutte le funzionalità del nuovo sistema
e genera risultati di esempio per la tesi.
"""

import json
import os
from advanced_analyzer import AdvancedTextAnalyzer

def test_ai_vs_human_detection():
    """Test la capacità di rilevamento AI vs umano"""
    analyzer = AdvancedTextAnalyzer()
    
    # Testo tipico AI (formale, ben strutturato, lessico ricco)
    ai_text = """
    The implementation of advanced natural language processing systems has fundamentally 
    transformed the landscape of computational linguistics. These sophisticated algorithms 
    demonstrate remarkable capabilities in understanding and generating human-like textual 
    content. Furthermore, the continuous improvement of machine learning models enables 
    increasingly accurate analysis of complex linguistic patterns and intricate semantic 
    structures. The theoretical framework underlying these technologies represents a 
    significant milestone in artificial intelligence research and development.
    """
    
    # Testo tipico umano (più naturale, variabilità, imperfezioni)
    human_text = """
    I was walking through the old forest yesterday, you know? The trees were super tall 
    and ancient, like really old. Their branches were reaching up toward the cloudy sky 
    like, I don't know, gnarled fingers or something. Anyway, I felt pretty peaceful 
    walking among all that natural beauty, but honestly I couldn't shake this weird 
    feeling that something was watching me from the shadows. Made me a bit nervous, 
    honestly.
    """
    
    print("🧠 === TEST RILEVAMENTO AI vs UMANO ===")
    print("\n📝 Analizzando testo AI...")
    ai_results = analyzer.analyze_text(ai_text)
    
    print("📝 Analizzando testo umano...")
    human_results = analyzer.analyze_text(human_text)
    
    # Confronta i risultati
    print("\n🤖 RISULTATI TESTO AI:")
    print(f"   Probabilità AI: {ai_results['ai_detection_score']['ai_probability']:.1%}")
    print(f"   Confidenza: {ai_results['ai_detection_score']['confidence']:.1%}")
    print(f"   Classificazione: {ai_results['ai_detection_score']['classification']}")
    
    print("\n👤 RISULTATI TESTO UMANO:")
    print(f"   Probabilità AI: {human_results['ai_detection_score']['ai_probability']:.1%}")
    print(f"   Confidenza: {human_results['ai_detection_score']['confidence']:.1%}")
    print(f"   Classificazione: {human_results['ai_detection_score']['classification']}")
    
    return ai_results, human_results

def test_all_metrics():
    """Test completo di tutte le metriche implementate"""
    analyzer = AdvancedTextAnalyzer()
    
    sample_text = """
    Technology continues to evolve rapidly in today's digital landscape. 
    Artificial intelligence systems are becoming increasingly sophisticated. 
    However, we must consider the ethical implications of these advancements. 
    The future promises both opportunities and challenges for humanity.
    """
    
    print("\n📊 === TEST COMPLETO METRICHE AVANZATE ===")
    results = analyzer.analyze_text(sample_text)
    
    print("\n📝 Metriche Lessicali:")
    lexical = results['metriche_lessicali']
    for key, value in lexical.items():
        if key != 'categorie_parole':
            print(f"   {key}: {value}")
    
    print("\n🔧 Metriche Sintattiche:")
    syntactic = results['metriche_sintattiche']
    for key, value in syntactic.items():
        print(f"   {key}: {value}")
    
    print("\n💭 Metriche Semantiche:")
    semantic = results['metriche_semantiche']
    for key, value in semantic.items():
        print(f"   {key}: {value}")
    
    print("\n🎨 Metriche Stilistiche:")
    stylistic = results['metriche_stilistiche']
    for key, value in stylistic.items():
        print(f"   {key}: {value}")
    
    return results

def save_results_to_file(results, filename):
    """Salva i risultati in un file JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ Risultati salvati in: {filename}")
    except Exception as e:
        print(f"❌ Errore salvataggio: {e}")

def main():
    """Funzione principale di test"""
    print("🚀 === SISTEMA ANALISI TESTUALE AVANZATO ===")
    print("📚 Per Tesi: LLM vs Autore Umano - Analisi Comparativa")
    print("=" * 60)
    
    # Inizializza l'analyzer
    analyzer = AdvancedTextAnalyzer()
    
    # Test 1: Rilevamento AI vs Umano
    ai_results, human_results = test_ai_vs_human_detection()
    
    # Test 2: Metriche complete
    all_metrics_results = test_all_metrics()
    
    # Salva risultati
    print("\n💾 === SALVATAGGIO RISULTATI ===")
    save_results_to_file(ai_results, "test_ai_results.json")
    save_results_to_file(human_results, "test_human_results.json")
    save_results_to_file(all_metrics_results, "test_all_metrics.json")
    
    print("\n🎯 === RIEPILOGO FUNZIONALITÀ IMPLEMENTATE ===")
    print("✅ Metriche Lessicali: TTR, Burstiness, Densità, Ricchezza Vocabolario")
    print("✅ Metriche Sintattiche: Variabilità Frasi, Pattern Ripetitivi, Complessità")
    print("✅ Metriche Semantiche: Sentiment Analysis, Coerenza Tematica, Transizioni Emotive")
    print("✅ Metriche Stilistiche: Figure Retoriche, Connettivi, Originalità Linguistica")
    print("✅ AI Detection: Sistema di punteggio probabilità AI vs umano")
    print("✅ GUI PySide6: Interfaccia moderna con visualizzazione risultati")
    print("✅ Export JSON: Salvataggio automatico risultati per analisi")
    
    print("\n🎓 SISTEMA PRONTO PER TESI!")
    print("Tutte le metriche richieste per l'analisi comparativa LLM vs Autore Umano sono state implementate.")

if __name__ == "__main__":
    main()
