# Format CLIPBOARD - Kopiuj/Wklej

## Opis
Dane wklejone bezpośrednio przez użytkownika (copy-paste) bez określonego formatu wejściowego.

## Struktura
```
Dowolne dane tekstowe wklejone przez użytkownika.
Mogą zawierać:
- Czysty tekst
- Sformatowany tekst
- Kod źródłowy
- JSON/XML/CSV
- Mixed content
```

## Zasady Parsowania

### 1. Auto-detekcja formatu
System automatycznie próbuje rozpoznać format danych:

#### a) JSON
```
Sprawdź: czy zaczyna się od { lub [
Waliduj: spróbuj sparsować jako JSON
```

#### b) Markdown
```
Sprawdź: obecność # nagłówków, **, *, -, ```
Prawdopodobieństwo: wysoka jeśli zawiera wiele znaczników MD
```

#### c) XML
```
Sprawdź: czy zaczyna się od <?xml lub <tag>
Waliduj: spróbuj sparsować jako XML
```

#### d) CSV/TSV
```
Sprawdź: równe liczby separatorów w liniach (,;|\t)
Waliduj: co najmniej 2 kolumny
```

#### e) Kod źródłowy
```
Sprawdź: słowa kluczowe języków (function, class, def, var, const)
Rozpoznaj: język programowania
```

#### f) Czysty tekst
```
Default: jeśli nic innego nie pasuje
```

### 2. Heurystyki rozpoznawania

#### Sygnały JSON
- Zaczyna się od `{` lub `[`
- Zawiera pary `"key": value`
- Zamykające nawiasy

#### Sygnały Markdown
- `#` na początku linii (nagłówki)
- `**`, `*`, `__`, `_` (formatowanie)
- ` ``` ` (bloki kodu)
- `-`, `*`, `1.` (listy)

#### Sygnały kodu
- Słowa kluczowe: `function`, `class`, `def`, `import`, `const`, `var`
- Nawiasy i bloki: `{}`, `()`, `[]`
- Średnik na końcu linii
- Wcięcia (indentacja)

#### Sygnały tabeli/CSV
- Separator w każdej linii: `,`, `;`, `|`, `\t`
- Równa liczba kolumn
- Opcjonalnie nagłówki w pierwszej linii

### 3. Preprocessing
```
1. Usuń BOM (Byte Order Mark)
2. Normalizuj line endings (\r\n → \n)
3. Usuń leading/trailing whitespace (opcjonalne)
4. Wykryj encoding (UTF-8, Latin-1, etc.)
```

### 4. Fallback
```
Jeśli auto-detekcja nie działa:
→ Traktuj jako plain text
→ Podziel na paragrafy (podwójny \n)
→ Zachowaj podstawową strukturę
```

## Przykład - Mixed Content
```
# Mój projekt

Opis projektu w tekście.

{
  "config": {
    "name": "test",
    "version": "1.0"
  }
}

function example() {
  console.log("Hello");
}

| Kolumna 1 | Kolumna 2 |
|-----------|-----------|
| Data 1    | Data 2    |
```

**Rozpoznane sekcje**:
1. Markdown header
2. Plain text
3. JSON block
4. JavaScript code
5. Markdown table

## Parametry Konfiguracji
```json
{
  "auto_detect": true,
  "detection_confidence_threshold": 0.7,
  "enable_multiformat": true,
  "split_mixed_content": true,
  "fallback_to_plaintext": true,
  "preserve_original": true,
  "max_size": 1048576
}
```

## Obsługiwane Operacje
- ✅ Auto-detekcja formatu
- ✅ Multi-format parsing
- ✅ Ekstakcja mixed content
- ✅ Fallback do plain text
- ✅ Encoding detection
- ✅ Content splitting
- ✅ Format suggestion dla użytkownika

## Przykład użycia
```python
from parsers.clipboard_parser import ClipboardParser

parser = ClipboardParser()
data = parser.parse(clipboard_content)

print(f"Detected format: {data.detected_format}")
print(f"Confidence: {data.confidence}")
print(f"Sections: {len(data.sections)}")
```

## Uwagi
- Zawsze zachowuj oryginalną zawartość
- Daj użytkownikowi możliwość manualnego wyboru formatu
- Pokazuj confidence level przy auto-detekcji
- Obsługuj edge cases (puste, bardzo małe, bardzo duże dane)
