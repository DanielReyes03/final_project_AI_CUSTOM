# Sprint 1 — Planificación

**Proyecto:** Sistema CAG con Memoria Contextual  
**Duración:** 1 semana (ajustar a fechas reales)  
**Equipo:** Daniel Reyes

---

## Objetivo del Sprint

> **"Verificar base del proyecto e implementar ContextStore funcional"**

Al finalizar este sprint, el `ContextStore` debe estar implementado y testeado con pruebas unitarias TDD, y la sesión de contexto debe mantenerse correctamente entre llamadas al backend.

---

## Historias seleccionadas

| ID | Historia | Story Points | Estado inicial |
|---|---|---|---|
| US-01 | Memoria de contexto entre preguntas | 5 | Por hacer |
| US-04 | Pruebas TDD para ContextStore y apply_context | 3 | Por hacer |

**Velocidad del sprint:** 8 story points

---

## Desglose de tareas

### US-01 — Memoria de contexto entre preguntas (5 SP)

| # | Tarea | Descripción | Estimación |
|---|---|---|---|
| T-01-1 | Revisar `ContextStore` existente | Leer `backend/context_store.py` y documentar el estado actual de la clase | 1h |
| T-01-2 | Implementar `add_turn` | Método que agrega un par (pregunta, respuesta) al historial de sesión | 1h |
| T-01-3 | Implementar `get_context` | Método que retorna el historial de una sesión dado su `session_id` | 1h |
| T-01-4 | Implementar límite FIFO | Lógica de descarte del turno más antiguo cuando se supera `max_turns` | 1h |
| T-01-5 | Integrar `ContextStore` en `cag.py` | Conectar el store al pipeline de generación de respuestas | 1.5h |
| T-01-6 | Prueba de integración manual | Verificar con `curl` o la UI que el contexto persiste entre preguntas | 0.5h |

### US-04 — Pruebas TDD para ContextStore y apply_context (3 SP)

| # | Tarea | Descripción | Estimación |
|---|---|---|---|
| T-04-1 | Crear archivo de tests | Crear `tests/unit/test_context_store.py` con estructura base | 0.5h |
| T-04-2 | Test: inicialización vacía | Verificar que `get_context` retorna `[]` para sesión nueva | 0.5h |
| T-04-3 | Test: agregar y recuperar turnos | Verificar orden de inserción y contenido exacto | 0.5h |
| T-04-4 | Test: límite máximo FIFO | Verificar descarte del turno más antiguo al superar `max_turns` | 1h |
| T-04-5 | Crear `tests/unit/test_apply_context.py` | Tests para la función `apply_context` de `cag.py` | 0.5h |
| T-04-6 | Test: apply_context con historial | Verificar que retorna historial + consulta concatenados | 0.5h |
| T-04-7 | Test: apply_context con historial vacío | Verificar que retorna solo la consulta original | 0.5h |
| T-04-8 | Ejecutar suite completo | Correr `pytest tests/unit/` y confirmar que todos pasan | 0.5h |

---

## Definición de Done (DoD) — Sprint 1

Un ítem se considera **Terminado** cuando cumple **todos** los criterios siguientes:

- [ ] El código implementado está en el repositorio en la rama `main` (o rama de feature mergeada).
- [ ] Todos los tests unitarios relacionados con la tarea pasan (`pytest` sin errores).
- [ ] Los tests existentes de base (`tests/base/`) siguen pasando sin regresiones.
- [ ] El código no tiene errores de sintaxis ni warnings críticos de linter.
- [ ] La funcionalidad fue verificada manualmente al menos una vez (smoke test).
- [ ] La historia cumple todos sus criterios de aceptación definidos en el backlog.

---

## Riesgos identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| `ContextStore` tiene bugs en la implementación base | Media | Alto | Cubrir con tests TDD antes de integrar |
| La integración en `cag.py` rompe el flujo existente | Baja | Alto | Correr `tests/base/` después de cada cambio |
| Tiempo insuficiente para US-01 completo | Media | Medio | US-04 tiene prioridad; US-01 se puede extender al Sprint 2 si es necesario |

---

## Notas

- Los scripts `scripts/run_base_tests.sh` y `scripts/validate_student_cag.sh` deben seguir pasando al final del sprint.
- No modificar `tests/base/` ni `tests/validation/` — son tests de contrato del proyecto base.
