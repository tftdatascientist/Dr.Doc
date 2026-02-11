# Destinacja: ChatGPT Context

## Opis
Dane zoptymalizowane jako kontekst dla ChatGPT/Claude/innych AI asystentów. Format maksymalizuje zrozumienie przez LLM przy minimalnej liczbie tokenów.

## Zasady Optymalizacji

### 1. Struktura hierarchiczna
```markdown
# GŁÓWNY KONTEKST

## Cel i Zadanie
[Jasno określony cel w 1-3 zdaniach]

## Kluczowe Informacje
[Najważniejsze fakty w punktach]

## Szczegóły
[Rozwiniecie informacji]

## Przykłady
[Konkretne przykłady jeśli dostępne]

## Constraints/Wymagania
[Ograniczenia i wymogi]
```

### 2. Optymalizacja tokenów
- ✅ Zwięzłość bez utraty kontekstu
- ✅ Usunięcie redundancji
- ✅ Połączenie powtarzających się informacji
- ✅ Struktura zamiast długich opisów
- ❌ Unikaj powtórzeń
- ❌ Unikaj zbędnych słów wypełniających

### 3. Format czytelny dla AI
```markdown
## Struktura danych

**Format**: JSON
**Cel**: Konfiguracja aplikacji
**Użycie**: Import przez aplikację

```json
{
  "key": "value"
}
```

**Pola**:
- `key`: Opis pola (typ: string)
```

## Szablon Kontekstu

```markdown
# [NAZWA PROJEKTU/ZADANIA]

## 🎯 Cel
[Czego oczekujesz od AI - konkretne zadanie]

## 📊 Dane wejściowe

### Typ danych
[Format: TXT/JSON/Code/etc.]

### Zawartość
```
[Dane lub ich reprezentacja]
```

### Struktura
- Element 1: opis
- Element 2: opis

## 🔧 Wymagania

### Funkcjonalne
1. Wymaganie 1
2. Wymaganie 2

### Techniczne
- Technologia: [nazwa]
- Język: [język]
- Format wyjścia: [format]

## 📝 Kontekst dodatkowy

### Środowisko
[Informacje o środowisku wykonania]

### Ograniczenia
[Co należy uwzględnić]

### Preferencje
[Preferowany styl, podejście]

## 💡 Przykłady

### Input
```
[Przykładowe dane wejściowe]
```

### Expected Output
```
[Oczekiwany wynik]
```

## ❓ Pytania do AI
1. [Konkretne pytanie 1]
2. [Konkretne pytanie 2]
```

## Typy Kontekstów

### A) Project Brief
```markdown
# PROJECT: [Nazwa]

**Typ**: [Web App / CLI Tool / Library / etc.]
**Technologie**: [Lista technologii]
**Deadline**: [Opcjonalnie]

## Cel biznesowy
[Jaki problem rozwiązuje]

## Funkcje główne
1. Feature 1
2. Feature 2
3. Feature 3

## User Stories
- Jako [rola], chcę [akcja], aby [cel]
- Jako [rola], chcę [akcja], aby [cel]

## Techniczne wymagania
- Requirement 1
- Requirement 2

## Ograniczenia
- Constraint 1
- Constraint 2
```

### B) Code Context
```markdown
# CODE CONTEXT: [Moduł/Funkcja]

## Cel kodu
[Co ma robić]

## Obecna implementacja
```[language]
[kod]
```

## Problem/Zadanie
[Co należy zrobić]

## Wymagania
1. [Wymaganie 1]
2. [Wymaganie 2]

## Dodatkowe informacje
- [Info 1]
- [Info 2]
```

### C) Documentation Context
```markdown
# DOCS: [Nazwa dokumentacji]

## Temat
[O czym jest dokumentacja]

## Audience
[Dla kogo: developers/users/admins]

## Zakres
- [Temat 1]
- [Temat 2]

## Źródła informacji
```
[Dane źródłowe]
```

## Struktura oczekiwana
1. [Sekcja 1]
2. [Sekcja 2]

## Styl
- Ton: [formalny/casual/techniczny]
- Poziom: [beginner/intermediate/advanced]
```

### D) Debug Context
```markdown
# DEBUG: [Problem]

## Błąd
```
[Error message/stack trace]
```

## Kod
```[language]
[Problematyczny kod]
```

## Środowisko
- OS: [OS]
- Wersja: [Version]
- Zależności: [Lista]

## Kroki do reprodukcji
1. [Krok 1]
2. [Krok 2]

## Oczekiwane zachowanie
[Jak powinno działać]

## Aktualne zachowanie
[Co się dzieje]
```

## Mapowanie Danych Wejściowych

### Z formatu TXT
```
Nagłówki → Sections (## Sekcje)
Paragrafy → Punkty lub collapsed text
Listy → Zachowane jako listy
Długie bloki → Summarized + link "Details below"
```

### Z formatu JSON
```json
{
  "data": {...}
}
```
Przekształć na:
```markdown
## Dane

**Struktura**:
- field1: opis (type)
- field2: opis (type)

**Przykład**:
```json
{...}
```
```

### Z formatu Markdown
```
Zachowaj strukturę, zoptymalizuj:
- Scal podobne sekcje
- Skróć rozwlekłe opisy
- Wydziel kod do bloków
- Dodaj meta-informacje
```

### Z kodu źródłowego
```
Function/Class → Dokumentacja:
- Signature
- Purpose
- Parameters
- Returns
- Example usage
```

## Reguły Transformacji

### 1. Redukcja redundancji
```
PRZED:
"Ta funkcja służy do przetwarzania danych. Funkcja przetwarza dane wejściowe
i zwraca dane wyjściowe po przetworzeniu."

PO:
"Przetwarza dane wejściowe i zwraca wynik."
```

### 2. Strukturyzacja
```
PRZED: 
Długi paragraf tekstu z wieloma informacjami pomieszanymi razem...

PO:
## Kategoria
- Punkt 1
- Punkt 2

## Inna kategoria
- Punkt A
- Punkt B
```

### 3. Priorytetyzacja
```
Kolejność informacji:
1. CEL (co ma być zrobione)
2. KONTEKST (dlaczego)
3. SZCZEGÓŁY (jak)
4. PRZYKŁADY (demonstracje)
5. DODATKOWE (edge cases)
```

### 4. Code snippets
```
Zawsze z:
- Nazwą języka dla syntax highlighting
- Komentarzem wyjaśniającym
- Kontekstem użycia
```

## Parametry Konfiguracji
```json
{
  "max_tokens": 4000,
  "optimize_tokens": true,
  "include_examples": true,
  "verbosity": "concise",
  "structure_type": "auto",
  "add_emojis": true,
  "code_block_limit": 50,
  "summarize_long_sections": true
}
```

## Metryki jakości
- Token count: < 4000 (dla pojedynczego kontekstu)
- Readability: High (jasna struktura)
- Completeness: Wszystkie kluczowe info
- Redundancy: < 5%

## Output Format
```markdown
# [KONTEKST]

[Zoptymalizowana treść według szablonu]

---
**Meta**:
- Tokens: ~[liczba]
- Type: [typ kontekstu]
- Optimized: [data]
```
