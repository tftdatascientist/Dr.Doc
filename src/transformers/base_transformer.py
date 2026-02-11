"""
Base Transformer Class
Definiuje interfejs dla transformerów przekształcających dane
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..parsers.base_parser import ParsedData


class TransformedData:
    """Wynik transformacji danych"""
    
    def __init__(self):
        self.destination: str = ""           # Typ destinacji (github, chatgpt, etc.)
        self.files: Dict[str, str] = {}      # Pliki do wygenerowania {path: content}
        self.structure: Dict[str, Any] = {}  # Struktura katalogów
        self.metadata: Dict[str, Any] = {}   # Metadane transformacji
        self.errors: List[str] = []          # Błędy podczas transformacji
    
    def add_file(self, path: str, content: str):
        """Dodaje plik do wyniku transformacji"""
        self.files[path] = content
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje do słownika"""
        return {
            'destination': self.destination,
            'files': self.files,
            'structure': self.structure,
            'metadata': self.metadata,
            'errors': self.errors
        }


class BaseTransformer(ABC):
    """
    Abstrakcyjna klasa bazowa dla transformerów.
    Każdy transformer przekształca sparsowane dane do formatu docelowego.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Args:
            config: Konfiguracja transformera
        """
        self.config = config or {}
    
    @abstractmethod
    def transform(self, parsed_data: ParsedData, **kwargs) -> TransformedData:
        """
        Transformuje sparsowane dane do formatu docelowego.
        
        Args:
            parsed_data: Dane po parsowaniu
            **kwargs: Dodatkowe parametry
            
        Returns:
            TransformedData: Przetransformowane dane
        """
        pass
    
    @abstractmethod
    def get_destination_type(self) -> str:
        """Zwraca typ destinacji (github, chatgpt, etc.)"""
        pass
    
    def validate_input(self, parsed_data: ParsedData) -> tuple[bool, List[str]]:
        """
        Waliduje dane wejściowe przed transformacją.
        
        Args:
            parsed_data: Dane do walidacji
            
        Returns:
            tuple: (is_valid, errors_list)
        """
        errors = []
        
        if not parsed_data:
            errors.append("Brak danych wejściowych")
            return False, errors
        
        if not parsed_data.content:
            errors.append("Pusta zawartość")
            return False, errors
        
        return True, errors


class TransformerRegistry:
    """Rejestr transformerów"""
    
    def __init__(self):
        self._transformers: Dict[str, BaseTransformer] = {}
    
    def register(self, destination: str, transformer: BaseTransformer):
        """Rejestruje transformer dla danej destinacji"""
        self._transformers[destination] = transformer
    
    def get_transformer(self, destination: str) -> BaseTransformer:
        """Zwraca transformer dla danej destinacji"""
        return self._transformers.get(destination)
    
    def list_destinations(self) -> List[str]:
        """Zwraca listę dostępnych destinacji"""
        return list(self._transformers.keys())
    
    def transform(self, destination: str, parsed_data: ParsedData, **kwargs) -> TransformedData:
        """
        Transformuje dane używając odpowiedniego transformera.
        
        Args:
            destination: Typ destinacji
            parsed_data: Sparsowane dane
            **kwargs: Dodatkowe parametry
            
        Returns:
            TransformedData: Przetransformowane dane
        """
        transformer = self.get_transformer(destination)
        
        if not transformer:
            result = TransformedData()
            result.destination = destination
            result.errors.append(f"Nieznany typ destinacji: {destination}")
            return result
        
        return transformer.transform(parsed_data, **kwargs)


# Singleton instance
transformer_registry = TransformerRegistry()
