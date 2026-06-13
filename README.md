# CAG Lab — Sistema RAG + CAG con Memoria Contextual

Asistente conversacional universitario que combina **RAG** (Retrieval-Augmented Generation) para responder desde una base de conocimiento del curso, con **CAG** (Context-Augmented Generation) para adaptar las respuestas según el contexto y preferencias acumuladas de cada usuario. El sistema expone una API REST en Python puro (sin frameworks) y una interfaz web en HTML/JS vanilla que permite hacer preguntas y gestionar el contexto de forma interactiva.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│   index.html · styles.css · app.js                     │
│                                                         │
│   [Formulario pregunta]    [Panel Mi Contexto]          │
│   [Respuesta + badge CAG]  [Formulario guardar ctx]     │
└────────────────────┬────────────────────────────────────┘
                     │  HTTP (fetch)
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   backend/server.py                     │
│              ThreadingHTTPServer · puerto 8000          │
│                                                         │
│   POST /api/ask ──────────────────────────────────┐    │
│   POST /api/context ──────────────────────────┐   │    │
│   GET  /api/context?user_id= ─────────────┐   │   │    │
│   GET  /health                            │   │   │    │
└───────────────────────────────────────────┼───┼───┼────┘
                                            │   │   │
              ┌─────────────────────────────┘   │   │
              ▼                                 │   │
┌─────────────────────────┐                    │   │
│  backend/context_store  │◄───────────────────┘   │
│  ContextStore (RAM)     │                         │
│  {user_id: {key:value}} │                         │
└─────────────────────────┘                         │
                                                    ▼
              ┌────────────────────────────────────────────┐
              │           backend/assistant.py             │
              │         answer_question(user_id,           │
              │           question, context_store)         │
              └──────────┬─────────────────┬──────────────┘
                         │                 │
              ┌──────────▼──────┐  ┌───────▼──────────────┐
              │ backend/        │  │ backend/cag.py        │
              │ knowledge.py    │  │ apply_context(...)    │
              │                 │  │                       │
              │ retrieve_       │  │ base_answer +         │
              │ snippets()      │  │ context_items         │
              │ (búsqueda por   │  │ → respuesta           │
              │  términos)      │  │   enriquecida         │
              └──────────┬──────┘  └───────┬──────────────┘
                         │                 │
              ┌──────────▼─────────────────▼──────────────┐
              │           data/knowledge_base.json         │
              │   RAG · SDD · BDD · TDD · CAG · Jarvis    │
              └────────────────────────────────────────────┘
```

---

## Módulo CAG — Qué se implementó

### `backend/context_store.py` — Almacén de contexto en memoria

`ContextStore` mantiene un diccionario de dos niveles `{user_id → {key → value}}` en RAM. Cada usuario tiene su propio espacio aislado.

| Método | Comportamiento |
|---|---|
| `save(user_id, key, value)` | Crea el espacio del usuario si no existe; inserta o sobreescribe la key. Retorna `True`. |
| `list_for_user(user_id)` | Retorna `[{"key": ..., "value": ...}]`. Lista vacía si el usuario no tiene contexto. |

El servidor crea una única instancia al arrancar y la comparte con todos los handlers, garantizando consistencia entre `POST /api/context` y `GET /api/ask`.

### `backend/cag.py` — Enriquecimiento de respuestas

`apply_context(user_id, question, base_answer, context_items)` toma la respuesta RAG base y la combina con el contexto del usuario:

- **Sin contexto** (`context_items` vacío o `None`): retorna `base_answer` sin modificar, `context_used: []`.
- **Con contexto**: construye una respuesta enriquecida que incluye el texto original seguido de los pares `key: value` del contexto, garantizando que los valores del usuario aparecen literalmente en la respuesta. Retorna `{"answer": ..., "context_used": [keys...]}`.

### `backend/assistant.py` — Integración del pipeline completo

`answer_question` orquesta el flujo end-to-end:

```
pregunta → retrieve_snippets() → base_answer
        → context_store.list_for_user() → context_items
        → apply_context() → respuesta final con context_used
```

---

## Cómo ejecutar

**Requisitos:** Python 3.10+

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd final_project_AI_CUSTOM

# 2. Instalar dependencias de desarrollo
pip install -r requirements.txt

# 3. Levantar el backend
PYTHONPATH=. python3 backend/server.py
# Backend disponible en http://127.0.0.1:8000

# 4. Abrir el frontend
# Abrir frontend/index.html en el navegador
# (o servir con: python3 -m http.server 3000 --directory frontend)
```

> El backend no requiere dependencias externas. Usa únicamente la biblioteca estándar de Python (`http.server`, `json`, `pathlib`, `threading`).

---

## Cómo correr las pruebas

