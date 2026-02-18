# 🩺 Dr.Doc - Data Transformation Tool

> **Narzędzie do inteligentnej transformacji danych według ich docelowego miejsca wykorzystania**

Dr.Doc to potężne narzędzie dostępne jako **aplikacja CLI** oraz **Web UI**, które automatycznie przekształca dane z różnych formatów wejściowych (TXT, Markdown, JSON) do optymalnych struktur dostosowanych do konkretnego celu użycia (GitHub Repository, ChatGPT Context, Project Brief).

## 🎯 Problem

Często mamy dane w jednym formacie, ale potrzebujemy ich w zupełnie innej strukturze:
- Dokumentacja projektowa → Repozytorium GitHub
- Notatki → Kontekst dla AI
- Różne pliki → Spójny Project Brief

**Dr.Doc rozwiązuje ten problem automatycznie!**

## ✨ Funkcje

### 📥 DATA IN - Wiele formatów wejściowych
- **TXT** - Proste pliki tekstowe
- **Markdown** - Pełne parsowanie MD z nagłówkami, listami, kodem
- **JSON** - Strukturalne dane JSON
- **DOC** - Dokumenty Word (planned)
- **PHP** - Pliki PHP/konfiguracje (planned)
- **Clipboard** - Kopiuj/wklej z auto-detekcją (planned)

### 🔄 TRANSFORMATION - Inteligentne przetwarzanie
- Auto-detekcja formatu wejściowego
- Ekstrakcja struktury (nagłówki, sekcje, kod)
- Mapowanie danych do struktury docelowej
- Optymalizacja treści

### 📤 DATA OUT - Dostosowane destinacje
- **GitHub** - Pełna struktura repo (README, docs/, src/, LICENSE)
- **ChatGPT** - Zoptymalizowany kontekst dla AI
- **Project Brief** - Profesjonalny brief projektowy (planned)

## 🚀 Szybki Start

### Wymagania
- Python 3.7+

### Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/tftdatascientist/Dr.Doc.git
cd Dr.Doc

# Opcjonalnie: Zainstaluj Flask dla Web UI
pip install -r requirements.txt
```

### Użycie - Web UI 🌐

**Najprostszy sposób - interfejs graficzny w przeglądarce!**

```bash
# Uruchom serwer
python3 web/app.py

# Otwórz w przeglądarce
# http://localhost:5000
```

**Funkcje Web UI:**
- 📝 Wklejanie tekstu lub upload pliku
- 🔍 Auto-detekcja formatu
- 🎯 Wybór destinacji (wizualne karty)
- ⚙️ Konfiguracja opcji (nazwa, autor, licencja)
- 👁️ Podgląd wyników w czasie rzeczywistym
- 📊 Wizualizacja struktury plików
- 💾 Tryb preview lub generowanie plików

### Użycie - CLI 🖥️

```bash
# Transformacja pliku Markdown do struktury GitHub
./drdoc.py -i examples/example_markdown.md -d github -o output/

# Auto-detekcja formatu + kontekst ChatGPT
./drdoc.py -i examples/example_json.json -d chatgpt --project-name "My API"

# Tylko podgląd (bez generowania plików)
./drdoc.py -i examples/example_text.txt -d github --preview

# Ze stdin
cat data.txt | ./drdoc.py --stdin -d chatgpt
```

### Detekcja formatu

```bash
# Sprawdź jaki format został wykryty
./drdoc.py -i unknown_file.txt --detect
```

## 📖 Dokumentacja

### Struktura Projektu

```
drdoc/
├── drdoc.py                    # Główna aplikacja CLI
├── src/
│   ├── parsers/                # Parsery formatów wejściowych
│   │   ├── base_parser.py      # Klasa bazowa
│   │   ├── txt_parser.py       # Parser TXT
│   │   ├── md_parser.py        # Parser Markdown
│   │   └── json_parser.py      # Parser JSON
│   ├── transformers/           # Transformery destinacji
│   │   ├── base_transformer.py
│   │   ├── github_transformer.py
│   │   └── chatgpt_transformer.py
│   └── generators/             # Generatory plików wyjściowych
│       └── file_generator.py
├── config/
│   ├── inputs/                 # Konfiguracje formatów wejściowych
│   │   ├── TXT.md
│   │   ├── MD.md
│   │   ├── JSON.md
│   │   ├── DOC.md
│   │   ├── PHP.md
│   │   └── CLIPBOARD.md
│   └── destinations/           # Wzorce destinacji
│       ├── GITHUB.md
│       ├── CHATGPT.md
│       └── PROJECT_BRIEF.md
├── examples/                   # Przykładowe pliki
├── data/
│   ├── input/                  # Dane wejściowe
│   └── output/                 # Wygenerowane pliki
└── README.md
```

### Użycie CLI

```
usage: drdoc.py [-h] (-i INPUT | --stdin) [-o OUTPUT] 
                [-d {github,chatgpt,project_brief}]
                [-f {txt,md,json,doc,php,clipboard}]
                [--detect] [--preview] [--project-name PROJECT_NAME]
                [--author AUTHOR] [--description DESCRIPTION] 
                [--license LICENSE] [-v]

