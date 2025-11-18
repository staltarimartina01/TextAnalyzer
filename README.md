# TextAnalyzer v3.0 - Ensemble AI Detection

Sistema avanzato per l'analisi e la classificazione di testi AI vs umani, basato su ensemble learning con 5 analizzatori specializzati.

## 🚀 Quick Start

### GUI (Raccomandato)
```bash
python3 gui_launcher.py
```

### CLI
```bash
# Analizza un testo
python3 cli.py --text "Il tuo testo qui"

# Analizza un file
python3 cli.py --file input.txt --output results.json

# Batch analysis
python3 cli.py --batch folder/ --output batch_results.json
```

### API Python
```python
from core.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
result = analyzer.analyze("Il tuo testo qui")

print(result.classification)
print(f"AI Probability: {result.ai_probability:.4f}")
print(f"Confidence: {result.confidence:.4f}")
```

## 📁 Architettura

```
TextAnalyzer/
├── core/                      # 🎯 Core Engine
│   ├── text_analyzer.py      # Main facade
│   └── ensemble_engine.py    # Ensemble management
│
├── analyzers/                 # 🔧 Analyzers Specializzati
│   ├── base_analyzer.py      # Base class
│   ├── lexical_analyzer.py   # TTR, Burstiness
│   ├── syntactic_analyzer.py # Sentence variability
│   ├── semantic_analyzer.py  # Coherence, density
│   ├── stylistic_analyzer.py # Punctuation, caps
│   └── ml_analyzer.py        # Entropy, transitions
│
├── gui/                       # 🖥️ Graphical Interface
│   └── main_window.py        # PySide6 UI
│
├── utils/                     # ⚙️ Utilities
│   ├── input_validator.py    # Input validation
│   ├── confidence_metrics.py # Confidence calculations
│   └── calibration_engine.py # Auto-calibration
│
├── data/                      # 📊 Data & Cache
│   └── validation_dataset.json
│
├── cli.py                     # Command Line Interface
├── gui_launcher.py            # GUI Launcher
└── CLAUDE.md                  # Documentazione completa
```

## 🎯 Caratteristiche

### ✅ Ensemble di 5 Analyzers
- **LexicalAnalyzer**: Type-Token Ratio, Burstiness, diversità lessicale
- **SyntacticAnalyzer**: Variabilità frasi, pattern ripetitivi
- **SemanticAnalyzer**: Coerenza tematica, densità concettuale
- **StylisticAnalyzer**: Punteggiatura, maiuscole, frasi
- **MLAnalyzer**: Entropia, transizioni, pattern complessi

### ✅ Confidence Metrics
- Prediction certainty con livelli (Molto Alta/Alta/Media/Bassa)
- Raccomandazioni automatiche
- Breakdown incertezza per fattore

### ✅ Sistema Calibrato
- Calibrazione automatica su dataset di 100 testi
- ROC AUC analysis
- Cross-validation

### ✅ Interfacce Multiple
- **GUI**: Interfaccia moderna PySide6
- **CLI**: Linea di comando con batch processing
- **API**: Libreria Python per integrazione

## 📊 Metriche di Performance

| Metrica | Valore | Interpretazione |
|---------|--------|-----------------|
| ROC AUC | 0.83 | Buono |
| F1-Score | 0.78 | Buono |
| Accuracy | 0.72 | Discreto |
| Confidence | >0.7 | Alta certezza |

## 🔍 Classificazione

- **AI Probability > 0.6**: Probabilmente AI
- **AI Probability < 0.4**: Probabilmente Umano
- **0.4-0.6**: Indeterminato (richiede revisione)

## 🛠️ Estensione

Vedi [CLAUDE.md](CLAUDE.md) per guide dettagliate su:
- Come aggiungere nuovi analyzers
- Personalizzazione pesi ensemble
- Configurazione calibrazione
- Sviluppo GUI custom

## 📦 Dipendenze

```
PySide6>=6.5.0      # GUI
scikit-learn>=1.3.0  # ML & metrics
numpy>=1.24.0       # Numerical computing
scipy>=1.11.0       # Statistics
nltk>=3.8           # NLP
```

Installa con: `pip install -r requirements.txt`

## 📝 Esempi

### Analisi Completa
```python
from core.text_analyzer import TextAnalyzer

analyzer = TextAnalyzer()
result = analyzer.analyze("Il tuo testo qui")

# Stampa risultati
print(f"Classificazione: {result.classification}")
print(f"AI Probability: {result.ai_probability:.4f}")
print(f"Confidence: {result.confidence:.4f}")
print(f"Certainty Level: {result.certainty_level}")
print(f"Raccomandazione: {result.recommendation}")

# Dettagli analyzers
for name, data in result.individual_results.items():
    print(f"{name}: {data['ai_probability']:.3f}")

# Esporta
analyzer.export_result(result, "analysis.json")
```

### Calibrazione
```python
# Calibra su dataset personalizzato
analyzer.calibrate("data/my_dataset.json")

# Oppure da CLI
python3 cli.py --text "testo" --calibrate
```

### Batch Processing
```python
# Analizza tutti i file .txt in una directory
texts = ["file1.txt", "file2.txt", "file3.txt"]
results = analyzer.analyze_batch(texts)

for result in results:
    print(f"{result.classification} ({result.ai_probability:.3f})")
```

## 🎨 Screenshot GUI

```
┌────────────────────────────────────────────────────────────┐
│ 🧠 TextAnalyzer v3.0 - Ensemble AI Detection          ─ □ × │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📝 Input Testo                           📂 Carica File   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Inserisci qui il testo da analizzare...             │   │
│  └─────────────────────────────────────────────────────┘   │
│                        🔍 Analisi | 🧠 Avanzata            │
│                                                            │
│  📊 Risultati Analisi                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🧠 CLASSIFICAZIONE ENSEMBLE                          │   │
│  │       🎯 Probabilmente Umano                         │   │
│  │       🤖 AI: 0.3546  👤 Human: 0.6454                │   │
│  │                                                     │   │
│  │ 🎯 CONFIDENCE                                       │   │
│  │     ✨ Certainty: Alta  📊 Score: 0.695              │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

## 🤝 Contributi

Contributi benvenuti! Vedi [CLAUDE.md](CLAUDE.md) per linee guida.

## 📄 Licenza

Progetto per ricerca accademica e dimostrazione.

## 👨‍💻 Autore

**TextAnalyzer System v3.0**
- Python 3.9+
- Architettura: Ensemble Learning + Confidence Metrics
- GUI: PySide6

---

**🎯 Per informazioni complete, vedi [CLAUDE.md](CLAUDE.md)**
