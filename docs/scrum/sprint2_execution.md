# Sprint 2 — Diario de Ejecución

**Proyecto:** Sistema CAG con Memoria Contextual  
**Sprint objetivo:** Implementar módulo CAG completo: ContextStore, apply_context e integración en assistant  
**Fecha:** 2026-06-12  
**Equipo:** Fredy Reyes

---

## Resumen de implementación

### Fase 1 — Verificación de la base

Antes de implementar, se ejecutó el script `scripts/run_base_tests.sh` para confirmar que el proyecto base estaba intacto. Los 3 tests de `tests/base/test_base_api.py` pasaron correctamente, estableciendo la línea base.

Se identificó que todo el backend usa únicamente stdlib de Python (no hay dependencias de terceros). Se creó `requirements.txt` con `pytest>=7.0` como única dependencia de desarrollo.

### Fase 2 — Implementación de `ContextStore`

**Archivo:** `backend/context_store.py`

Se reemplazó el placeholder con `NotImplementedError` por una implementación real:

- Almacenamiento en memoria con `self._store = {}` (dict de dicts: `{user_id: {key: value}}`)
- `save(user_id, key, value)`: crea el espacio del usuario si no existe, guarda o actualiza la key, retorna `True`
- `list_for_user(user_id)`: convierte el dict interno en lista de `{"key": ..., "value": ...}`; retorna `[]` si el usuario no existe

### Fase 3 — Implementación de `apply_context`

**Archivo:** `backend/cag.py`

Se reemplazó el stub que retornaba `base_answer` sin cambios:

- Sin contexto (`context_items` vacío): retorna `{"answer": base_answer, "context_used": []}`
- Con contexto: construye una respuesta enriquecida que incluye el `base_answer` original seguido de un bloque "Adaptado segun tu contexto:" con los pares `key: value` literales
- Retorna `{"answer": enriched_answer, "context_used": [keys...]}`

El requisito crítico cumplido: el `value` del contexto aparece literalmente en la respuesta, lo que permite que el test verifique `assertIn("principiante", body["answer"].lower())`.

### Fase 4 — Integración en `assistant.py`

**Archivo:** `backend/assistant.py`

Se refactorizó `answer_question` para cerrar el pipeline completo:

- Firma extendida: `answer_question(user_id, question, context_store)`
- Obtiene contexto del usuario: `context_items = context_store.list_for_user(user_id)`
- Llama a `apply_context` en ambos caminos (con y sin snippets del RAG)
- Usa el dict retornado por `apply_context` para construir la respuesta final con `context_used`

**Archivo:** `backend/server.py` (cambio mínimo)

Una sola línea modificada: la llamada a `answer_question` ahora pasa la instancia `context_store` que ya existía en el módulo del servidor. Esto garantiza que todos los endpoints comparten el mismo estado en memoria.

---

## Resultados de los tests

### Ejecución: `python -m pytest tests/ -v`

```
============================= test session starts ==============================
platform darwin -- Python 3.10.10, pytest-7.4.3

tests/base/test_base_api.py::BaseApiTest::test_ask_answers_from_knowledge_base PASSED
tests/base/test_base_api.py::BaseApiTest::test_ask_requires_user_and_question   PASSED
tests/base/test_base_api.py::BaseApiTest::test_health_returns_ok                PASSED
tests/validation/test_cag_contract.py::CagContractTest::test_ask_uses_context_to_influence_later_response PASSED
tests/validation/test_cag_contract.py::CagContractTest::test_retrieves_context_for_user                   PASSED
tests/validation/test_cag_contract.py::CagContractTest::test_saves_context_for_user                       PASSED

6 passed in 1.05s
```

**Resultado: 6/6 tests pasan. Sin regresiones.**

---

## Estado final de la Definición de Done

- [x] Código en repositorio
- [x] `pytest tests/base/` — 3/3 pasan
- [x] `pytest tests/validation/` — 3/3 pasan
- [x] Sin errores de sintaxis ni warnings críticos
- [x] Verificación manual realizada (llamadas directas al servidor)
- [x] Criterios de aceptación de US-01 y US-02 cumplidos
