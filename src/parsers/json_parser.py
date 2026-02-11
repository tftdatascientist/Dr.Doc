"""
JSON Parser - Parser dla plików JSON
"""

import json
import re
from typing import Dict, List, Any
from .base_parser import BaseParser, ParsedData, DataType


class JsonParser(BaseParser):
    """Parser dla plików JSON"""
    
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'strict_mode': True,
            'allow_comments': False,
            'preserve_order': True,
            'parse_numbers_as_strings': False,
            'max_depth': 100
        }
        if config:
            default_config.update(config)
        super().__init__(default_config)
    
    def can_parse(self, content: str) -> float:
        """Wykrywa czy zawartość to JSON"""
        if not content:
            return 0.0
        
        stripped = content.strip()
        
        # Musi zaczynać się od { lub [
        if not (stripped.startswith('{') or stripped.startswith('[')):
            return 0.0
        
        # Spróbuj sparsować
        try:
            json.loads(stripped)
            return 1.0  # Pełna pewność - poprawny JSON
        except json.JSONDecodeError:
            # Może być JSON z komentarzami lub błędami
            if self.config.get('allow_comments', False):
                try:
                    cleaned = self._remove_comments(stripped)
                    json.loads(cleaned)
                    return 0.9  # Prawdopodobnie JSON z komentarzami
                except:
                    pass
            
            # Sprawdź czy ma charakterystyczne cechy JSON
            has_quotes = '"' in stripped
            has_colons = ':' in stripped
            has_braces = '{' in stripped or '[' in stripped
            
            if has_quotes and has_colons and has_braces:
                return 0.5  # Może być uszkodzonym JSON
            
            return 0.0
    
    def parse(self, content: str, **kwargs) -> ParsedData:
        """Parsuje JSON"""
        is_valid, errors = self.validate(content)
        
        result = ParsedData(
            format="json",
            data_type=DataType.STRUCTURED,
            content=content,
            errors=errors
        )
        
        if not is_valid:
            return result
        
        # Statystyki
        result.stats = self.calculate_stats(content)
        
        # Usuń komentarze jeśli dozwolone
        cleaned_content = content
        if self.config.get('allow_comments', False):
            cleaned_content = self._remove_comments(content)
        
        # Parsowanie JSON
        try:
            parsed = json.loads(cleaned_content)
            result.raw_structure = parsed
            
            # Analiza struktury
            result.metadata = self._analyze_structure(parsed)
            
            # Ekstrakcja typowych pól
            if isinstance(parsed, dict):
                # Tytuł z typowych pól
                for title_field in ['title', 'name', 'label', 'id']:
                    if title_field in parsed:
                        result.title = str(parsed[title_field])
                        break
                
                # Metadata
                if 'metadata' in parsed and isinstance(parsed['metadata'], dict):
                    result.metadata.update(parsed['metadata'])
                
                # Tworzenie sekcji z top-level keys
                for key, value in parsed.items():
                    result.sections.append({
                        'title': key,
                        'level': 1,
                        'content': json.dumps(value, indent=2),
                        'data': value
                    })
            
            elif isinstance(parsed, list):
                # Lista - każdy element to sekcja
                for i, item in enumerate(parsed):
                    title = f"Item {i + 1}"
                    if isinstance(item, dict) and 'name' in item:
                        title = item['name']
                    
                    result.sections.append({
                        'title': title,
                        'level': 1,
                        'content': json.dumps(item, indent=2),
                        'data': item
                    })
            
            result.confidence = 1.0
            
        except json.JSONDecodeError as e:
            result.errors.append(f"JSON parsing error: {str(e)}")
            result.confidence = 0.0
        
        return result
    
    def _remove_comments(self, content: str) -> str:
        """Usuwa komentarze // i /* */ z JSON"""
        # Usuń komentarze jednoliniowe //
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        
        # Usuń komentarze wieloliniowe /* */
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        return content
    
    def _analyze_structure(self, obj: Any, depth: int = 0) -> Dict[str, Any]:
        """Analizuje strukturę JSON"""
        if depth > self.config.get('max_depth', 100):
            return {'error': 'Max depth exceeded'}
        
        result = {
            'type': type(obj).__name__,
            'depth': depth
        }
        
        if isinstance(obj, dict):
            result['keys'] = list(obj.keys())
            result['key_count'] = len(obj)
            result['nested_structures'] = {}
            
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    result['nested_structures'][key] = self._analyze_structure(value, depth + 1)
        
        elif isinstance(obj, list):
            result['length'] = len(obj)
            if obj:
                result['item_types'] = list(set(type(item).__name__ for item in obj))
                # Analiza pierwszego elementu jako reprezentatywnego
                if isinstance(obj[0], (dict, list)):
                    result['item_structure'] = self._analyze_structure(obj[0], depth + 1)
        
        elif isinstance(obj, (str, int, float, bool, type(None))):
            result['value'] = obj if not isinstance(obj, str) or len(str(obj)) < 100 else str(obj)[:100] + '...'
        
        return result
    
    def get_value_by_path(self, parsed_data: ParsedData, path: str) -> Any:
        """
        Pobiera wartość z JSON po ścieżce (JSON Path style).
        
        Args:
            parsed_data: Sparsowane dane
            path: Ścieżka np. "data.users[0].name"
            
        Returns:
            Wartość pod wskazaną ścieżką lub None
        """
        if not parsed_data.raw_structure:
            return None
        
        obj = parsed_data.raw_structure
        parts = path.replace('[', '.').replace(']', '').split('.')
        
        for part in parts:
            if not part:
                continue
            
            try:
                if isinstance(obj, dict):
                    obj = obj.get(part)
                elif isinstance(obj, list):
                    obj = obj[int(part)]
                else:
                    return None
                
                if obj is None:
                    return None
            except (KeyError, IndexError, ValueError):
                return None
        
        return obj
    
    def flatten(self, parsed_data: ParsedData, separator: str = '.') -> Dict[str, Any]:
        """
        Spłaszcza zagnieżdżoną strukturę JSON do płaskiego słownika.
        
        Args:
            parsed_data: Sparsowane dane
            separator: Separator dla kluczy (domyślnie '.')
            
        Returns:
            Płaski słownik
        """
        if not parsed_data.raw_structure:
            return {}
        
        def _flatten(obj, parent_key=''):
            items = []
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_key = f"{parent_key}{separator}{key}" if parent_key else key
                    if isinstance(value, (dict, list)):
                        items.extend(_flatten(value, new_key).items())
                    else:
                        items.append((new_key, value))
            
            elif isinstance(obj, list):
                for i, value in enumerate(obj):
                    new_key = f"{parent_key}[{i}]"
                    if isinstance(value, (dict, list)):
                        items.extend(_flatten(value, new_key).items())
                    else:
                        items.append((new_key, value))
            
            return dict(items)
        
        return _flatten(parsed_data.raw_structure)
    
    def to_csv(self, parsed_data: ParsedData) -> str:
        """
        Konwertuje JSON do CSV (dla prostych struktur).
        
        Args:
            parsed_data: Sparsowane dane
            
        Returns:
            String w formacie CSV
        """
        import csv
        from io import StringIO
        
        if not parsed_data.raw_structure:
            return ""
        
        obj = parsed_data.raw_structure
        
        # Obsługa listy obiektów
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=obj[0].keys())
            writer.writeheader()
            writer.writerows(obj)
            return output.getvalue()
        
        # Obsługa pojedynczego obiektu
        elif isinstance(obj, dict):
            flat = self.flatten(parsed_data)
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Key', 'Value'])
            for key, value in flat.items():
                writer.writerow([key, value])
            return output.getvalue()
        
        return ""
