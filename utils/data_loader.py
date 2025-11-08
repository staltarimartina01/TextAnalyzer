# -*- coding: utf-8 -*-
"""
Data Loader - Utility per caricamento e gestione dati
Modulo per la gestione dei file di input e output
"""

import os
import glob
import json
from typing import List, Dict, Any
from datetime import datetime


class DataLoader:
    """Utility per caricamento e gestione dati"""
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.md', '.json']
        self.max_file_size = 10 * 1024 * 1024  # 10MB

    def load_text_file(self, file_path: str) -> str:
        """Carica un file di testo"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File non trovato: {file_path}")
        
        if os.path.getsize(file_path) > self.max_file_size:
            raise ValueError(f"File troppo grande (max {self.max_file_size/1024/1024:.1f}MB)")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Prova con encoding alternativi
            encodings = ['latin-1', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Impossibile decodificare il file: {file_path}")

    def load_files_from_directory(self, directory: str, pattern: str = "*.txt") -> List[str]:
        """Carica tutti i file che corrispondono al pattern dalla directory"""
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory non trovata: {directory}")
        
        search_path = os.path.join(directory, pattern)
        files = glob.glob(search_path)
        
        # Filtra per estensioni supportate
        supported_files = []
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.supported_extensions and os.path.getsize(file_path) < self.max_file_size:
                supported_files.append(file_path)
        
        return sorted(supported_files)

    def save_analysis_result(self, result: Dict[str, Any], output_path: str):
        """Salva il risultato dell'analisi in formato JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            raise ValueError(f"Errore nel salvataggio: {e}")

    def load_analysis_result(self, file_path: str) -> Dict[str, Any]:
        """Carica un risultato di analisi salvato"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Errore nel caricamento: {e}")

    def create_sample_data(self, directory: str, num_samples: int = 10):
        """Crea dati di esempio per testing"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Crea file di esempio AI e umani
        ai_samples = [
            """L'intelligenza artificiale rappresenta una delle tecnologie più rivoluzionarie del nostro tempo. 
            Attraverso algoritmi complessi e apprendimento automatico, i sistemi AI sono in grado di elaborare 
            enormi quantità di dati e identificare pattern nascosti. Questa capacità di elaborazione supera 
            di gran lunga le possibilità umane tradizionali.""",
            
            """L'elaborazione del linguaggio naturale costituisce un campo di ricerca multidisciplinare che 
            combina linguistica computazionale, informatica e intelligenza artificiale. Gli obiettivi principali 
            includono la comprensione automatica del testo, la generazione di linguaggio naturale e la traduzione 
            automatica tra diverse lingue.""",
            
            """Le reti neurali artificiali sono modelli matematici ispirati al funzionamento del cervello umano. 
            Ogni neurone artificiale riceve input multipli, applica una funzione di attivazione e produce un output. 
            L'addestramento avviene attraverso algoritmi di backpropagation che ajustano i pesi delle connessioni 
            per minimizzare l'errore di predizione."""
        ]
        
        human_samples = [
            """Beh, non saprei proprio cosa dire. È una cosa un po' strana da raccontare, ma provo a spiegartela 
            come meglio posso. Ieri mentre tornavo a casa, ho visto una scena davvero curiosa. C'era questo gatto 
            che cercava di attraversare la strada, ma sembrava molto confuso. Continuava a girare in tondo come 
            se non sapesse da che parte andare.""",
            
            """Ma davvero non ci posso credere! Oggi è successa una cosa pazzesca al lavoro. Immaginati che il 
            capo è arrivato tutto arrabbiato perché il computer non funzionava, e noi ovviamente non c'entravamo 
            niente. Alla fine si è scoperto che aveva semplicemente dimenticato di accenderlo! Noi ci siamo 
            guardati e non sapevamo se ridere o piangere.""",
            
            """Ecco, ti spiego come la vedo io questa storia. Secondo me bisogna prendere le cose con più 
            filosofia, non tutto è così drammatico come sembra. Certo, i problemi ci sono, ma esistono sempre 
            delle soluzioni, basta sapersi adattare e non farsi prendere dallo sconforto. L'importante è 
            non perdere la speranza e continuare a lottare."""
        ]
        
        # Crea file AI
        for i in range(min(num_samples // 2, len(ai_samples))):
            with open(f"{directory}/ai_sample_{i+1}.txt", 'w', encoding='utf-8') as f:
                f.write(ai_samples[i])
        
        # Crea file umani
        for i in range(min(num_samples // 2, len(human_samples))):
            with open(f"{directory}/human_sample_{i+1}.txt", 'w', encoding='utf-8') as f:
                f.write(human_samples[i])
        
        return f"Creati {min(num_samples // 2, len(ai_samples))} file AI e {min(num_samples // 2, len(human_samples))} file umani in {directory}"

    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Valida un file prima dell'analisi"""
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        if not os.path.exists(file_path):
            validation['valid'] = False
            validation['errors'].append("File non trovato")
            return validation
        
        # Informazioni file
        file_stat = os.stat(file_path)
        validation['file_info'] = {
            'size': file_stat.st_size,
            'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
            'extension': os.path.splitext(file_path)[1].lower()
        }
        
        # Controlli di validità
        if file_stat.st_size == 0:
            validation['valid'] = False
            validation['errors'].append("File vuoto")
        
        if file_stat.st_size > self.max_file_size:
            validation['valid'] = False
            validation['errors'].append(f"File troppo grande (max {self.max_file_size/1024/1024:.1f}MB)")
        
        if validation['file_info']['extension'] not in self.supported_extensions:
            validation['warnings'].append(f"Estensione non supportata: {validation['file_info']['extension']}")
        
        # Prova a leggere il file
        try:
            content = self.load_text_file(file_path)
            if len(content.strip()) < 10:
                validation['warnings'].append("Contenuto molto breve (meno di 10 caratteri)")
        except Exception as e:
            validation['valid'] = False
            validation['errors'].append(f"Impossibile leggere il file: {str(e)}")
        
        return validation
