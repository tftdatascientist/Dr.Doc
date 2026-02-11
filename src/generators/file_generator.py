"""
File Generator
Generuje pliki fizyczne z przetransformowanych danych
"""

import os
from pathlib import Path
from typing import Dict, List
from ..transformers.base_transformer import TransformedData


class FileGenerator:
    """Klasa generująca pliki wyjściowe"""
    
    def __init__(self, output_dir: str = "data/output"):
        """
        Args:
            output_dir: Katalog wyjściowy dla plików
        """
        self.output_dir = Path(output_dir)
    
    def generate(self, transformed_data: TransformedData, 
                 project_name: str = None) -> Dict[str, str]:
        """
        Generuje pliki z przetransformowanych danych.
        
        Args:
            transformed_data: Dane po transformacji
            project_name: Nazwa projektu (używana jako subdirectory)
            
        Returns:
            Dict: Mapowanie {ścieżka_względna: ścieżka_absolutna} wygenerowanych plików
        """
        if not project_name:
            project_name = f"project_{transformed_data.destination}"
        
        # Utwórz katalog projektu
        project_dir = self.output_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        
        # Generuj każdy plik
        for rel_path, content in transformed_data.files.items():
            file_path = project_dir / rel_path
            
            # Utwórz katalogi jeśli potrzebne
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Zapisz plik
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files[rel_path] = str(file_path.absolute())
        
        return generated_files
    
    def generate_structure_only(self, transformed_data: TransformedData,
                                project_name: str = None) -> List[str]:
        """
        Generuje tylko strukturę katalogów bez plików.
        
        Args:
            transformed_data: Dane po transformacji
            project_name: Nazwa projektu
            
        Returns:
            List: Lista utworzonych katalogów
        """
        if not project_name:
            project_name = f"project_{transformed_data.destination}"
        
        project_dir = self.output_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        created_dirs = [str(project_dir.absolute())]
        
        # Utwórz katalogi ze struktury
        if transformed_data.structure:
            for dir_name in transformed_data.structure.keys():
                if dir_name.endswith('/'):
                    dir_path = project_dir / dir_name.rstrip('/')
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(dir_path.absolute()))
        
        return created_dirs
    
    def preview(self, transformed_data: TransformedData) -> str:
        """
        Generuje podgląd struktury plików jako tekst.
        
        Args:
            transformed_data: Dane po transformacji
            
        Returns:
            str: Podgląd struktury plików
        """
        preview = f"Preview for destination: {transformed_data.destination}\n"
        preview += "=" * 60 + "\n\n"
        
        if transformed_data.errors:
            preview += "⚠️  ERRORS:\n"
            for error in transformed_data.errors:
                preview += f"  - {error}\n"
            preview += "\n"
        
        preview += "📁 File Structure:\n"
        preview += "-" * 60 + "\n"
        
        # Sortuj pliki
        sorted_files = sorted(transformed_data.files.keys())
        
        for file_path in sorted_files:
            content = transformed_data.files[file_path]
            size = len(content)
            lines = content.count('\n') + 1
            
            preview += f"  {file_path}\n"
            preview += f"    Size: {size} bytes, Lines: {lines}\n"
        
        preview += "\n"
        preview += f"📊 Metadata:\n"
        preview += "-" * 60 + "\n"
        for key, value in transformed_data.metadata.items():
            preview += f"  {key}: {value}\n"
        
        return preview
    
    def get_file_tree(self, transformed_data: TransformedData) -> str:
        """
        Generuje drzewiastą reprezentację struktury plików.
        
        Args:
            transformed_data: Dane po transformacji
            
        Returns:
            str: ASCII tree struktura
        """
        files = sorted(transformed_data.files.keys())
        
        # Buduj drzewo
        tree = {}
        for file_path in files:
            parts = file_path.split('/')
            current = tree
            
            for part in parts[:-1]:  # Katalogi
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Plik (liść)
            current[parts[-1]] = None
        
        # Konwertuj na string
        def render_tree(node: dict, prefix: str = "", is_last: bool = True) -> str:
            result = ""
            items = sorted(node.items())
            
            for i, (name, children) in enumerate(items):
                is_last_item = (i == len(items) - 1)
                connector = "└── " if is_last_item else "├── "
                
                result += prefix + connector + name
                
                if children is not None:  # Katalog
                    result += "/\n"
                    extension = "    " if is_last_item else "│   "
                    result += render_tree(children, prefix + extension, is_last_item)
                else:  # Plik
                    result += "\n"
            
            return result
        
        return ".\n" + render_tree(tree)
