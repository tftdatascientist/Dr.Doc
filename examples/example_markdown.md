# Przykładowy Projekt - E-Commerce Platform

## Wprowadzenie

Platforma e-commerce do sprzedaży produktów online z pełnym systemem zarządzania.

## Funkcje

- Katalog produktów z filtrowaniem
- Koszyk zakupowy
- Płatności online
- Panel administracyjny
- System użytkowników

## Technologie

### Frontend
- React.js
- TypeScript
- Tailwind CSS

### Backend
- Node.js
- Express
- PostgreSQL
- Redis

## Instalacja

```bash
# Klonowanie
git clone https://github.com/user/ecommerce.git

# Instalacja zależności
npm install

# Konfiguracja
cp .env.example .env

# Uruchomienie
npm run dev
```

## Przykład użycia API

```javascript
// Pobranie produktów
fetch('/api/products')
  .then(res => res.json())
  .then(products => {
    console.log(products);
  });

// Dodanie do koszyka
fetch('/api/cart', {
  method: 'POST',
  body: JSON.stringify({ productId: 123, quantity: 1 })
});
```

## Struktura Bazy Danych

Tabele:
- users - Użytkownicy
- products - Produkty
- orders - Zamówienia
- cart_items - Elementy koszyka

## Roadmap

1. Integracja z większą ilością dostawców płatności
2. Aplikacja mobilna (React Native)
3. System rekomendacji AI
4. Multi-language support

## Licencja

MIT License
