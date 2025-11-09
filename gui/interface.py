# -*- coding: utf-8 -*-
"""
GUI Interface - Interfaccia grafica per AI vs Human Text Analyzer
Interfaccia utente intuitiva per l'analisi dei testi
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from datetime import datetime
from typing import Dict, List, Any

# Aggiungi il path del progetto per importare i moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import TextAnalyzer
from utils.data_loader import DataLoader
from utils.evaluator import ModelEvaluator


class TextAnalyzerGUI:
    """Interfaccia grafica per l'analizzatore di testi AI vs umani"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("TextAnalyzer Professional - AI vs Human + Sentiment + Readability")
        self.root.geometry("1200x800")
        self.root.configure(bg='#F8F9FA')
        
        # Inizializza componenti
        self.analyzer = TextAnalyzer()
        self.data_loader = DataLoader()
        self.evaluator = ModelEvaluator()
        
        # Variabili di stato
        self.current_file = None
        self.analysis_results = None
        
        self.setup_ui()
        self.setup_styles()
    
    def setup_styles(self):
        """Configura stili per l'interfaccia con tema moderno"""
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
        
        # Configurazioni base per un aspetto più moderno
        style.configure('TFrame', background=background_color, relief='flat')
        style.configure('TLabel', background=background_color, foreground=text_color, 
                       font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9), padding=(10, 5))
        style.configure('TEntry', font=('Consolas', 9))
        style.configure('TNotebook', tabposition='n', font=('Segoe UI', 9))
        style.configure('TNotebook.Tab', padding=(15, 8), font=('Segoe UI', 9, 'bold'))
        
        # Stili personalizzati con colori moderni
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       background=background_color, 
                       foreground=modern_blue)
        
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       background=background_color, 
                       foreground=modern_purple)
        
        style.configure('AI.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=modern_red, 
                       background=background_color)
        
        style.configure('Human.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=modern_green, 
                       background=background_color)
        
        style.configure('Confidence.TLabel', 
                       font=('Segoe UI', 10, 'italic'), 
                       background=background_color, 
                       foreground='#7F8C8D')
        
        style.configure('Modern.TLabelframe', 
                       background=background_color, 
                       borderwidth=1, 
                       relief='solid',
                       bordercolor=border_color)
        
        style.configure('Modern.TLabelframe.Label', 
                       background=background_color, 
                       foreground=modern_blue,
                       font=('Segoe UI', 10, 'bold'))
    
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configura griglia principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titolo
        title_label = ttk.Label(main_frame, text="AI vs Human Text Analyzer", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Pannello di controllo
        self.setup_control_panel(main_frame)
        
        # Notebook per i risultati
        self.setup_results_panel(main_frame)
        
        # Pannello di stato
        self.setup_status_panel(main_frame)
    
    def setup_control_panel(self, parent):
        """Configura il pannello di controllo"""
        control_frame = ttk.LabelFrame(parent, text="Controlli", padding="10", style='Modern.TLabelframe')
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # Pulsante carica file
        ttk.Button(control_frame, text="📁 Carica File", 
                  command=self.load_file).grid(row=0, column=0, padx=(0, 10))
        
        # Pulsante analisi
        self.analyze_btn = ttk.Button(control_frame, text="🔍 Analizza Testo", 
                                     command=self.analyze_text, state='disabled')
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
        """Configura il pannello dei risultati"""
        # Notebook per i risultati
        self.results_notebook = ttk.Notebook(parent)
        self.results_notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Tab testo originale
        self.text_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.text_frame, text="📄 Testo Originale")
        
        self.text_display = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10), height=15)
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab risultati analisi
        self.analysis_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.analysis_frame, text="📊 Risultati Analisi")
        
        # Scrollable frame per i risultati
        self.setup_analysis_results(self.analysis_frame)
        
        # Tab confronti
        self.comparison_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.comparison_frame, text="🔄 Confronti")
        
        self.setup_comparison_panel(self.comparison_frame)
    
    def setup_analysis_results(self, parent):
        """Configura il pannello dei risultati dell'analisi"""
        # Canvas e scrollbar
        canvas = tk.Canvas(parent, bg='white')
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
        status_frame = ttk.LabelFrame(parent, text="Stato", padding="5", style='Modern.TLabelframe')
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Pronto per l'analisi", 
                                     style='Confidence.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
    
    def load_file(self):
        """Carica un file di testo"""
        file_path = filedialog.askopenfilename(
            title="Seleziona file di testo",
            filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
        )
        
        if file_path:
            try:
                self.update_status("Caricamento file...")
                text = self.data_loader.load_text_file(file_path)
                
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
    
    def analyze_text(self):
        """Analizza il testo corrente"""
        if not self.current_file:
            messagebox.showwarning("Attenzione", "Nessun file da analizzare")
            return
        
        # Avvia analisi in thread separato
        threading.Thread(target=self._analyze_worker, daemon=True).start()
    
    def _analyze_worker(self):
        """Worker per l'analisi (eseguito in thread separato)"""
        try:
            self.update_status("Analisi in corso...")
            self.progress.start()
            
            # Disabilita interfaccia durante l'analisi
            self.root.after(0, lambda: self._set_ui_state('disabled'))
            
            # Analizza il file
            result = self.analyzer.analyze_file(self.current_file)
            self.analysis_results = result
            
            # Aggiorna interfaccia
            self.root.after(0, self._display_analysis_results)
            self.root.after(0, lambda: self._set_ui_state('normal'))
            self.root.after(0, lambda: self.progress.stop())
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore durante l'analisi:\n{str(e)}"))
            self.root.after(0, lambda: self._set_ui_state('normal'))
            self.root.after(0, lambda: self.progress.stop())
    
    def _display_analysis_results(self):
        """Visualizza i risultati dell'analisi"""
        if not self.analysis_results or 'error' in self.assessment_results():
            return
        
        # Pulisce i risultati precedenti
        for widget in self.results_content.winfo_children():
            widget.destroy()
        
        assessment = self.assessment_results()
        prediction = assessment.get('prediction', 'Sconosciuto')
        confidence = assessment.get('confidence', 0)
        
        # Header risultato
        if prediction == 'AI':
            result_label = ttk.Label(self.results_content, text=f"🧠 RISULTATO: {prediction}", 
                                   style='AI.TLabel')
        else:
            result_label = ttk.Label(self.results_content, text=f"👤 RISULTATO: {prediction}", 
                                   style='Human.TLabel')
        result_label.pack(pady=10)
        
        # Confidence
        conf_label = ttk.Label(self.results_content, 
                              text=f"Confidenza: {confidence:.1%}", 
                              style='Confidence.TLabel')
        conf_label.pack()
        
        # Separatore
        ttk.Separator(self.results_content, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Statistiche del testo
        stats = self.analysis_results.get('text_stats', {})
        ttk.Label(self.results_content, text="📊 STATISTICHE TESTO:", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        stats_text = f"""
• Caratteri: {stats.get('char_count', 0):,}
• Parole: {stats.get('word_count', 0):,}
• Frasi: {stats.get('sentence_count', 0):,}
• Paragrafi: {stats.get('paragraph_count', 0):,}
• Diversità lessicale: {stats.get('lexical_diversity', 0):.3f}
• Lunghezza media parola: {stats.get('avg_word_length', 0):.1f} caratteri
• Lunghezza media frase: {stats.get('avg_sentence_length', 0):.1f} parole
        """
        
        ttk.Label(self.results_content, text=stats_text, 
                 font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Features principali
        features = self.analysis_results.get('features', {})
        lexical = features.get('lexical', {})
        syntactic = features.get('syntactic', {})
        style = features.get('style', {})
        
        # Features lessicali
        if lexical:
            ttk.Label(self.results_content, text="🔤 ANALISI LESSICALE:", 
                     style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            
            lex_text = f"""
• Diversità lessicale: {lexical.get('lexical_diversity', 0):.3f}
• Rapporto tipi/token: {lexical.get('type_token_ratio', 0):.3f}
• Parole lunghe (>6): {lexical.get('long_words_ratio', 0):.1%}
• Parole molto lunghe (>10): {lexical.get('very_long_words_ratio', 0):.1%}
• Entropia del testo: {lexical.get('text_entropy', 0):.3f}
            """
            
            ttk.Label(self.results_content, text=lex_text, 
                     font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Features sintattiche
        if syntactic:
            ttk.Label(self.results_content, text="📝 ANALISI SINTATTICA:", 
                     style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            
            synt_text = f"""
• Lunghezza media frase: {syntactic.get('avg_sentence_length', 0):.1f} parole
• Frasi complesse: {syntactic.get('complex_sentences_ratio', 0):.1%}
• Densità punteggiatura: {syntactic.get('punctuation_density', 0):.1%}
• Rapporti subordinazione: {syntactic.get('subordination_ratio', 0):.1%}
            """
            
            ttk.Label(self.results_content, text=synt_text, 
                     font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Features stilistiche
        if style:
            ttk.Label(self.results_content, text="🎨 ANALISI STILISTICA:", 
                     style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            
            style_text = f"""
• Consistenza stilistica: {style.get('stylistic_consistency', 0):.3f}
• Rapporto maiuscole: {style.get('uppercase_ratio', 0):.1%}
• Ripetizione parole: {style.get('word_repetition_ratio', 0):.1%}
• Numeri: {style.get('numbers_ratio', 0):.1%}
            """
            
            ttk.Label(self.results_content, text=style_text, 
                     font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Sentiment Analysis
        sentiment = features.get('sentiment', {})
        if sentiment:
            ttk.Label(self.results_content, text="😊 ANALISI SENTIMENT:", 
                     style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            
            # Determina l'etichetta del sentiment
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
            
            dominant_emotion = sentiment.get('dominant_emotion', 0.5)
            if dominant_emotion > 0.7:
                emotion_text = "Gioia"
            elif dominant_emotion > 0.4:
                emotion_text = "Sorpresa"
            elif dominant_emotion > 0.2:
                emotion_text = "Rabbia"
            elif dominant_emotion > 0.1:
                emotion_text = "Paura"
            elif dominant_emotion > 0.05:
                emotion_text = "Tristezza"
            else:
                emotion_text = "Neutro"
            
            sentiment_text = f"""
• Sentiment generale: {sentiment_color} {sentiment_label}
• Emozione dominante: {emotion_text}
• Intensità emotiva: {sentiment.get('sentiment_intensity', 0):.1%}
• Chiarezza emotiva: {sentiment.get('emotional_clarity', 0):.1%}
• Consistenza emotiva: {sentiment.get('emotional_consistency', 0):.1%}
• Gioia: {sentiment.get('joy_indicators_ratio', 0):.1%}
• Tristezza: {sentiment.get('sadness_indicators_ratio', 0):.1%}
• Rabbia: {sentiment.get('anger_indicators_ratio', 0):.1%}
            """
            
            ttk.Label(self.results_content, text=sentiment_text, 
                     font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Readability Analysis
        readability = features.get('readability', {})
        if readability:
            ttk.Label(self.results_content, text="📖 INDICE DI LEGGIBILITÀ:", 
                     style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            
            # Determina il livello di leggibilità
            flesch_score = readability.get('flesch_reading_ease', 0)
            if flesch_score >= 90:
                readability_level = "Molto Facile"
                readability_color = "🟢"
            elif flesch_score >= 80:
                readability_level = "Facile"
                readability_color = "🟡"
            elif flesch_score >= 70:
                readability_level = "Abbastanza Facile"
                readability_color = "🟡"
            elif flesch_score >= 60:
                readability_level = "Standard"
                readability_color = "🟠"
            elif flesch_score >= 50:
                readability_level = "Abbastanza Difficile"
                readability_color = "🟠"
            elif flesch_score >= 30:
                readability_level = "Difficile"
                readability_color = "🔴"
            else:
                readability_level = "Molto Difficile"
                readability_color = "🔴"
            
            fk_grade = readability.get('flesch_kincaid_grade', 0)
            gunning_fog = readability.get('gunning_fog_index', 0)
            
            readability_text = f"""
• Livello di leggibilità: {readability_color} {readability_level}
• Flesch Reading Ease: {flesch_score:.1f}/100
• Flesch-Kincaid Grade: {fk_grade:.1f} (scuola)
• Gunning Fog Index: {gunning_fog:.1f}
• SMOG Index: {readability.get('smog_index', 0):.1f}
• Lunghezza media frase: {readability.get('avg_sentence_length', 0):.1f} parole
• Parole complesse: {readability.get('complex_words_ratio', 0):.1%}
• Parole polisillabiche: {readability.get('polysyllabic_words_ratio', 0):.1%}
• Termini tecnici: {readability.get('technical_terms_ratio', 0):.1%}
            """
            
            ttk.Label(self.results_content, text=readability_text, 
                     font=('Segoe UI', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Spiegazione del risultato
        ttk.Label(self.results_content, text="💡 SPIEGAZIONE:", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
        
        explanation = self._generate_explanation(prediction, confidence, features)
        ttk.Label(self.results_content, text=explanation, 
                 font=('Segoe UI', 9), justify=tk.LEFT, wraplength=800).pack(anchor=tk.W)
        
        # Abilita esportazione
        self.root.after(0, lambda: self._enable_export())
    
    def assessment_results(self):
        """Ottiene i risultati dell'assessment"""
        if not self.analysis_results or 'error' in self.analysis_results:
            return {}
        return self.analysis_results.get('final_assessment', {})
    
    def _generate_explanation(self, prediction: str, confidence: float, features: Dict) -> str:
        """Genera spiegazione del risultato"""
        explanation_parts = []
        
        # Spiegazione della classificazione principale
        if prediction == 'AI':
            reasons = []
            lexical = features.get('lexical', {})
            style = features.get('style', {})
            
            if lexical.get('lexical_diversity', 0) > 0.7:
                reasons.append("alta diversità lessicale")
            if style.get('stylistic_consistency', 1) < 0.4:
                reasons.append("bassa consistenza stilistica")
            
            explanation_parts.append(f"Classificazione: GENERATO DA INTELLIGENZA ARTIFICIALE (confidenza: {confidence:.1%})")
            explanation_parts.append(f"Indicazioni principali: {', '.join(reasons) if reasons else 'pattern linguistici complessi'}")
            explanation_parts.append("I sistemi AI tendono a produrre testi con strutture più regolari, vocabolario vario e pattern sintattici più uniformi.")
        else:
            reasons = []
            style = features.get('style', {})
            
            if style.get('stylistic_consistency', 0) > 0.6:
                reasons.append("elevata consistenza stilistica")
            if style.get('word_repetition_ratio', 0) > 0.3:
                reasons.append("ripetizioni naturali di parole")
            
            explanation_parts.append(f"Classificazione: SCRITTO DA UN ESSERE UMANO (confidenza: {confidence:.1%})")
            explanation_parts.append(f"Indicazioni principali: {', '.join(reasons) if reasons else 'variazioni naturali nello stile'}")
            explanation_parts.append("I testi umani mostrano più variabilità, ripetizioni naturali e meno struttura regolare rispetto ai testi generati da AI.")
        
        # Analisi del sentiment
        sentiment = features.get('sentiment', {})
        if sentiment:
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            if net_sentiment > 0.1:
                sentiment_desc = "positivo"
            elif net_sentiment < -0.1:
                sentiment_desc = "negativo"
            else:
                sentiment_desc = "neutrale"
            
            explanation_parts.append(f"Analisi del sentiment: il testo presenta un tono {sentiment_desc}")
            
            dominant_emotion = sentiment.get('dominant_emotion', 0.5)
            if dominant_emotion > 0.7:
                emotion_text = "gioia"
            elif dominant_emotion > 0.4:
                emotion_text = "sorpresa"
            elif dominant_emotion > 0.2:
                emotion_text = "rabbia"
            elif dominant_emotion > 0.1:
                emotion_text = "paura"
            elif dominant_emotion > 0.05:
                emotion_text = "tristezza"
            else:
                emotion_text = "neutro"
            
            explanation_parts.append(f"Emozione dominante: {emotion_text}")
        
        # Analisi della leggibilità
        readability = features.get('readability', {})
        if readability:
            flesch_score = readability.get('flesch_reading_ease', 0)
            if flesch_score >= 90:
                readability_level = "molto facile"
            elif flesch_score >= 80:
                readability_level = "facile"
            elif flesch_score >= 70:
                readability_level = "abbastanza facile"
            elif flesch_score >= 60:
                readability_level = "standard"
            elif flesch_score >= 50:
                readability_level = "abbastanza difficile"
            elif flesch_score >= 30:
                readability_level = "difficile"
            else:
                readability_level = "molto difficile"
            
            explanation_parts.append(f"Livello di leggibilità: {readability_level} (Flesch: {flesch_score:.1f}/100)")
            
            fk_grade = readability.get('flesch_kincaid_grade', 0)
            explanation_parts.append(f"Niveau scolastico stimato: {fk_grade:.1f} classe")
        
        # Ricapitola
        explanation_parts.append("Questa analisi combina classificazione AI/umano con valutazione emotiva e leggibilità per un quadro completo del testo.")
        
        return "\n\n".join(explanation_parts)
    
    def batch_analyze(self):
        """Esegue analisi batch su una directory"""
        directory = filedialog.askdirectory(title="Seleziona directory con file di testo")
        
        if directory:
            threading.Thread(target=self._batch_analyze_worker, args=(directory,), daemon=True).start()
    
    def _batch_analyze_worker(self, directory):
        """Worker per l'analisi batch"""
        try:
            self.update_status("Analisi batch in corso...")
            self.progress.start()
            
            # Analizza tutti i file
            results = self.analyzer.batch_analyze(directory)
            
            # Aggiorna interfaccia
            self.root.after(0, lambda: self._display_batch_results(results))
            self.root.after(0, lambda: self.progress.stop())
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore durante l'analisi batch:\n{str(e)}"))
            self.root.after(0, lambda: self.progress.stop())
    
    def _display_batch_results(self, results):
        """Visualizza risultati dell'analisi batch"""
        if not results:
            messagebox.showinfo("Informazione", "Nessun file trovato nella directory selezionata")
            return
        
        # Genera report
        report = self.analyzer.generate_report(results, None)
        
        # Mostra nel tab confronti
        self.comparison_text.delete(1.0, tk.END)
        self.comparison_text.insert(1.0, report)
        self.results_notebook.select(2)  # Tab confronti
        
        # Abilita esportazione
        self._enable_export()
        
        # Salva risultati per esportazione
        self.batch_results = results
        
        self.update_status(f"Analisi batch completata: {len(results)} file analizzati")
    
    def create_samples(self):
        """Crea file di esempio per testing"""
        directory = filedialog.askdirectory(title="Seleziona directory per creare esempi")
        
        if directory:
            try:
                self.data_loader.create_sample_data(directory, 10)
                messagebox.showinfo("Successo", f"File di esempio creati in:\n{directory}")
                self.update_status("File di esempio creati")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nella creazione degli esempi:\n{str(e)}")
    
    def export_report(self):
        """Esporta il report corrente"""
        if hasattr(self, 'analysis_results') and self.analysis_results:
            # Singolo file
            file_path = filedialog.asksaveasfilename(
                title="Salva report",
                defaultextension=".txt",
                filetypes=[("File di testo", "*.txt"), ("File JSON", "*.json"), ("Tutti i file", "*.*")]
            )
            
            if file_path:
                try:
                    if file_path.endswith('.json'):
                        self.data_loader.save_analysis_result(self.analysis_results, file_path)
                    else:
                        report = self.analyzer.generate_report([self.analysis_results], None)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(report)
                    
                    messagebox.showinfo("Successo", f"Report salvato in:\n{file_path}")
                    self.update_status("Report esportato")
                    
                except Exception as e:
                    messagebox.showerror("Errore", f"Errore nell'esportazione:\n{str(e)}")
        
        elif hasattr(self, 'batch_results'):
            # Batch results
            file_path = filedialog.asksaveasfilename(
                title="Salva report batch",
                defaultextension=".txt",
                filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")]
            )
            
            if file_path:
                try:
                    report = self.analyzer.generate_report(self.batch_results, file_path)
                    messagebox.showinfo("Successo", f"Report batch salvato in:\n{file_path}")
                    self.update_status("Report batch esportato")
                except Exception as e:
                    messagebox.showerror("Errore", f"Errore nell'esportazione:\n{str(e)}")
    
    def _enable_export(self):
        """Abilita il pulsante di esportazione"""
        self.root.after(0, lambda: self._set_ui_state('normal'))
        # L'esportazione è già abilitata nel setup
    
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
    
    def update_status(self, message):
        """Aggiorna il messaggio di stato"""
        self.status_label.config(text=message)


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = TextAnalyzerGUI(root)
    
    # Centro la finestra
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
