#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextAnalyzer GUI - Main Window
Interfaccia grafica moderna PySide6 per TextAnalyzer
"""

import sys
sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QHBoxLayout,
                               QWidget, QTextEdit, QPushButton, QLabel, QFileDialog,
                               QMessageBox, QGroupBox, QScrollArea, QProgressBar,
                               QStatusBar, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap

from datetime import datetime
from typing import Dict, Any

from core.text_analyzer import TextAnalyzer, AnalysisResult


class TextAnalyzerGUI(QMainWindow):
    """Interfaccia grafica principale per TextAnalyzer"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextAnalyzer v3.0 - Ensemble AI Detection")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Core components
        self.analyzer = TextAnalyzer(auto_calibrate=False, debug=False)
        self.current_file = None
        self.analysis_result: AnalysisResult = None

        # Setup UI
        self._setup_ui()
        self._setup_styles()
        self._setup_status_bar()

        # Show welcome message
        QTimer.singleShot(1000, self._show_welcome_message)

    def _setup_ui(self):
        """Configura l'interfaccia utente"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)

        # Input section
        input_group = self._create_input_section()
        main_layout.addWidget(input_group, 2)

        # Results section
        results_group = self._create_results_section()
        main_layout.addWidget(results_group, 3)

        # Footer
        footer_layout = self._create_footer()
        main_layout.addLayout(footer_layout)

    def _create_header(self):
        """Crea sezione header"""
        layout = QHBoxLayout()

        # Title
        title = QLabel("🧠 TextAnalyzer - Ensemble AI Detection")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2e86c1;")
        layout.addWidget(title)

        layout.addStretch()

        # Stats
        self.stats_label = QLabel("Ready")
        self.stats_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.stats_label)

        return layout

    def _create_input_section(self):
        """Crea sezione input testo"""
        group = QGroupBox("📝 Input Testo")
        group.setStyleSheet(self._get_group_style("#2e86c1"))
        layout = QVBoxLayout(group)

        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Inserisci qui il testo da analizzare...\n\n"
            "Oppure carica un file usando il pulsante '📂 Carica File'"
        )
        layout.addWidget(self.text_input, 1)

        # Button layout
        button_layout = QHBoxLayout()

        # File buttons
        self.load_btn = QPushButton("📂 Carica File")
        self.load_btn.clicked.connect(self._load_file)
        button_layout.addWidget(self.load_btn)

        self.clear_btn = QPushButton("🗑️ Pulisci")
        self.clear_btn.clicked.connect(self._clear_text)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()

        # Analyze buttons
        self.analyze_btn = QPushButton("🔍 Analisi Standard")
        self.analyze_btn.clicked.connect(self._analyze_text)
        self.analyze_btn.setEnabled(False)
        button_layout.addWidget(self.analyze_btn)

        self.advanced_btn = QPushButton("🧠 Analisi Avanzata")
        self.advanced_btn.clicked.connect(self._analyze_advanced)
        self.analyze_btn.setEnabled(False)
        button_layout.addWidget(self.advanced_btn)

        layout.addLayout(button_layout)

        # Connect text change
        self.text_input.textChanged.connect(self._on_text_changed)

        return group

    def _create_results_section(self):
        """Crea sezione risultati"""
        group = QGroupBox("📊 Risultati Analisi")
        group.setStyleSheet(self._get_group_style("#28a745"))
        layout = QVBoxLayout(group)

        # Scroll area for results
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Results widget
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)

        # Placeholder
        self._show_results_placeholder()

        scroll.setWidget(self.results_widget)
        layout.addWidget(scroll)

        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self.export_btn = QPushButton("💾 Esporta Risultati")
        self.export_btn.clicked.connect(self._export_results)
        self.export_btn.setEnabled(False)
        export_layout.addWidget(self.export_btn)

        layout.addLayout(export_layout)

        return group

    def _create_footer(self):
        """Crea sezione footer"""
        layout = QHBoxLayout()

        # Info
        info_label = QLabel("Ensemble Text Analyzer v3.0 | 5 Analyzers | Calibrated System")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(info_label)

        layout.addStretch()

        # Help button
        help_btn = QPushButton("❓ Aiuto")
        help_btn.clicked.connect(self._show_help)
        layout.addWidget(help_btn)

        return layout

    def _setup_status_bar(self):
        """Configura status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Inserisci un testo per iniziare")

        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _setup_styles(self):
        """Configura stili CSS"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin: 5px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
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
                background-color: #ccc;
                color: #666;
            }
            QPushButton#advanced {
                background-color: #6f42c1;
            }
            QPushButton#advanced:hover {
                background-color: #5a32a3;
            }
        """)

    def _get_group_style(self, color: str) -> str:
        """Genera stile per group box"""
        return f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                color: {color};
                border: 2px solid {color};
                border-radius: 8px;
                margin: 5px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }}
        """

    def _show_results_placeholder(self):
        """Mostra placeholder nei risultati"""
        # Clear previous results
        for i in reversed(range(self.results_layout.count())):
            child = self.results_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        placeholder = QLabel("📊 I risultati dell'analisi appariranno qui")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("""
            color: #999;
            font-size: 16px;
            padding: 40px;
            background-color: white;
            border: 2px dashed #ddd;
            border-radius: 8px;
        """)
        self.results_layout.addWidget(placeholder)
        self.results_layout.addStretch()

    def _on_text_changed(self):
        """Gestisce cambio testo"""
        has_text = len(self.text_input.toPlainText().strip()) > 0
        self.analyze_btn.setEnabled(has_text)
        self.advanced_btn.setEnabled(has_text)

    def _load_file(self):
        """Carica file di testo"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File di Testo",
            "",
            "File di Testo (*.txt);;Tutti i File (*)"
        )

        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.setPlainText(content)
                self.current_file = filepath
                self.status_bar.showMessage(f"File caricato: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile caricare il file:\n{str(e)}")

    def _clear_text(self):
        """Pulisce il testo"""
        self.text_input.clear()
        self.current_file = None
        self.analysis_result = None
        self._show_results_placeholder()
        self.export_btn.setEnabled(False)
        self.status_bar.showMessage("Testo pulito")

    def _analyze_text(self):
        """Esegue analisi standard"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Attenzione", "Inserisci un testo da analizzare")
            return

        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
            self.status_bar.showMessage("Analisi in corso...")
            QApplication.processEvents()

            # Analyze
            result = self.analyzer.analyze(text)
            self.analysis_result = result

            # Display
            self._display_results(result)

            self.status_bar.showMessage(f"Analisi completata in {result.processing_time_ms:.0f}ms")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'analisi:\n{str(e)}")
            self.status_bar.showMessage("Errore nell'analisi")
        finally:
            self.progress_bar.setVisible(False)

    def _analyze_advanced(self):
        """Esegue analisi avanzata (stessa di standard per ora)"""
        self._analyze_text()

    def _display_results(self, result: AnalysisResult):
        """Visualizza risultati dell'analisi"""
        # Clear previous results
        for i in reversed(range(self.results_layout.count())):
            child = self.results_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        # Classification card
        self._create_classification_card(result)

        # Confidence card
        self._create_confidence_card(result)

        # Individual analyzers card
        self._create_analyzers_card(result)

        # System info card
        self._create_system_card(result)

        self.results_layout.addStretch()

        # Enable export
        self.export_btn.setEnabled(True)

    def _create_classification_card(self, result: AnalysisResult):
        """Crea card classificazione"""
        card = QGroupBox("🧠 CLASSIFICAZIONE ENSEMBLE")
        card.setStyleSheet(self._get_group_style("#2e86c1"))

        layout = QVBoxLayout(card)

        # Classification
        class_label = QLabel(f"🎯 {result.classification}")
        class_label.setFont(QFont("Arial", 16, QFont.Bold))
        class_label.setAlignment(Qt.AlignCenter)
        class_label.setStyleSheet("color: #2e86c1; padding: 10px;")
        layout.addWidget(class_label)

        # Probabilities
        prob_layout = QGridLayout()
        prob_layout.addWidget(QLabel("🤖 AI Probability:"), 0, 0)
        prob_layout.addWidget(QLabel(f"{result.ai_probability:.4f}"), 0, 1)
        prob_layout.addWidget(QLabel("👤 Human Probability:"), 1, 0)
        prob_layout.addWidget(QLabel(f"{result.human_probability:.4f}"), 1, 1)

        for i in range(2):
            prob_layout.itemAt(i*2).widget().setStyleSheet("font-weight: bold;")
            prob_layout.itemAt(i*2+1).widget().setStyleSheet("font-size: 14px; color: #2e86c1;")

        layout.addLayout(prob_layout)

        self.results_layout.addWidget(card)

    def _create_confidence_card(self, result: AnalysisResult):
        """Crea card confidenza"""
        card = QGroupBox("🎯 CONFIDENCE METRICS")
        card.setStyleSheet(self._get_group_style("#28a745"))

        layout = QVBoxLayout(card)

        certainty_label = QLabel(f"✨ Certainty: {result.certainty_level}")
        certainty_label.setFont(QFont("Arial", 14, QFont.Bold))
        certainty_label.setStyleSheet("color: #28a745;")
        layout.addWidget(certainty_label)

        confidence_label = QLabel(f"📊 Confidence Score: {result.confidence:.4f}")
        confidence_label.setStyleSheet("font-size: 13px;")
        layout.addWidget(confidence_label)

        recommendation_label = QLabel(f"💡 {result.recommendation}")
        recommendation_label.setWordWrap(True)
        recommendation_label.setStyleSheet("""
            font-size: 12px;
            color: #666;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 4px;
        """)
        layout.addWidget(recommendation_label)

        self.results_layout.addWidget(card)

    def _create_analyzers_card(self, result: AnalysisResult):
        """Crea card analyzers individuali"""
        card = QGroupBox("👥 ANALIZZATORI INDIVIDUALI")
        card.setStyleSheet(self._get_group_style("#6f42c1"))

        layout = QVBoxLayout(card)

        for name, data in result.individual_results.items():
            if isinstance(data, dict) and 'ai_probability' in data:
                ai_prob = data['ai_probability']
                conf = data.get('confidence', 0)
                analyzer_label = QLabel(f"🔹 {name}: AI={ai_prob:.3f}, Conf={conf:.3f}")
                analyzer_label.setStyleSheet("font-size: 12px; padding: 2px;")
                layout.addWidget(analyzer_label)

        self.results_layout.addWidget(card)

    def _create_system_card(self, result: AnalysisResult):
        """Crea card informazioni sistema"""
        card = QGroupBox("⚙️ SYSTEM INFO")
        card.setStyleSheet(self._get_group_style("#607d8b"))

        layout = QVBoxLayout(card)

        time_label = QLabel(f"⏱️ Processing Time: {result.processing_time_ms:.2f}ms")
        time_label.setStyleSheet("font-size: 12px;")
        layout.addWidget(time_label)

        timestamp_label = QLabel(f"🕐 Timestamp: {result.timestamp[:19]}")
        timestamp_label.setStyleSheet("font-size: 11px; color: #666;")
        layout.addWidget(timestamp_label)

        self.results_layout.addWidget(card)

    def _export_results(self):
        """Esporta risultati"""
        if not self.analysis_result:
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Risultati",
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )

        if filepath:
            try:
                self.analyzer.export_result(self.analysis_result, filepath)
                QMessageBox.information(self, "Successo", f"Risultati salvati in:\n{filepath}")
                self.status_bar.showMessage(f"Risultati esportati: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore nell'esportazione:\n{str(e)}")

    def _show_welcome_message(self):
        """Mostra messaggio di benvenuto"""
        self.status_bar.showMessage(
            "Welcome! Inserisci un testo e clicca '🧠 Analisi Avanzata' per iniziare"
        )

    def _show_help(self):
        """Mostra dialog di aiuto"""
        QMessageBox.information(
            self,
            "Aiuto - TextAnalyzer v3.0",
            """🧠 TextAnalyzer - Ensemble AI Detection

COMANDI:
• 🔍 Analisi Standard: Analisi base con ensemble
• 🧠 Analisi Avanzata: Analisi completa con confidence metrics

ANalyzers UTILIZZATI:
1. LexicalAnalyzer - Metriche lessicali (TTR, Burstiness)
2. SyntacticAnalyzer - Variabilità frasi, pattern
3. SemanticAnalyzer - Coerenza, densità concettuale
4. StylisticAnalyzer - Punteggiatura, maiuscole
5. MLAnalyzer - Entropia, transizioni, ML proxy

CLASSIFICAZIONE:
• AI Probability > 0.6: Probabilmente AI
• AI Probability < 0.4: Probabilmente Umano
• 0.4-0.6: Indeterminato

Per calibrazione automatica, usa il comando:
python3 core/text_analyzer.py --calibrate

Per ulteriori info, vedi CLAUDE.md"""
        )


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    # Set application info
    app.setApplicationName("TextAnalyzer")
    app.setApplicationVersion("3.0")
    app.setOrganizationName("TextAnalyzer Project")

    # Create and show window
    window = TextAnalyzerGUI()
    window.show()

    # Run
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
