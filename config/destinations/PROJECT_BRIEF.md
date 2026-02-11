# Destinacja: Project Brief

## Opis
Skonsolidowany brief projektowy - zwięzły dokument zawierający wszystkie kluczowe informacje o projekcie. Idealny dla stakeholderów, zespołów projektowych, lub jako punkt startowy.

## Struktura Standardowa

```markdown
# PROJECT BRIEF: [Nazwa Projektu]

**Data**: [YYYY-MM-DD]
**Status**: [Planning / In Progress / Review / Completed]
**Autor**: [Nazwa]
**Version**: [1.0]

---

## 📋 Executive Summary
[2-3 zdania opisujące istotę projektu]

---

## 🎯 Cele Projektu

### Cel główny
[Główny cel biznesowy/techniczny]

### Cele szczegółowe
1. [Cel 1]
2. [Cel 2]
3. [Cel 3]

### Success Metrics
- Metryka 1: [target]
- Metryka 2: [target]

---

## 👥 Stakeholderzy

| Rola | Osoba | Odpowiedzialność |
|------|-------|------------------|
| Project Owner | [Nazwa] | [Opis] |
| Tech Lead | [Nazwa] | [Opis] |
| Developer | [Nazwa] | [Opis] |

---

## 🔍 Problem Statement

### Obecna sytuacja
[Opis obecnego stanu]

### Wyzwania
- Challenge 1
- Challenge 2

### Proponowane rozwiązanie
[Jak projekt rozwiązuje problem]

---

## 💡 Scope

### In Scope
✅ [Feature/funkcja 1]
✅ [Feature/funkcja 2]
✅ [Feature/funkcja 3]

### Out of Scope
❌ [Co NIE jest częścią projektu 1]
❌ [Co NIE jest częścią projektu 2]

---

## 🏗️ Architektura / Stack Technologiczny

### Frontend
- [Technologia 1]
- [Technologia 2]

### Backend
- [Technologia 1]
- [Technologia 2]

### Infrastructure
- [Hosting/Cloud]
- [Database]
- [CI/CD]

### Diagram
```
[Prosty diagram ASCII lub opis architektury]
```

---

## 📦 Deliverables

1. **[Deliverable 1]**
   - Opis
   - Deadline: [data]

2. **[Deliverable 2]**
   - Opis
   - Deadline: [data]

---

## 📅 Timeline

| Faza | Zakres | Termin |
|------|--------|--------|
| Planning | [Zakres] | [Data] |
| Development | [Zakres] | [Data] |
| Testing | [Zakres] | [Data] |
| Launch | [Zakres] | [Data] |

### Milestones
- 🎯 [Milestone 1]: [Data]
- 🎯 [Milestone 2]: [Data]

---

## 💰 Budget (opcjonalne)

| Kategoria | Szacunek |
|-----------|----------|
| Development | [Koszt] |
| Infrastructure | [Koszt] |
| Tools/Licenses | [Koszt] |
| **Total** | **[Total]** |

---

## ⚠️ Risks & Assumptions

### Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Plan] |

### Assumptions
- [Założenie 1]
- [Założenie 2]

---

## 📚 Resources

### Documentation
- [Link 1]
- [Link 2]

### Tools
- [Tool 1]: [Link]
- [Tool 2]: [Link]

### References
- [Reference 1]
- [Reference 2]

---

## ✅ Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| [Role] | [Name] | _______ | ____ |

---

## 📝 Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | [Date] | Initial brief | [Name] |

```

## Mapowanie Danych

### 1. Executive Summary
**Źródła**:
- Pierwsze 2-3 zdania z głównego dokumentu
- Sekcja "Opis" lub "About"
- Metadata: description

**Transformacja**:
```
Długi opis → Wyciągnij najważniejsze → Maksymalnie 3 zdania
```

### 2. Cele
**Źródła**:
- Sekcja "Goals", "Objectives"
- Lista features → abstrakcja do celów
- Problem statement → implikowane cele

### 3. Stakeholderzy
**Źródła**:
- Metadata: author, contributors
- Sekcja "Team", "Contributors"
- Git: commit authors

### 4. Scope
**Źródła**:
- Lista features → In Scope
- Sekcja "Future work", "Out of scope" → Out of Scope
- TODO items → scope lub future work

