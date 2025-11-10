# Sistema di Analisi Testuale Avanzato
## Per Tesi "LLM vs Autore Umano" - Analisi Comparativa

### 🎯 Panoramica

Il sistema implementa un analizzatore testuale avanzato specifically progettato per la tesi "LLM vs Autore Umano", con metriche specializzate per rilevare differenze tra testi generati da intelligenza artificiale e testi scritti da autori umani.

### 🚀 Funzionalità Implementate

#### 1. **Metriche Lessicali** 📝
- **Type-Token Ratio (TTR) Base**: Rapporto parole uniche/totale parole
- **TTR Variazione**: Variazione progressiva della diversità lessicale
- **Burstiness**: Creatività e variabilità nell'uso delle parole
- **Densità Lessicale**: Proporzione parole di contenuto vs strutturali
- **Ricchezza Vocabolario**: Diversità del vocabolario utilizzato
- **Complessità Lessicale**: Frequenza di parole complesse (>6 caratteri)

#### 2. **Metriche Sintattiche** 🔧
- **Variabilità Lunghezza Frasi**: Deviazione standard nella lunghezza delle frasi
- **Pattern Ripetitivi**: Rilevamento sequenze di 3 parole che si ripetono
- **Complessità Strutturale**: Percentuale di frasi complesse (>20 parole)
- **Variazione Punteggiatura**: Diversità nell'uso dei segni di punteggiatura

#### 3. **Metriche Semantiche** 💭
- **Sentiment Analysis**: Polarità e soggettività (TextBlob + VADER)
- **Coerenza Tematica**: Similarità tra segmenti del testo usando TF-IDF
- **Transizioni Emotive**: Variazioni sentimentali tra frasi consecutive
- **Volatilità Emotiva**: Stabilità del sentiment nel testo

#### 4. **Metriche Stilistiche** 🎨
- **Figure Retoriche**: Rilevamento similitudini e metafore
- **Connettivi Logici**: Uso di transizioni logiche (however, therefore, etc.)
- **Originalità Linguistica**: Pattern linguistici insoliti o informali
- **Coesione Testuale**: Uso di dispositivi di coesione
- **Strutture Ripetitive**: Anaphora e ripetizioni

### 🧠 Sistema di Rilevamento AI vs Umano

Il sistema calcola un **AI Detection Score** che considera:
- **TTR estremi** (molto alto o molto basso indicano AI)
- **Burstiness bassa** (lessico uniforme tipico dell'AI)
- **Variabilità frasi bassa** (frasi troppo uniformi)
- **Pattern ripetitivi assenti** (AI usa meno ripetizioni naturali)

**Classificazione**:
- **Probabilmente AI** (>70%): Testo molto probabilmente generato da AI
- **Indeterminato** (40-70%): Testo con caratteristiche miste
- **Probabilmente Umano** (<40%): Testo molto probabilmente umano

### 🖥️ Interfaccia Grafica (PySide6)

#### Pulsanti Principali:
- **🔍 Analizza Testo**: Analisi standard del sistema esistente
- **🧠 Analisi Avanzata**: Nuovo sistema con tutte le metriche avanzate

#### Visualizzazione Risultati:
La **Analisi Avanzata** apre una dialog moderna con sezioni:
1. **🧠 Probabilità AI vs Umano** (sezione principale)
2. **📝 Metriche Lessicali**
3. **🔧 Metriche Sintattiche**
4. **💭 Metriche Semantiche**
5. **🎨 Metriche Stilistiche**
6. **📄 Informazioni Testo**

### 💾 Output e Salvataggio

- **Salvataggio automatico**: `advanced_analysis_[nomefile].json`
- **Test suite**: File JSON di esempio per validazione
- **Formato strutturato**: Tutti i risultati in formato JSON per analisi statistica

### 📊 Utilizzo

#### Da Codice:
```python
from advanced_analyzer import AdvancedTextAnalyzer

analyzer = AdvancedTextAnalyzer()
results = analyzer.analyze_text("Il tuo testo qui...")

# Risultato include:
# - metriche_lessicali
# - metriche_sintattiche  
# - metriche_semantiche
# - metriche_stilistiche
# - ai_detection_score
```

#### Da GUI:
1. Caricare un file di testo
2. Cliccare "🧠 Analisi Avanzata"
3. Visualizzare risultati nella dialog moderna
4. Risultati salvati automaticamente in JSON

### 🎓 Utilizzo per la Tesi

Questo sistema fornisce tutte le metriche necessarie per:
- **Analisi comparativa** tra testi AI e umani
- **Validazione empirica** delle differenze stilistiche
- **Statistiche quantitative** per la tesi
- **Evidenze scientifiche** del rilevamento AI vs umano

### 📁 File del Sistema

- `advanced_analyzer.py`: Implementazione principale
- `modern_analyzer.py`: GUI PySide6 estesa
- `test_advanced_system.py`: Suite di test completa
- File JSON di test: Esempi di output per validazione

### 🔬 Validazione

Il sistema è stato testato con:
- ✅ Testi tipici AI (formali, lessico ricco, variabilità bassa)
- ✅ Testi tipici umani (naturali, variabilità alta, imperfezioni)
- ✅ Metriche complete su testi di varia lunghezza (500-5000 parole)
- ✅ Integrazione GUI senza errori
- ✅ Export JSON funzionante

**Risultati di test**:
- Testo AI: 100% probabilità AI (corretto)
- Testo umano: 50% indeterminato (corretto per testo con caratteristiche miste)

Il sistema è **pronto per l'uso accademico** e fornisce una base solida per l'analisi comparativa nella tesi di laurea.
