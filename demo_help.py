#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Help System - TextAnalyzer V2
Mostra come funzionano i pulsanti ? e le finestre di informazioni
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyzer_v2 import MetricInfoWindow, EnhancedTextAnalyzer

def demo_help_system():
    """Demo del sistema di help con pulsanti ?"""
    print("📚 Demo Help System - TextAnalyzer V2")
    print("=" * 50)
    
    # Crea finestra demo
    root = tk.Tk()
    root.title("Demo Help System - TextAnalyzer V2")
    root.geometry("600x400")
    root.configure(bg='#F8F9FA')
    
    # Titolo
    title = ttk.Label(root, text="🎯 Demo Sistema Help", 
                     font=('Segoe UI', 16, 'bold'),
                     foreground='#2E86C1')
    title.pack(pady=20)
    
    # Descrizione
    desc = ttk.Label(root, 
                    text="Clicca sui pulsanti ? per vedere le spiegazioni delle metriche",
                    font=('Segoe UI', 10))
    desc.pack(pady=(0, 20))
    
    # Frame per i pulsanti demo
    demo_frame = ttk.LabelFrame(root, text="Metriche Disponibili", padding="20")
    demo_frame.pack(fill=tk.X, padx=20, pady=10)
    
    # Inizializza analizzatore per le spiegazioni
    analyzer = EnhancedTextAnalyzer()
    
    # Pulsanti demo per ogni metrica
    metrics = [
        ('flesch_reading_ease', 'Indice Flesch Reading Ease', '📖'),
        ('sentiment_analysis', 'Analisi Sentiment', '😊'),
        ('sentence_variance', 'Varianza Lunghezza Frasi', '📈')
    ]
    
    for i, (key, title, emoji) in enumerate(metrics):
        frame = ttk.Frame(demo_frame)
        frame.pack(fill=tk.X, pady=5)
        
        # Etichetta metrica
        label = ttk.Label(frame, text=f"{emoji} {title}", 
                         font=('Segoe UI', 12, 'bold'))
        label.pack(side=tk.LEFT)
        
        # Pulsante help
        help_btn = ttk.Button(frame, text="?", style='Help.TButton',
                             command=lambda k=key: show_metric_demo(k, analyzer))
        help_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    # Pulsante chiudi
    close_btn = ttk.Button(root, text="Chiudi Demo", 
                          command=root.destroy,
                          style='TButton')
    close_btn.pack(pady=20)
    
    # Applica stili (semplificati per demo)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Help.TButton', font=('Segoe UI', 10), width=3)
    style.configure('TButton', font=('Segoe UI', 10), padding=(10, 5))
    
    print("✅ Finestra demo creata")
    print("💡 Clicca sui pulsanti ? per vedere le spiegazioni")
    
    # Centra la finestra
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (600 // 2)
    y = (root.winfo_screenheight() // 2) - (400 // 2)
    root.geometry(f"600x400+{x}+{y}")
    
    root.mainloop()

def show_metric_demo(metric_key: str, analyzer: EnhancedTextAnalyzer):
    """Mostra la finestra di help per una metrica specifica"""
    if metric_key in analyzer.metric_explanations:
        info = analyzer.metric_explanations[metric_key]
        MetricInfoWindow(None, info['title'], info['text'])
        print(f"📖 Aperta finestra help per: {info['title']}")
    else:
        print(f"❌ Spiegazione non trovata per: {metric_key}")

def main():
    """Funzione principale del demo"""
    try:
        demo_help_system()
    except Exception as e:
        print(f"❌ Errore durante il demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
