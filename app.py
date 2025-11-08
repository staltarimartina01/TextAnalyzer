# -*- coding: utf-8 -*-
"""
AI vs Human Text Analyzer - Professional Edition
Sistema completo per l'analisi e classificazione di testi generati da AI vs umani

Autore: Sistema di Analisi Testuale Professionale
Versione: 2.0
Data: 2025
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import List, Dict, Any

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.analyzer import TextAnalyzer
try:
    from gui.interface import main as gui_main
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    gui_main = None


class TextAnalyzerApp:
    """Applicazione principale per l'analisi testi AI vs umani"""
    
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.version = "2.0"
        self.description = "AI vs Human Text Analyzer - Professional Edition"
    
    def run_gui(self):
        """Avvia l'interfaccia grafica"""
        if not GUI_AVAILABLE:
            print("❌ Interfaccia grafica non disponibile (tkinter non trovato)")
            print("💡 Usa le modalità command-line: file, batch, interactive")
            return
        
        print(f"🚀 Avvio {self.description} v{self.version}")
        print("=" * 60)
        gui_main()
    
    def analyze_file(self, file_path: str, output: str = None, detailed: bool = True) -> Dict[str, Any]:
        """Analizza un singolo file"""
        if not os.path.exists(file_path):
            print(f"❌ Errore: File non trovato - {file_path}")
            return None
        
        print(f"📄 Analisi file: {file_path}")
        print("-" * 40)
        
        result = self.analyzer.analyze_file(file_path)
        
        if 'error' in result:
            print(f"❌ Errore: {result['error']}")
            return result
        
        # Mostra risultati
        self._display_result(result, detailed)
        
        # Salva se richiesto
        if output:
            self._save_result(result, output)
        
        return result
    
    def analyze_batch(self, directory: str, pattern: str = "*.txt", 
                     output: str = None, detailed: bool = False) -> List[Dict[str, Any]]:
        """Analizza multiple files"""
        if not os.path.exists(directory):
            print(f"❌ Errore: Directory non trovata - {directory}")
            return []
        
        print(f"📁 Analisi batch directory: {directory}")
        print(f"🔍 Pattern: {pattern}")
        print("-" * 40)
        
        results = self.analyzer.batch_analyze(directory, pattern)
        
        if not results:
            print("❌ Nessun file trovato")
            return []
        
        print(f"✅ Trovati {len(results)} file da analizzare")
        
        # Mostra statistiche
        self._display_batch_summary(results)
        
        # Mostra dettagli se richiesto
        if detailed:
            for i, result in enumerate(results, 1):
                print(f"\n--- File {i}/{len(results)} ---")
                self._display_result(result, False)
        
        # Genera report
        if output:
            report = self.analyzer.generate_report(results, output)
            print(f"\n💾 Report salvato in: {output}")
        
        return results
    
    def interactive_mode(self):
        """Modalità interattiva per analisi testo diretto"""
        print("🎯 Modalità Interattiva")
        print("Inserisci il testo da analizzare (riga vuota per terminare):")
        print("-" * 50)
        
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            except KeyboardInterrupt:
                break
        
        if not lines:
            print("❌ Nessun testo inserito")
            return
        
        text = "\n".join(lines)
        print("\n🔍 Analisi in corso...")
        
        result = self.analyzer.analyze_text(text, "testo_interattivo.txt")
        self._display_result(result, True)
    
    def _display_result(self, result: Dict[str, Any], detailed: bool = True):
        """Visualizza i risultati dell'analisi"""
        if 'error' in result:
            print(f"❌ Errore: {result['error']}")
            return
        
        assessment = result.get('final_assessment', {})
        prediction = assessment.get('prediction', 'Sconosciuto')
        confidence = assessment.get('confidence', 0)
        
        # Risultato principale
        if prediction == 'AI':
            print(f"🧠 RISULTATO: {prediction}")
        else:
            print(f"👤 RISULTATO: {prediction}")
        
        print(f"📊 Confidenza: {confidence:.1%}")
        print("-" * 30)
        
        # Statistiche base
        stats = result.get('text_stats', {})
        print(f"📄 Caratteri: {stats.get('char_count', 0):,}")
        print(f"🔤 Parole: {stats.get('word_count', 0):,}")
        print(f"📝 Frasi: {stats.get('sentence_count', 0):,}")
        print(f"🌈 Diversità lessicale: {stats.get('lexical_diversity', 0):.3f}")
        
        if detailed:
            # Features avanzate
            features = result.get('features', {})
            lexical = features.get('lexical', {})
            style = features.get('style', {})
            
            print("\n🔍 Analisi Approfondita:")
            print(f"  • Rapporto tipi/token: {lexical.get('type_token_ratio', 0):.3f}")
            print(f"  • Consistenza stilistica: {style.get('stylistic_consistency', 0):.3f}")
            print(f"  • Parole lunghe (>6): {lexical.get('long_words_ratio', 0):.1%}")
            print(f"  • Ripetizione parole: {style.get('word_repetition_ratio', 0):.1%}")
    
    def _display_batch_summary(self, results: List[Dict[str, Any]]):
        """Mostra summary dell'analisi batch"""
        if not results:
            return
        
        # Conta predizioni
        ai_count = sum(1 for r in results if r.get('final_assessment', {}).get('prediction') == 'AI')
        human_count = sum(1 for r in results if r.get('final_assessment', {}).get('prediction') == 'UMANO')
        
        print(f"\n📊 RISULTATI BATCH:")
        print(f"  🧠 Testi AI: {ai_count} ({ai_count/len(results)*100:.1f}%)")
        print(f"  👤 Testi Umani: {human_count} ({human_count/len(results)*100:.1f}%)")
        
        # Confidence media
        confidences = [r.get('final_assessment', {}).get('confidence', 0) for r in results]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            print(f"  📈 Confidenza media: {avg_confidence:.1%}")
    
    def _save_result(self, result: Dict[str, Any], output_path: str):
        """Salva risultato in file"""
        try:
            if output_path.endswith('.json'):
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            else:
                report = self.analyzer.generate_report([result], None)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report)
            print(f"💾 Risultato salvato in: {output_path}")
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")
    
    def show_info(self):
        """Mostra informazioni sul sistema"""
        print(f"🤖 {self.description}")
        print(f"Versione: {self.version}")
        print("=" * 60)
        print("Caratteristiche principali:")
        print("• 🧠 Classificazione AI vs testi umani")
        print("• 📊 Analisi lessicale avanzata")
        print("• 🎨 Analisi stilistica e sintattica")
        print("• 📁 Elaborazione batch di file")
        print("• 💾 Export risultati in multiple formati")
        print("• 🖥️ Interfaccia grafica intuitiva")
        print("\nTecnologie utilizzate:")
        print("• Python 3.12+")
        print("• Text processing avanzato")
        print("• Machine Learning (rule-based + ML)")
        print("• GUI con tkinter")
        print("=" * 60)
        print("\nUso:")
        print("  python app.py gui                    # Interfaccia grafica")
        print("  python app.py file <path>            # Analizza un file")
        print("  python app.py batch <dir>            # Analisi batch")
        print("  python app.py interactive            # Modalità interattiva")
        print("  python app.py info                   # Informazioni")


