# Sprint 2 — Planificación

**Proyecto:** Sistema CAG con Memoria Contextual  
**Duración:** 1 semana  
**Equipo:** Daniel Reyes  
**Fecha:** 2026-06-12

---

## Objetivo del Sprint

> **"Implementar módulo CAG completo: ContextStore, apply_context e integración en assistant"**

Al finalizar este sprint, el pipeline completo CAG debe funcionar end-to-end: el usuario puede guardar contexto, hacer preguntas, y recibir respuestas enriquecidas con su contexto personal. Todos los tests de contrato y base deben pasar.

---

## Historias completadas

| ID | Historia | Story Points | Estado |
|---|---|---|---|
| US-01 | Memoria de contexto entre preguntas | 5 | Completado |
| US-02 | Preferencias de usuario persistentes | 3 | Completado |

**Velocity del sprint:** 8 story points

---

## Tareas técnicas realizadas

### US-01 — Memoria de contexto entre preguntas (5 SP)

| # | Tarea | Archivo | Descripción |
|---|---|---|---|
| T-01-1 | Implementar `ContextStore.__init__` | `backend/context_store.py` | Inicializa `self._store = {}` como dict en RAM |
| T-01-2 | Implementar `ContextStore.save` | `backend/context_store.py` | Guarda `{key: value}` por `user_id`; actualiza si la key ya existe; retorna `True` |
| T-01-3 | Implementar `ContextStore.list_for_user` | `backend/context_store.py` | Retorna `[{key, value}]` para el usuario; lista vacía si no existe |
| T-01-4 | Integrar `context_store` en `assistant.py` | `backend/assistant.py` | `answer_question` recibe `context_store` como parámetro y consulta el contexto del usuario |
| T-01-5 | Actualizar llamada en `server.py` | `backend/server.py` | Pasa la instancia existente de `context_store` a `answer_question` |

### US-02 — Preferencias de usuario persistentes (3 SP)

| # | Tarea | Archivo | Descripción |
|---|---|---|---|
| T-02-1 | Implementar `apply_context` | `backend/cag.py` | Sin contexto: retorna `base_answer` sin cambios. Con contexto: construye respuesta enriquecida con los valores literales del contexto |
| T-02-2 | Integrar `apply_context` en `assistant.py` | `backend/assistant.py` | Llama a `apply_context` después del RAG y usa el dict `{answer, context_used}` retornado |
| T-02-3 | Verificar contrato end-to-end | `tests/validation/` | Confirmar que los 3 tests de contrato CAG pasan |

---

## Definición de Done — Sprint 2

- [x] `ContextStore.save` implementado y retorna `True`
- [x] `ContextStore.list_for_user` retorna lista vacía para usuarios sin contexto
- [x] `apply_context` enriquece la respuesta con los values literales del contexto
- [x] `answer_question` usa la misma instancia de `ContextStore` que el servidor
- [x] `tests/validation/test_cag_contract.py` — 3/3 pasan
- [x] `tests/base/test_base_api.py` — 3/3 pasan (sin regresiones)
- [x] Suite completa: 6/6 tests pasan
