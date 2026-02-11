# Format TXT - Pliki Tekstowe

## Opis
Prosty format tekstowy zawierający dane w postaci niesformatowanego tekstu.

## Struktura
```
Dowolny tekst bez specjalnej struktury.
Każda linia jest traktowana jako część zawartości.
```

## Zasady Parsowania

### 1. Kodowanie
- Domyślne: UTF-8
- Alternatywne: ASCII, Latin-1

### 2. Rozpoznawanie struktury
- **Nagłówki**: Linie zakończone dwukropkiem lub WIELKIE LITERY
- **Paragrafy**: Oddzielone pustymi liniami
- **Listy**: Linie rozpoczynające się od `-`, `*`, `•`, lub cyfr z kropką

### 3. Metadane
- Brak wbudowanych metadanych
- Pierwsza linia może być traktowana jako tytuł (opcjonalnie)

## Przykład
```
TYTUŁ DOKUMENTU

To jest pierwszy paragraf tekstu.
Zawiera wiele linii.

To jest drugi paragraf.

Lista elementów:
- Element 1
- Element 2
- Element 3
```

## Parametry Konfiguracji
```json
{
  "encoding": "utf-8",
  "detect_headers": true,
  "first_line_as_title": false,
  "preserve_formatting": true,
  "line_ending": "auto"
}
```

## Obsługiwane Operacje
- ✅ Odczyt zawartości
- ✅ Wykrywanie struktury
- ✅ Ekstrakcja paragrafów
- ✅ Rozpoznawanie list
- ❌ Formatowanie tekstu (bold, italic)
