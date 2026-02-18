# Dr.Doc Web UI

Interfejs graficzny dla Dr.Doc - Data Transformation Tool.

## 🌟 Funkcje

### Interfejs użytkownika
- **Modern Design** - Czyste, nowoczesne UI z gradient colors
- **Responsywny** - Działa na desktop, tablet i mobile
- **Intuicyjny** - Łatwy w użyciu, bez instrukcji

### Główne możliwości
1. **Input Methods**
   - Wklejanie tekstu bezpośrednio
   - Upload plików (drag & drop)
   - Character counter
   - File info display

2. **Format Detection**
   - Auto-detekcja z confidence score
   - Manual format selection
   - Supported: TXT, MD, JSON, DOC, PHP

3. **Destination Selection**
   - Wizualne karty z opisami
   - GitHub (pełna struktura repo)
   - ChatGPT (AI-optimized context)
   - Project Brief (professional brief)

4. **Configuration Options**
   - Project name
   - Author
   - Description
   - License selection (MIT, Apache, GPL, BSD, Unlicense)
   - Preview mode toggle

5. **Results Display**
   - File statistics
   - ASCII file tree visualization
   - File preview (expandable)
   - Download option

## 🏗️ Architektura

```
web/
├── app.py                 # Flask server & API endpoints
├── templates/
│   └── index.html        # Main HTML interface
└── static/
    ├── css/
    │   └── style.css     # Styles (responsive, modern)
    └── js/
        └── app.js        # Frontend logic
```

## 🚀 Uruchomienie

### Development Mode

```bash
# Z głównego katalogu projektu
python3 web/app.py
```

Serwer uruchomi się na `http://localhost:5000`

### Production Mode

Dla produkcji użyj WSGI server (np. Gunicorn):

```bash
# Zainstaluj Gunicorn
pip install gunicorn

# Uruchom
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

## 📡 API Endpoints

### Health Check
```http
GET /api/health

Response:
{
  "status": "healthy",
  "service": "Dr.Doc API",
  "version": "1.0.0"
}
```

### Detect Format
```http
POST /api/detect
Content-Type: application/json

Request:
{
  "content": "# My content..."
}

Response:
{
  "success": true,
  "format": "md",
  "confidence": 0.85
}
```

### Transform Data
```http
POST /api/transform
Content-Type: application/json

Request:
{
  "content": "# My Project...",
  "format": "md",
  "destination": "github",
  "options": {
    "project_name": "my-project",
    "author": "Author Name",
    "description": "Project description",
    "license": "MIT",
    "preview": true
  }
}

Response:
{
  "success": true,
  "result": {
    "files_count": 4,
    "destination": "github",
    "file_tree": "...",
    "files": {
      "README.md": "content...",
      ...
    }
  }
}
```

## 🎨 Customizacja

### Zmiana kolorów (CSS variables)
Edytuj `static/css/style.css`:

```css
:root {
    --primary-color: #4F46E5;    /* Main brand color */
    --secondary-color: #10B981;  /* Success/accent */
    --danger-color: #EF4444;     /* Error/warning */
    /* ... */
}
```

### Dodanie nowej destinacji

1. Dodaj kartę w HTML (`templates/index.html`):
```html
<div class="destination-card" data-destination="my-dest">
    <div class="card-icon">🎯</div>
    <h3>My Destination</h3>
    <p>Description...</p>
</div>
```

2. Zaimplementuj transformer w `src/transformers/`

3. Zarejestruj w `src/transformers/__init__.py`

## 🐛 Debugowanie

### Włącz debug mode
W `app.py`:
```python
app.run(debug=True)  # Już włączone domyślnie
```

### Check logs
Flask wyświetla logi w konsoli:
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### Test API bezpośrednio
```bash
# Health check
curl http://localhost:5000/api/health

# Detect format
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"content": "# Test"}'
```

## 🔒 Security

### Development
- Tylko dla local development
- Debug mode włączony
- Brak autentykacji

### Production Checklist
- [ ] Wyłącz debug mode: `app.run(debug=False)`
- [ ] Użyj WSGI server (Gunicorn, uWSGI)
- [ ] Dodaj rate limiting
- [ ] Dodaj CORS configuration jeśli potrzebne
- [ ] Dodaj authentication jeśli wymagane
- [ ] HTTPS w production
- [ ] Environment variables dla secrets

## 📱 Responsywność

Interfejs jest w pełni responsywny:

- **Desktop** (>768px): 2-column layout, full features
- **Tablet** (768px): 1-column, optimized spacing
- **Mobile** (<768px): Stacked layout, touch-friendly

## 🎯 Roadmap

- [ ] File download as ZIP
- [ ] Multiple file batch processing
- [ ] Save/load configurations
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts
- [ ] Real-time collaboration
- [ ] API authentication
- [ ] Template marketplace

## 💡 Przykłady użycia

### Scenario 1: Quick transformation
1. Wklej Markdown w textarea
2. Kliknij "Wykryj format"
3. Wybierz "GitHub" destination
4. Kliknij "Transformuj"
5. Zobacz podgląd wyników

### Scenario 2: File upload
1. Przeciągnij plik JSON na upload area
2. Wybierz "ChatGPT" destination
3. Ustaw projekt name/author
4. Kliknij "Transformuj"
5. Zobacz zoptymalizowany kontekst AI

### Scenario 3: Custom configuration
1. Wprowadź dane
2. Wybierz destination
3. Wypełnij wszystkie opcje (name, author, description, license)
4. Wyłącz preview mode
5. Transformuj i zapisz pliki na serwerze

## 🆘 Troubleshooting

### "Port 5000 already in use"
```bash
# Znajdź proces
lsof -i :5000

# Zabij proces
kill -9 <PID>

# Lub użyj innego portu
python3 web/app.py --port 8000
```

### "Module not found: flask"
```bash
pip install -r requirements.txt
```

### "File too large"
Max file size: 16MB (configured in `app.py`)

Zwiększ limit:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

## 📄 Licencja

MIT License - see main project LICENSE file
