# BDD — Mapeo de escenarios a tests Python

**Proyecto:** Sistema CAG con Memoria Contextual  
**Escenarios fuente:** `docs/bdd/scenarios.md`  
**Tests existentes:** `tests/validation/test_cag_contract.py`

---

## Relación entre escenarios Gherkin y tests de Python

Los escenarios BDD describen el comportamiento del sistema en lenguaje de dominio. Los tests de Python en `test_cag_contract.py` son la implementación ejecutable de esos escenarios. La tabla siguiente muestra el mapeo directo:

| Escenario BDD | Método en `test_cag_contract.py` | Cobertura |
|---|---|---|
| Escenario 1 — Guardar contexto exitosamente | `test_saves_context_for_user` | Completa |
| Escenario 2 — Recuperar contexto existente | `test_retrieves_context_for_user` | Completa |
| Escenario 3 — Usuario sin historial | *(no implementado)* | Pendiente |
| Escenario 4 — Respuesta base sin contexto | `test_ask_answers_from_knowledge_base` (en `tests/base/`) | Completa |
| Escenario 5 — Respuesta adaptada con contexto | `test_ask_uses_context_to_influence_later_response` | Completa |
| Escenario 6 — Múltiples contextos acumulados | *(no implementado)* | Pendiente |
| Escenario 7 — Actualizar contexto (misma key) | *(no implementado)* | Pendiente |

---

## Análisis detallado por escenario

### Escenario 1 → `test_saves_context_for_user`

```python
def test_saves_context_for_user(self):
    status, body = self.post_json(
        "/api/context",
        {"user_id": "ana", "key": "preferred_style", "value": "explicaciones con analogias"},
    )
    self.assertEqual(status, 201)
    self.assertTrue(body["saved"])
```

**Given** implícito: el servidor está levantado y "ana" no tiene contexto previo (estado inicial del test).  
**When**: `post_json("/api/context", {...})` ejecuta la acción del escenario.  
**Then**: `assertEqual(201)` y `assertTrue(body["saved"])` verifican las postcondiciones.

---

### Escenario 2 → `test_retrieves_context_for_user`

```python
def test_retrieves_context_for_user(self):
    self.post_json(
        "/api/context",
        {"user_id": "ana", "key": "project", "value": "usa arquitectura monolitica moderna"},
    )
    status, body = self.get_json("/api/context?user_id=ana")
    self.assertEqual(status, 200)
    self.assertEqual(body["user_id"], "ana")
    self.assertIn({"key": "project", "value": "usa arquitectura monolitica moderna"}, body["context"])
```

**Given**: el primer `post_json` establece la precondición del escenario.  
**When**: `get_json("/api/context?user_id=ana")` es la acción principal.  
**Then**: los tres `assert` verifican código, user_id y presencia del par en la lista.

> **Nota:** este test comparte instancia de servidor con `test_saves_context_for_user`, por lo que "ana" puede tener el contexto de `preferred_style` también. El escenario BDD es más estricto al requerir estado limpio; el test actual lo tolera con `assertIn` en lugar de `assertEqual`.

---

### Escenario 3 → *(pendiente de implementar)*

El escenario cubre el caso borde de un usuario que nunca guardó contexto. No existe test explícito para esto en `test_cag_contract.py`, aunque el comportamiento está implícito en `test_ask_answers_from_knowledge_base` (que usa `"base-user"` sin contexto y espera `context_used: []`).

**Test sugerido:**
```python
def test_empty_context_for_new_user(self):
    status, body = self.get_json("/api/context?user_id=usuario_nuevo_xyz")
    self.assertEqual(status, 200)
    self.assertEqual(body["context"], [])
```

---

### Escenario 4 → `test_ask_answers_from_knowledge_base` (en `tests/base/`)

```python
def test_ask_answers_from_knowledge_base(self):
    status, body = self.post_json(
        "/api/ask",
        {"user_id": "base-user", "question": "Que es RAG en el curso?"},
    )
    self.assertEqual(status, 200)
    self.assertIn("RAG recupera", body["answer"])
    self.assertIn("rag", body["sources"])
    self.assertEqual(body["context_used"], [])
```

**Given** implícito: "base-user" no tiene contexto (usuario sin historial).  
**Then**: verifica que la respuesta viene directamente de la base de conocimiento y `context_used` está vacío.

---

### Escenario 5 → `test_ask_uses_context_to_influence_later_response`

```python
def test_ask_uses_context_to_influence_later_response(self):
    self.post_json(
        "/api/context",
        {"user_id": "luis", "key": "audience", "value": "explicar como principiante"},
    )
    status, body = self.post_json(
        "/api/ask",
        {"user_id": "luis", "question": "Que es CAG?"},
    )
    self.assertEqual(status, 200)
    self.assertIn("principiante", body["answer"].lower())
    self.assertIn("audience", body["context_used"])
```

**Given**: el primer `post_json` es la precondición del escenario (contexto guardado).  
**When**: el segundo `post_json` es la pregunta del usuario.  
**Then**: los dos `assertIn` verifican que el contexto influyó en la respuesta y fue reportado en `context_used`.

Este es el escenario más representativo del módulo CAG completo: verifica la cadena entera `ContextStore → apply_context → answer_question`.

---

### Escenarios 6 y 7 → *(pendientes de implementar)*

Estos escenarios cubren casos que el contrato actual no prueba explícitamente:

- **Escenario 6** (múltiples contextos): requeriría guardar 2+ pares para un usuario y verificar que todos aparecen en `context_used` y en el texto de la respuesta.
- **Escenario 7** (actualización de key): requeriría guardar la misma key dos veces y verificar que `list_for_user` retorna exactamente un elemento con el valor más reciente.

Ambos corresponden a la historia **US-03** del backlog (pruebas BDD formales) y están planificados para implementación con `pytest-bdd`.

---

## Cómo ejecutar los tests existentes

```bash
# Tests base (incluye Escenario 4)
PYTHONPATH=. python3 -m pytest tests/base/ -v

# Tests de contrato CAG (Escenarios 1, 2 y 5)
PYTHONPATH=. python3 -m pytest tests/validation/ -v

# Suite completa
PYTHONPATH=. python3 -m pytest tests/ -v
```

## Próximos pasos (US-03 del backlog)

1. Instalar `pytest-bdd`: `pip install pytest-bdd`
2. Crear `tests/bdd/features/cag.feature` con los escenarios Gherkin
3. Crear `tests/bdd/test_cag_bdd.py` con los step definitions en Python
4. Implementar los Escenarios 3, 6 y 7 que actualmente no tienen cobertura
