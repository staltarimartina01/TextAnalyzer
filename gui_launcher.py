#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextAnalyzer GUI Launcher
Entry point per avviare l'interfaccia grafica
"""

import sys
import os
sys.path.insert(0, '/home/martina/PycharmProjects/TextAnalyzer')

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

from gui.main_window import TextAnalyzerGUI


def check_dependencies():
    """Verifica che tutte le dipendenze siano installate"""
    missing = []

    # Check PySide6
    try:
        import PySide6
    except ImportError:
        missing.append("PySide6")

    # Check core dependencies
    try:
        import numpy
        import scipy
        from sklearn import metrics
    except ImportError as e:
        missing.append(str(e).split("'")[1] if "'" in str(e) else "scipy/sklearn")

    # Check analyzers
    try:
        from analyzers import list_available_analyzers
        analyzers = list_available_analyzers()
        if len(analyzers) < 5:
            missing.append(f"Missing analyzers (found {len(analyzers)}, need 5)")
    except Exception as e:
        missing.append(f"Analyzers error: {str(e)}")

    return missing


def setup_application(app: QApplication):
    """Configura l'applicazione Qt"""
    # Application info
    app.setApplicationName("TextAnalyzer")
    app.setApplicationVersion("3.0")
    app.setOrganizationName("TextAnalyzer Project")
    app.setOrganizationDomain("textanalyzer.local")

    # High DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Load styles
    style = """
        QApplication {
            background-color: #f5f5f5;
        }
    """
    app.setStyleSheet(style)


def show_startup_message():
    """Mostra messaggio di avvio"""
    return QMessageBox.information(
        None,
        "TextAnalyzer v3.0",
        """🧠 Benvenuto in TextAnalyzer!

Ensemble AI Detection System
• 5 Analyzers Specializzati
• Confidence Metrics
• Calibrated System

Inserisci un testo e clicca '🧠 Analisi Avanzata' per iniziare!

Per supporto, vedi CLAUDE.md"""
    )


def main():
    """Main entry point per GUI"""
    # Create QApplication
    app = QApplication(sys.argv)

    # Setup
    setup_application(app)

    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()

    if missing:
        error_msg = "❌ Missing dependencies:\n\n" + "\n".join(f"• {m}" for m in missing)
        error_msg += "\n\nInstall with:\npip install PySide6 numpy scipy scikit-learn"
        QMessageBox.critical(None, "Dependencies Error", error_msg)
        return 1

    print("✅ All dependencies OK")

    # Show startup message
    try:
        show_startup_message()
    except:
        pass  # Ignore if dialog fails

    # Create and show window
    print("🖥️ Starting GUI...")
    window = TextAnalyzerGUI()
    window.show()

    print("✅ TextAnalyzer GUI started!")
    print("   Window size: 1400x900")
    print("   Analyzers: 5")
    print("\n💡 Tips:")
    print("   • Use '🧠 Analisi Avanzata' per analysis completa")
    print("   • Export results with '💾 Esporta Risultati'")
    print("   • See CLAUDE.md for documentation")

    # Run event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
