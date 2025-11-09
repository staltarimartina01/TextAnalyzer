# TextAnalyzer V2 - Enhanced Edition - Guida Utente

## 🎯 **Panoramica**
TextAnalyzer V2 è la versione migliorata del tuo analizzatore testuale, che include funzionalità avanzate per l'analisi del testo e la rilevazione di contenuti generati da AI.

## 🚀 **Come Avviare**

### **Versione 2 (Raccomandata) - Enhanced Edition**
```bash
python3 launcher.py v2
```
Oppure direttamente:
```bash
python3 analyzer_v2.py
```

### **Versione 1 (Originale)**
```bash
python3 launcher.py v1
```

### **Menu Interattivo**
```bash
python3 launcher.py
```

## ✨ **Nuove Funzionalità V2**

### **1. 🎯 Analisi Comprensiva Multi-Metrica**
Combina tutte le metriche per una valutazione più accurata:
- Classificazione base AI vs Umano
- Varianza lunghezza frasi (nuovo!)
- Pattern emotivi
- Indici di leggibilità

### **2. 📊 Varianza Lunghezza Frasi (Rilevazione AI)**
**Cosa fa:** Calcola la varianza della lunghezza delle frasi per distinguere testi AI da umani.

**Come funziona:**
- **Varianza Bassa** (< 15): Frasi simili → Probabile AI
- **Varianza Alta** (> 30): Grande diversità → Probabile Umano

**Perché è efficace:** I modelli AI tendono a mantenere lunghezze di frasi regolari, mentre gli esseri umani variano naturalmente.

### **3. ❓ Sistema Help Integrato**
Pulsanti "?" accanto a ogni metrica importante:
- **📖 Indice Flesch**: Spiega la leggibilità
- **😊 Analisi Sentiment**: Dettagli sul rilevamento emotivo
- **📈 Varianza Frasi**: Come funziona la rilevazione AI

**Come usare:** Clicca sul pulsante "?" per aprire una finestra modale con spiegazioni dettagliate.

### **4. 🎨 Interfaccia Migliorata**
- Design moderno con tema Clam
- Font professionali (Segoe UI + Consolas)
- Palette colori moderna
- Layout ottimizzato

## 📋 **Guida Passo-Passo**

### **STEP 1: Avvia TextAnalyzer V2**
```bash
python3 launcher.py v2
```

### **STEP 2: Carica un File**
- Clicca su "📁 Carica File"
- Seleziona un file .txt dal tuo computer

### **STEP 3: Analizza**
- Clicca su "🔍 Analisi Avanzata"
- Attendi che l'analisi venga completata

### **STEP 4: Esplora i Risultati**
Vai alla tab **"📊 Analisi Avanzata"** per vedere:

#### **📈 Sezione Varianza Frasi (Nuovo!)**
- **Valore numerico** della varianza
- **Classificazione suggerita** (AI/Umano)
- **Livello di confidenza** della predizione
- **Pulsante ?** per spiegazioni dettagliate

#### **😊 Sezione Sentiment Analysis**
- **Sentiment generale** (Positivo/Negativo/Neutro)
- **Emozione dominante** (Gioia, Tristezza, ecc.)
- **Intensità emotiva** in percentuale
- **Pulsante ?** per spiegazioni del sistema

#### **📖 Sezione Leggibilità**
- **Flesch Reading Ease** (0-100)
- **Grade Level** (livello scolastico stimato)
- **Pulsante ?** per comprendere gli indici

### **STEP 5: Usa il Help System**
- Clicca sui pulsanti "?" per aprire spiegazioni dettagliate
- Ogni spiegazione include esempi e interpretazione
- Le finestre sono modali (chiudibili con "Chiudi")

## 🧪 **Test delle Funzionalità**

### **Test Rapido delle Funzioni**
```bash
python3 launcher.py test
```

### **Demo del Sistema Help**
```bash
python3 demo_help.py
```

### **Confronto V1 vs V2**
```bash
python3 launcher.py compare
```

## 📊 **Esempio di Output V2**

```
🧠 ANALISI COMPRENSIVA
Analisi Comprensiva: Umano (Potenziato)
Indicatori AI: 1, Indicatori Umano: 2
Metriche valutate: 4

📈 Varianza Lunghezza Frasi
Varianza: 76.39
Classificazione: Molto Probabile Umano
Confidenza: Alta
Frasi analizzate: 18

😊 Analisi Sentiment
Sentiment: ⚪ NEUTRALE
Intensità: 22.3%

📖 Indice di Leggibilità
Flesch Score: 68.3/100
Grade Level: 6.7
```

## 🎯 **Quando Usare Ogni Versione**

### **Usa V1 Original se:**
- Preferisci un'interfaccia semplice
- Non hai bisogno del sistema help
- Vuoi solo classificazione base AI vs Umano

### **Usa V2 Enhanced se:**
- Vuoi la massima accuratezza
- Hai bisogno di spiegazioni dettagliate
- Analizzi testi per scopi professionali/accademici
- Vuoi comprendere il "perché" dietro le classificazioni

## 🛠️ **Risoluzione Problemi**

### **"ImportError"**
- Verifica che tutti i file siano presenti
- Assicurati di essere nella directory giusta

### **"GUI non si apre"**
- Verifica che tkinter sia installato
- Su Linux: `sudo apt-get install python3-tk`

### **"Nessun risultato varianza"**
- Il testo deve avere almeno 2 frasi
- Prova con un testo più lungo (200+ parole)

## 📝 **File del Progetto**

- `analyzer_v2.py` - Interfaccia principale V2
- `launcher.py` - Launcher con menu
- `demo_help.py` - Demo del sistema help
- `test_variance_example.txt` - File di test
- `app.py` - Versione originale V1

## 🎉 **Caratteristiche Principali V2**

✅ **Varianza Frasi per AI Detection**  
✅ **Sistema Help con pulsanti ?**  
✅ **Analisi Comprensiva multi-metrica**  
✅ **Interfaccia moderna e professionale**  
✅ **Spiegazioni dettagliate delle metriche**  
✅ **Classificazione potenziata AI vs Umano**  
✅ **Backward compatibility con V1**  

---

**TextAnalyzer V2 Enhanced Edition - L'analisi testuale del futuro! 🚀**