Opcje:
  -i, --input           Ścieżka do pliku wejściowego
  --stdin               Czytaj dane ze stdin
  -o, --output          Katalog wyjściowy (domyślnie: data/output)
  -d, --destination     Typ destinacji (github/chatgpt/project_brief)
  -f, --format          Format wejściowy (opcjonalny, auto-detect)
  --detect              Tylko wykryj format
  --preview             Podgląd bez generowania plików
  --project-name        Nazwa projektu
  --author              Autor projektu
  --description         Opis projektu
  --license             Typ licencji (domyślnie: MIT)
  -v, --verbose         Tryb verbose
```

## 🔧 Rozszerzanie

### Dodawanie nowego parsera

1. Utwórz plik w `src/parsers/`:

```python
from .base_parser import BaseParser, ParsedData, DataType

class MyParser(BaseParser):
    def can_parse(self, content: str) -> float:
        # Logika wykrywania formatu
        return confidence_score
    
    def parse(self, content: str, **kwargs) -> ParsedData:
        # Logika parsowania
        return parsed_data
```

2. Zarejestruj w `src/parsers/__init__.py`:

```python
from .my_parser import MyParser

def init_parsers():
    parser_registry.register('myformat', MyParser())
```

### Dodawanie nowej destinacji

1. Utwórz wzorzec w `config/destinations/MY_DESTINATION.md`

2. Utwórz transformer w `src/transformers/`:

```python
from .base_transformer import BaseTransformer, TransformedData

class MyTransformer(BaseTransformer):
    def get_destination_type(self) -> str:
        return "mydestination"
    
    def transform(self, parsed_data: ParsedData, **kwargs) -> TransformedData:
        # Logika transformacji
        return transformed_data
```

3. Zarejestruj w `src/transformers/__init__.py`

## 📚 Przykłady

### Przykład 1: Markdown → GitHub

**Input** (`project.md`):
```markdown
# My Awesome Library

A Python library for data processing.

## Features
- Fast processing
- Easy to use
- Well documented
```

**Command**:
```bash
./drdoc.py -i project.md -d github --project-name awesome-lib
```

**Output**: Pełna struktura repo z README.md, LICENSE, .gitignore, docs/

### Przykład 2: JSON → ChatGPT Context

**Input** (`api_spec.json`):
```json
{
  "name": "User API",
  "endpoints": [
    {"method": "GET", "path": "/users"},
    {"method": "POST", "path": "/users"}
  ]
}
```

**Command**:
```bash
./drdoc.py -i api_spec.json -d chatgpt
```

**Output**: Zoptymalizowany kontekst dla AI w formacie Markdown

## 🗺️ Roadmap

- [x] Parsery: TXT, Markdown, JSON
- [x] Destinacje: GitHub, ChatGPT
- [ ] Parser: DOC (DOCX)
- [ ] Parser: PHP
- [ ] Parser: CLIPBOARD (auto-detect)
- [ ] Destinacja: Project Brief
- [ ] Destinacja: Documentation Site
- [ ] Web UI (interfejs graficzny)
- [ ] API REST
- [ ] Integracje (GitHub Actions, VS Code extension)

## 🤝 Współpraca

Chętnie przyjmujemy pull requesty!

1. Fork projektu
2. Utwórz branch (`git checkout -b feature/amazing-feature`)
3. Commit zmian (`git commit -m 'Add amazing feature'`)
4. Push do brancha (`git push origin feature/amazing-feature`)
5. Otwórz Pull Request

## 📝 Licencja

MIT License - zobacz [LICENSE](LICENSE) dla szczegółów.

## 👥 Autor

Projekt Dr.Doc

## 🙏 Podziękowania

- Społeczność open-source za inspirację
- Wszystkim kontrybutoromprojektu

---

**Dr.Doc** - Because data should adapt to you, not the other way around! 🩺✨
