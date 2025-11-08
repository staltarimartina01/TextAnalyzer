#!/bin/bash
# Setup script per AI vs Human Text Analyzer
# Crea ambiente virtuale e installa dipendenze

set -e  # Exit on any error

echo "🤖 AI vs Human Text Analyzer - Setup Environment"
echo "================================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Controlla Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 non trovato! Installa Python 3.8+ prima di continuare.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python trovato: $PYTHON_VERSION${NC}"

# Crea directory venv se non esiste
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Tentativo creazione ambiente virtuale...${NC}"
    if python3 -m venv venv 2>/dev/null; then
        echo -e "${GREEN}✅ Ambiente virtuale creato!${NC}"
    else
        echo -e "${YELLOW}⚠️  Ambiente virtuale non disponibile (ensurepip mancante)${NC}"
        echo -e "${YELLOW}💡 Il progetto funziona con librerie standard Python${NC}"
        echo -e "${YELLOW}💡 Per creare venv: sudo apt-get install python3-venv${NC}"
        echo -e "${YELLOW}💡 Oppure usa direttamente python3${NC}"
        # Crea directory vuota per evitare errori
        mkdir -p venv
    fi
else
    echo -e "${YELLOW}📦 Ambiente virtuale già esiste${NC}"
fi

# Attiva venv solo se esiste e funziona
if [ -d "venv/bin" ] && [ -f "venv/bin/activate" ]; then
    echo -e "${YELLOW}🔧 Attivazione ambiente virtuale...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Ambiente attivato!${NC}"
else
    echo -e "${YELLOW}🔧 Uso Python di sistema (venv non disponibile)${NC}"
fi

# Upgrade pip (solo se disponibile)
if command -v pip &> /dev/null; then
    echo -e "${YELLOW}⬆️  Upgrade pip...${NC}"
    pip install --upgrade pip
else
    echo -e "${YELLOW}⚠️  pip non disponibile (normale in ambienti container)${NC}"
fi

# Installa dipendenze base (solo librerie standard)
echo -e "${YELLOW}📚 Verifica librerie standard...${NC}"
python3 -c "import sys, os, re, json, threading, statistics, collections; print('✅ Tutte le librerie standard sono disponibili')" 2>/dev/null || {
    echo -e "${RED}❌ Errore con librerie standard Python${NC}"
    exit 1
}

# Test tkinter (GUI)
echo -e "${YELLOW}🖥️  Test interfaccia grafica (tkinter)...${NC}"
python3 -c "import tkinter; print('✅ tkinter disponibile per GUI')" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  tkinter non disponibile - GUI disabilitata${NC}"
    echo -e "${YELLOW}   Su Linux: sudo apt-get install python3-tk${NC}"
}

# Crea directories necessarie
echo -e "${YELLOW}📁 Creazione directory progetto...${NC}"
mkdir -p data/{training_data,test_data}
mkdir -p models
mkdir -p reports
mkdir -p temp

echo -e "${GREEN}🎉 Setup completato con successo!${NC}"
echo ""
echo "Per attivare l'ambiente virtuale:"
echo -e "${GREEN}source venv/bin/activate${NC}"
echo ""
echo "Per disattivare:"
echo -e "${YELLOW}deactivate${NC}"
echo ""
echo "Per installare dipendenze opzionali (ML/AI):"
if command -v pip &> /dev/null; then
    echo -e "${YELLOW}pip install -r requirements.txt${NC}"
else
    echo -e "${YELLOW}# pip non disponibile - installare pip prima${NC}"
    echo -e "${YELLOW}# Il progetto funziona con sole librerie standard${NC}"
fi
echo ""
echo "Per avviare l'applicazione:"
echo -e "${GREEN}python3 app.py gui${NC}"
echo -e "${GREEN}python3 app.py --help${NC}"
