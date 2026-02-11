"""
ChatGPT Context Transformer
Optymalizuje dane jako kontekst dla AI (ChatGPT/Claude/etc.)
"""

from typing import Dict, Any
from .base_transformer import BaseTransformer, TransformedData
from ..parsers.base_parser import ParsedData


class ChatGPTTransformer(BaseTransformer):
    """Transformer optymalizujący dane jako kontekst AI"""
    
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'max_tokens': 4000,
            'optimize_tokens': True,
            'include_examples': True,
            'verbosity': 'concise',
            'structure_type': 'auto',
            'add_emojis': True,
            'code_block_limit': 50,
            'summarize_long_sections': True
        }
        if config:
            default_config.update(config)
        super().__init__(default_config)
    
    def get_destination_type(self) -> str:
        return "chatgpt"
    
    def transform(self, parsed_data: ParsedData, **kwargs) -> TransformedData:
        """Transformuje dane do kontekstu AI"""
        result = TransformedData()
        result.destination = "chatgpt"
        
        # Walidacja
        is_valid, errors = self.validate_input(parsed_data)
        if not is_valid:
            result.errors = errors
            return result
        
        # Typ kontekstu
        context_type = kwargs.get('context_type', 'general')
        
        # Generuj kontekst
        if context_type == 'code':
            context = self._generate_code_context(parsed_data, **kwargs)
        elif context_type == 'project_brief':
            context = self._generate_project_context(parsed_data, **kwargs)
        elif context_type == 'debug':
            context = self._generate_debug_context(parsed_data, **kwargs)
        else:
            context = self._generate_general_context(parsed_data, **kwargs)
        
        result.add_file('context.md', context)
        
        # Statystyki
        token_estimate = self._estimate_tokens(context)
        result.metadata = {
            'context_type': context_type,
            'token_estimate': token_estimate,
            'optimized': self.config.get('optimize_tokens', True)
        }
        
        return result
    
    def _generate_general_context(self, data: ParsedData, **kwargs) -> str:
        """Generuje ogólny kontekst AI"""
        title = data.title or "Context"
        
        context = f"# {title}\n\n"
        
        # Cel (jeśli podany)
        if 'goal' in kwargs:
            context += f"## 🎯 Cel\n\n{kwargs['goal']}\n\n"
        
        # Dane wejściowe
        context += "## 📊 Dane\n\n"
        
        # Jeśli są sekcje, użyj ich
        if data.sections:
            for section in data.sections:
                context += f"### {section['title']}\n\n"
                content = section['content']
                
                # Skróć długie sekcje
                if self.config.get('summarize_long_sections', True) and len(content) > 500:
                    content = content[:500] + "\n\n[...treść skrócona...]"
                
                context += f"{content}\n\n"
        else:
            # Bez sekcji - użyj paragrafów
            for para in data.paragraphs[:5]:  # Max 5 paragrafów
                context += f"{para}\n\n"
        
        # Code blocks
        if data.code_blocks and self.config.get('include_examples', True):
            context += "## 💻 Kod\n\n"
            for i, block in enumerate(data.code_blocks[:3]):  # Max 3 bloki
                lang = block.get('language', 'text')
                code = block['code']
                
                # Ogranicz długość kodu
                if len(code) > self.config.get('code_block_limit', 50) * 10:
                    code = code[:self.config.get('code_block_limit', 50) * 10] + "\n// ..."
                
                context += f"```{lang}\n{code}\n```\n\n"
        
        # Wymagania (jeśli podane)
        if 'requirements' in kwargs:
            context += f"## 🔧 Wymagania\n\n{kwargs['requirements']}\n\n"
        
        # Metadata na końcu
        context += "\n---\n\n"
        context += f"**Meta**: Format: {data.format}, Type: {data.data_type.value}\n"
        
        return context
    
    def _generate_code_context(self, data: ParsedData, **kwargs) -> str:
        """Generuje kontekst dla kodu"""
        context = "# CODE CONTEXT\n\n"
        
        # Cel
        if 'goal' in kwargs:
            context += f"## Cel\n\n{kwargs['goal']}\n\n"
        
        # Obecna implementacja
        if data.code_blocks:
            context += "## Obecna implementacja\n\n"
            for block in data.code_blocks:
                context += f"```{block['language']}\n{block['code']}\n```\n\n"
        
        # Problem/Zadanie
        if 'problem' in kwargs:
            context += f"## Problem\n\n{kwargs['problem']}\n\n"
        
        # Wymagania
        if 'requirements' in kwargs:
            reqs = kwargs['requirements']
            if isinstance(reqs, list):
                context += "## Wymagania\n\n"
                for i, req in enumerate(reqs, 1):
                    context += f"{i}. {req}\n"
            else:
                context += f"## Wymagania\n\n{reqs}\n"
            context += "\n"
        
        return context
    
    def _generate_project_context(self, data: ParsedData, **kwargs) -> str:
        """Generuje kontekst projektu (brief)"""
        project_name = kwargs.get('project_name', data.title or 'Project')
        
        context = f"# PROJECT: {project_name}\n\n"
        
        # Typ projektu
        if 'project_type' in kwargs:
            context += f"**Typ**: {kwargs['project_type']}\n\n"
        
        # Technologie
        if 'technologies' in kwargs:
            context += f"**Technologie**: {kwargs['technologies']}\n\n"
        
        # Cel biznesowy
        if 'business_goal' in kwargs:
            context += f"## Cel biznesowy\n\n{kwargs['business_goal']}\n\n"
        
        # Funkcje główne
        if data.lists:
            context += "## Funkcje główne\n\n"
            for item in data.lists[0]['items']:
                context += f"- {item}\n"
            context += "\n"
        
        # Wymagania techniczne
        if 'tech_requirements' in kwargs:
            context += f"## Wymagania techniczne\n\n{kwargs['tech_requirements']}\n\n"
        
        # Constraints
        if 'constraints' in kwargs:
            context += f"## Ograniczenia\n\n{kwargs['constraints']}\n\n"
        
        return context
    
    def _generate_debug_context(self, data: ParsedData, **kwargs) -> str:
        """Generuje kontekst debugowania"""
        context = "# DEBUG CONTEXT\n\n"
        
        # Błąd
        if 'error' in kwargs:
            context += f"## Błąd\n\n```\n{kwargs['error']}\n```\n\n"
        
        # Kod problematyczny
        if data.code_blocks:
            context += "## Kod\n\n"
            for block in data.code_blocks:
                context += f"```{block['language']}\n{block['code']}\n```\n\n"
        
        # Środowisko
        if 'environment' in kwargs:
            context += f"## Środowisko\n\n{kwargs['environment']}\n\n"
        
        # Kroki do reprodukcji
        if 'steps' in kwargs:
            context += "## Kroki do reprodukcji\n\n"
            if isinstance(kwargs['steps'], list):
                for i, step in enumerate(kwargs['steps'], 1):
                    context += f"{i}. {step}\n"
            else:
                context += kwargs['steps']
            context += "\n"
        
        # Oczekiwane vs aktualne
        if 'expected' in kwargs:
            context += f"## Oczekiwane zachowanie\n\n{kwargs['expected']}\n\n"
        
        if 'actual' in kwargs:
            context += f"## Aktualne zachowanie\n\n{kwargs['actual']}\n\n"
        
        return context
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Szacuje liczbę tokenów (przybliżenie).
        ~4 znaki = 1 token dla języka angielskiego
        ~3 znaki = 1 token dla języka polskiego (więcej znaków diakrytycznych)
        """
        # Proste przybliżenie
        return len(text) // 4
    
    def optimize_for_tokens(self, text: str, max_tokens: int) -> str:
        """Optymalizuje tekst do limitu tokenów"""
        estimated = self._estimate_tokens(text)
        
        if estimated <= max_tokens:
            return text
        
        # Przytnij do odpowiedniej długości
        target_chars = max_tokens * 4
        return text[:target_chars] + "\n\n[...treść przycięta do limitu tokenów...]"