```bash
# Pruebas base (deben pasar desde el inicio del proyecto)
PYTHONPATH=. python3 -m pytest tests/base/ -v

# Pruebas de contrato CAG (validan el módulo completo)
PYTHONPATH=. python3 -m pytest tests/validation/ -v

# Pruebas unitarias del estudiante (TDD: ContextStore + apply_context)
PYTHONPATH=. python3 -m pytest tests/student/ -v

# Suite completa (16 tests)
PYTHONPATH=. python3 -m pytest tests/ -v

# Script original del proyecto base
./scripts/run_base_tests.sh
```

**Resultado esperado:** `16 passed` sin errores ni warnings.

---

## Metodología Scrum

El proyecto se desarrolló en sprints semanales siguiendo la metodología Scrum. La documentación completa está en `docs/scrum/`.

| Sprint | Objetivo | Historias | Estado |
|---|---|---|---|
| **Sprint 1** | Verificar base del proyecto e implementar ContextStore funcional | US-01 (parcial), US-04 | Completado |
| **Sprint 2** | Implementar módulo CAG completo: ContextStore, apply_context e integración en assistant | US-01, US-02 | Completado |
| **Sprint 3** | Pruebas BDD para el flujo CAG completo | US-03 | Planificado |
| **Sprint 4** | Mejoras de UX y cierre del proyecto | — | Planificado |

### Product Backlog (resumen)

| ID | Historia | SP | Prioridad |
|---|---|---|---|
| US-01 | Como usuario quiero que el sistema recuerde mi contexto entre preguntas | 5 | Alta |
| US-02 | Como usuario quiero guardar preferencias y que el sistema las aplique | 3 | Media |
| US-03 | Como desarrollador quiero pruebas BDD que validen el flujo CAG completo | 5 | Alta |
| US-04 | Como desarrollador quiero pruebas TDD unitarias para ContextStore y apply_context | 3 | Alta |

---

## Estructura del repositorio

```
final_project_AI_CUSTOM/
│
├── backend/                      # Lógica del servidor y módulo CAG
│   ├── server.py                 # HTTP server (ThreadingHTTPServer), routing
│   ├── assistant.py              # Orquesta RAG + CAG → respuesta final
│   ├── knowledge.py              # RAG: carga y búsqueda en knowledge_base.json
│   ├── context_store.py          # CAG: almacén de contexto en memoria por usuario
│   ├── cag.py                    # CAG: enriquecimiento de respuestas con contexto
│   └── __init__.py
│
├── frontend/                     # Interfaz web (HTML/CSS/JS vanilla)
│   ├── index.html                # Estructura: formulario pregunta + panel CAG
│   ├── styles.css                # Diseño visual, indicadores de contexto usado
│   └── app.js                    # Lógica: saveContext, loadContext, badge CAG
│
├── data/
│   └── knowledge_base.json       # Base de conocimiento del curso (RAG, CAG, SDD, BDD, TDD)
│
├── tests/
│   ├── base/                     # Pruebas del proyecto base (no modificar)
│   │   └── test_base_api.py      # 3 tests: /health, /api/ask, validación de campos
│   ├── validation/               # Pruebas de contrato CAG (no modificar)
│   │   └── test_cag_contract.py  # 3 tests: guardar, recuperar y usar contexto
│   └── student/                  # Pruebas TDD escritas por el estudiante
│       ├── test_context_store.py # 6 tests unitarios para ContextStore
│       └── test_cag_apply.py     # 4 tests unitarios para apply_context
│
├── docs/
│   ├── scrum/                    # Documentación Scrum del proyecto
│   │   ├── backlog.md            # Product Backlog con US-01 a US-04
│   │   ├── sprint1_planning.md   # Planificación Sprint 1
│   │   ├── sprint1_execution.md  # Diario de ejecución Sprint 1
│   │   ├── sprint2_planning.md   # Planificación Sprint 2
│   │   ├── sprint2_execution.md  # Resumen de implementación Sprint 2
│   │   └── sprint2_retrospective.md
│   ├── bdd/
│   │   └── scenarios.md          # 7 escenarios Gherkin (Given/When/Then)
│   └── evidencias/               # Capturas de pantalla y evidencias visuales
│
├── scripts/
│   ├── run_base_tests.sh         # Script para ejecutar pruebas base
│   └── validate_student_cag.sh  # Script de validación de entrega final
│
├── requirements.txt              # pytest>=7.0 (única dependencia externa)
├── test.sh                       # Script de validación rápida
└── README.md                     # Este archivo
```

---

## Evidencias

Las capturas de pantalla, evidencias de ejecución de pruebas y registros visuales del funcionamiento del sistema se encuentran en `docs/evidencias/`.

Se recomienda incluir al menos:

- Captura del frontend con una respuesta enriquecida (badge CAG visible)
- Output de terminal con `16 passed` al ejecutar la suite completa
- Captura del panel "Mi Contexto Guardado" con pares cargados
