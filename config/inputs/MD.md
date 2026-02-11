# Format MD - Markdown

## Opis
Markdown to lekki język znaczników do formatowania tekstu z prostą składnią.

## Struktura
```markdown
# Nagłówek 1
## Nagłówek 2
### Nagłówek 3

**Pogrubienie** i *kursywa*

- Lista punktowana
- Element 2

1. Lista numerowana
2. Element 2

[Link](https://example.com)
![Obraz](image.png)

`kod inline`

```
blok kodu
```
```

## Zasady Parsowania

### 1. Hierarchia nagłówków
- `#` do `######` - 6 poziomów nagłówków
- Nagłówki tworzą strukturę drzewa dokumentu

### 2. Formatowanie
- `**tekst**` lub `__tekst__` - pogrubienie
- `*tekst*` lub `_tekst_` - kursywa
- `~~tekst~~` - przekreślenie
- `` `tekst` `` - kod inline

### 3. Bloki
- Listy punktowane: `-`, `*`, `+`
- Listy numerowane: `1.`, `2.`, etc.
- Cytaty: `>`
- Kod: ` ``` ` lub wcięcie 4 spacje
- Tabele: `|` separatory

### 4. Linki i multimedia
- Linki: `[tekst](url)`
- Obrazy: `![alt](url)`
- Referencje: `[tekst][ref]` + `[ref]: url`

## Przykład
```markdown
# Projekt Dr.Doc

## Wprowadzenie
To jest **ważny** projekt do *transformacji* danych.

### Funkcje
- Parser danych
- Transformator
- Generator wyjścia

## Kod
```python
def transform_data(input_data):
    return output_data
```
```

## Parametry Konfiguracji
```json
{
  "flavor": "CommonMark",
  "extensions": ["tables", "strikethrough", "autolinks"],
  "preserve_structure": true,
  "extract_metadata": true,
  "parse_frontmatter": true
}
```

## Obsługiwane Operacje
- ✅ Pełne parsowanie składni Markdown
- ✅ Ekstrakcja struktury dokumentu
- ✅ Rozpoznawanie wszystkich elementów formatowania
- ✅ Obsługa Front Matter (YAML metadata)
- ✅ Konwersja do HTML/Plain text
