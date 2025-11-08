# -*- coding: utf-8 -*-
"""
ANALIZZATORE LESSICALE - VERSIONE MIGLIORATA
"""

import os
import string
from collections import Counter


def analizza_testo(nome_file):
    """Analizza un file di testo e calcola le metriche base"""

    print(f"\n📖 Analisi in corso per: {nome_file}")
    print("=" * 40)

    try:
        with open(nome_file, 'r', encoding='utf-8') as file:
            testo = file.read()

        # Pulizia del testo
        traduttore = str.maketrans('', '', string.punctuation)
        parole = testo.translate(traduttore).lower().split()

        # Divisione in frasi (migliorata)
        frasi = [f for f in testo.split('.') if f.strip()]

        # Calcolo metriche
        parole_totali = len(parole)
        parole_uniche = set(parole)
        ttr = len(parole_uniche) / parole_totali if parole_totali > 0 else 0

        lunghezza_media_frase = sum(len(f.split()) for f in frasi) / len(frasi) if frasi else 0

        # Risultati
        print(f"📊 Parole totali: {parole_totali}")
        print(f"🎨 Parole uniche: {len(parole_uniche)}")
        print(f"🌈 TTR (Ricchezza lessicale): {ttr:.3f}")
        print(f"📏 Lunghezza media frase: {lunghezza_media_frase:.1f} parole")
        print(f"🔤 Numero di frasi: {len(frasi)}")

        parole_comuni = Counter(parole).most_common(5)
        print(f"🏆 Parole più frequenti: {[parola for parola, count in parole_comuni]}")

    except FileNotFoundError:
        print(f"❌ Errore: File {nome_file} non trovato!")
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}")


# ===== PROGRAMMA PRINCIPALE =====
if __name__ == "__main__":
    print("🦜 BENVENUTA NEL TUO ANALIZZATORE LESSICALE!")
    print("=" * 50)

    cartella_testi = "testi"

    # VERIFICA SE LA CARTELLA ESISTE E È UNA CARTELLA
    if not os.path.exists(cartella_testi):
        print(f"📁 Creazione cartella '{cartella_testi}'...")
        os.makedirs(cartella_testi)
        print(f"✅ Cartella '{cartella_testi}' creata!")
        print(f"💡 Inserisci i tuoi file .txt nella cartella '{cartella_testi}'")

    elif not os.path.isdir(cartella_testi):
        print(f"❌ ERRORE: '{cartella_testi}' esiste ma non è una cartella!")
        print("🔧 Elimina il file chiamato 'testi' e ricrea come cartella")

    else:
        # Analizza tutti i file .txt nella cartella
        file_trovati = False
        for file in os.listdir(cartella_testi):
            if file.endswith(".txt"):
                percorso_completo = os.path.join(cartella_testi, file)
                analizza_testo(percorso_completo)
                file_trovati = True

        if not file_trovati:
            print(f"📁 Inserisci i file .txt nella cartella '{cartella_testi}'")
            print("💡 Puoi creare file .txt copiando testo da PDF o Word")

    print("\n" + "=" * 50)
    print("🎉 Analisi completata!")
    input("Premi Invio per uscire...")