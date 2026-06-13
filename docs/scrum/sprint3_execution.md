# Sprint 3 — Diario de Ejecución

**Proyecto:** Sistema CAG con Memoria Contextual  
**Sprint objetivo:** Documentar comportamiento con BDD, escribir pruebas TDD propias y mejorar frontend  
**Fecha:** 2026-06-12  
**Equipo:** Fredy Reyes

---

## Resumen de implementación

### Fase 1 — Escenarios BDD (US-03)

**Archivo:** `docs/bdd/scenarios.md`

Se redactaron 7 escenarios en formato Gherkin cubriendo el ciclo completo del módulo CAG:

| Escenario | Comportamiento verificado |
|---|---|
| 1 | Guardar contexto por primera vez → 201, `saved: true` |
| 2 | Recuperar contexto existente → 200, lista con par guardado |
| 3 | Usuario sin historial → 200, `context: []` |
| 4 | Pregunta sin contexto → respuesta base, `context_used: []` |
| 5 | Pregunta con contexto → respuesta contiene value literal, key en `context_used` |
| 6 | Múltiples contextos acumulados → todos reflejados en answer y context_used |
| 7 | Actualizar key existente → lista final con exactamente 1 elemento por key |

Cada escenario usa `user_id` diferente para garantizar independencia de estado.

**Archivo:** `tests/bdd/README.md`

Se documentó el mapeo de cada escenario Gherkin al método Python correspondiente en `test_cag_contract.py`. Se identificaron los escenarios 3, 6 y 7 como **sin cobertura de test actual** e incluye el código de test sugerido para cada uno. Incluye comandos de ejecución y pasos para formalizar con `pytest-bdd`.

---

### Fase 2 — Pruebas TDD unitarias (US-04)

**Archivo:** `tests/student/test_context_store.py`

6 tests unitarios con `unittest.TestCase`. Cada test parte de una instancia fresca (`setUp` con `ContextStore()` nuevo):

| Test | Qué verifica |
|---|---|
| `test_save_returns_true` | El método retorna `True` al guardar |
| `test_save_stores_key_value` | El par aparece en `list_for_user` después de guardar |
| `test_list_empty_for_new_user` | Usuario sin historial retorna `[]` |
| `test_save_updates_existing_key` | Misma key guardada dos veces: count = 1, valor = el nuevo |
| `test_multiple_users_isolated` | Contexto de "ana" no aparece en "luis" y viceversa |
| `test_multiple_keys_same_user` | Un usuario puede tener 3 keys distintas |

**Archivo:** `tests/student/test_cag_apply.py`

4 tests unitarios para `apply_context`:

| Test | Qué verifica |
|---|---|
| `test_no_context_returns_base_answer` | `context_items=None` → answer sin modificar, `context_used: []` |
| `test_context_answer_contains_value` | El value literal aparece en la respuesta enriquecida |
| `test_context_used_contains_key` | La key aparece en `context_used` |
| `test_empty_context_list` | `context_items=[]` → mismo comportamiento que sin contexto |

---

### Fase 3 — Mejoras de frontend

**Archivos:** `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`

El panel CAG fue completamente reemplazado. Cambios implementados:

- **HTML:** `#context-list` para renderizar pares; formulario `#save-context-form` con inputs key/value; banner `#context-used-banner` oculto por defecto con `.hidden`
- **CSS:** `.context-item` / `.context-item-key` / `.context-item-value` para visualizar pares; `.badge-used` y `.key-tag` para el indicador verde de contexto aplicado; `.btn-secondary` naranja para distinguir el botón de guardar del principal
- **JS:** `saveContext(userId, key, value)` → POST a `/api/context`; `loadContext(userId)` ahora llama a `renderContextList` en lugar de volcar JSON crudo; `showContextUsedBanner(usedKeys)` muestra u oculta el badge; `escapeHtml()` sanitiza todo valor antes de insertarlo en el DOM (previene XSS)
- Al cargar la página se llama `loadContext()` inmediatamente para mostrar el contexto existente

---

### Fase 4 — Documentación final

**Archivo:** `README.md`

Reescritura completa del README con:
- Descripción del sistema en 3 oraciones
- Diagrama ASCII de 3 niveles (Frontend → server.py → RAG/CAG)
- Descripción técnica de `ContextStore` y `apply_context`
- Instrucciones de instalación y ejecución
- 5 comandos de prueba con resultado esperado
- Tabla de 4 sprints Scrum y resumen del backlog
- Árbol del repositorio con descripción de cada archivo
- 8 imágenes de evidencia ubicadas en secciones relevantes

---

## Resultados de los tests

### Ejecución: `python -m pytest tests/ -v`

```
============================= test session starts ==============================
platform darwin -- Python 3.10.10, pytest-7.4.3

tests/base/test_base_api.py::BaseApiTest::test_ask_answers_from_knowledge_base  PASSED [  6%]
tests/base/test_base_api.py::BaseApiTest::test_ask_requires_user_and_question   PASSED [ 12%]
tests/base/test_base_api.py::BaseApiTest::test_health_returns_ok                PASSED [ 18%]
tests/student/test_cag_apply.py::TestApplyContext::test_context_answer_contains_value  PASSED [ 25%]
tests/student/test_cag_apply.py::TestApplyContext::test_context_used_contains_key      PASSED [ 31%]
tests/student/test_cag_apply.py::TestApplyContext::test_empty_context_list             PASSED [ 37%]
tests/student/test_cag_apply.py::TestApplyContext::test_no_context_returns_base_answer PASSED [ 43%]
tests/student/test_context_store.py::TestContextStore::test_list_empty_for_new_user    PASSED [ 50%]
tests/student/test_context_store.py::TestContextStore::test_multiple_keys_same_user    PASSED [ 56%]
tests/student/test_context_store.py::TestContextStore::test_multiple_users_isolated    PASSED [ 62%]
tests/student/test_context_store.py::TestContextStore::test_save_returns_true          PASSED [ 68%]
tests/student/test_context_store.py::TestContextStore::test_save_stores_key_value      PASSED [ 75%]
tests/student/test_context_store.py::TestContextStore::test_save_updates_existing_key  PASSED [ 81%]
tests/validation/test_cag_contract.py::CagContractTest::test_ask_uses_context_to_influence_later_response PASSED [ 87%]
tests/validation/test_cag_contract.py::CagContractTest::test_retrieves_context_for_user                   PASSED [ 93%]
tests/validation/test_cag_contract.py::CagContractTest::test_saves_context_for_user                       PASSED [100%]

16 passed in 1.08s
```

**Resultado: 16/16 tests pasan. Sin regresiones.**

---

## Estado final de la Definición de Done

- [x] `docs/bdd/scenarios.md` — 7 escenarios Gherkin completos
- [x] `tests/bdd/README.md` — mapeo documentado, pendientes identificados
- [x] `pytest tests/student/` — 10/10 pasan
- [x] `pytest tests/` — 16/16 pasan
- [x] Frontend: panel CAG funcional con pares key/value y badge de contexto usado
- [x] README con imágenes de evidencia integradas
- [x] Sin regresiones en tests base ni de contrato