def main():
    """Funzione principale CLI"""
    parser = argparse.ArgumentParser(description='AI vs Human Text Analyzer')
    parser.add_argument('command', choices=['gui', 'file', 'batch', 'interactive', 'info'],
                       help='Comando da eseguire')
    parser.add_argument('path', nargs='?', help='Path del file o directory')
    parser.add_argument('--output', '-o', help='File di output per i risultati')
    parser.add_argument('--detailed', '-d', action='store_true', 
                       help='Mostra risultati dettagliati')
    parser.add_argument('--pattern', '-p', default='*.txt', 
                       help='Pattern per file batch (default: *.txt)')
    
    args = parser.parse_args()
    
    app = TextAnalyzerApp()
    
    if args.command == 'gui':
        app.run_gui()
    
    elif args.command == 'file':
        if not args.path:
            print("❌ Errore: Specificare il path del file")
            return
        result = app.analyze_file(args.path, args.output, args.detailed)
    
    elif args.command == 'batch':
        if not args.path:
            print("❌ Errore: Specificare la directory")
            return
        results = app.analyze_batch(args.path, args.pattern, args.output, args.detailed)
    
    elif args.command == 'interactive':
        app.interactive_mode()
    
    elif args.command == 'info':
        app.show_info()


if __name__ == "__main__":
    main()
