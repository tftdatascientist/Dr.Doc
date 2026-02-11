# Format DOC - Dokument Word

## Opis
Format dokumentów Microsoft Word (DOC/DOCX). DOCX to format oparty na XML.

## Struktura
```
Dokument Word zawiera:
- Tekst z formatowaniem
- Style (nagłówki, paragrafy)
- Tabele
- Obrazy
- Metadane dokumentu
```

## Zasady Parsowania

### 1. Ekstakcja tekstu
- Czysty tekst bez formatowania
- Zachowanie struktury paragrafów
- Rozpoznawanie nagłówków (Heading 1-9)

### 2. Formatowanie
- **Pogrubienie** (bold)
- *Kursywa* (italic)
- <u>Podkreślenie</u> (underline)
- ~~Przekreślenie~~ (strikethrough)

### 3. Elementy strukturalne
- Nagłówki (H1-H9)
- Paragrafy
- Listy (punktowane i numerowane)
- Tabele (wiersze i kolumny)

### 4. Metadane
- Tytuł dokumentu
- Autor
- Data utworzenia/modyfikacji
- Komentarze
- Własności niestandardowe

### 5. Media
- Obrazy (ekstakcja do oddzielnych plików)
- Wykresy
- Kształty

## Przykład struktury DOCX (uproszczone)
```xml
<document>
  <body>
    <p>
      <pPr><pStyle val="Heading1"/></pPr>
      <r><t>Tytuł dokumentu</t></r>
    </p>
    <p>
      <r><t>To jest zwykły paragraf tekstu.</t></r>
    </p>
    <p>
      <r><rPr><b/></rPr><t>Pogrubiony tekst</t></r>
    </p>
  </body>
</document>
```

## Parametry Konfiguracji
```json
{
  "extract_text_only": false,
  "preserve_formatting": true,
  "extract_images": true,
  "extract_tables": true,
  "extract_metadata": true,
  "convert_to": "markdown",
  "image_output_dir": "images/"
}
```

## Obsługiwane Operacje
- ✅ Ekstakcja tekstu
- ✅ Rozpoznawanie struktury
- ✅ Ekstakcja metadanych
- ✅ Ekstakcja obrazów
- ✅ Parsowanie tabel
- ✅ Konwersja do Markdown/HTML
- ⚠️ Wymaga biblioteki python-docx lub similar

## Uwagi Implementacyjne
- DOCX: Format ZIP zawierający XML (łatwiejszy do parsowania)
- DOC: Format binarny (wymaga specjalnych bibliotek)
- Rekomendacja: Praca z DOCX
