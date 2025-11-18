# TextAnalyzer - Claude Code Reference

## 📖 INDICE
1. [Architettura](#-architettura)
2. [Struttura File](#-struttura-file)
3. [Come Usare](#-come-usare)
4. [Come Estendere](#-come-estendere)
5. [Convenzioni](#-convenzioni)
6. [Troubleshooting](#-troubleshooting)

---

## 🏗️ ARCHITETTURA

### Principi Guida
- **Pragmatico**: Semplicità e praticità sopra tutto
- **Monolitico**: Sistema integrato e coeso
- **Modulare**: Componenti separati e riutilizzabili
- **Estensibile**: Facile aggiungere nuove funzionalità

### Pattern Utilizzati
- **Facade Pattern**: `TextAnalyzer` nasconde complessità
- **Registry Pattern**: Analyzers registrati dinamicamente
- **Strategy Pattern**: Diversi algoritmi analizzatori
- **Factory Pattern**: Creazione analyzers e UI

### Dipendenze Principali
```
PySide6>=6.5.0      # GUI moderna
scikit-learn>=1.3.0  # ML e metriche
numpy>=1.24.0       # Calcoli numerici
scipy>=1.11.0       # Statistiche avanzate
nltk>=3.8           # NLP
textblob>=0.17.0    # Sentiment analysis
```

---

## 📁 STRUTTURA FILE

```
TextAnalyzer/
│
├── 📂 core/                           # ENGINE PRINCIPALE
│   ├── text_analyzer.py              # Facade principale - ENTRY POINT
│   ├── ensemble_engine.py            # Sistema ensemble 5 analyzers
│   ├── analyzer_registry.py          # Registry per analyzers
│   └── __init__.py
│
├── 📂 analyzers/                      # ANALYZERS SPECIALIZZATI
│   ├── base_analyzer.py              # Classe base per tutti gli analyzers
│   ├── lexical_analyzer.py           # TTR, Burstiness, Diversità
│   ├── syntactic_analyzer.py         # Variabilità frasi, Pattern
│   ├── semantic_analyzer.py          # Coerenza, Densità concettuale
│   ├── stylistic_analyzer.py         # Punteggiatura, Maiuscole
│   ├── ml_analyzer.py                # Entropia, Transizioni, ML proxy
│   └── __init__.py
│
├── 📂 gui/                           # INTERFACCIA GRAFICA
│   ├── main_window.py                # Finestra principale PySide6
│   ├── dialogs/                      # Dialog components
│   │   ├── results_dialog.py         # Display risultati ensemble
│   │   ├── calibration_dialog.py     # UI calibrazione
│   │   ├── help_dialog.py           # Sistema help
│   │   └── __init__.py
│   ├── widgets/                      # Custom widgets
│   │   ├── metric_card.py           # Card per metriche
│   │   ├── confidence_gauge.py      # Gauge confidenza
│   │   └── __init__.py
│   └── __init__.py
│
├── 📂 utils/                         # UTILITIES
│   ├── input_validator.py            # Validazione input robusta
│   ├── calibration_engine.py         # Auto-calibrazione soglie
│   ├── confidence_metrics.py         # Bootstrap, Bayesian, CI
│   ├── roc_analyzer.py              # ROC, AUC, PR analysis
│   ├── data_loader.py               # Loading dataset
│   └── __init__.py
│
├── 📂 data/                          # DATI E CACHE
│   ├── validation_dataset.json       # Dataset 100 testi (50 AI + 50 umani)
│   ├── templates/                    # Template per test
│   ├── cache/                        # Cache risultati
│   └── __init__.py
│
├── 📄 cli.py                          # INTERFACCIA COMMAND LINE
├── 📄 gui_launcher.py                # LAUNCHER GUI (main entry)
├── 📄 requirements.txt               # Dipendenze
├── 📄 CLAUDE.md                      # QUESTO FILE
└── 📄 README.md                      # Documentazione utente
```

---

## 🚀 COME USARE

### 1. GUI (Raccomandato)
```bash
python3 gui_launcher.py
```

**Funzionalità:**
- Interfaccia moderna PySide6
- Caricamento file o input diretto
- Analisi con 1 click
- Visualizzazione risultati dettagliata
- Calibrazione automatica

**Workflow:**
1. Scrivi testo o carica file
2. Clicca "🧠 Analisi Avanzata"
3. Vedi risultati ensemble nella dialog
4. Esporta risultati JSON

### 2. CLI
```bash
python3 cli.py --text "Il tuo testo qui" --output results.json
python3 cli.py --file input.txt --format json
python3 cli.py --batch folder/ --calibrate
```

### 3. API Python
```python
from core.text_analyzer import TextAnalyzer

# Inizializza
analyzer = TextAnalyzer()

# Analizza testo
result = analyzer.analyze("Il tuo testo qui")

# Risultati
print(result.classification)        # "Probabilmente Umano"
print(result.ai_probability)        # 0.3546
print(result.confidence)            # 0.695 (Alta)

# Per analisi avanzata
result = analyzer.analyze_advanced("Testo...")
print(result.individual_results)    # Risultati 5 analyzers
print(result.confidence_metrics)    # Bootstrap, Bayesian, etc.
```

### 4. Solo Ensemble (per testing)
```python
from core.ensemble_engine import EnsembleEngine

ensemble = EnsembleEngine()
result = ensemble.analyze("Testo...")

# Risultati strutturati
{
    'ensemble_result': {
        'classification': 'Probabilmente Umano',
        'ai_probability': 0.3546,
        'agreement_score': 0.938
    },
    'individual_results': {
        'LexicalAnalyzer': {'ai_probability': 0.700, 'confidence': 0.750},
        'SyntacticAnalyzer': {...},
        ...
    },
    'overall_confidence': 0.695
}
```

---

## 🔧 COME ESTENDERE

### Aggiungere un Nuovo Analyzer

#### 1. Crea il File
```python
# analyzers/my_custom_analyzer.py

from .base_analyzer import BaseAnalyzer

class MyCustomAnalyzer(BaseAnalyzer):
    """Analizzatore personalizzato"""

    def __init__(self):
        super().__init__()
        self.name = "MyCustomAnalyzer"

    def analyze(self, text: str) -> dict:
        """
        Analizza il testo e ritorna metriche specifiche

        Returns:
            dict con chiavi: 'metric1', 'metric2', ..., 'confidence'
        """
        # Il tuo codice qui
        metric1 = self.calculate_metric1(text)
        metric2 = self.calculate_metric2(text)

        confidence = self._calculate_confidence(metric1, metric2)

        return {
            'metric1': metric1,
            'metric2': metric2,
            'confidence': confidence
        }

    def predict(self, metrics: dict) -> tuple:
        """
        Predice AI vs Human probability

        Args:
            metrics: Dizionario con metriche dall'analyze()

        Returns:
            tuple: (ai_probability, human_probability)
        """
        # Logica di predizione
        ai_score = metrics['metric1'] * 0.7 + metrics['metric2'] * 0.3
        ai_prob = min(1.0, max(0.0, ai_score))

        return ai_prob, 1.0 - ai_prob
```

#### 2. Registra nel Registry
```python
# analyzers/__init__.py

from .my_custom_analyzer import MyCustomAnalyzer

# Aggiungi al registry
REGISTRY = {
    # ... altri analyzers ...
    'my_custom': MyCustomAnalyzer
}
```

#### 3. Usa nell'Ensemble
```python
from core.ensemble_engine import EnsembleEngine
from analyzers import my_custom_analyzer

# L'analyzer verrà caricato automaticamente
ensemble = EnsembleEngine(include=['lexical', 'syntactic', 'my_custom'])
result = ensemble.analyze("Testo...")

# Vedrai MyCustomAnalyzer nei risultati individual
```

### Aggiungere una Nuova Dialog GUI

#### 1. Crea Dialog
```python
# gui/dialogs/my_custom_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class MyCustomDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.setWindowTitle("Titolo Dialog")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Il tuo contenuto
        label = QLabel(f"Dati: {data}")
        layout.addWidget(label)

        # Pulsante chiudi
        close_btn = QPushButton("Chiudi")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
```

#### 2. Integra nella Main Window
```python
# gui/main_window.py

from .dialogs.my_custom_dialog import MyCustomDialog

def show_custom_dialog(self):
    dialog = MyCustomDialog(self, self.analysis_data)
    dialog.exec()
```

### Aggiungere Nuova Utilità

```python
# utils/my_utility.py

class MyUtility:
    """Utility personalizzata"""

    @staticmethod
    def my_function(data):
        """Funzione utility"""
        # Logica qui
        return processed_data
```

---

## 📏 CONVENZIONI

### Naming
- **Classi**: PascalCase (`MyClass`)
- **Funzioni/Metodi**: snake_case (`my_function`)
- **Variabili**: snake_case (`my_variable`)
- **Costanti**: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- **File**: snake_case (`my_file.py`)

### Struttura Classi
```python
class MyAnalyzer(BaseAnalyzer):
    """Breve descrizione in una riga.

    Descrizione più dettagliata se necessario.
    """

    def __init__(self):
        super().__init__()
        self.name = "MyAnalyzer"
        self.description = "Cosa fa questo analyzer"

    def analyze(self, text: str) -> dict:
        """Analizza il testo.

        Args:
            text: Testo da analizzare

        Returns:
            dict con metriche calcolate

        Raises:
            ValueError: se testo è vuoto
        """
        # Implementazione

    def predict(self, metrics: dict) -> tuple:
        """Predice AI vs Human probability.

        Args:
            metrics: Metriche dall'analyze()

        Returns:
            tuple: (ai_probability, human_probability)
        """
        # Implementazione
```

### Docstrings
```python
"""Breve descrizione.

Descrizione più lunga che può
occupare più righe.

Args:
    param1: Descrizione param1
    param2: Descrizione param2

Returns:
    Descrizione del valore di ritorno

Raises:
    ExceptionType: Quando si verifica questa condizione

Examples:
    >>> my_function("test")
    'result'
"""
```

### Commenti
- **Legenda**: `# NOTE:`, `# FIXME:`, `# TODO:`, `# HACK:`
- **Sezioni**: `# ----- ANALISI PRINCIPALE -----`
- **Spiegazioni**: `# Questo calcola X perché Y`

### Configurazione
```python
# utils/config.py

class Config:
    """Configurazione globale TextAnalyzer"""

    # GUI
    GUI_THEME = "modern"  # "modern", "classic"
    GUI_FONT_SIZE = 12

    # Ensemble
    DEFAULT_WEIGHTS = {
        'lexical': 0.25,
        'syntactic': 0.25,
        'semantic': 0.20,
        'stylistic': 0.15,
        'ml': 0.15
    }

    # Calibration
    CALIBRATION_DATASET_PATH = "data/validation_dataset.json"
    CALIBRATION_METHOD = "grid_search"  # "grid_search", "roc_optimization"

    # Confidence
    CONFIDENCE_BOOTSTRAP_SAMPLES = 1000
    CONFIDENCE_LEVEL = 0.95

    # Caching
    ENABLE_CACHE = True
    CACHE_DIR = "data/cache"
    CACHE_TTL = 3600  # 1 hour
```

---

## 🔍 TROUBLESHOOTING

### Problemi Comuni

#### 1. ImportError: No module named 'core'
**Causa**: Path Python non include la directory del progetto
**Soluzione**:
```bash
cd /home/martina/PycharmProjects/TextAnalyzer
python3 gui_launcher.py
```

#### 2. EnsembleAnalyzer non trova analyzers
**Causa**: Analyzer non registrato nel registry
**Soluzione**: Verificare `analyzers/__init__.py`

#### 3. GUI non si avvia (PySide6 error)
**Causa**: PySide6 non installato o versione incompatibile
**Soluzione**:
```bash
pip install PySide6>=6.5.0
```

#### 4. Calibrazione fallisce
**Causa**: Dataset mancante o corrotto
**Soluzione**:
```bash
python3 dataset_generator.py  # Rigenera dataset
```

#### 5. Confidence metrics errore (scipy mancante)
**Causa**: Dipendenze scipy non installate
**Soluzione**:
```bash
pip install scipy>=1.11.0
```

#### 6. Performance lenta su testi lunghi
**Causa**: Analisi senza caching o ottimizzazione
**Soluzione**:
```python
# Abilita caching
analyzer = TextAnalyzer(enable_cache=True)
```

### Debug Mode
```python
# Abilita logging debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Analizza con debug
analyzer = TextAnalyzer(debug=True)
result = analyzer.analyze("Testo...")
```

### Test Sistema
```bash
# Test completo
python3 -m pytest tests/ -v

# Test singolo analyzer
python3 analyzers/lexical_analyzer.py

# Test ensemble
python3 core/ensemble_engine.py

# Test GUI
python3 gui/main_window.py
```

---

## 📊 METRICHE E CALIBRAZIONE

### Metriche Calcolate

#### Ensemble Result
- `classification`: "Probabilmente Umano", "Probabilmente AI", "Indeterminato"
- `ai_probability`: 0.0000 - 1.0000 (più alto = più probabilmente AI)
- `human_probability`: 0.0000 - 1.0000 (più alto = più probabilmente umano)
- `agreement_score`: 0.0000 - 1.0000 (accordo tra analyzers)
- `weighted_confidence`: Confidenza ponderata

#### Confidence Metrics
- `prediction_certainty`: 0.0000 - 1.0000 (certezza della prediction)
- `certainty_level`: "Molto Alta", "Alta", "Media", "Bassa", "Molto Bassa"
- `recommendation`: Testo con raccomandazioni
- `uncertainty_breakdown`: Breakdown incertezza

#### Individual Analyzers
- Ogni analyzer ritorna metriche specifiche + `confidence`
- Confidence = 0.0 - 1.0 (basata su robustezza metriche)

### Calibrazione

#### Automatico
```python
analyzer = TextAnalyzer(auto_calibrate=True)
# Calibra automaticamente al primo avvio (~30 sec)
```

#### Manuale
```python
from utils.calibration_engine import CalibrationEngine

calibrator = CalibrationEngine()
result = calibrator.calibrate(dataset_path="data/my_dataset.json")
# Salva parametri calibrati in config
```

#### Interpretazione Risultati
- **ROC AUC > 0.9**: Eccellente
- **ROC AUC 0.8-0.9**: Buono
- **ROC AUC 0.7-0.8**: Discreto
- **F1-Score > 0.8**: Ottimo
- **Confidence > 0.7**: Alta certezza

---

## 🎨 PERSONALIZZAZIONE

### Theme GUI
```python
# gui/themes/modern_dark.py

DARK_THEME = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ffffff;
}
QPushButton {
    background-color: #3b3b3b;
    border: 1px solid #555;
}
"""
```

### Pesi Ensemble
```python
# Personalizza pesi analyzers
custom_weights = {
    'lexical': 0.30,    # Più peso al lessico
    'syntactic': 0.30,
    'semantic': 0.15,
    'stylistic': 0.15,
    'ml': 0.10
}

ensemble = EnsembleEngine(weights=custom_weights)
```

---

## 📚 RISORSE AGGIUNTIVE

### Paper di Riferimento
- "Detecting AI-Generated Text" (2023)
- "Stylometric Analysis for Authorship Attribution"
- "Ensemble Methods in Text Classification"

### Link Utili
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [NLTK Book](https://www.nltk.org/book/)

---

## 🤝 CONTRIBUTING

Per contribuire al progetto:

1. **Fork** il repository
2. Crea **branch** per feature (`git checkout -b feature/amazing-feature`)
3. **Commit** con messaggi chiari
4. **Push** al branch
5. Apri **Pull Request**

### Code Style
- Formatta con `black` e `isort`
- Max line length: 88 caratteri
- Docstrings obbligatori per funzioni pubbliche
- Test per nuove feature

---

## 📄 LICENSE

Progetto per ricerca accademica e dimostrazione.
Vedi LICENSE per dettagli.

---

## 👨‍💻 AUTHOR

**TextAnalyzer System**
- Version: 3.0 Professional
- Python: 3.9+
- GUI: PySide6
- ML: scikit-learn

---

**🎯 REMEMBER**: Questo file è la fonte di verità per il progetto. Mantieni aggiornato!
