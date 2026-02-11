"""
GitHub Transformer
Przekształca dane do struktury repozytorium GitHub
"""

from typing import Dict, Any
from .base_transformer import BaseTransformer, TransformedData
from ..parsers.base_parser import ParsedData


class GitHubTransformer(BaseTransformer):
    """Transformer dla repozytorium GitHub"""
    
    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            'include_license': True,
            'include_contributing': True,
            'include_changelog': False,
            'include_github_actions': False,
            'readme_max_length': 500,
            'split_large_docs': True,
            'extract_code_blocks': True,
            'add_badges': True,
            'add_emojis': True,
            'license_type': 'MIT'
        }
        if config:
            default_config.update(config)
        super().__init__(default_config)
    
    def get_destination_type(self) -> str:
        return "github"
    
    def transform(self, parsed_data: ParsedData, **kwargs) -> TransformedData:
        """Transformuje dane do struktury GitHub"""
        result = TransformedData()
        result.destination = "github"
        
        # Walidacja
        is_valid, errors = self.validate_input(parsed_data)
        if not is_valid:
            result.errors = errors
            return result
        
        # Metadata projektu
        project_meta = kwargs.get('metadata', {})
        project_name = project_meta.get('project_name', parsed_data.title or 'Untitled')
        description = project_meta.get('description', 'Project description')
        author = project_meta.get('author', 'Author')
        
        # Generuj README.md
        readme = self._generate_readme(parsed_data, project_name, description, author)
        result.add_file('README.md', readme)
        
        # Generuj .gitignore
        gitignore = self._generate_gitignore(parsed_data)
        result.add_file('.gitignore', gitignore)
        
        # LICENSE
        if self.config.get('include_license', True):
            license_content = self._generate_license(author)
            result.add_file('LICENSE', license_content)
        
        # CONTRIBUTING.md
        if self.config.get('include_contributing', True):
            contributing = self._generate_contributing()
            result.add_file('CONTRIBUTING.md', contributing)
        
        # Dokumentacja w docs/
        if self.config.get('split_large_docs', True) and len(parsed_data.sections) > 3:
            docs = self._generate_docs(parsed_data)
            for filename, content in docs.items():
                result.add_file(f'docs/{filename}', content)
        
        # Code blocks → src/
        if self.config.get('extract_code_blocks', True) and parsed_data.code_blocks:
            for i, code_block in enumerate(parsed_data.code_blocks):
                ext = code_block.get('language', 'txt')
                filename = f'example_{i+1}.{ext}'
                result.add_file(f'examples/{filename}', code_block['code'])
        
        # Struktura katalogów
        result.structure = {
            'root': ['README.md', 'LICENSE', '.gitignore'],
            'docs/': ['installation.md', 'usage.md'],
            'examples/': [],
            'src/': [],
            'tests/': []
        }
        
        # Metadata
        result.metadata = {
            'project_name': project_name,
            'files_generated': len(result.files),
            'has_code_examples': len(parsed_data.code_blocks) > 0 if parsed_data.code_blocks else False
        }
        
        return result
    
    def _generate_readme(self, data: ParsedData, project_name: str, 
                        description: str, author: str) -> str:
        """Generuje README.md"""
        emoji = "📦" if self.config.get('add_emojis', True) else ""
        
        readme = f"""# {emoji} {project_name}

## 📋 Opis

{description}

"""
        
        # Features z list/sekcji
        if data.lists:
            readme += "## ✨ Funkcje\n\n"
            for lst in data.lists[:1]:  # Pierwsza lista
                for item in lst['items'][:5]:  # Max 5 items
                    readme += f"- {item}\n"
            readme += "\n"
        
        # Instalacja
        readme += """## 🚀 Instalacja

```bash
# Clone repository
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install  # or: pip install -r requirements.txt
```

## 💻 Użycie

```bash
# Run the application
npm start  # or: python main.py
```

"""
        
        # Kod jeśli są code blocks
        if data.code_blocks:
            readme += "## 📚 Przykłady\n\n"
            first_block = data.code_blocks[0]
            readme += f"```{first_block['language']}\n{first_block['code'][:200]}\n```\n\n"
        
        # Dokumentacja
        readme += """## 📖 Dokumentacja

Szczegółowa dokumentacja dostępna w katalogu [docs/](docs/).

## 🤝 Współpraca

Pull requesty są mile widziane! Zobacz [CONTRIBUTING.md](CONTRIBUTING.md).

"""
        
        # Licencja
        readme += f"""## 📝 Licencja

Projekt licencjonowany na [MIT License](LICENSE).

## 👥 Autor

- {author}
"""
        
        return readme
    
    def _generate_gitignore(self, data: ParsedData) -> str:
        """Generuje .gitignore na podstawie wykrytych technologii"""
        gitignore = "# Dr.Doc generated .gitignore\n\n"
        
        # Auto-detect języka z code blocks
        languages = set()
        if data.code_blocks:
            for block in data.code_blocks:
                languages.add(block.get('language', '').lower())
        
        # Python
        if 'python' in languages or 'py' in languages:
            gitignore += """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

"""
        
        # Node.js
        if 'javascript' in languages or 'typescript' in languages or 'js' in languages:
            gitignore += """# Node.js
node_modules/
npm-debug.log
yarn-error.log
package-lock.json
.npm

"""
        
        # IDE
        gitignore += """# IDEs
.vscode/
.idea/
*.swp
*.swo

"""
        
        # OS
        gitignore += """# OS
.DS_Store
Thumbs.db
desktop.ini

"""
        
        # Data
        gitignore += """# Dr.Doc
data/output/
*.tmp
*.log
"""
        
        return gitignore
    
    def _generate_license(self, author: str) -> str:
        """Generuje plik LICENSE (MIT)"""
        from datetime import datetime
        year = datetime.now().year
        
        return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    def _generate_contributing(self) -> str:
        """Generuje CONTRIBUTING.md"""
        return """# Contributing to this project

Thank you for your interest in contributing! 

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

Please follow the existing code style in the project.

## Reporting Issues

Use GitHub Issues to report bugs or suggest features.

## Code of Conduct

Be respectful and inclusive in all interactions.
"""
    
    def _generate_docs(self, data: ParsedData) -> Dict[str, str]:
        """Generuje pliki dokumentacji w docs/"""
        docs = {}
        
        # installation.md
        docs['installation.md'] = """# Instalacja

## Wymagania

- [Lista wymagań]

## Kroki instalacji

1. Krok 1
2. Krok 2
3. Krok 3

## Weryfikacja

Sprawdź czy instalacja przebiegła poprawnie...
"""
        
        # usage.md
        docs['usage.md'] = """# Użycie

## Podstawowe użycie

[Opis podstawowego użycia]

## Zaawansowane funkcje

[Opis zaawansowanych funkcji]

## Przykłady

[Przykłady użycia]
"""
        
        return docs
