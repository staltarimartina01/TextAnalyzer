@echo off
REM Setup script per AI vs Human Text Analyzer (Windows)
REM Crea ambiente virtuale e installa dipendenze

echo 🤖 AI vs Human Text Analyzer - Setup Environment
echo =================================================

REM Controlla Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato! Installa Python 3.8+ prima di continuare.
    pause
    exit /b 1
)

echo ✅ Python trovato

REM Crea directory venv se non esiste
if not exist "venv" (
    echo 📦 Creazione ambiente virtuale...
    python -m venv venv
    echo ✅ Ambiente virtuale creato!
) else (
    echo 📦 Ambiente virtuale già esiste
)

REM Attiva venv
echo 🔧 Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
echo ✅ Ambiente attivato!

REM Upgrade pip
echo ⬆️  Upgrade pip...
python -m pip install --upgrade pip

REM Test librerie base
echo 📚 Verifica librerie standard...
python -c "import sys, os, re, json, threading, statistics, collections; print('✅ Tutte le librerie standard sono disponibili')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Errore con librerie standard Python
    pause
    exit /b 1
)

REM Test tkinter
echo 🖥️  Test interfaccia grafica (tkinter)...
python -c "import tkinter; print('✅ tkinter disponibile per GUI')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  tkinter non disponibile - GUI disabilitata
    echo    Su Windows, tkinter dovrebbe essere incluso in Python standard
    echo    Se manca, reinstalla Python con l'opzione "tcl/tk and IDLE"
)

REM Crea directories
echo 📁 Creazione directory progetto...
if not exist "data" mkdir data
if not exist "data\training_data" mkdir data\training_data
if not exist "data\test_data" mkdir data\test_data
if not exist "models" mkdir models
if not exist "reports" mkdir reports
if not exist "temp" mkdir temp

echo 🎉 Setup completato con successo!
echo.
echo Per attivare l'ambiente virtuale:
echo venv\Scripts\activate.bat
echo.
echo Per disattivare:
echo deactivate
echo.
echo Per installare dipendenze opzionali (ML/AI):
echo pip install -r requirements.txt
echo.
echo Per avviare l'applicazione:
echo python app.py gui
echo python app.py --help

pause
