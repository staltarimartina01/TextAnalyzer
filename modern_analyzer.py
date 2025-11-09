# -*- coding: utf-8 -*-
"""
TextAnalyzer Modern UI con PySide6
Interfaccia moderna e professionale per TextAnalyzer
Include: Sentiment Analysis, Readability Metrics, Varianza Frasi, Help System
"""

import sys
import os
import math
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

# PySide6 imports
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Aggiungi il path del progetto per importare i moduli esistenti
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import TextAnalyzer
from features.feature_extractor import FeatureExtractor

class MetricInfoDialog(QDialog):
    """Finestra moderna per mostrare informazioni sulle metriche"""
    
    def __init__(self, parent: QWidget, title: str, explanation: str):
        super().__init__(parent)
        self.setWindowTitle(f"ℹ️ {title}")
        self.setFixedSize(600, 400)
        self.setModal(True)
        
        # Style moderno
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border: 2px solid #2e86c1;
                border-radius: 8px;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #2e86c1;
                margin: 10px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                background-color: white;
                color: #000000;
                font-size: 11px;
                selection-background-color: #2e86c1;
            }
            QPushButton {
                background-color: #2e86c1;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1f5f99;
            }
        """)
        
        self._setup_ui(title, explanation)
        
    def _setup_ui(self, title: str, explanation: str):
        """Configura l'interfaccia della finestra di aiuto"""
        layout = QVBoxLayout(self)
        
        # Titolo
        title_label = QLabel(title)
        title_label.setObjectName("title")
        layout.addWidget(title_label)
        
        # Scroll area per il testo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        text_widget = QTextEdit()
        text_widget.setPlainText(explanation)
        text_widget.setReadOnly(True)
        text_widget.setMaximumHeight(280)
        scroll.setWidget(text_widget)
        
        layout.addWidget(scroll)
        
        # Pulsante chiudi
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Chiudi")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        # Centra la finestra
        self.center_window()
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

