# Guida Rapida: Setup Ambiente Virtuale
# AI vs Human Text Analyzer

## 🚀 Setup Automatico

### Linux/Mac:
```bash
# Rendi eseguibile lo script
chmod +x setup_venv.sh

# Esegui setup
./setup_venv.sh
```

### Windows:
```cmd
# Esegui setup
setup_venv.bat
```

## 📦 Setup Manuale

### 1. Crea Ambiente Virtuale
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Verifica Installazione
```bash
python3 --version  # Dovrebbe essere >= 3.8
```

### 3. Test Sistema (opzionale)
```bash
# Test librerie standard
python3 -c "import tkinter; print('GUI OK')" 2>/dev/null || echo "GUI non disponibile"

# Test sistema completo
python3 app.py info
```

## 🔧 Dipendenze

### Base (Librerie Standard)
Il progetto funziona con sole librerie Python standard:
- `os`, `sys`, `json`, `re`, `threading`
- `statistics`, `collections`, `tempfile`
- `tkinter` (per GUI - spesso incluso)

### Opzionali (per funzionalità avanzate)
```bash
pip install -r requirements.txt
```

Include:
- `pandas`, `numpy` (Data processing)
- `scikit-learn` (Machine Learning)
- `matplotlib` (Grafici)

## 🎯 Test Sistema

```bash
# Attiva ambiente
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate.bat  # Windows

# Test applicazione
python3 app.py info                    # Info sistema
python3 app.py file testi/testoai.txt  # Analisi singolo file
python3 app.py batch testi/            # Analisi batch
```

## 🖥️ GUI Setup

### Linux:
```bash
sudo apt-get install python3-tk
```

### Windows/Mac:
tkinter è incluso in Python standard

## ❗ Risoluzione Problemi

### "python3 non trovato"
```bash
# Ubuntu/Debian
sudo apt-get install python3

# CentOS/RHEL
sudo yum install python3

# macOS (con Homebrew)
brew install python3
```

### "tkinter non trovato" (Linux)
```bash
sudo apt-get install python3-tk
```

### "Permission denied" (Linux/Mac)
```bash
chmod +x setup_venv.sh
```

## 📁 Struttura Dopo Setup

```
TextAnalyzer/
├── venv/                 # Ambiente virtuale
├── data/                 # Dati del progetto
├── models/               # Modelli ML
├── reports/              # Report generati
├── temp/                 # File temporanei
└── *.py                  # Codice sorgente
```

## 🔄 Utilizzo Daily

```bash
# Attiva ambiente
source venv/bin/activate

# Usa l'applicazione
python3 app.py gui          # GUI (se disponibile)
python3 app.py file X.txt   # Analizza file
python3 app.py batch dir/   # Analisi batch

# Disattiva quando hai finito
deactivate
```

## 📊 Features per Dipendenza

| Dipendenza | Features Disponibili |
|------------|---------------------|
| Solo Standard Lib | ✅ Classificazione base<br>✅ Report testuali<br>✅ CLI completa |
| + tkinter | ✅ Interfaccia grafica<br>✅ GUI intuitiva |
| + ML libs | ✅ Features avanzate<br>✅ Modelli ML<br>✅ Grafici e visualizzazioni |

## 🎉 Pronto!

Una volta completato il setup, il sistema è pronto per l'uso:
- Classificazione testi AI vs umani
- Analisi batch di documenti  
- Report dettagliati
- Interfaccia grafica (se tkinter disponibile)
