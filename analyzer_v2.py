# -*- coding: utf-8 -*-
"""
TextAnalyzer V2 - Enhanced Edition
Analizzatore avanzato con interfaccia GUI migliorata
Include: Sentiment Analysis, Readability Metrics, AI Detection, e Help System
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import math
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

# Aggiungi il path del progetto per importare i moduli esistenti
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import TextAnalyzer
from features.feature_extractor import FeatureExtractor

class MetricInfoWindow:
    """Finestra modale per mostrare informazioni sulle metriche"""
    
    def __init__(self, parent: tk.Tk, title: str, explanation: str):
        self.parent = parent
        self.window = None
        
        # Crea finestra modale
        self.window = tk.Toplevel(parent)
        self.window.title(f"ℹ️ {title}")
        self.window.geometry("500x300")
        self.window.configure(bg='#F8F9FA')
        self.window.transient(parent)
        self.window.grab_set()  # Rende la finestra modale
        
        # Centra la finestra
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"500x300+{x}+{y}")
        
        self._setup_ui(title, explanation)
        
    def _setup_ui(self, title: str, explanation: str):
        """Configura l'interfaccia della finestra di aiuto"""
        # Frame principale
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titolo
        title_label = ttk.Label(main_frame, text=title, 
                               font=('Segoe UI', 14, 'bold'),
                               foreground='#2E86C1')
        title_label.pack(pady=(0, 15))
        
        # Scrollable text area per la spiegazione
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        text_widget = scrolledtext.ScrolledText(text_frame, 
                                               wrap=tk.WORD,
                                               font=('Segoe UI', 10),
                                               height=10,
                                               state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Inserisci il testo
        text_widget.config(state='normal')
        text_widget.insert('1.0', explanation)
        text_widget.config(state='disabled')
        
        # Pulsante chiudi
        close_btn = ttk.Button(main_frame, text="Chiudi", 
                              command=self.close,
                              style='TButton')
        close_btn.pack()
    
    def close(self):
        """Chiude la finestra"""
        if self.window:
            self.window.destroy()

class EnhancedTextAnalyzer:
    """Analizzatore migliorato con nuove funzionalità"""
    
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.feature_extractor = FeatureExtractor()
        
        # Dizionario di spiegazioni metriche
        self.metric_explanations = {
            'flesch_reading_ease': {
                'title': 'Indice Flesch Reading Ease',
                'text': """L'Indice Flesch Reading Ease misura la leggibilità del testo su una scala da 0 a 100.

• Punteggi 90-100: Molto facile (scuola elementare)
• Punteggi 80-89: Facile (scuola media)
• Punteggi 70-79: Abbastanza facile (scuola superiore)
• Punteggi 60-69: Standard (scuola superiore)
• Punteggi 50-59: Abbastanza difficile (università)
• Punteggi 30-49: Difficile (laureati)
• Punteggi 0-29: Molto difficile (livello post-laurea)

Il calcolo considera la lunghezza media delle frasi e delle parole.
Testi AI spesso mostrano punteggi molto alti (molto facili da leggere) 
perché le frasi tendono ad essere più regolari e prevedibili."""
            },
            'sentiment_analysis': {
                'title': 'Analisi Sentiment',
                'text': """L'Analisi Sentiment determina la polarità emotiva del testo (Positivo/Negativo/Neutro).

Il sistema utilizza un lessico di parole emotive in italiano per:
• Identificare parole positive (felicità, successo, gioia, ecc.)
• Identificare parole negative (tristezza, fallimento, rabbia, ecc.)
• Calcolare il sentiment netto e l'intensità emotiva

Tipi di Emozioni Rilevate:
• Gioia: felice, contento, gioioso, allegro
• Tristezza: triste, mesto, addolorato, depresso
• Rabbia: arrabbiato, furioso, irritato, indignato
• Paura: paura, terrore, panico, spavento
• Sorpresa: sorpresa, stupore, meravigliato

I testi AI spesso mostrano sentiment più neutro e costante
rispetto ai testi umani che presentano maggiori variazioni emotive."""
            },
            'sentence_variance': {
                'title': 'Varianza Lunghezza Frasi',
                'text': """La Varianza Lunghezza Frasi misura la diversità nella struttura delle frasi.

Calcolo:
1. Divide il testo in frasi individuali
2. Conta le parole in ogni frase
3. Calcola la varianza statistica di queste lunghezze

Interpretazione:
• Varianza Bassa: Frasi di lunghezza simile → Probabile AI
  (I modelli AI tendono a mantenere lunghezze costanti)
• Varianza Alta: Grande diversità nelle lunghezze → Probabile Umano
  (Gli esseri umani variano naturalmente la lunghezza delle frasi)

Esempi:
• Varianza < 5: Molto probabile AI
• Varianza 5-15: Probabile AI
• Varianza 15-30: Indeterminato
• Varianza > 30: Probabile Umano

Questa metrica è particolarmente efficace per testi di media lunghezza 
(200-2000 parole) dove i pattern diventano più evidenti."""
            }
        }
    
    def calculate_sentence_variance(self, text: str) -> Dict[str, Any]:
        """Calcola la varianza della lunghezza delle frasi per rilevare pattern AI"""
        try:
            # Dividi in frasi (approssimazione semplificata senza NLTK)
            sentences = self._simple_sentence_tokenize(text)
            
            if len(sentences) < 2:
                return {
                    'error': 'Testo troppo breve per calcolo varianza (minimo 2 frasi)',
                    'sentence_variance': 0.0,
                    'sentence_lengths': [],
                    'avg_sentence_length': 0.0,
                    'ai_likelihood': 'Indeterminato'
                }
            
            # Calcola lunghezza di ogni frase
            sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
            
            if len(sentence_lengths) < 2:
                return {
                    'error': 'Numero insufficiente di frasi valide',
                    'sentence_variance': 0.0,
                    'sentence_lengths': sentence_lengths,
                    'avg_sentence_length': sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
                    'ai_likelihood': 'Indeterminato'
                }
            
            # Calcola varianza
            mean_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
            
            # Classificazione basata sulla varianza
            if variance < 5:
                ai_likelihood = "Molto Probabile AI"
                confidence = "Alta"
            elif variance < 15:
                ai_likelihood = "Probabile AI" 
                confidence = "Media"
            elif variance < 30:
                ai_likelihood = "Indeterminato"
                confidence = "Bassa"
            else:
                ai_likelihood = "Molto Probabile Umano"
                confidence = "Alta"
            
            return {
                'sentence_variance': variance,
                'sentence_lengths': sentence_lengths,
                'avg_sentence_length': mean_length,
                'min_sentence_length': min(sentence_lengths),
                'max_sentence_length': max(sentence_lengths),
                'ai_likelihood': ai_likelihood,
                'confidence': confidence,
                'total_sentences': len(sentences)
            }
            
        except Exception as e:
            return {
                'error': f'Errore nel calcolo varianza: {str(e)}',
                'sentence_variance': 0.0,
                'sentence_lengths': [],
                'avg_sentence_length': 0.0,
                'ai_likelihood': 'Errore'
            }
    
    def _simple_sentence_tokenize(self, text: str) -> List[str]:
        """Tokenizzazione semplificata delle frasi senza NLTK"""
        # Pattern per identificare fine frase
        sentence_enders = r'[.!?]+'
        
        # Dividi il testo mantenendo i separatori
        parts = re.split(sentence_enders, text)
        
        sentences = []
        for part in parts:
            part = part.strip()
            if len(part) > 10:  # Filtra frasi troppo corte
                sentences.append(part)
        
        return sentences
    
    def comprehensive_analysis(self, text: str, file_name: str = None) -> Dict[str, Any]:
        """Analisi completa con tutte le metriche migliorate"""
        try:
            # Analisi base esistente
            base_result = self.analyzer.analyze_text(text, file_name)
            
            if 'error' in base_result:
                return base_result
            
            # Calcola varianza frasi (nuova funzionalità)
            sentence_variance_result = self.calculate_sentence_variance(text)
            
            # Combina tutti i risultati
            enhanced_result = {
                **base_result,
                'enhanced_features': {
                    'sentence_variance': sentence_variance_result,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'enhanced_version': '2.0'
                },
                'comprehensive_assessment': self._generate_comprehensive_assessment(
                    base_result, sentence_variance_result
                )
            }
            
            return enhanced_result
            
        except Exception as e:
            return {
                'error': f'Errore nell\'analisi avanzata: {str(e)}',
                'text_preview': text[:100] + '...' if len(text) > 100 else text
            }
    
    def _generate_comprehensive_assessment(self, base_result: Dict, sentence_variance: Dict) -> Dict[str, Any]:
        """Genera valutazione comprensiva combinando tutte le metriche"""
        assessments = []
        
        # Valutazione base AI vs Umano
        base_assessment = base_result.get('final_assessment', {})
        if base_assessment:
            assessments.append({
                'metric': 'Classificazione Base',
                'result': f"{base_assessment.get('prediction', 'Sconosciuto')} ({base_assessment.get('confidence', 0):.1%})",
                'weight': 0.4
            })
        
        # Valutazione varianza frasi
        if 'error' not in sentence_variance:
            variance_score = sentence_variance.get('ai_likelihood', 'Indeterminato')
            assessments.append({
                'metric': 'Varianza Frasi',
                'result': f"{variance_score} (σ²={sentence_variance.get('sentence_variance', 0):.1f})",
                'weight': 0.3
            })
        
        # Valutazione sentiment
        features = base_result.get('features', {})
        sentiment = features.get('sentiment', {})
        if sentiment:
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            if abs(net_sentiment) < 0.1:
                sentiment_assessment = "Sentiment Neutro → AI-like"
            else:
                sentiment_assessment = "Sentiment Variabile → Umano-like"
            
            assessments.append({
                'metric': 'Pattern Emotivo',
                'result': sentiment_assessment,
                'weight': 0.15
            })
        
        # Valutazione leggibilità
        readability = features.get('readability', {})
        if readability:
            flesch = readability.get('flesch_reading_ease', 50)
            if flesch > 80:
                readability_assessment = "Molto Facile → AI-like"
            elif flesch < 40:
                readability_assessment = "Difficile → Umano-like"
            else:
                readability_assessment = "Standard"
            
            assessments.append({
                'metric': 'Leggibilità',
                'result': readability_assessment,
                'weight': 0.15
            })
        
        return {
            'individual_assessments': assessments,
            'enhanced_confidence': self._calculate_enhanced_confidence(assessments),
            'summary': self._generate_summary(assessments)
        }
    
    def _calculate_enhanced_confidence(self, assessments: List[Dict]) -> float:
        """Calcola confidenza migliorata pesando tutte le metriche"""
        if not assessments:
            return 0.5
        
        total_weighted_score = 0
        total_weight = 0
        
        for assessment in assessments:
            weight = assessment.get('weight', 0.1)
            result = assessment.get('result', '')
            
            # Calcola score basato sul contenuto
            if 'AI' in result or 'AI-like' in result:
                ai_score = 0.8
            elif 'Umano' in result or 'Umano-like' in result:
                ai_score = 0.2
            else:
                ai_score = 0.5  # Indeterminato
            
            total_weighted_score += ai_score * weight
            total_weight += weight
        
        return total_weighted_score / total_weight if total_weight > 0 else 0.5
    
    def _generate_summary(self, assessments: List[Dict]) -> str:
        """Genera riepilogo delle valutazioni"""
        if not assessments:
            return "Nessuna valutazione disponibile"
        
        ai_indicators = 0
        human_indicators = 0
        
        for assessment in assessments:
            result = assessment.get('result', '')
            if 'AI' in result or 'AI-like' in result:
                ai_indicators += 1
            elif 'Umano' in result or 'Umano-like' in result:
                human_indicators += 1
        
        if ai_indicators > human_indicators:
            final_prediction = "AI (Potenziato)"
        elif human_indicators > ai_indicators:
            final_prediction = "Umano (Potenziato)"
        else:
            final_prediction = "Indeterminato"
        
        summary = f"Analisi Comprensiva: {final_prediction}\n"
        summary += f"Indicatori AI: {ai_indicators}, Indicatori Umano: {human_indicators}\n"
        summary += f"Metriche valutate: {len(assessments)}"
        
        return summary


class EnhancedTextAnalyzerGUI:
    """Interfaccia grafica migliorata con help system e nuove funzionalità"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("TextAnalyzer V2 - Enhanced Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#F8F9FA')
        
        # Inizializza analizzatore migliorato
        self.enhanced_analyzer = EnhancedTextAnalyzer()
        
        # Variabili di stato
        self.current_file = None
        self.analysis_results = None
        
        self.setup_ui()
        self.setup_styles()
    
    def setup_styles(self):
        """Configura stili per l'interfaccia migliorata"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colori moderni
        modern_blue = '#2E86C1'
        modern_green = '#28B463'
        modern_red = '#E74C3C'
        modern_orange = '#F39C12'
        modern_purple = '#8E44AD'
        background_color = '#F8F9FA'
        text_color = '#2C3E50'
        border_color = '#BDC3C7'
        
        # Configurazioni base moderne
        style.configure('TFrame', background=background_color, relief='flat')
        style.configure('TLabel', background=background_color, foreground=text_color, 
                       font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9), padding=(10, 5))
        style.configure('TEntry', font=('Consolas', 9))
        style.configure('TNotebook', tabposition='n', font=('Segoe UI', 9))
        style.configure('TNotebook.Tab', padding=(15, 8), font=('Segoe UI', 9, 'bold'))
        
        # Stili per pulsanti di help
        style.configure('Help.TButton', 
                       font=('Segoe UI', 8), 
                       padding=(5, 2),
                       width=3)
        
        # Stili per metriche
        style.configure('Metric.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       background=background_color, 
                       foreground=modern_purple)
        
        style.configure('Value.TLabel', 
                       font=('Consolas', 9), 
                       background=background_color, 
                       foreground=text_color)
    
    def setup_ui(self):
        """Configura l'interfaccia utente migliorata"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configura griglia principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titolo migliorato
        title_label = ttk.Label(main_frame, 
                               text="TextAnalyzer V2 - Enhanced Edition", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Pannello di controllo
        self.setup_control_panel(main_frame)
        
        # Notebook per i risultati
        self.setup_results_panel(main_frame)
        
        # Pannello di stato
        self.setup_status_panel(main_frame)
    
    def setup_control_panel(self, parent):
        """Configura il pannello di controllo migliorato"""
        control_frame = ttk.LabelFrame(parent, text="Controlli Avanzati", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # Pulsante carica file
        ttk.Button(control_frame, text="📁 Carica File", 
                  command=self.load_file).grid(row=0, column=0, padx=(0, 10))
        
        # Pulsante analisi avanzata
        self.analyze_btn = ttk.Button(control_frame, text="🔍 Analisi Avanzata", 
                                     command=self.enhanced_analyze_text, state='disabled')
        self.analyze_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Pulsante batch analysis
        ttk.Button(control_frame, text="📊 Analisi Batch", 
                  command=self.batch_analyze).grid(row=0, column=2, padx=(0, 10))
        
        # Pulsante crea sample
        ttk.Button(control_frame, text="📝 Crea Esempi", 
                  command=self.create_samples).grid(row=0, column=3, padx=(0, 10))
        
        # Pulsante esporta
        ttk.Button(control_frame, text="💾 Esporta Report", 
                  command=self.export_report, state='disabled').grid(row=0, column=4)
        
        # Etichetta file corrente
        self.file_label = ttk.Label(control_frame, text="Nessun file caricato", 
                                   style='Confidence.TLabel')
        self.file_label.grid(row=1, column=0, columnspan=5, pady=(10, 0), sticky=tk.W)
    
    def setup_results_panel(self, parent):
        """Configura il pannello dei risultati con sezioni migliorate"""
        # Notebook per i risultati
        self.results_notebook = ttk.Notebook(parent)
        self.results_notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Tab testo originale
        self.text_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.text_frame, text="📄 Testo Originale")
        
        self.text_display = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10), height=15)
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab risultati analisi avanzata
        self.analysis_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.analysis_frame, text="📊 Analisi Avanzata")
        
        # Scrollable frame per i risultati
        self.setup_analysis_results(self.analysis_frame)
        
        # Tab confronti
        self.comparison_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.comparison_frame, text="🔄 Confronti")
        
        self.setup_comparison_panel(self.comparison_frame)
    
    def setup_analysis_results(self, parent):
        """Configura il pannello dei risultati dell'analisi avanzata"""
        # Canvas e scrollbar
        canvas = tk.Canvas(parent, bg='#F8F9FA')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Contenuto dei risultati
        self.results_content = scrollable_frame
    
    def setup_comparison_panel(self, parent):
        """Configura il pannello dei confronti"""
        ttk.Label(parent, text="Confronti tra testi", style='Heading.TLabel').pack(pady=10)
        
        self.comparison_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, 
                                                        font=('Consolas', 10), height=15)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_status_panel(self, parent):
        """Configura il pannello di stato"""
        status_frame = ttk.LabelFrame(parent, text="Stato Sistema", padding="5")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Pronto per l'analisi avanzata", 
                                     style='Confidence.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
    
    def show_metric_info(self, metric_key: str):
        """Mostra informazioni dettagliate su una metrica"""
        if metric_key in self.enhanced_analyzer.metric_explanations:
            info = self.enhanced_analyzer.metric_explanations[metric_key]
            MetricInfoWindow(self.root, info['title'], info['text'])
        else:
            messagebox.showinfo("Info", f"Informazioni non disponibili per: {metric_key}")
    
    def enhanced_analyze_text(self):
        """Esegue l'analisi avanzata del testo"""
        if not self.current_file:
            messagebox.showwarning("Attenzione", "Nessun file da analizzare")
            return
        
        # Avvia analisi in thread separato
        threading.Thread(target=self._enhanced_analyze_worker, daemon=True).start()
    
    def _enhanced_analyze_worker(self):
        """Worker per l'analisi avanzata (eseguito in thread separato)"""
        try:
            self.update_status("Analisi avanzata in corso...")
            self.progress.start()
            
            # Disabilita interfaccia durante l'analisi
            self.root.after(0, lambda: self._set_ui_state('disabled'))
            
            # Leggi file
            with open(self.current_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Analisi avanzata
            result = self.enhanced_analyzer.comprehensive_analysis(text, 
                                                                os.path.basename(self.current_file))
            self.analysis_results = result
            
            # Aggiorna interfaccia
            self.root.after(0, self._display_enhanced_analysis_results)
            self.root.after(0, lambda: self._set_ui_state('normal'))
            self.root.after(0, lambda: self.progress.stop())
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore durante l'analisi:\n{str(e)}"))
            self.root.after(0, lambda: self._set_ui_state('normal'))
            self.root.after(0, lambda: self.progress.stop())
    
    def _display_enhanced_analysis_results(self):
        """Visualizza i risultati dell'analisi avanzata"""
        if not self.analysis_results or 'error' in self.analysis_results:
            return
        
        # Pulisce i risultati precedenti
        for widget in self.results_content.winfo_children():
            widget.destroy()
        
        # Header risultato
        enhanced_features = self.analysis_results.get('enhanced_features', {})
        comprehensive_assessment = self.analysis_results.get('comprehensive_assessment', {})
        
        # Risultato principale
        result_label = ttk.Label(self.results_content, text="🧠 ANALISI COMPRENSIVA", 
                               style='Title.TLabel')
        result_label.pack(pady=10)
        
        # Valutazione comprensiva
        if comprehensive_assessment:
            summary = comprehensive_assessment.get('summary', '')
            if summary:
                summary_label = ttk.Label(self.results_content, text=summary,
                                        font=('Segoe UI', 10, 'bold'),
                                        justify=tk.LEFT)
                summary_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Sezione Varianza Frasi (nuova funzionalità)
        sentence_variance = enhanced_features.get('sentence_variance', {})
        if sentence_variance and 'error' not in sentence_variance:
            variance_frame = ttk.LabelFrame(self.results_content, text="📈 Varianza Lunghezza Frasi")
            variance_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Pulsante help per varianza
            help_frame = ttk.Frame(variance_frame)
            help_frame.pack(anchor=tk.E, padx=10, pady=(5, 0))
            
            ttk.Button(help_frame, text="?", style='Help.TButton',
                      command=lambda: self.show_metric_info('sentence_variance')).pack()
            
            # Contenuto varianza
            content_frame = ttk.Frame(variance_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            variance_value = sentence_variance.get('sentence_variance', 0)
            ai_likelihood = sentence_variance.get('ai_likelihood', 'N/A')
            confidence = sentence_variance.get('confidence', 'N/A')
            
            ttk.Label(content_frame, text=f"Varianza: {variance_value:.2f}", 
                     style='Metric.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Classificazione: {ai_likelihood}", 
                     style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Confidenza: {confidence}", 
                     style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Statistiche Testo (come V1)
        text_stats = self.analysis_results.get('text_stats', {})
        if text_stats:
            stats_frame = ttk.LabelFrame(self.results_content, text="📊 Statistiche Testo")
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            content_frame = ttk.Frame(stats_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            char_count = text_stats.get('char_count', 0)
            word_count = text_stats.get('word_count', 0)
            sentence_count = text_stats.get('sentence_count', 0)
            lexical_diversity = text_stats.get('lexical_diversity', 0)
            
            ttk.Label(content_frame, text=f"Caratteri: {char_count:,}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Parole: {word_count:,}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Frasi: {sentence_count:,}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Diversità lessicale: {lexical_diversity:.3f}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Lessicale (come V1)
        features = self.analysis_results.get('features', {})
        lexical = features.get('lexical', {})
        if lexical:
            lexical_frame = ttk.LabelFrame(self.results_content, text="📚 Analisi Lessicale")
            lexical_frame.pack(fill=tk.X, padx=10, pady=5)
            
            content_frame = ttk.Frame(lexical_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            type_token_ratio = lexical.get('type_token_ratio', 0)
            lexical_diversity = lexical.get('lexical_diversity', 0)
            long_words_ratio = lexical.get('long_words_ratio', 0)
            
            ttk.Label(content_frame, text=f"Rapporto tipi/token: {type_token_ratio:.3f}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Diversità lessicale: {lexical_diversity:.3f}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Parole lunghe (>6): {long_words_ratio:.1%}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Stilistica (come V1)
        style = features.get('style', {})
        if style:
            style_frame = ttk.LabelFrame(self.results_content, text="🎨 Analisi Stilistica")
            style_frame.pack(fill=tk.X, padx=10, pady=5)
            
            content_frame = ttk.Frame(style_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            stylistic_consistency = style.get('stylistic_consistency', 0)
            word_repetition_ratio = style.get('word_repetition_ratio', 0)
            
            ttk.Label(content_frame, text=f"Consistenza stilistica: {stylistic_consistency:.3f}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Ripetizione parole: {word_repetition_ratio:.1%}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Sintattica (come V1)
        syntactic = features.get('syntactic', {})
        if syntactic:
            syntactic_frame = ttk.LabelFrame(self.results_content, text="📝 Analisi Sintattica")
            syntactic_frame.pack(fill=tk.X, padx=10, pady=5)
            
            content_frame = ttk.Frame(syntactic_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            avg_sentence_length = syntactic.get('avg_sentence_length', 0)
            complex_sentences_ratio = syntactic.get('complex_sentences_ratio', 0)
            punctuation_density = syntactic.get('punctuation_density', 0)
            
            ttk.Label(content_frame, text=f"Lunghezza media frase: {avg_sentence_length:.1f} parole", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Frasi complesse: {complex_sentences_ratio:.1%}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Densità punteggiatura: {punctuation_density:.1%}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Sentiment con Help
        sentiment = features.get('sentiment', {})
        if sentiment:
            sentiment_frame = ttk.LabelFrame(self.results_content, text="😊 Analisi Sentiment")
            sentiment_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Pulsante help per sentiment
            help_frame = ttk.Frame(sentiment_frame)
            help_frame.pack(anchor=tk.E, padx=10, pady=(5, 0))
            
            ttk.Button(help_frame, text="?", style='Help.TButton',
                      command=lambda: self.show_metric_info('sentiment_analysis')).pack()
            
            # Contenuto sentiment completo
            content_frame = ttk.Frame(sentiment_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            if net_sentiment > 0.1:
                sentiment_label = "POSITIVO"
                sentiment_color = "🟢"
            elif net_sentiment < -0.1:
                sentiment_label = "NEGATIVO"
                sentiment_color = "🔴"
            else:
                sentiment_label = "NEUTRALE"
                sentiment_color = "⚪"
            
            ttk.Label(content_frame, text=f"Sentiment generale: {sentiment_color} {sentiment_label}", style='Metric.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Emozione dominante: {self._get_emotion_text(sentiment.get('dominant_emotion', 0.5))}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Intensità emotiva: {sentiment.get('sentiment_intensity', 0):.1%}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Gioia: {sentiment.get('joy_indicators_ratio', 0):.1%}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Tristezza: {sentiment.get('sadness_indicators_ratio', 0):.1%}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Rabbia: {sentiment.get('anger_indicators_ratio', 0):.1%}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Sezione Leggibilità con Help
        readability = features.get('readability', {})
        if readability:
            readability_frame = ttk.LabelFrame(self.results_content, text="📖 Indice di Leggibilità")
            readability_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Pulsante help per Flesch
            help_frame = ttk.Frame(readability_frame)
            help_frame.pack(anchor=tk.E, padx=10, pady=(5, 0))
            
            ttk.Button(help_frame, text="?", style='Help.TButton',
                      command=lambda: self.show_metric_info('flesch_reading_ease')).pack()
            
            # Contenuto leggibilità completo
            content_frame = ttk.Frame(readability_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=10)
            
            flesch_score = readability.get('flesch_reading_ease', 0)
            fk_grade = readability.get('flesch_kincaid_grade', 0)
            gunning_fog = readability.get('gunning_fog_index', 0)
            smog_index = readability.get('smog_index', 0)
            complex_words_ratio = readability.get('complex_words_ratio', 0)
            
            # Determina il livello di leggibilità
            if flesch_score >= 90:
                readability_level = "Molto Facile"
            elif flesch_score >= 80:
                readability_level = "Facile"
            elif flesch_score >= 70:
                readability_level = "Abbastanza Facile"
            elif flesch_score >= 60:
                readability_level = "Standard"
            elif flesch_score >= 50:
                readability_level = "Abbastanza Difficile"
            elif flesch_score >= 30:
                readability_level = "Difficile"
            else:
                readability_level = "Molto Difficile"
            
            ttk.Label(content_frame, text=f"Livello: {readability_level} ({flesch_score:.1f}/100)", style='Metric.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Flesch-Kincaid Grade: {fk_grade:.1f} (scuola)", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Gunning Fog Index: {gunning_fog:.1f}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"SMOG Index: {smog_index:.1f}", style='Value.TLabel').pack(anchor=tk.W)
            ttk.Label(content_frame, text=f"Parole complesse: {complex_words_ratio:.1%}", style='Value.TLabel').pack(anchor=tk.W)
        
        # Abilita esportazione
        self.root.after(0, lambda: self._enable_export())
    
    def load_file(self):
        """Carica un file di testo"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file di testo",
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            try:
                self.update_status("Caricamento file...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                self.current_file = file_path
                self.file_label.config(text=f"📄 {os.path.basename(file_path)}")
                
                # Mostra il testo
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(1.0, text)
                
                # Abilita analisi
                self.analyze_btn.config(state='normal')
                
                self.update_status("File caricato con successo")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel caricamento del file:\n{str(e)}")
                self.update_status("Errore nel caricamento file")
    
    def _set_ui_state(self, state):
        """Imposta lo stato dell'interfaccia"""
        if state == 'disabled':
            for child in self.root.winfo_children():
                if isinstance(child, (ttk.Button, ttk.Entry)):
                    child.config(state='disabled')
        else:
            for child in self.root.winfo_children():
                if isinstance(child, (ttk.Button, ttk.Entry)):
                    child.config(state='normal')
        
        # Mantieni il pulsante analizza disabilitato se nessun file
        if not self.current_file:
            self.analyze_btn.config(state='disabled')
    
    def _get_emotion_text(self, dominant_emotion: float) -> str:
        """Converte il valore numerico dell'emozione in testo"""
        if dominant_emotion > 0.7:
            return "Gioia"
        elif dominant_emotion > 0.4:
            return "Sorpresa"
        elif dominant_emotion > 0.2:
            return "Rabbia"
        elif dominant_emotion > 0.1:
            return "Paura"
        elif dominant_emotion > 0.05:
            return "Tristezza"
        else:
            return "Neutro"

    def update_status(self, message):
        """Aggiorna il messaggio di stato"""
        self.status_label.config(text=message)
    
    def _enable_export(self):
        """Abilita il pulsante di esportazione"""
        # L'esportazione è già abilitata nel setup
    
    def batch_analyze(self):
        """Placeholder per analisi batch"""
        messagebox.showinfo("Info", "Funzionalità batch in sviluppo")
    
    def create_samples(self):
        """Placeholder per creazione esempi"""
        messagebox.showinfo("Info", "Funzionalità sample in sviluppo")
    
    def export_report(self):
        """Placeholder per esportazione report"""
        messagebox.showinfo("Info", "Funzionalità export in sviluppo")


def main():
    """Funzione principale per avviare l'applicazione migliorata"""
    root = tk.Tk()
    app = EnhancedTextAnalyzerGUI(root)
    
    # Centro la finestra
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1400 // 2)
    y = (root.winfo_screenheight() // 2) - (900 // 2)
    root.geometry(f"1400x900+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
