# Sprint 1 — Diario de Ejecución

**Proyecto:** Sistema CAG con Memoria Contextual  
**Sprint objetivo:** Verificar base del proyecto e implementar ContextStore funcional  
**Fechas:** [FECHA INICIO] → [FECHA FIN]  
**Equipo:** Daniel Reyes

---

## Registro diario (Daily Scrum)

> Completa cada entrada con: ¿Qué hice? ¿Qué haré? ¿Hay algún impedimento?

---

### Día 1 — [DD/MM/YYYY]

**¿Qué hice ayer / al inicio del sprint?**

- [ ] Leí el README y entendí la estructura base del proyecto
- [ ] Ejecuté `test.sh` o `scripts/run_base_tests.sh` para verificar el estado inicial
- [ ] Revisé `backend/context_store.py` para entender la implementación actual

**¿Qué haré hoy?**

- [ ] [Completar]

**Impedimentos:**

- Ninguno / [Describir si los hay]

**Notas:**

> [Espacio libre para observaciones del día]

---

### Día 2 — [DD/MM/YYYY]

**¿Qué hice ayer?**

- [ ] [Completar]

**¿Qué haré hoy?**

- [ ] [Completar]

**Impedimentos:**

- [Completar]

**Notas:**

> [Espacio libre para observaciones del día]

---

### Día 3 — [DD/MM/YYYY]

**¿Qué hice ayer?**

- [ ] [Completar]

**¿Qué haré hoy?**

- [ ] [Completar]

**Impedimentos:**

- [Completar]

**Notas:**

> [Espacio libre para observaciones del día]

---

### Día 4 — [DD/MM/YYYY]

**¿Qué hice ayer?**

- [ ] [Completar]

**¿Qué haré hoy?**

- [ ] [Completar]

**Impedimentos:**

- [Completar]

**Notas:**

> [Espacio libre para observaciones del día]

---

### Día 5 — [DD/MM/YYYY] *(día de cierre)*

**¿Qué hice ayer?**

- [ ] [Completar]

**¿Qué haré hoy?**

- [ ] Sprint Review: demostrar lo implementado
- [ ] Sprint Retrospectiva: documentar aprendizajes

**Impedimentos:**

- [Completar]

**Notas:**

> [Espacio libre para observaciones del día]

---

## Seguimiento de tareas

Actualiza el estado de cada tarea a medida que avanzas.  
**Estados:** `Por hacer` → `En progreso` → `Terminado` → `Bloqueado`

| Tarea | Historia | Estado | Fecha inicio | Fecha fin | Notas |
|---|---|---|---|---|---|
| T-01-1 Revisar ContextStore existente | US-01 | Por hacer | | | |
| T-01-2 Implementar `add_turn` | US-01 | Por hacer | | | |
| T-01-3 Implementar `get_context` | US-01 | Por hacer | | | |
| T-01-4 Implementar límite FIFO | US-01 | Por hacer | | | |
| T-01-5 Integrar en `cag.py` | US-01 | Por hacer | | | |
| T-01-6 Prueba de integración manual | US-01 | Por hacer | | | |
| T-04-1 Crear archivo de tests | US-04 | Por hacer | | | |
| T-04-2 Test: inicialización vacía | US-04 | Por hacer | | | |
| T-04-3 Test: agregar y recuperar turnos | US-04 | Por hacer | | | |
| T-04-4 Test: límite máximo FIFO | US-04 | Por hacer | | | |
| T-04-5 Crear test_apply_context.py | US-04 | Por hacer | | | |
| T-04-6 Test: apply_context con historial | US-04 | Por hacer | | | |
| T-04-7 Test: apply_context vacío | US-04 | Por hacer | | | |
| T-04-8 Ejecutar suite completo | US-04 | Por hacer | | | |

---

## Sprint Review — [DD/MM/YYYY]

### Demostración

**¿Qué se comprometió al inicio del sprint?**

- US-01: Memoria de contexto entre preguntas (5 SP)
- US-04: Pruebas TDD para ContextStore y apply_context (3 SP)

**¿Qué se completó?**

| Historia | Completada | Observaciones |
|---|---|---|
| US-01 | Sí / No / Parcial | [Completar] |
| US-04 | Sí / No / Parcial | [Completar] |

**Demo realizada:**

> [Describir brevemente qué se mostró: output de pytest, llamada al endpoint, captura de la UI, etc.]

**Velocity real del sprint:**

- Story points comprometidos: 8
- Story points completados: [Completar]

---

## Sprint Retrospectiva — [DD/MM/YYYY]

### ¿Qué salió bien?

1. [Completar]
2. [Completar]
3. [Completar]

### ¿Qué se puede mejorar?

1. [Completar]
2. [Completar]

### Acciones concretas para el próximo sprint

| Acción | Responsable | Fecha límite |
|---|---|---|
| [Completar] | Daniel Reyes | [Completar] |
| [Completar] | Daniel Reyes | [Completar] |

---

## Estado final de la Definición de Done

Marca cada criterio al cierre del sprint:

- [ ] Código en repositorio (`main` o rama mergeada)
- [ ] Todos los tests unitarios pasan (`pytest tests/unit/`)
- [ ] Tests de base siguen pasando (`scripts/run_base_tests.sh`)
- [ ] Sin errores de sintaxis ni warnings críticos
- [ ] Verificación manual realizada (smoke test)
- [ ] Criterios de aceptación de US-01 y US-04 cumplidos
