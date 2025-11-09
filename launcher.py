#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher per TextAnalyzer V2 - Enhanced Edition
Facilita l'avvio delle diverse versioni del TextAnalyzer
"""

import sys
import os
import argparse

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def launch_v2():
    """Avvia TextAnalyzer V2 Enhanced"""
    print("🚀 Avvio TextAnalyzer V2 - Enhanced Edition")
    print("=" * 60)
    print("✨ Funzionalità incluse:")
    print("  • Sentiment Analysis con lessico VADER")
    print("  • Indice di Leggibilità (Flesch, FK-Grade, ecc.)")
    print("  • Varianza Lunghezza Frasi (AI Detection)")
    print("  • Help System con pulsanti (?)")
    print("  • Interfaccia GUI moderna con tema Clam")
    print("  • Analisi Comprensiva multi-metrica")
    print("=" * 60)
    
    try:
        from analyzer_v2 import main
        main()
    except ImportError as e:
        print(f"❌ Errore di importazione: {e}")
        print("💡 Verifica che analyzer_v2.py sia presente")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")

def launch_v1():
    """Avvia TextAnalyzer V1 (versione originale)"""
    print("🚀 Avvio TextAnalyzer V1 - Original Edition")
    print("=" * 60)
    
    try:
        from app import main as original_main
        original_main()
    except ImportError as e:
        print(f"❌ Errore di importazione: {e}")
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {e}")

def test_v2_features():
    """Testa le funzionalità di TextAnalyzer V2"""
    print("🧪 Test TextAnalyzer V2 - Funzionalità")
    print("=" * 60)
    
    try:
        from analyzer_v2 import EnhancedTextAnalyzer
        
        # Test analizzatore
        analyzer = EnhancedTextAnalyzer()
        
        # Testo di esempio
        test_text = """
        Questo è un testo di esempio. Ha frasi di lunghezza variabile per testare 
        l'analisi della varianza. Alcune frasi sono corte, altre sono più lunghe 
        e complesse. I modelli AI tendono a produrre frasi di lunghezza più regolare.
        Oggi è una bellissima giornata! Il sole splende e gli uccelli cantano.
        """
        
        # Test analisi comprensiva
        result = analyzer.comprehensive_analysis(test_text, "test_example.txt")
        
        if 'error' not in result:
            print("✅ Analisi comprensiva completata")
            
            # Test varianza frasi
            variance_result = analyzer.calculate_sentence_variance(test_text)
            if 'error' not in variance_result:
                print(f"✅ Varianza frasi: {variance_result['sentence_variance']:.2f}")
                print(f"   Classificazione: {variance_result['ai_likelihood']}")
            
            # Test spiegazioni metriche
            explanations = analyzer.metric_explanations
            print(f"✅ Spiegazioni metriche disponibili: {len(explanations)}")
            
            print("🎉 Tutti i test superati!")
        else:
            print(f"❌ Errore nell'analisi: {result['error']}")
            
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()

def show_comparison():
    """Mostra confronto tra V1 e V2"""
    print("📊 Confronto TextAnalyzer V1 vs V2")
    print("=" * 80)
    print("TextAnalyzer V1 - Original Edition:")
    print("  ✅ Classificazione AI vs Umano")
    print("  ✅ Sentiment Analysis (base)")
    print("  ✅ Indice di Leggibilità (base)")
    print("  ✅ GUI con tema Clam")
    print("  ❌ Help System")
    print("  ❌ Varianza Frasi")
    print("  ❌ Analisi Comprensiva")
    print()
    print("TextAnalyzer V2 - Enhanced Edition:")
    print("  ✅ Tutte le funzionalità V1")
    print("  ✅ Help System con pulsanti (?)")
    print("  ✅ Varianza Lunghezza Frasi (AI Detection)")
    print("  ✅ Analisi Comprensiva multi-metrica")
    print("  ✅ Spiegazioni dettagliate metriche")
    print("  ✅ Interfaccia migliorata")
    print("=" * 80)

def main():
    """Funzione principale del launcher"""
    parser = argparse.ArgumentParser(description='TextAnalyzer Launcher')
    parser.add_argument('version', choices=['v1', 'v2', 'test', 'compare'],
                       help='Versione da avviare')
    parser.add_argument('--gui', action='store_true', 
                       help='Forza avvio GUI (disponibile per v2)')
    
    args = parser.parse_args()
    
    if args.version == 'v1':
        launch_v1()
    elif args.version == 'v2':
        launch_v2()
    elif args.version == 'test':
        test_v2_features()
    elif args.version == 'compare':
        show_comparison()

if __name__ == "__main__":
    # Se chiamato senza argomenti, mostra menu
    if len(sys.argv) == 1:
        print("🎯 TextAnalyzer Launcher - Menu Principale")
        print("=" * 50)
        print("Versioni disponibili:")
        print("  v1  - Original Edition (classificazione base)")
        print("  v2  - Enhanced Edition (tutte le funzionalità)")
        print("  test - Test funzionalità V2")
        print("  compare - Confronto V1 vs V2")
        print()
        print("Uso:")
        print("  python launch.py v2    # Avvia V2 Enhanced")
        print("  python launch.py v1    # Avvia V1 Original")
        print("  python launch.py test  # Testa V2")
        print("  python launch.py compare # Mostra confronto")
        sys.exit(0)
    
    main()
