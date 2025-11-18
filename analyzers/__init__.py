#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyzers Package per TextAnalyzer
Contiene tutti gli analizzatori specializzati
"""

from .base_analyzer import BaseAnalyzer, EnsembleAnalyzer
from .lexical_analyzer import LexicalAnalyzer
from .syntactic_analyzer import SyntacticAnalyzer
from .semantic_analyzer import SemanticAnalyzer
from .stylistic_analyzer import StylisticAnalyzer
from .ml_analyzer import MLAnalyzer

# Registry di tutti gli analyzers disponibili
REGISTRY = {
    'lexical': LexicalAnalyzer,
    'syntactic': SyntacticAnalyzer,
    'semantic': SemanticAnalyzer,
    'stylistic': StylisticAnalyzer,
    'ml': MLAnalyzer
}

# Lista di analyzers predefiniti (default ensemble)
DEFAULT_ANALYZERS = [
    'lexical',
    'syntactic',
    'semantic',
    'stylistic',
    'ml'
]

# Pesi predefiniti per ensemble (devono corrispondere a DEFAULT_ANALYZERS)
DEFAULT_WEIGHTS = {
    'lexical': 0.25,
    'syntactic': 0.25,
    'semantic': 0.20,
    'stylistic': 0.15,
    'ml': 0.15
}


def get_analyzer(analyzer_name: str):
    """
    Ottieni un analyzer per nome dal registry.

    Args:
        analyzer_name: Nome dell'analyzer ('lexical', 'syntactic', etc.)

    Returns:
        Classe analyzer corrispondente

    Raises:
        ValueError: Se analyzer_name non trovato
    """
    if analyzer_name not in REGISTRY:
        available = ', '.join(REGISTRY.keys())
        raise ValueError(f"Analyzer '{analyzer_name}' not found. Available: {available}")
    return REGISTRY[analyzer_name]


def create_analyzer(analyzer_name: str):
    """
    Crea un'istanza di analyzer per nome.

    Args:
        analyzer_name: Nome dell'analyzer

    Returns:
        Istanza dell'analyzer

    Raises:
        ValueError: Se analyzer_name non trovato
    """
    analyzer_class = get_analyzer(analyzer_name)
    return analyzer_class()


def create_default_ensemble():
    """
    Crea ensemble con analyzers predefiniti.

    Returns:
        EnsembleAnalyzer con default analyzers
    """
    from .base_analyzer import EnsembleAnalyzer

    analyzers = [create_analyzer(name) for name in DEFAULT_ANALYZERS]
    return EnsembleAnalyzer(analyzers)


def list_available_analyzers():
    """
    Lista tutti gli analyzers disponibili.

    Returns:
        Dict con nome -> description
    """
    return {
        name: cls().description
        for name, cls in REGISTRY.items()
    }


def get_analyzer_info(analyzer_name: str):
    """
    Ottieni informazioni dettagliate su un analyzer.

    Args:
        analyzer_name: Nome dell'analyzer

    Returns:
        Dict con info sull'analyzer
    """
    if analyzer_name not in REGISTRY:
        return None

    analyzer_class = REGISTRY[analyzer_name]
    instance = analyzer_class()
    return instance.get_info()


__all__ = [
    'BaseAnalyzer',
    'EnsembleAnalyzer',
    'LexicalAnalyzer',
    'SyntacticAnalyzer',
    'SemanticAnalyzer',
    'StylisticAnalyzer',
    'MLAnalyzer',
    'REGISTRY',
    'DEFAULT_ANALYZERS',
    'DEFAULT_WEIGHTS',
    'get_analyzer',
    'create_analyzer',
    'create_default_ensemble',
    'list_available_analyzers',
    'get_analyzer_info'
]
