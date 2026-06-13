# Sprint 3 — Planificación

**Proyecto:** Sistema CAG con Memoria Contextual  
**Duración:** 1 semana  
**Equipo:** Fredy Reyes  
**Fecha:** 2026-06-12

---

## Objetivo del Sprint

> **"Documentar el comportamiento del sistema con escenarios BDD, escribir pruebas TDD propias y mejorar la experiencia de usuario del frontend"**

Al finalizar este sprint, el proyecto debe tener cobertura completa de pruebas (base + contrato + unitarias del estudiante), documentación BDD en formato Gherkin, un frontend funcional que visualice el contexto CAG en tiempo real, y un README profesional con evidencias del funcionamiento del sistema.

---

## Historias seleccionadas

| ID | Historia | Story Points | Estado inicial |
|---|---|---|---|
| US-03 | Pruebas BDD para el flujo CAG completo | 5 | Por hacer |
| US-04 | Pruebas TDD unitarias para ContextStore y apply_context | 3 | Por hacer |

**Velocity del sprint:** 8 story points

---

## Desglose de tareas

### US-03 — Pruebas BDD para el flujo CAG completo (5 SP)

| # | Tarea | Archivo | Descripción | Estimación |
|---|---|---|---|---|
| T-03-1 | Escribir escenarios Gherkin | `docs/bdd/scenarios.md` | 7 escenarios Given/When/Then cubriendo: guardar contexto, recuperar contexto, usuario sin historial, respuesta base, respuesta adaptada, múltiples contextos, actualizar key existente | 1.5h |
| T-03-2 | Documentar mapeo Gherkin → Python | `tests/bdd/README.md` | Para cada escenario: qué método de `test_cag_contract.py` lo implementa, cómo se mapea cada bloque, cuáles están pendientes | 1h |
| T-03-3 | Identificar escenarios sin cobertura | `tests/bdd/README.md` | Escenarios 3, 6 y 7 no tienen test Python equivalente; documentar tests sugeridos | 0.5h |
| T-03-4 | Definir pasos para implementar pytest-bdd | `tests/bdd/README.md` | Listar comandos y estructura de archivos necesarios para formalizar BDD ejecutable | 0.5h |

### US-04 — Pruebas TDD unitarias (3 SP)

| # | Tarea | Archivo | Descripción | Estimación |
|---|---|---|---|---|
| T-04-1 | Crear suite para ContextStore | `tests/student/test_context_store.py` | 6 tests: save retorna True, almacena par, lista vacía para usuario nuevo, actualiza key existente, aislamiento entre usuarios, múltiples keys por usuario | 1h |
| T-04-2 | Crear suite para apply_context | `tests/student/test_cag_apply.py` | 4 tests: sin contexto retorna base_answer, con contexto el answer contiene el value, context_used contiene la key, lista vacía equivale a sin contexto | 0.5h |
| T-04-3 | Verificar aislamiento entre tests | — | Confirmar que `setUp` crea instancia fresca de `ContextStore` por test, sin estado compartido | 0.5h |
| T-04-4 | Ejecutar suite completa | — | `pytest tests/` debe mostrar 16 passed sin warnings | 0.5h |

### Tareas adicionales del sprint

| # | Tarea | Archivo | Descripción | Estimación |
|---|---|---|---|---|
| T-FE-1 | Mejorar panel CAG en frontend | `frontend/index.html` | Reemplazar placeholder con `#context-list` y formulario save-context (key + value) | 0.5h |
| T-FE-2 | Implementar saveContext y loadContext | `frontend/app.js` | `saveContext(userId, key, value)` → POST; `loadContext(userId)` → GET con render HTML de pares | 1h |
| T-FE-3 | Agregar badge de contexto usado | `frontend/app.js` + `styles.css` | Banner verde visible cuando `context_used` no está vacío; chips con cada key aplicada | 0.5h |
| T-FE-4 | Sanitización XSS en frontend | `frontend/app.js` | Función `escapeHtml` aplicada a todos los valores antes de insertarlos en el DOM | 0.5h |
| T-DOC-1 | Reescribir README.md | `README.md` | Descripción, diagrama ASCII de arquitectura, instrucciones de ejecución y pruebas, Scrum, árbol del repo, evidencias con imágenes | 1h |

---

## Definición de Done — Sprint 3

- [x] `docs/bdd/scenarios.md` contiene al menos 6 escenarios en formato Gherkin válido
- [x] `tests/bdd/README.md` mapea cada escenario a su test Python o lo marca como pendiente
- [x] `tests/student/test_context_store.py` — 6 tests pasan
- [x] `tests/student/test_cag_apply.py` — 4 tests pasan
- [x] Suite completa: `pytest tests/` → **16 passed**
- [x] Frontend muestra el contexto guardado como lista de pares key/value
- [x] Frontend muestra badge verde cuando la respuesta usa contexto CAG
- [x] README incluye imágenes de evidencia y es legible sin ejecutar el código
