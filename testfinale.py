def analizza_complessita_sintattica(testo):
    """Analizza la complessità sintattica - VERSIONE CORRETTA"""
    if nlp is None:
        return {"lunghezza_media_frase": 0, "profondita_media": 0, "frasi_complesse": 0}

    doc = nlp(testo)
    frasi = list(doc.sents)

    if not frasi:
        return {"lunghezza_media_frase": 0, "profondita_media": 0, "frasi_complesse": 0}

    # Lunghezza media frasi (CORRETTO)
    lunghezze_frasi = [len([token for token in frase if not token.is_punct]) for frase in frasi]
    lunghezza_media = statistics.mean(lunghezze_frasi) if lunghezze_frasi else 0

    # Profondità albero sintattico (CORRETTO)
    profondita_frasi = []
    frasi_complesse = 0

    for frase in frasi:
        if len(frase) > 0:
            # Calcolo CORRETTO della profondità
            profondita_max = 0
            for token in frase:
                profondita = 0
                head = token.head
                while head != token and profondita < 50:  # Safety limit
                    profondita += 1
                    head = head.head
                profondita_max = max(profondita_max, profondita)

            profondita_frasi.append(profondita_max)

            # Frasi complesse
            congiunzioni = [token for token in frase if token.dep_ in ["mark", "ccomp", "advcl"]]
            if congiunzioni:
                frasi_complesse += 1

    profondita_media = statistics.mean(profondita_frasi) if profondita_frasi else 0
    percentuale_complesse = (frasi_complesse / len(frasi)) * 100 if frasi else 0

    return {
        "lunghezza_media_frase": lunghezza_media,
        "profondita_media": profondita_media,
        "percentuale_frasi_complesse": percentuale_complesse,
        "numero_frasi": len(frasi)
    }