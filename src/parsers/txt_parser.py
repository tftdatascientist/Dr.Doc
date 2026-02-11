"""
TXT Parser - Parser dla prostych plików tekstowych
"""

import re
from typing import Dict, List, Any
from .base_parser import BaseParser, ParsedData, DataType


class TxtParser(BaseParser):
    """Parser dla plików tekstowych (.txt)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'encoding': 'utf-8',
            'detect_headers': True,
            'first_line_as_title': False,
            'preserve_formatting': True,
            'line_ending': 'auto'
        }
        if config:
            default_config.update(config)
        super().__init__(default_config)
    
    def can_parse(self, content: str) -> float:
        """
        TXT może obsłużyć wszystko, ale z niskim priorytetem.
        Zwraca 0.3 jako fallback parser.
        """
        if not content:
            return 0.0
        
        # TXT jest fallback'iem - niski priorytet
        # Ale jeśli nie ma żadnych specjalnych znaczników, to pewnie TXT
        has_markdown = bool(re.search(r'^#{1,6}\s', content, re.MULTILINE))
        has_json = content.strip().startswith('{') or content.strip().startswith('[')
        has_xml = bool(re.search(r'<[^>]+>', content))
        has_code_syntax = bool(re.search(r'(function|class|def|import|const|var)\s+\w+', content))
        
        # Jeśli nie ma żadnych specjalnych znaczników, prawdopodobnie to TXT
        if not (has_markdown or has_json or has_xml or has_code_syntax):
            return 0.6
        
        return 0.3  # Niski priorytet jako fallback
    
    def parse(self, content: str, **kwargs) -> ParsedData:
        """Parsuje plik tekstowy"""
        is_valid, errors = self.validate(content)
        
        result = ParsedData(
            format="txt",
            data_type=DataType.TEXT,
            content=content,
            errors=errors
        )
        
        if not is_valid:
            return result
        
        # Statystyki
        result.stats = self.calculate_stats(content)
        
        # Wykrywanie tytułu (pierwsza linia lub CAPS)
        result.title = self._extract_title(content)
        
        # Wykrywanie nagłówków
        if self.config.get('detect_headers', True):
            result.headers = self._extract_headers(content)
        
        # Wykrywanie paragrafów
        result.paragraphs = self._extract_paragraphs(content)
        
        # Wykrywanie list
        result.lists = self._extract_lists(content)
        
        # Tworzenie sekcji
        result.sections = self._create_sections(content, result.headers)
        
        # Metadane
        result.metadata = {
            'has_headers': len(result.headers) > 0,
            'has_lists': len(result.lists) > 0,
            'paragraph_count': len(result.paragraphs)
        }
        
        return result
    
    def _extract_title(self, content: str) -> str:
        """Wydobywa tytuł z tekstu"""
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        if not lines:
            return None
        
        first_line = lines[0]
        
        # Jeśli konfiguracja mówi, że pierwsza linia to tytuł
        if self.config.get('first_line_as_title', False):
            return first_line
        
        # Jeśli pierwsza linia jest w CAPS i krótsza niż 100 znaków
        if first_line.isupper() and len(first_line) < 100:
            return first_line
        
        # Jeśli pierwsza linia kończy się dwukropkiem
        if first_line.endswith(':') and len(first_line) < 100:
            return first_line.rstrip(':')
        
        return None
    
    def _extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Wykrywa nagłówki w tekście"""
        headers = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            
            # WIELKIE LITERY (całe słowa kapitalikami)
            if stripped.isupper() and len(stripped) < 100 and len(stripped.split()) > 1:
                headers.append({
                    'text': stripped,
                    'level': 1,
                    'line': i + 1,
                    'type': 'uppercase'
                })
            
            # Linia kończy się dwukropkiem
            elif stripped.endswith(':') and not stripped.endswith('::'):
                headers.append({
                    'text': stripped.rstrip(':'),
                    'level': 2,
                    'line': i + 1,
                    'type': 'colon'
                })
        
        return headers
    
    def _extract_paragraphs(self, content: str) -> List[str]:
        """Wydobywa paragrafy (tekst oddzielony pustymi liniami)"""
        paragraphs = []
        current_paragraph = []
        
        for line in content.split('\n'):
            stripped = line.strip()
            
            # Pusta linia - koniec paragrafu
            if not stripped:
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
            else:
                # Pomijamy linie które wyglądają jak nagłówki lub listy
                if not self._is_header_line(line) and not self._is_list_item(line):
                    current_paragraph.append(stripped)
        
        # Ostatni paragraf
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return paragraphs
    
    def _extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Wykrywa listy w tekście"""
        lists = []
        current_list = []
        current_list_type = None
        
        list_markers = {
            'bullet': ['-', '*', '•', '◦', '▪', '▫'],
            'numeric': r'^\d+[\.\)]\s'
        }
        
        for line in content.split('\n'):
            stripped = line.strip()
            
            if self._is_list_item(stripped):
                item_type, item_text = self._parse_list_item(stripped)
                
                # Nowa lista lub kontynuacja
                if current_list_type is None or current_list_type == item_type:
                    current_list_type = item_type
                    current_list.append(item_text)
                else:
                    # Inna lista - zapisz poprzednią
                    if current_list:
                        lists.append({
                            'type': current_list_type,
                            'items': current_list
                        })
                    current_list = [item_text]
                    current_list_type = item_type
            else:
                # Koniec listy
                if current_list:
                    lists.append({
                        'type': current_list_type,
                        'items': current_list
                    })
                    current_list = []
                    current_list_type = None
        
        # Ostatnia lista
        if current_list:
            lists.append({
                'type': current_list_type,
                'items': current_list
            })
        
        return lists
    
    def _is_header_line(self, line: str) -> bool:
        """Sprawdza czy linia to nagłówek"""
        stripped = line.strip()
        return (stripped.isupper() or stripped.endswith(':')) and len(stripped) < 100
    
    def _is_list_item(self, line: str) -> bool:
        """Sprawdza czy linia to element listy"""
        stripped = line.strip()
        if not stripped:
            return False
        
        # Bullet points
        if stripped[0] in ['-', '*', '•', '◦', '▪', '▫']:
            return True
        
        # Numerowane
        if re.match(r'^\d+[\.\)]\s', stripped):
            return True
        
        return False
    
    def _parse_list_item(self, line: str) -> tuple:
        """Parsuje element listy i zwraca (typ, tekst)"""
        stripped = line.strip()
        
        # Bullet
        if stripped[0] in ['-', '*', '•', '◦', '▪', '▫']:
            return 'bullet', stripped[1:].strip()
        
        # Numerowane
        match = re.match(r'^(\d+[\.\)])\s+(.+)$', stripped)
        if match:
            return 'numeric', match.group(2)
        
        return 'unknown', stripped
    
    def _create_sections(self, content: str, headers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tworzy sekcje na podstawie nagłówków"""
        if not headers:
            # Brak nagłówków - cała zawartość to jedna sekcja
            return [{
                'title': None,
                'level': 0,
                'content': content
            }]
        
        sections = []
        lines = content.split('\n')
        
        for i, header in enumerate(headers):
            start_line = header['line']
            end_line = headers[i + 1]['line'] if i + 1 < len(headers) else len(lines)
            
            section_lines = lines[start_line:end_line]
            section_content = '\n'.join(section_lines).strip()
            
            sections.append({
                'title': header['text'],
                'level': header['level'],
                'content': section_content
            })
        
        return sections
