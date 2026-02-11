#!/usr/bin/env python3
"""
Dr.Doc - Data Transformation Tool
Główna aplikacja CLI
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Dodaj src do path
sys.path.insert(0, str(Path(__file__).parent))

from src.parsers import parse_content, detect_format
from src.transformers import transform_data
from src.generators.file_generator import FileGenerator


def load_input(input_path: str = None, stdin: bool = False) -> tuple[str, str]:
    """
    Ładuje dane wejściowe z pliku lub stdin.
    
    Returns:
        tuple: (content, format_hint)
    """
    format_hint = None
    
    if stdin or input_path == '-':
        # Czytaj ze stdin
        content = sys.stdin.read()
        format_hint = None
    elif input_path:
        # Czytaj z pliku
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {input_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Podpowiedź formatu z rozszerzenia
        ext = path.suffix.lstrip('.').lower()
        if ext in ['txt', 'md', 'json', 'php']:
            format_hint = ext
    else:
        raise ValueError("Musisz podać ścieżkę do pliku lub użyć --stdin")
    
    return content, format_hint


def main():
    parser = argparse.ArgumentParser(
        description='Dr.Doc - Narzędzie do transformacji danych według destinacji',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  
  # Podstawowa transformacja
  %(prog)s -i data.txt -d github -o output/
  
  # Auto-detekcja formatu
  %(prog)s -i document.md -d chatgpt
  
  # Ze stdin
  cat data.json | %(prog)s --stdin -d github
  
  # Tylko podgląd (bez generowania plików)
  %(prog)s -i data.txt -d github --preview
  
  # Detekcja formatu
  %(prog)s -i unknown.txt --detect
  
Dostępne destinacje:
  - github         : Struktura repozytorium GitHub
  - chatgpt        : Kontekst dla AI (ChatGPT/Claude)
  - project_brief  : Brief projektowy (TODO)
        """
    )
    
    # Input
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input', 
                            help='Ścieżka do pliku wejściowego')
    input_group.add_argument('--stdin', action='store_true',
                            help='Czytaj dane ze stdin')
    
    # Output
    parser.add_argument('-o', '--output', default='data/output',
                       help='Katalog wyjściowy (domyślnie: data/output)')
    
    # Destinacja
    parser.add_argument('-d', '--destination', 
                       choices=['github', 'chatgpt', 'project_brief'],
                       help='Typ destinacji')
    
    # Format
    parser.add_argument('-f', '--format',
                       choices=['txt', 'md', 'json', 'doc', 'php', 'clipboard'],
                       help='Format wejściowy (opcjonalnie, auto-detect)')
    
    # Opcje
    parser.add_argument('--detect', action='store_true',
                       help='Tylko wykryj format i zakończ')
    parser.add_argument('--preview', action='store_true',
                       help='Tylko podgląd, nie generuj plików')
    parser.add_argument('--project-name',
                       help='Nazwa projektu (dla katalogu wyjściowego)')
    
    # Metadata
    parser.add_argument('--author', help='Autor projektu')
    parser.add_argument('--description', help='Opis projektu')
    parser.add_argument('--license', default='MIT', help='Typ licencji (domyślnie: MIT)')
    
    # Debugging
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Tryb verbose')
    
    args = parser.parse_args()
    
    try:
        # 1. LOAD INPUT
        if args.verbose:
            print("📥 Ładowanie danych wejściowych...")
        
        content, format_hint = load_input(args.input, args.stdin)
        
        # Override format hint jeśli podano
        if args.format:
            format_hint = args.format
        
        if args.verbose:
            print(f"   Rozmiar: {len(content)} znaków")
        
        # 2. DETECT FORMAT
        detected_format, confidence = detect_format(content)
        
        if args.detect:
            print(f"Wykryty format: {detected_format}")
            print(f"Pewność: {confidence:.2%}")
            return 0
        
        if args.verbose:
            print(f"🔍 Wykryty format: {detected_format} (pewność: {confidence:.2%})")
        
        # 3. PARSE
        if args.verbose:
            print("📖 Parsowanie danych...")
        
        parsed = parse_content(content, format_hint or detected_format)
        
        if parsed.errors:
            print("⚠️  Ostrzeżenia podczas parsowania:")
            for error in parsed.errors:
                print(f"   - {error}")
        
        if args.verbose:
            print(f"   Tytuł: {parsed.title or '(brak)'}")
            print(f"   Sekcje: {len(parsed.sections)}")
            print(f"   Bloki kodu: {len(parsed.code_blocks) if parsed.code_blocks else 0}")
        
        # Sprawdź czy podano destinację
        if not args.destination:
            print("❌ Błąd: Musisz podać destinację (-d/--destination)")
            print("   Dostępne: github, chatgpt, project_brief")
            return 1
        
        # 4. TRANSFORM
        if args.verbose:
            print(f"🔄 Transformacja do: {args.destination}")
        
        # Metadata dla transformera
        metadata = {
            'project_name': args.project_name or 'my-project',
            'author': args.author or 'Unknown',
            'description': args.description or 'Project description',
            'license': args.license
        }
        
        transformed = transform_data(args.destination, parsed, metadata=metadata)
        
        if transformed.errors:
            print("❌ Błędy podczas transformacji:")
            for error in transformed.errors:
                print(f"   - {error}")
            return 1
        
        if args.verbose:
            print(f"   Pliki do wygenerowania: {len(transformed.files)}")
        
        # 5. GENERATE lub PREVIEW
        generator = FileGenerator(args.output)
        
        if args.preview:
            # Tylko podgląd
            print("\n" + "=" * 70)
            print(generator.preview(transformed))
            print("=" * 70)
            print("\n📁 Struktura plików:")
            print(generator.get_file_tree(transformed))
        else:
            # Generuj pliki
            if args.verbose:
                print(f"💾 Generowanie plików w: {args.output}")
            
            project_name = args.project_name or f"{args.destination}_output"
            generated = generator.generate(transformed, project_name)
            
            print(f"\n✅ Wygenerowano {len(generated)} plików:")
            for rel_path, abs_path in generated.items():
                print(f"   ✓ {rel_path}")
            
            print(f"\n📂 Lokalizacja: {Path(args.output).absolute() / project_name}")
            
            if args.verbose:
                print("\n📁 Struktura:")
                print(generator.get_file_tree(transformed))
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Błąd: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Błąd: {e}")
        return 1
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
