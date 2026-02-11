"""
Base Parser Class
Definiuje interfejs dla wszystkich parserów danych wejściowych.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class DataType(Enum):
    """Typy danych rozpoznawane przez system"""
    TEXT = "text"
    CODE = "code"
    STRUCTURED = "structured"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class ParsedData:
    """
    Zunifikowana struktura danych po parsowaniu.
    Każdy parser zwraca ten sam format dla spójności.
    """
    # Podstawowe info
    format: str                          # Źródłowy format (txt, md, json, etc.)
    data_type: DataType                  # Typ danych
    content: str                         # Oryginalna zawartość
    
    # Struktura
    title: Optional[str] = None          # Tytuł/nazwa
    sections: List[Dict[str, Any]] = None  # Sekcje dokumentu
    metadata: Dict[str, Any] = None      # Metadane
    
    # Elementy strukturalne
    headers: List[Dict[str, Any]] = None  # Nagłówki
    paragraphs: List[str] = None         # Paragrafy
    lists: List[Dict[str, Any]] = None   # Listy
    code_blocks: List[Dict[str, Any]] = None  # Bloki kodu
    tables: List[Dict[str, Any]] = None  # Tabele
    links: List[Dict[str, str]] = None   # Linki
    images: List[Dict[str, str]] = None  # Obrazy
    
    # Statystyki
    stats: Dict[str, int] = None         # Statystyki (line count, word count, etc.)
    
    # Dodatkowe
    raw_structure: Any = None            # Surowa struktura (dla JSON, XML, etc.)
    confidence: float = 1.0              # Pewność parsowania (0-1)
    errors: List[str] = None             # Lista błędów/ostrzeżeń
    
    def __post_init__(self):
        """Inicjalizacja pustych kolekcji"""
        if self.sections is None:
            self.sections = []
        if self.metadata is None:
            self.metadata = {}
        if self.headers is None:
            self.headers = []
        if self.paragraphs is None:
            self.paragraphs = []
        if self.lists is None:
            self.lists = []
        if self.code_blocks is None:
            self.code_blocks = []
        if self.tables is None:
            self.tables = []
        if self.links is None:
            self.links = []
        if self.images is None:
            self.images = []
        if self.stats is None:
            self.stats = {}
        if self.errors is None:
            self.errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwersja do słownika"""
        return {
            'format': self.format,
            'data_type': self.data_type.value,
            'content': self.content,
            'title': self.title,
            'sections': self.sections,
            'metadata': self.metadata,
            'headers': self.headers,
            'paragraphs': self.paragraphs,
            'lists': self.lists,
            'code_blocks': self.code_blocks,
            'tables': self.tables,
            'links': self.links,
            'images': self.images,
            'stats': self.stats,
            'confidence': self.confidence,
            'errors': self.errors
        }


class BaseParser(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich parserów.
    Każdy parser musi implementować metodę parse().
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Args:
            config: Konfiguracja parsera (opcjonalna)
        """
        self.config = config or {}
    
    @abstractmethod
    def parse(self, content: str, **kwargs) -> ParsedData:
        """
        Parsuje zawartość do zunifikowanej struktury.
        
        Args:
            content: Zawartość do sparsowania
            **kwargs: Dodatkowe parametry specyficzne dla parsera
            
        Returns:
            ParsedData: Sparsowane dane w zunifikowanym formacie
        """
        pass
    
    @abstractmethod
    def can_parse(self, content: str) -> float:
        """
        Sprawdza czy parser może obsłużyć daną zawartość.
        
        Args:
            content: Zawartość do sprawdzenia
            
        Returns:
            float: Confidence score (0.0 - 1.0), gdzie:
                   1.0 = na pewno ten format
                   0.5 = prawdopodobnie ten format
                   0.0 = na pewno nie ten format
        """
        pass
    
    def validate(self, content: str) -> tuple[bool, List[str]]:
        """
        Waliduje zawartość przed parsowaniem.
        
        Args:
            content: Zawartość do walidacji
            
        Returns:
            tuple: (is_valid, errors_list)
        """
        errors = []
        
        if not content:
            errors.append("Pusta zawartość")
            return False, errors
        
        if not isinstance(content, str):
            errors.append(f"Nieprawidłowy typ: {type(content)}, oczekiwano str")
            return False, errors
        
        return True, errors
    
    def calculate_stats(self, content: str) -> Dict[str, int]:
        """
        Oblicza podstawowe statystyki dla zawartości.
        
        Args:
            content: Zawartość do analizy
            
        Returns:
            Dict: Statystyki (lines, words, chars, etc.)
        """
        lines = content.split('\n')
        words = content.split()
        
        return {
            'lines': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'words': len(words),
            'characters': len(content),
            'characters_no_spaces': len(content.replace(' ', '').replace('\n', ''))
        }


class ParserRegistry:
    """
    Rejestr dostępnych parserów.
    Umożliwia auto-detekcję formatu i wybór odpowiedniego parsera.
    """
    
    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {}
    
    def register(self, format_name: str, parser: BaseParser):
        """Rejestruje parser dla danego formatu"""
        self._parsers[format_name] = parser
    
    def get_parser(self, format_name: str) -> Optional[BaseParser]:
        """Zwraca parser dla danego formatu"""
        return self._parsers.get(format_name)
    
    def detect_format(self, content: str) -> tuple[str, float]:
        """
        Auto-detekcja formatu zawartości.
        
        Args:
            content: Zawartość do analizy
            
        Returns:
            tuple: (format_name, confidence_score)
        """
        best_format = "txt"  # fallback
        best_score = 0.0
        
        for format_name, parser in self._parsers.items():
            score = parser.can_parse(content)
            if score > best_score:
                best_score = score
                best_format = format_name
        
        return best_format, best_score
    
    def parse_auto(self, content: str) -> ParsedData:
        """
        Automatyczne parsowanie z detekcją formatu.
        
        Args:
            content: Zawartość do sparsowania
            
        Returns:
            ParsedData: Sparsowane dane
        """
        format_name, confidence = self.detect_format(content)
        parser = self.get_parser(format_name)
        
        if parser:
            result = parser.parse(content)
            result.confidence = confidence
            return result
        
        # Fallback - zwróć surowe dane
        return ParsedData(
            format="unknown",
            data_type=DataType.UNKNOWN,
            content=content,
            confidence=0.0,
            errors=["Nie znaleziono odpowiedniego parsera"]
        )
    
    def list_parsers(self) -> List[str]:
        """Zwraca listę zarejestrowanych parserów"""
        return list(self._parsers.keys())


# Singleton instance
parser_registry = ParserRegistry()
