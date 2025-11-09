#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher per TextAnalyzer con interfaccia moderna PySide6
"""

import sys
import os

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def launch_modern():
    """Avvia TextAnalyzer con interfaccia moderna PySide6"""
    print("🚀 Avvio TextAnalyzer - Modern Edition (PySide6)")
    print("=" * 60)
    print("✨ Funzionalità incluse:")
    print("  • Interfaccia Qt moderna e professionale")
    print("  • Sentiment Analysis con lessico VADER")
    print("  • Indice di Leggibilità (Flesch, FK-Grade, ecc.)")
    print("  • Varianza Lunghezza Frasi (AI Detection)")
    print("  • Help System con pulsanti (?) moderni")
    print("  • Stili CSS e design contemporaneo")
    print("  • Layout Qt ottimizzati")
    print("=" * 60)
    
    try:
        from modern_analyzer import main
        main()
    except ImportError as e:
        print(f"❌ Errore di importazione: {e}")
        print("💡 Verifica che PySide6 sia installato: pip install PySide6")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")
        import traceback
        traceback.print_exc()

def test_modern_features():
    """Testa le funzionalità dell'interfaccia moderna"""
    print("🧪 Test TextAnalyzer Modern - Funzionalità")
    print("=" * 60)
    
    try:
        from modern_analyzer import ModernTextAnalyzer
        
        # Test analizzatore
        analyzer = ModernTextAnalyzer()
        
        # Test varianza frasi
        test_text = """
        Questo è un testo di esempio. Ha frasi di lunghezza variabile per testare 
        l'analisi della varianza. Alcune frasi sono corte, altre sono più lunghe 
        e complesse. I modelli AI tendono a produrre frasi di lunghezza più regolare.
        Oggi è una bellissima giornata! Il sole splende e gli uccelli cantano.
        """
        
        variance_result = analyzer.calculate_sentence_variance(test_text)
        
        if 'error' not in variance_result:
            print(f"✅ Varianza frasi: {variance_result['sentence_variance']:.2f}")
            print(f"   Classificazione: {variance_result['ai_likelihood']}")
        
        # Test spiegazioni metriche
        explanations = analyzer.metric_explanations
        print(f"✅ Spiegazioni metriche disponibili: {len(explanations)}")
        
        print("🎉 Tutti i test superati!")
        
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

def show_comparison():
    """Mostra confronto interfacce"""
    print("📊 Confronto Interfacce TextAnalyzer")
    print("=" * 80)
    print("Tkinter (V1 Originale):")
    print("  ✅ Funzionale ma aspetto datato")
    print("  ✅ Tema Clam disponibile")
    print("  ✅ Widget standard tkinter")
    print("  ❌ Stili limitati")
    print("  ❌ Layout meno flessibili")
    print()
    print("PySide6 Qt (Modern Edition):")
    print("  ✅ Design moderno e professionale")
    print("  ✅ Stili CSS e theming avanzato")
    print("  ✅ Widget Qt nativi e eleganti")
    print("  ✅ Layout Qt potenti e flessibili")
    print("  ✅ Animazioni e effetti")
    print("  ✅ Cross-platform nativo")
    print("  ✅ UX/UI superiore")
    print("=" * 80)

def main():
    """Funzione principale del launcher"""
    if len(sys.argv) == 1:
        print("🎯 TextAnalyzer Modern Launcher")
        print("=" * 50)
        print("Opzioni disponibili:")
        print("  (nessun argomento) - Avvia interfaccia moderna")
        print("  test - Testa funzionalità")
        print("  compare - Confronto interfacce")
        print()
        print("Uso:")
        print("  python modern_launcher.py      # Avvia GUI moderna")
        print("  python modern_launcher.py test # Testa funzionalità")
        print("  python modern_launcher.py compare # Mostra confronto")
        sys.exit(0)
    
    arg = sys.argv[1]
    
    if arg == 'test':
        test_modern_features()
    elif arg == 'compare':
        show_comparison()
    else:
        launch_modern()

if __name__ == "__main__":
    main()
