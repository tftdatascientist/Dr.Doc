# Format JSON - JavaScript Object Notation

## Opis
JSON to lekki format wymiany danych, łatwy do czytania i pisania przez ludzi oraz parsowania przez maszyny.

## Struktura
```json
{
  "klucz": "wartość",
  "liczba": 42,
  "tablica": [1, 2, 3],
  "obiekt": {
    "zagnieżdżony": "klucz"
  },
  "boolean": true,
  "null": null
}
```

## Zasady Parsowania

### 1. Typy danych
- **String**: `"tekst"`
- **Number**: `42`, `3.14`, `-10`, `1e5`
- **Boolean**: `true`, `false`
- **Null**: `null`
- **Array**: `[...]`
- **Object**: `{...}`

### 2. Walidacja
- Poprawna składnia JSON
- Klucze muszą być w cudzysłowach
- Nie ma komentarzy (standardowy JSON)
- UTF-8 encoding

### 3. Struktura zagnieżdżona
- Nieograniczona głębokość zagnieżdżenia
- Mapowanie hierarchii obiektów
- Zachowanie typów danych

### 4. Specjalne przypadki
- Puste obiekty: `{}`
- Puste tablice: `[]`
- Escape sequences: `\n`, `\t`, `\"`, `\\`
- Unicode: `\uXXXX`

## Przykład
```json
{
  "project": {
    "name": "Dr.Doc",
    "version": "1.0.0",
    "description": "Data transformation tool"
  },
  "inputs": [
    {
      "type": "txt",
      "path": "data/input.txt"
    },
    {
      "type": "json",
      "path": "data/config.json"
    }
  ],
  "settings": {
    "encoding": "utf-8",
    "validate": true,
    "pretty_print": false
  },
  "metadata": {
    "created": "2024-01-01T00:00:00Z",
    "author": "Dr.Doc",
    "tags": ["data", "transformation", "tool"]
  }
}
```

## Parametry Konfiguracji
```json
{
  "strict_mode": true,
  "allow_comments": false,
  "preserve_order": true,
  "parse_numbers_as_strings": false,
  "max_depth": 100,
  "encoding": "utf-8"
}
```

## Obsługiwane Operacje
- ✅ Pełne parsowanie JSON
- ✅ Walidacja składni
- ✅ Ekstrakcja wartości po ścieżce (JSON Path)
- ✅ Transformacja struktury
- ✅ Merge i diff obiektów
- ✅ Schema validation (JSON Schema)
- ✅ Pretty printing
