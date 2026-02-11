# Destinacja: GitHub Repository

## Opis
Struktura danych zoptymalizowana pod repozytorium GitHub, zgodna z best practices open-source.

## Struktura Katalogów
```
repository/
├── README.md              # Główna dokumentacja projektu
├── LICENSE                # Licencja projektu
├── .gitignore            # Pliki ignorowane przez Git
├── CONTRIBUTING.md       # Przewodnik dla kontrybutorów
├── CODE_OF_CONDUCT.md    # Kodeks postępowania
├── CHANGELOG.md          # Historia zmian
├── SECURITY.md           # Polityka bezpieczeństwa
├── docs/                 # Dokumentacja szczegółowa
│   ├── installation.md
│   ├── usage.md
│   ├── api.md
│   └── examples.md
├── src/                  # Kod źródłowy
│   └── ...
├── tests/                # Testy
│   └── ...
├── examples/             # Przykłady użycia
│   └── ...
├── .github/              # Konfiguracja GitHub
│   ├── workflows/        # GitHub Actions
│   ├── ISSUE_TEMPLATE/   # Szablony issues
│   └── PULL_REQUEST_TEMPLATE.md
└── assets/               # Zasoby (obrazy, logo)
    └── ...
```

## Szablon README.md
```markdown
# [Nazwa Projektu]

![Logo](assets/logo.png)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/workflow/status/user/repo/CI)](https://github.com/user/repo/actions)

## 📋 Opis

[Krótki opis projektu - 1-2 zdania]

## ✨ Funkcje

- Funkcja 1
- Funkcja 2
- Funkcja 3

## 🚀 Szybki Start

### Wymagania

- Requirement 1
- Requirement 2

### Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/user/repo.git
cd repo

# Instalacja zależności
npm install  # lub pip install -r requirements.txt
```

### Użycie

```bash
# Przykład użycia
command --option value
```

## 📖 Dokumentacja

Pełna dokumentacja dostępna w katalogu [docs/](docs/).

## 🤝 Współpraca

Chętnie przyjmujemy pull requesty! Zobacz [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Licencja

Ten projekt jest licencjonowany na [MIT License](LICENSE).

## 👥 Autorzy

- [Imię Nazwisko](https://github.com/username)

## 🙏 Podziękowania

- Osoba/Projekt 1
- Osoba/Projekt 2
```

## Mapowanie Danych

### 1. README.md
**Źródła danych**:
- Tytuł → Główny nagłówek dokumentu wejściowego
- Opis → Pierwszy paragraf lub summary
- Funkcje → Sekcja z listami/punktami
- Instalacja → Bloki kodu lub instrukcje
- Użycie → Przykłady kodu
- Licencja → Metadata lub dedykowana sekcja

### 2. Kod źródłowy (src/)
**Struktura**:
```
src/
├── main.[ext]           # Główny plik wejściowy
├── lib/                 # Biblioteki/moduły
│   ├── module1.[ext]
│   └── module2.[ext]
├── utils/               # Narzędzia pomocnicze
│   └── helpers.[ext]
└── config/              # Konfiguracja
    └── settings.[ext]
```

**Mapowanie**:
- Code blocks → Pliki źródłowe
- Functions → Osobne moduły (jeśli duże)
- Config objects → config/settings

### 3. Dokumentacja (docs/)
**Struktura**:
```
docs/
├── installation.md      # Proces instalacji
├── usage.md            # Podstawowe użycie
├── api.md              # Dokumentacja API
├── examples.md         # Przykłady
├── troubleshooting.md  # Rozwiązywanie problemów
└── faq.md              # FAQ
```

**Mapowanie**:
- Sections z nagłówkami → Osobne pliki MD
- Podsekcje → Sekcje w plikach
- Code examples → Bloki kodu w docs

### 4. Przykłady (examples/)
```
examples/
├── basic/
│   ├── example1.[ext]
│   └── README.md
├── advanced/
│   ├── example2.[ext]
│   └── README.md
└── README.md           # Indeks przykładów
```

### 5. Testy (tests/)
```
tests/
├── unit/
│   └── test_*.ext
├── integration/
│   └── test_*.ext
└── README.md
```

### 6. .gitignore
**Automatyczne generowanie** na podstawie języka/technologii:
```
# Python
__pycache__/
*.py[cod]
venv/

# Node.js
node_modules/
npm-debug.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## Reguły Transformacji

### 1. Podział dokumentu
```
JEŚLI dokument > 500 linii:
  → Podziel na README.md + docs/
  
JEŚLI zawiera code blocks:
  → Wydziel do src/ lub examples/
  
JEŚLI zawiera konfigurację:
  → Utwórz pliki config
```

### 2. Optymalizacja dla GitHub
- ✅ Emoji w nagłówkach (📋 🚀 📖 🤝)
- ✅ Badges (Build, License, Version)
- ✅ Table of Contents (dla długich README)
- ✅ Screenshots w assets/
- ✅ Anchor links

### 3. Best Practices
- README.md max 300-500 linii
- Każdy plik docs/ skupiony na jednym temacie
- Przykłady uruchamialne (working code)
- Wyraźna hierarchia katalogów
- Konsystentne nazewnictwo

## Parametry Konfiguracji
```json
{
  "include_license": true,
  "include_contributing": true,
  "include_changelog": true,
  "include_github_actions": false,
  "readme_max_length": 500,
  "split_large_docs": true,
  "extract_code_blocks": true,
  "add_badges": true,
  "add_emojis": true,
  "language": "auto-detect"
}
```

## Wymagane Metadane
```json
{
  "project_name": "string (wymagane)",
  "description": "string (wymagane)",
  "author": "string (opcjonalne)",
  "license": "string (domyślnie: MIT)",
  "version": "string (domyślnie: 1.0.0)",
  "language": "string (auto-detect)",
  "repository_url": "string (opcjonalne)"
}
```

## Output
Po transformacji generowane pliki:
- ✅ README.md
- ✅ Struktura katalogów
- ✅ Pliki dokumentacji w docs/
- ✅ .gitignore
- ⚠️ LICENSE (jeśli brak, sugestia)
- ⚠️ CONTRIBUTING.md (opcjonalnie)