class ModernTextAnalyzer(QMainWindow):
    """Interfaccia moderna con PySide6 per TextAnalyzer"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextAnalyzer - Modern Edition")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Inizializza analizzatore
        self.analyzer = TextAnalyzer()
        self.feature_extractor = FeatureExtractor()
        
        # Variabili di stato
        self.current_file = None
        self.analysis_results = None
        
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
Testi AI spesso mostrano punteggi molto alti (molto facili da leggere)."""
            },
            'sentiment_analysis': {
                'title': 'Analisi Sentiment',
                'text': """L'Analisi Sentiment determina la polarità emotiva del testo (Positivo/Negativo/Neutro).

Il sistema utilizza un lessico di parole emotive in italiano per:
• Identificare parole positive (felicità, successo, gioia)
• Identificare parole negative (tristezza, fallimento, rabbia)
• Calcolare il sentiment netto e l'intensità emotiva

Tipi di Emozioni Rilevate:
• Gioia: felice, contento, gioioso, allegro
• Tristezza: triste, mesto, addolorato
• Rabbia: arrabbiato, furioso, irritato
• Paura: paura, terrore, panico
• Sorpresa: sorpresa, stupore, meravigliato

I testi AI spesso mostrano sentiment più neutro e costante."""
            },
            'sentence_variance': {
                'title': 'Varianza Lunghezza Frasi',
                'text': """La Varianza Lunghezza Frasi misura la diversità nella struttura delle frasi.

Interpretazione:
• Varianza Bassa: Frasi di lunghezza simile → Probabile AI
  (I modelli AI tendono a mantenere lunghezze costanti)
• Varianza Alta: Grande diversità nelle lunghezze → Probabile Umano
  (Gli esseri umani variano naturalmente la lunghezza)

Esempi:
• Varianza < 5: Molto probabile AI
• Varianza 5-15: Probabile AI
• Varianza 15-30: Indeterminato
• Varianza > 30: Probabile Umano

Questa metrica è efficace per testi di media lunghezza."""
            }
        }
        
        self.setup_ui()
        self.apply_modern_style()
    
    def setup_ui(self):
        """Configura l'interfaccia utente moderna"""
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        self.create_header(main_layout)
        
        # Tab widget
        self.create_tabs(main_layout)
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self, layout: QVBoxLayout):
        """Crea l'header con controlli"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_layout = QHBoxLayout(header_frame)
        
        # Titolo
        title_label = QLabel("TextAnalyzer - Modern Edition")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2e86c1;
                padding: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Pulsanti controllo
        self.load_btn = QPushButton("📁 Carica File")
        self.load_btn.clicked.connect(self.load_file)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        header_layout.addWidget(self.load_btn)
        
        self.analyze_btn = QPushButton("🔍 Analizza Testo")
        self.analyze_btn.clicked.connect(self.analyze_text)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        header_layout.addWidget(self.analyze_btn)
        
        self.batch_btn = QPushButton("📊 Analisi Batch")
        self.batch_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e06a00;
            }
        """)
        header_layout.addWidget(self.batch_btn)
        
        # Label file corrente
        self.file_label = QLabel("Nessun file caricato")
        self.file_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-style: italic;
                padding: 5px;
            }
        """)
        header_layout.addWidget(self.file_label)
        
        layout.addWidget(header_frame)
    
    def create_tabs(self, layout: QVBoxLayout):
        """Crea le tab per i risultati"""
        self.tabs = QTabWidget()
        
        # Tab Testo Originale
        self.create_original_text_tab()
        
        # Tab Risultati Analisi
        self.create_analysis_tab()
        
        # Tab Confronti
        self.create_comparison_tab()
        
        layout.addWidget(self.tabs)
    
    def create_original_text_tab(self):
        """Crea la tab per il testo originale"""
        text_widget = QWidget()
        layout = QVBoxLayout(text_widget)
        
        label = QLabel("📄 Testo Originale")
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #000000;")
        layout.addWidget(label)
        
        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Carica un file per visualizzare il testo...")
        self.text_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                background-color: #ffffff;
                color: #000000;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #2e86c1;
            }
        """)
        layout.addWidget(self.text_display)
        
        self.tabs.addTab(text_widget, "📄 Testo Originale")
    
    def create_analysis_tab(self):
        """Crea la tab per i risultati dell'analisi"""
        analysis_widget = QWidget()
        self.analysis_layout = QVBoxLayout(analysis_widget)
        
        # Scroll area per i risultati
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        scroll.setWidget(self.results_widget)
        
        self.analysis_layout.addWidget(scroll)
        
        self.tabs.addTab(analysis_widget, "📊 Risultati Analisi")
    
    def create_comparison_tab(self):
        """Crea la tab per i confronti"""
        comparison_widget = QWidget()
        layout = QVBoxLayout(comparison_widget)
        
        label = QLabel("🔄 Confronti tra testi")
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #000000;")
        layout.addWidget(label)
        
        self.comparison_display = QTextEdit()
        self.comparison_display.setPlaceholderText("I risultati dell'analisi batch appariranno qui...")
        self.comparison_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px;
                background-color: #ffffff;
                color: #000000;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #2e86c1;
            }
        """)
        layout.addWidget(self.comparison_display)
        
        self.tabs.addTab(comparison_widget, "🔄 Confronti")
    
    def create_status_bar(self):
        """Crea la status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto per l'analisi")
    
    def apply_modern_style(self):
        """Applica stili moderni all'interfaccia"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2e86c1;
                border-bottom: 2px solid #2e86c1;
            }
            QTabBar::tab:hover {
                background-color: #dee2e6;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2e86c1;
            }
            QLabel {
                color: #000000;
            }
            QTextEdit {
                color: #000000;
            }
        """)
    
    def calculate_sentence_variance(self, text: str) -> Dict[str, Any]:
        """Calcola la varianza della lunghezza delle frasi"""
        try:
            # Dividi in frasi (approssimazione semplificata)
            sentences = self._simple_sentence_tokenize(text)
            
            if len(sentences) < 2:
                return {
                    'error': 'Testo troppo breve per calcolo varianza',
                    'sentence_variance': 0.0,
                    'ai_likelihood': 'Indeterminato'
                }
            
            # Calcola lunghezza di ogni frase
            sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
            
            if len(sentence_lengths) < 2:
                return {
                    'error': 'Numero insufficiente di frasi valide',
                    'sentence_variance': 0.0,
                    'ai_likelihood': 'Indeterminato'
                }
            
            # Calcola varianza
            mean_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((length - mean_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
            
            # Classificazione basata sulla varianza
            if variance < 5:
                ai_likelihood = "Molto Probabile AI"
            elif variance < 15:
                ai_likelihood = "Probabile AI" 
            elif variance < 30:
                ai_likelihood = "Indeterminato"
            else:
                ai_likelihood = "Molto Probabile Umano"
            
            return {
                'sentence_variance': variance,
                'sentence_lengths': sentence_lengths,
                'avg_sentence_length': mean_length,
                'ai_likelihood': ai_likelihood,
                'total_sentences': len(sentences)
            }
            
        except Exception as e:
            return {
                'error': f'Errore nel calcolo varianza: {str(e)}',
                'sentence_variance': 0.0,
                'ai_likelihood': 'Errore'
            }
    
    def _simple_sentence_tokenize(self, text: str) -> List[str]:
        """Tokenizzazione semplificata delle frasi"""
        sentence_enders = r'[.!?]+'
        parts = re.split(sentence_enders, text)
        
        sentences = []
        for part in parts:
            part = part.strip()
            if len(part) > 10:
                sentences.append(part)
        
        return sentences
    
    def load_file(self):
        """Carica un file di testo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona file di testo",
            "",
            "File di testo (*.txt);;Tutti i file (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                self.current_file = file_path
                self.file_label.setText(f"📄 {os.path.basename(file_path)}")
                
                # Mostra il testo
                self.text_display.setPlainText(text)
                
                # Abilita analisi
                self.analyze_btn.setEnabled(True)
                
                self.status_bar.showMessage("File caricato con successo")
                
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore nel caricamento del file:\n{str(e)}")
                self.status_bar.showMessage("Errore nel caricamento file")
    
    def analyze_text(self):
        """Analizza il testo corrente"""
        if not self.current_file:
            QMessageBox.warning(self, "Attenzione", "Nessun file da analizzare")
            return
        
        try:
            # Leggi il testo
            with open(self.current_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            self.status_bar.showMessage("Analisi in corso...")
            QApplication.processEvents()
            
            # Esegui analisi completa
            result = self.analyzer.analyze_text(text, os.path.basename(self.current_file))
            self.analysis_results = result
            
            if 'error' in result:
                QMessageBox.critical(self, "Errore", f"Errore nell'analisi:\n{result['error']}")
                self.status_bar.showMessage("Errore nell'analisi")
                return
            
            # Calcola varianza frasi
            sentence_variance = self.calculate_sentence_variance(text)
            
            # Visualizza risultati
            self.display_analysis_results(result, sentence_variance)
            
            # Cambia alla tab risultati
            self.tabs.setCurrentIndex(1)
            
            self.status_bar.showMessage("Analisi completata")
            
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'analisi:\n{str(e)}")
            self.status_bar.showMessage("Errore durante l'analisi")
    
    def display_analysis_results(self, result: Dict, sentence_variance: Dict):
        """Visualizza i risultati dell'analisi in formato moderno"""
        # Pulisci risultati precedenti
        for i in reversed(range(self.results_layout.count())):
            child = self.results_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Sezione Risultato Principale
        self.create_main_result_section(result)
        
        # Sezione Statistiche Testo
        self.create_stats_section(result)
        
        # Sezione Varianza Frasi (Nuova!)
        self.create_variance_section(sentence_variance)
        
        # Sezione Sentiment
        self.create_sentiment_section(result)
        
        # Sezione Leggibilità
        self.create_readability_section(result)
        
        # Sezioni metriche esistenti
        self.create_existing_sections(result)
        
        self.results_layout.addStretch()
    
    def create_main_result_section(self, result: Dict):
        """Crea la sezione del risultato principale"""
        group = self.create_metric_group("")
        
        # Titolo centrato dentro il box
        title_label = QLabel("🧠 Risultato Principale")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 5px;
            text-align: center;
            margin: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(title_label)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #dee2e6; margin: 5px;")
        group.layout().addWidget(line)
        
        # Risultato della classificazione
        assessment = result.get('final_assessment', {})
        prediction = assessment.get('prediction', 'Sconosciuto')
        confidence = assessment.get('confidence', 0)
        
        # Mostra il risultato principale
        result_text = f"Classificazione: {prediction} (Confidenza: {confidence:.1%})"
        if prediction == 'AI':
            result_text = f"🧠 {result_text}"
        else:
            result_text = f"👤 {result_text}"
        
        result_label = QLabel(result_text)
        result_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 10px;
            text-align: center;
        """)
        result_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(result_label)
        
        self.results_layout.addWidget(group)

    def create_metric_group(self, title: str) -> QGroupBox:
        """Crea un gruppo moderno per le metriche"""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        return group
    
    def create_stats_section(self, result: Dict):
        """Crea la sezione statistiche del testo"""
        group = self.create_metric_group("")
        
        # Titolo centrato dentro il box
        title_label = QLabel("📊 Statistiche Testo")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 5px;
            text-align: center;
            margin: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(title_label)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #dee2e6; margin: 5px;")
        group.layout().addWidget(line)
        
        text_stats = result.get('text_stats', {})
        if text_stats:
            char_count = text_stats.get('char_count', 0)
            word_count = text_stats.get('word_count', 0)
            sentence_count = text_stats.get('sentence_count', 0)
            lexical_diversity = text_stats.get('lexical_diversity', 0)
            
            stats_text = f"""
            • Caratteri: {char_count:,}
            • Parole: {word_count:,}
            • Frasi: {sentence_count:,}
            • Diversità lessicale: {lexical_diversity:.3f}
            """
            
            stats_label = QLabel(stats_text.strip())
            stats_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(stats_label)
        
        self.results_layout.addWidget(group)
    
    def create_variance_section(self, sentence_variance: Dict):
        """Crea la sezione varianza frasi (nuova funzionalità)"""
        group = self.create_metric_group("")
        
        # Titolo centrato dentro il box
        title_label = QLabel("📈 Varianza Lunghezza Frasi")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 5px;
            text-align: center;
            margin: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(title_label)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #dee2e6; margin: 5px;")
        group.layout().addWidget(line)
        
        # Pulsante help
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        
        help_btn = QPushButton("?")
        help_btn.setFixedSize(30, 30)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        help_btn.clicked.connect(lambda: self.show_metric_info('sentence_variance'))
        help_layout.addWidget(help_btn)
        group.layout().addLayout(help_layout)
        
        if 'error' not in sentence_variance:
            variance_value = sentence_variance.get('sentence_variance', 0)
            ai_likelihood = sentence_variance.get('ai_likelihood', 'N/A')
            
            variance_text = f"""
            • Varianza: {variance_value:.2f}
            • Classificazione: {ai_likelihood}
            • Frasi analizzate: {sentence_variance.get('total_sentences', 0)}
            """
            
            variance_label = QLabel(variance_text.strip())
            variance_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(variance_label)
        else:
            error_label = QLabel(f"Errore: {sentence_variance.get('error', 'Sconosciuto')}")
            error_label.setStyleSheet("font-size: 12px; color: #dc3545; padding: 5px 10px;")
            group.layout().addWidget(error_label)
        
        self.results_layout.addWidget(group)
    
    def create_sentiment_section(self, result: Dict):
        """Crea la sezione sentiment analysis"""
        group = self.create_metric_group("")
        
        # Titolo centrato dentro il box
        title_label = QLabel("😊 Analisi Sentiment")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 5px;
            text-align: center;
            margin: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(title_label)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #dee2e6; margin: 5px;")
        group.layout().addWidget(line)
        
        # Pulsante help
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        
        help_btn = QPushButton("?")
        help_btn.setFixedSize(30, 30)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        help_btn.clicked.connect(lambda: self.show_metric_info('sentiment_analysis'))
        help_layout.addWidget(help_btn)
        group.layout().addLayout(help_layout)
        
        features = result.get('features', {})
        sentiment = features.get('sentiment', {})
        
        if sentiment:
            net_sentiment = sentiment.get('net_sentiment_score', 0)
            if net_sentiment > 0.1:
                sentiment_label = "POSITIVO 🟢"
            elif net_sentiment < -0.1:
                sentiment_label = "NEGATIVO 🔴"
            else:
                sentiment_label = "NEUTRALE ⚪"
            
            sentiment_text = f"""
            • Sentiment generale: {sentiment_label}
            • Emozione dominante: {self._get_emotion_text(sentiment.get('dominant_emotion', 0.5))}
            • Intensità emotiva: {sentiment.get('sentiment_intensity', 0):.1%}
            • Gioia: {sentiment.get('joy_indicators_ratio', 0):.1%}
            • Tristezza: {sentiment.get('sadness_indicators_ratio', 0):.1%}
            • Rabbia: {sentiment.get('anger_indicators_ratio', 0):.1%}
            """
            
            sentiment_label_widget = QLabel(sentiment_text.strip())
            sentiment_label_widget.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(sentiment_label_widget)
        
        self.results_layout.addWidget(group)
    
    def create_readability_section(self, result: Dict):
        """Crea la sezione indice di leggibilità"""
        group = self.create_metric_group("")
        
        # Titolo centrato dentro il box
        title_label = QLabel("📖 Indice di Leggibilità")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2e86c1;
            padding: 5px;
            text-align: center;
            margin: 5px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        group.layout().addWidget(title_label)
        
        # Linea separatrice
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #dee2e6; margin: 5px;")
        group.layout().addWidget(line)
        
        # Pulsante help
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        
        help_btn = QPushButton("?")
        help_btn.setFixedSize(30, 30)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        help_btn.clicked.connect(lambda: self.show_metric_info('flesch_reading_ease'))
        help_layout.addWidget(help_btn)
        group.layout().addLayout(help_layout)
        
        features = result.get('features', {})
        readability = features.get('readability', {})
        
        if readability:
            flesch_score = readability.get('flesch_reading_ease', 0)
            fk_grade = readability.get('flesch_kincaid_grade', 0)
            gunning_fog = readability.get('gunning_fog_index', 0)
            smog_index = readability.get('smog_index', 0)
            
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
            
            readability_text = f"""
            • Livello: {readability_level} ({flesch_score:.1f}/100)
            • Flesch-Kincaid Grade: {fk_grade:.1f} (scuola)
            • Gunning Fog Index: {gunning_fog:.1f}
            • SMOG Index: {smog_index:.1f}
            • Parole complesse: {readability.get('complex_words_ratio', 0):.1%}
            """
            
            readability_label = QLabel(readability_text.strip())
            readability_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(readability_label)
        
        self.results_layout.addWidget(group)
    
    def create_existing_sections(self, result: Dict):
        """Crea le sezioni delle metriche esistenti"""
        features = result.get('features', {})
        
        # Sezione Lessicale
        lexical = features.get('lexical', {})
        if lexical:
            group = self.create_metric_group("")
            
            # Titolo centrato dentro il box
            title_label = QLabel("📚 Analisi Lessicale")
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2e86c1;
                padding: 5px;
                text-align: center;
                margin: 5px;
            """)
            title_label.setAlignment(Qt.AlignCenter)
            group.layout().addWidget(title_label)
            
            # Linea separatrice
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #dee2e6; margin: 5px;")
            group.layout().addWidget(line)
            
            lexical_text = f"""
            • Rapporto tipi/token: {lexical.get('type_token_ratio', 0):.3f}
            • Diversità lessicale: {lexical.get('lexical_diversity', 0):.3f}
            • Parole lunghe (>6): {lexical.get('long_words_ratio', 0):.1%}
            """
            
            lexical_label = QLabel(lexical_text.strip())
            lexical_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(lexical_label)
            self.results_layout.addWidget(group)
        
        # Sezione Stilistica
        style = features.get('style', {})
        if style:
            group = self.create_metric_group("")
            
            # Titolo centrato dentro il box
            title_label = QLabel("🎨 Analisi Stilistica")
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2e86c1;
                padding: 5px;
                text-align: center;
                margin: 5px;
            """)
            title_label.setAlignment(Qt.AlignCenter)
            group.layout().addWidget(title_label)
            
            # Linea separatrice
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #dee2e6; margin: 5px;")
            group.layout().addWidget(line)
            
            style_text = f"""
            • Consistenza stilistica: {style.get('stylistic_consistency', 0):.3f}
            • Ripetizione parole: {style.get('word_repetition_ratio', 0):.1%}
            """
            
            style_label = QLabel(style_text.strip())
            style_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(style_label)
            self.results_layout.addWidget(group)
        
        # Sezione Sintattica
        syntactic = features.get('syntactic', {})
        if syntactic:
            group = self.create_metric_group("")
            
            # Titolo centrato dentro il box
            title_label = QLabel("📝 Analisi Sintattica")
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #2e86c1;
                padding: 5px;
                text-align: center;
                margin: 5px;
            """)
            title_label.setAlignment(Qt.AlignCenter)
            group.layout().addWidget(title_label)
            
            # Linea separatrice
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #dee2e6; margin: 5px;")
            group.layout().addWidget(line)
            
            syntactic_text = f"""
            • Lunghezza media frase: {syntactic.get('avg_sentence_length', 0):.1f} parole
            • Frasi complesse: {syntactic.get('complex_sentences_ratio', 0):.1%}
            • Densità punteggiatura: {syntactic.get('punctuation_density', 0):.1%}
            """
            
            syntactic_label = QLabel(syntactic_text.strip())
            syntactic_label.setStyleSheet("font-size: 12px; color: #000000; padding: 5px 10px;")
            group.layout().addWidget(syntactic_label)
            self.results_layout.addWidget(group)
    
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
    
    def show_metric_info(self, metric_key: str):
        """Mostra informazioni dettagliate su una metrica"""
        if metric_key in self.metric_explanations:
            info = self.metric_explanations[metric_key]
            dialog = MetricInfoDialog(self, info['title'], info['text'])
            dialog.exec()
        else:
            QMessageBox.information(self, "Info", f"Informazioni non disponibili per: {metric_key}")

def main():
    """Funzione principale"""
    app = QApplication(sys.argv)
    
    # Imposta stile dell'applicazione
    app.setStyle('Fusion')
    
    # Crea e mostra la finestra
    window = ModernTextAnalyzer()
    window.show()
    
    # Esegui l'applicazione
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
