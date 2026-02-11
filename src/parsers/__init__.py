"""
Parser Manager & Auto-detector
Inicjalizuje wszystkie parsery i zapewnia auto-detekcję formatu.
"""

from .base_parser import parser_registry, ParsedData
from .txt_parser import TxtParser
from .md_parser import MarkdownParser
from .json_parser import JsonParser


def init_parsers():
    """Inicjalizuje i rejestruje wszystkie parsery"""
    parser_registry.register('txt', TxtParser())
    parser_registry.register('md', MarkdownParser())
    parser_registry.register('json', JsonParser())
    # DOC, PHP, CLIPBOARD będą dodane później


def parse_content(content: str, format_hint: str = None) -> ParsedData:
    """
    Główna funkcja parsująca zawartość.
    
    Args:
        content: Zawartość do sparsowania
        format_hint: Opcjonalna podpowiedź formatu ('txt', 'md', 'json', etc.)
        
    Returns:
        ParsedData: Sparsowane dane
    """
    # Upewnij się że parsery są zainicjalizowane
    if not parser_registry.list_parsers():
        init_parsers()
    
    # Jeśli podano format, użyj go
    if format_hint:
        parser = parser_registry.get_parser(format_hint)
        if parser:
            return parser.parse(content)
    
    # Auto-detekcja
    return parser_registry.parse_auto(content)


def detect_format(content: str) -> tuple[str, float]:
    """
    Wykrywa format zawartości.
    
    Args:
        content: Zawartość do analizy
        
    Returns:
        tuple: (format_name, confidence_score)
    """
    if not parser_registry.list_parsers():
        init_parsers()
    
    return parser_registry.detect_format(content)


# Inicjalizuj parsery przy imporcie modułu
init_parsers()


__all__ = [
    'parse_content',
    'detect_format',
    'parser_registry',
    'ParsedData',
    'TxtParser',
    'MarkdownParser',
    'JsonParser'
]
