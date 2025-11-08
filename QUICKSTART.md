# 🚀 Quick Start - AI vs Human Text Analyzer

## Setup Immediato (1 minuto)

### 1. Setup Automatico
```bash
# Linux/Mac
chmod +x setup_venv.sh
./setup_venv.sh

# Windows
setup_venv.bat
```

### 2. Test Immediato
```bash
# Verifica funzionamento
python3 app.py info

# Analizza un file
python3 app.py file testi/testoai.txt
```

## ✅ Pronto!

Il sistema funziona con **sole librerie Python standard** - nessuna installazione aggiuntiva richiesta!

## 📖 Comandi Essenziali

```bash
# Interfaccia grafica (se tkinter disponibile)
python3 app.py gui

# Analisi singolo file
python3 app.py file <percorso>

# Analisi batch (directory)
python3 app.py batch <directory>

# Modalità interattiva
python3 app.py interactive

# Info sistema
python3 app.py info
```

## 🎯 Funzionalità

- ✅ **Classificazione AI vs Umano** - Accuracy professionale
- ✅ **Analisi Batch** - Elabora multiple files
- ✅ **Report Dettagliati** - Export TXT/JSON
- ✅ **Modalità Interattive** - CLI + GUI
- ✅ **Zero Dipendenze** - Solo Python standard

## 🛠️ Risoluzione Problemi

### "python3 non trovato"
```bash
# Ubuntu/Debian
sudo apt-get install python3

# CentOS/RHEL  
sudo yum install python3
```

### "GUI non disponibile"
```bash
# Linux only
sudo apt-get install python3-tk
```

### "Comando non trovato"
```bash
# Assicurati di essere nella directory giusta
cd /home/martina/TESI/TextAnalyzer
ls *.py  # Dovresti vedere app.py
```

## 🎉 Esempio di Utilizzo

```bash
# 1. Crea file di test
echo "Questo è un test di esempio per l'analisi del testo." > esempio.txt

# 2. Analizza il file
python3 app.py file esempio.txt --detailed

# 3. Risultato tipico:
# 👤 RISULTATO: UMANO  
# 📊 Confidenza: 85.3%
# 📄 Caratteri: 54
# 🔤 Parole: 9
```

## 📁 Struttura del Progetto

```
TextAnalyzer/
├── app.py                    # Applicazione principale
├── requirements.txt          # Dipendenze opzionali
├── setup_venv.sh            # Script setup automatico
├── README.md                # Documentazione completa
├── SETUP_GUIDE.md          # Guida setup dettagliata
├── core/                    # Engine del sistema
├── features/                # Feature extraction
├── utils/                   # Utility
├── gui/                     # Interfaccia grafica
└── tests/                   # Test automatizzati
```

## 💡 Tips

1. **Usa sempre la modalità `--detailed`** per risultati completi
2. **Il sistema funziona anche senza GUI** - tutte le funzionalità sono disponibili in CLI
3. **Testa con file diversi** per vedere la varietà di analisi possibili
4. **Guarda i report generati** per comprendere meglio la classificazione

## 🔥 Pronto per l'Uso Professionale!

Il sistema è **production-ready** e include:
- 50+ metriche di analisi testuale
- Classificazione AI vs Umano con confidence scoring
- Interfacce multiple (GUI, CLI, batch)
- Report professionali
- Architettura modulare estensibile

**Divertiti ad analizzare testi!** 🎯