### 5. Stack Technologiczny
**Źródła**:
- Code files → auto-detect języki/frameworki
- Config files (package.json, requirements.txt) → dependencies
- Bloki kodu → użyte technologie

### 6. Timeline
**Źródła**:
- CHANGELOG.md → historia jako timeline
- Milestones z TODO
- Git tags → releases jako milestones

### 7. Deliverables
**Źródła**:
- Features → deliverables
- Major sections → deliverables
- Goals → mapowanie 1:1 do deliverables

## Typy Brief'ów

### A) Software Project Brief
Focus: technologia, architektura, development
```markdown
Dodatkowe sekcje:
## 🧪 Testing Strategy
## 🚀 Deployment Plan
## 🔒 Security Considerations
## 📊 Performance Requirements
```

### B) Business Project Brief
Focus: ROI, biznes value, stakeholderzy
```markdown
Dodatkowe sekcje:
## 💼 Business Case
## 📈 Expected ROI
## 🎯 KPIs
## 📊 Market Analysis
```

### C) Research Project Brief
Focus: metodologia, pytania badawcze, outcomes
```markdown
Dodatkowe sekcje:
## 🔬 Research Questions
## 📚 Methodology
## 📊 Expected Outcomes
## 📖 Literature Review
```

## Reguły Transformacji

### 1. Kondensacja informacji
```
Długie dokumenty → Wyciągnij esencję
Multiple files → Jeden spójny brief
Raw data → Structured format
```

### 2. Priorytetyzacja
```
Kolejność sekcji według ważności:
1. Executive Summary (must-have)
2. Goals (must-have)
3. Scope (must-have)
4. Timeline (important)
5. Stack (important)
6. Reszta (nice-to-have)
```

### 3. Długość
```
Executive Summary: 50-100 słów
Cały brief: 1000-2000 słów
Każda sekcja: focused, no fluff
```

### 4. Wizualizacje
```
Gdzie możliwe:
- Tabele zamiast list
- Timeline jako diagram/tabela
- Architecture jako prosty diagram
- Metrics jako liczby/targets
```

## Parametry Konfiguracji
```json
{
  "brief_type": "software|business|research|general",
  "include_budget": false,
  "include_risks": true,
  "include_approval_section": false,
  "detail_level": "concise|detailed",
  "max_pages": 5,
  "include_diagrams": false,
  "auto_generate_timeline": true,
  "extract_stakeholders_from_git": true
}
```

## Automatyczne Ekstrakcje

### 1. Z Git Repository
```python
# Stakeholderzy
git log --format='%an' | sort | uniq

# Timeline
git log --oneline --graph --all

# Current status
git describe --tags
```

### 2. Z Kodu
```python
# Stack technologiczny
- package.json → Node.js dependencies
- requirements.txt → Python dependencies
- pom.xml → Java dependencies
- Gemfile → Ruby dependencies

# Architecture
- Directory structure → layers/modules
- Import statements → dependencies graph
```

### 3. Z Dokumentacji
```python
# Goals & Features
README.md:
- "Features" section → Scope
- "Installation" → Deliverables
- "Roadmap" → Timeline/Future

# Risks
SECURITY.md → Security risks
CONTRIBUTING.md → Development risks
```

## Warianty Output

### Minimal Brief (1 strona)
```
- Executive Summary
- Goals
- Scope
- Timeline
- Stack
```

### Standard Brief (3-5 stron)
```
Pełna struktura jak w szablonie
```

### Comprehensive Brief (5+ stron)
```
Standard + dodatki:
- Detailed architecture
- Complete risk analysis
- Full stakeholder matrix
- Detailed budget breakdown
```

## Walidacja Brief'u

Checklist:
- ✅ Executive summary odpowiada na: co, dlaczego, dla kogo
- ✅ Cele są SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- ✅ Scope jest jasno zdefiniowany (in/out)
- ✅ Timeline ma konkretne daty
- ✅ Stakeholderzy mają przypisane role
- ✅ Brak redundancji między sekcjami
- ✅ Consistent terminology przez cały dokument

## Output
Pojedynczy plik: `PROJECT_BRIEF_[ProjectName].md`
