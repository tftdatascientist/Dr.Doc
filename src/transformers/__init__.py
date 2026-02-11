"""
Transformer Manager
Inicjalizuje transformery i zapewnia łatwy dostęp
"""

from .base_transformer import transformer_registry, TransformedData
from .github_transformer import GitHubTransformer
from .chatgpt_transformer import ChatGPTTransformer
from ..parsers.base_parser import ParsedData


def init_transformers():
    """Inicjalizuje i rejestruje wszystkie transformery"""
    transformer_registry.register('github', GitHubTransformer())
    transformer_registry.register('chatgpt', ChatGPTTransformer())
    # PROJECT_BRIEF będzie dodany później


def transform_data(destination: str, parsed_data: ParsedData, **kwargs) -> TransformedData:
    """
    Główna funkcja transformująca dane.
    
    Args:
        destination: Typ destinacji ('github', 'chatgpt', 'project_brief')
        parsed_data: Sparsowane dane
        **kwargs: Dodatkowe parametry dla transformera
        
    Returns:
        TransformedData: Przetransformowane dane
    """
    # Upewnij się że transformery są zainicjalizowane
    if not transformer_registry.list_destinations():
        init_transformers()
    
    return transformer_registry.transform(destination, parsed_data, **kwargs)


# Inicjalizuj transformery przy imporcie
init_transformers()


__all__ = [
    'transform_data',
    'transformer_registry',
    'TransformedData',
    'GitHubTransformer',
    'ChatGPTTransformer'
]
