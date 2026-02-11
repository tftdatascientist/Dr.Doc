"""
Markdown Parser - Parser dla plików Markdown
"""

import re
from typing import Dict, List, Any, Optional
from .base_parser import BaseParser, ParsedData, DataType


class MarkdownParser(BaseParser):
    """Parser dla plików Markdown (.md)"""
    
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'flavor': 'CommonMark',
            'extensions': ['tables', 'strikethrough', 'autolinks'],
            'preserve_structure': True,
            'extract_metadata': True,
            'parse_frontmatter': True
        }
        if config:
            default_config.update(config)
        super().__init__(default_config)
    
    def can_parse(self, content: str) -> float:
        """Wykrywa czy zawartość to Markdown"""
        if not content:
            return 0.0
        
        score = 0.0
        
        # Silne sygnały Markdown
        if re.search(r'^#{1,6}\s+.+', content, re.MULTILINE):
            score += 0.4  # Nagłówki ATX
        
        if re.search(r'\*\*[^*]+\*\*|\*[^*]+\*', content):
            score += 0.2  # Bold/italic
        
        if re.search(r'^[-*+]\s+', content, re.MULTILINE):
            score += 0.15  # Listy
        
        if re.search(r'```[\s\S]+?```', content):
            score += 0.2  # Code blocks
        
        if re.search(r'\[.+?\]\(.+?\)', content):
            score += 0.15  # Linki
        
        if re.search(r'^>\s+', content, re.MULTILINE):
            score += 0.1  # Cytaty
        
        # Jeśli są 3+ charakterystyczne elementy MD
        return min(score, 1.0)
    
    def parse(self, content: str, **kwargs) -> ParsedData:
        """Parsuje plik Markdown"""
        is_valid, errors = self.validate(content)
        
        result = ParsedData(
            format="md",
            data_type=DataType.TEXT,
            content=content,
            errors=errors
        )
        
        if not is_valid:
            return result
        
        # Statystyki
        result.stats = self.calculate_stats(content)
        
        # Front matter (YAML metadata na początku)
        if self.config.get('parse_frontmatter', True):
            content, frontmatter = self._extract_frontmatter(content)
            if frontmatter:
                result.metadata.update(frontmatter)
        
        # Nagłówki
        result.headers = self._extract_headers(content)
        result.title = result.headers[0]['text'] if result.headers else None
        
        # Sekcje (oparte na nagłówkach)
        result.sections = self._create_sections(content, result.headers)
        
        # Paragrafy
        result.paragraphs = self._extract_paragraphs(content)
        
        # Listy
        result.lists = self._extract_lists(content)
        
        # Bloki kodu
        result.code_blocks = self._extract_code_blocks(content)
        
        # Tabele
        result.tables = self._extract_tables(content)
        
        # Linki
        result.links = self._extract_links(content)
        
        # Obrazy
        result.images = self._extract_images(content)
        
        # Metadane dodatkowe
        result.metadata.update({
            'header_count': len(result.headers),
            'code_block_count': len(result.code_blocks),
            'table_count': len(result.tables),
            'link_count': len(result.links),
            'image_count': len(result.images)
        })
        
        return result
    
    def _extract_frontmatter(self, content: str) -> tuple[str, Dict[str, Any]]:
        """Wydobywa YAML front matter z początku dokumentu"""
        frontmatter = {}
        
        # Sprawdź czy dokument zaczyna się od ---
        if not content.startswith('---'):
            return content, frontmatter
        
        # Znajdź zamykające ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return content, frontmatter
        
        yaml_content = match.group(1)
        remaining_content = content[match.end():]
        
        # Proste parsowanie YAML (key: value)
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        
        return remaining_content, frontmatter
    
    def _extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Wydobywa nagłówki Markdown"""
        headers = []
        
        # ATX style headers (# ## ###)
        for match in re.finditer(r'^(#{1,6})\s+(.+?)(?:\s+#*)?$', content, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            
            headers.append({
                'text': text,
                'level': level,
                'position': match.start(),
                'style': 'atx'
            })
        
        return headers
    
    def _create_sections(self, content: str, headers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tworzy sekcje na podstawie nagłówków"""
        if not headers:
            return [{
                'title': None,
                'level': 0,
                'content': content
            }]
        
        sections = []
        
        for i, header in enumerate(headers):
            start_pos = header['position']
            end_pos = headers[i + 1]['position'] if i + 1 < len(headers) else len(content)
            
            section_content = content[start_pos:end_pos].strip()
            
            # Usuń sam nagłówek z zawartości sekcji
            section_lines = section_content.split('\n')
            if section_lines:
                section_lines = section_lines[1:]  # Pomijamy pierwszą linię (nagłówek)
            section_content = '\n'.join(section_lines).strip()
            
            sections.append({
                'title': header['text'],
                'level': header['level'],
                'content': section_content
            })
        
        return sections
    
    def _extract_paragraphs(self, content: str) -> List[str]:
        """Wydobywa paragrafy"""
        # Usuń code blocks, nagłówki, listy
        cleaned = content
        cleaned = re.sub(r'```[\s\S]+?```', '', cleaned)  # Code blocks
        cleaned = re.sub(r'^#{1,6}\s+.+$', '', cleaned, flags=re.MULTILINE)  # Headers
        cleaned = re.sub(r'^[-*+]\s+.+$', '', cleaned, flags=re.MULTILINE)  # Lists
        cleaned = re.sub(r'^\d+\.\s+.+$', '', cleaned, flags=re.MULTILINE)  # Numbered lists
        
        # Podziel na paragrafy (rozdzielone pustymi liniami)
        paragraphs = []
        for para in re.split(r'\n\s*\n', cleaned):
            para = para.strip()
            if para and len(para) > 10:  # Minimum 10 znaków
                paragraphs.append(para)
        
        return paragraphs
    
    def _extract_lists(self, content: str) -> List[Dict[str, Any]]:
        """Wydobywa listy"""
        lists = []
        
        # Listy punktowane (-, *, +)
        bullet_pattern = r'^([-*+])\s+(.+)$'
        current_list = []
        
        for line in content.split('\n'):
            match = re.match(bullet_pattern, line.strip())
            if match:
                current_list.append(match.group(2))
            elif current_list:
                lists.append({'type': 'bullet', 'items': current_list})
                current_list = []
        
        if current_list:
            lists.append({'type': 'bullet', 'items': current_list})
        
        # Listy numerowane
        numbered_pattern = r'^(\d+)\.\s+(.+)$'
        current_list = []
        
        for line in content.split('\n'):
            match = re.match(numbered_pattern, line.strip())
            if match:
                current_list.append(match.group(2))
            elif current_list:
                lists.append({'type': 'numeric', 'items': current_list})
                current_list = []
        
        if current_list:
            lists.append({'type': 'numeric', 'items': current_list})
        
        return lists
    
    def _extract_code_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Wydobywa bloki kodu"""
        code_blocks = []
        
        # Fenced code blocks (```)
        pattern = r'```(\w*)\n([\s\S]+?)```'
        for match in re.finditer(pattern, content):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            
            code_blocks.append({
                'language': language,
                'code': code,
                'position': match.start()
            })
        
        return code_blocks
    
    def _extract_tables(self, content: str) -> List[Dict[str, Any]]:
        """Wydobywa tabele Markdown"""
        tables = []
        
        # Pattern dla tabeli (uproszczony)
        table_pattern = r'(\|.+\|\n\|[-:\s|]+\|\n(?:\|.+\|\n?)+)'
        
        for match in re.finditer(table_pattern, content):
            table_text = match.group(1)
            lines = [l.strip() for l in table_text.split('\n') if l.strip()]
            
            if len(lines) < 2:
                continue
            
            # Parsuj nagłówki
            headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
            
            # Parsuj wiersze
            rows = []
            for line in lines[2:]:  # Pomijamy separator
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if cells:
                    rows.append(cells)
            
            tables.append({
                'headers': headers,
                'rows': rows,
                'position': match.start()
            })
        
        return tables
    
    def _extract_links(self, content: str) -> List[Dict[str, str]]:
        """Wydobywa linki"""
        links = []
        
        # Inline links [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(pattern, content):
            links.append({
                'text': match.group(1),
                'url': match.group(2),
                'type': 'inline'
            })
        
        return links
    
    def _extract_images(self, content: str) -> List[Dict[str, str]]:
        """Wydobywa obrazy"""
        images = []
        
        # Images ![alt](url)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(pattern, content):
            images.append({
                'alt': match.group(1),
                'url': match.group(2)
            })
        
        return images
