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
        self.root.title("AI vs Human Text Analyzer - Professional Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
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
        """Configura stili per l'interfaccia"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Stili personalizzati
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('AI.TLabel', font=('Arial', 12, 'bold'), foreground='red', background='#f0f0f0')
        style.configure('Human.TLabel', font=('Arial', 12, 'bold'), foreground='green', background='#f0f0f0')
        style.configure('Confidence.TLabel', font=('Arial', 10), background='#f0f0f0')
    
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
        control_frame = ttk.LabelFrame(parent, text="Controlli", padding="10")
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
                                                     font=('Arial', 10), height=15)
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
                                                        font=('Arial', 10), height=15)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_status_panel(self, parent):
        """Configura il pannello di stato"""
        status_frame = ttk.LabelFrame(parent, text="Stato", padding="5")
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
                 font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
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
                     font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
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
                     font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
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
                     font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Spiegazione del risultato
        ttk.Label(self.results_content, text="💡 SPIEGAZIONE:", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
        
        explanation = self._generate_explanation(prediction, confidence, features)
        ttk.Label(self.results_content, text=explanation, 
                 font=('Arial', 9), justify=tk.LEFT, wraplength=800).pack(anchor=tk.W)
        
        # Abilita esportazione
        self.root.after(0, lambda: self._enable_export())
    
    def assessment_results(self):
        """Ottiene i risultati dell'assessment"""
        if not self.analysis_results or 'error' in self.analysis_results:
            return {}
        return self.analysis_results.get('final_assessment', {})
    
    def _generate_explanation(self, prediction: str, confidence: float, features: Dict) -> str:
        """Genera spiegazione del risultato"""
        if prediction == 'AI':
            reasons = []
            lexical = features.get('lexical', {})
            style = features.get('style', {})
            
            if lexical.get('lexical_diversity', 0) > 0.7:
                reasons.append("alta diversità lessicale")
            if style.get('stylistic_consistency', 1) < 0.4:
                reasons.append("bassa consistenza stilistica")
            
            explanation = f"""
Il testo è stato classificato come GENERATO DA INTELLIGENZA ARTIFICIALE 
con una confidenza del {confidence:.1%}. 
Indicazioni principali: {', '.join(reasons) if reasons else 'pattern linguistici complessi'}.
I sistemi AI tendono a produrre testi con strutture più regolari, 
vocabolario vario e pattern sintattici più uniformi.
            """
        else:
            reasons = []
            style = features.get('style', {})
            
            if style.get('stylistic_consistency', 0) > 0.6:
                reasons.append("elevata consistenza stilistica")
            if style.get('word_repetition_ratio', 0) > 0.3:
                reasons.append("ripetizioni naturali di parole")
            
            explanation = f"""
Il testo è stato classificato come SCRITTO DA UN ESSERE UMANO 
con una confidenza del {confidence:.1%}.
Indicazioni principali: {', '.join(reasons) if reasons else 'variazioni naturali nello stile'}.
I testi umani mostrano più variabilità, ripetizioni naturali e 
meno struttura regolare rispetto ai testi generati da AI.
            """
        
        return explanation.strip()
    
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
