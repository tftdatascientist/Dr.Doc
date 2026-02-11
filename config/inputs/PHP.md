# Format PHP - PHP Code/Data

## Opis
Pliki PHP mogą zawierać kod PHP, HTML, lub struktury danych PHP (tablice, obiekty).

## Struktura

### 1. Kod PHP
```php
<?php
// Komentarz
function processData($input) {
    return $input;
}

$data = "przykładowe dane";
?>
```

### 2. PHP Data Arrays
```php
<?php
return [
    'config' => [
        'database' => 'mydb',
        'host' => 'localhost'
    ],
    'settings' => [
        'debug' => true,
        'timeout' => 30
    ]
];
?>
```

### 3. Mixed PHP/HTML
```php
<!DOCTYPE html>
<html>
<body>
    <?php echo "Hello World"; ?>
</body>
</html>
```

## Zasady Parsowania

### 1. Typy plików PHP
- **Config files**: Zwracają tablice z konfiguracją
- **Templates**: Mieszanka PHP i HTML
- **Classes**: Definicje klas PHP
- **Scripts**: Wykonywalne skrypty

### 2. Ekstakcja danych

#### a) PHP Config Arrays
```php
<?php
return [
    'key' => 'value',
    'nested' => ['a' => 1, 'b' => 2]
];
```
Traktowane jak JSON - konwersja do struktury danych.

#### b) Variables
```php
<?php
$config = [
    'option1' => 'value1',
    'option2' => 'value2'
];
```

#### c) Constants
```php
<?php
define('API_KEY', 'abc123');
const DATABASE = 'mydb';
```

### 3. Analiza kodu
- **Functions**: Lista funkcji i ich sygnatur
- **Classes**: Lista klas, metod, właściwości
- **Includes**: Zależności (require, include)
- **Namespaces**: Przestrzenie nazw

### 4. Dokumentacja
- **PHPDoc**: Komentarze dokumentacyjne
```php
/**
 * Opis funkcji
 * @param string $input Opis parametru
 * @return string Opis zwracanej wartości
 */
function example($input) {
    return $input;
}
```

## Przykład
```php
<?php
/**
 * Konfiguracja aplikacji Dr.Doc
 */
return [
    'app' => [
        'name' => 'Dr.Doc',
        'version' => '1.0.0',
        'debug' => true
    ],
    
    'inputs' => [
        'allowed_types' => ['txt', 'md', 'json', 'doc', 'php'],
        'max_size' => 10485760, // 10MB
    ],
    
    'outputs' => [
        'default_format' => 'markdown',
        'destination' => 'data/output/'
    ],
    
    'transformers' => [
        'github' => 'GitHubTransformer',
        'chatgpt' => 'ChatGPTTransformer'
    ]
];
```

## Parametry Konfiguracji
```json
{
  "parse_mode": "config_array",
  "execute_php": false,
  "extract_variables": true,
  "extract_functions": true,
  "extract_classes": true,
  "parse_phpdoc": true,
  "safe_mode": true
}
```

## Obsługiwane Operacje
- ✅ Parsowanie tablic konfiguracyjnych
- ✅ Ekstakcja zmiennych
- ✅ Analiza struktury kodu
- ✅ Parsowanie PHPDoc
- ⚠️ NIE wykonywanie kodu (bezpieczeństwo)
- ✅ Konwersja array PHP → JSON
- ✅ Analiza statyczna kodu

## Uwagi Bezpieczeństwa
⚠️ **NIGDY** nie wykonuj bezpośrednio kodu PHP z niezaufanych źródeł!
- Używaj parsera statycznego
- Nie używaj `eval()` ani `include()`
- Analizuj tylko strukturę danych
