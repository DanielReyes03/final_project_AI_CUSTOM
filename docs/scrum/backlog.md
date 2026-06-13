# Product Backlog

**Proyecto:** Sistema CAG con Memoria Contextual  
**Equipo:** Daniel Reyes  
**Última actualización:** 2026-06-12

---

## Historias de Usuario

### US-01 — Memoria de contexto entre preguntas

**Como** usuario,  
**quiero** que el sistema recuerde mi contexto entre preguntas,  
**para** recibir respuestas personalizadas y coherentes a lo largo de una sesión.

| Campo | Valor |
|---|---|
| **Prioridad** | Alta |
| **Estimación** | 5 story points |
| **Sprint** | Sprint 1 |

**Criterios de aceptación:**

1. Dado que el usuario hace una pregunta de seguimiento sin repetir el contexto previo, cuando el sistema procesa la pregunta, entonces la respuesta debe referenciar o incorporar información de la conversación anterior.
2. Dado que el usuario lleva al menos 3 turnos de conversación, cuando se inspecciona el `ContextStore`, entonces debe contener un historial ordenado con los últimos N intercambios (configurable).
3. Dado que se inicia una nueva sesión (session_id distinto), cuando el usuario hace la primera pregunta, entonces el sistema no debe usar contexto de sesiones anteriores.
4. Dado que el contexto acumulado supera el límite configurado, cuando se agrega un nuevo turno, entonces el contexto más antiguo se descarta (política FIFO) sin error.

---

### US-02 — Preferencias de usuario persistentes

**Como** usuario,  
**quiero** guardar preferencias como "explícame como principiante",  
**para** que el sistema las aplique automáticamente en todas mis respuestas sin que yo tenga que repetirlas.

| Campo | Valor |
|---|---|
| **Prioridad** | Media |
| **Estimación** | 3 story points |
| **Sprint** | Sprint 2 |

**Criterios de aceptación:**

1. Dado que el usuario declara una preferencia de estilo (e.g., "explícame como principiante"), cuando el sistema procesa preguntas posteriores en esa sesión, entonces las respuestas deben adaptarse al nivel indicado (vocabulario simple, analogías básicas).
2. Dado que se ha guardado una preferencia, cuando se llama a `apply_context`, entonces la preferencia se inyecta en el prompt junto con el historial de conversación.
3. Dado que el usuario declara una preferencia nueva que contradice la anterior (e.g., cambia de "principiante" a "experto"), cuando el sistema procesa la siguiente pregunta, entonces la preferencia más reciente toma precedencia.
4. Dado que no se ha declarado ninguna preferencia, cuando `apply_context` construye el prompt, entonces no se agrega ningún bloque de preferencias al contexto.

---

### US-03 — Pruebas BDD para el flujo CAG completo

**Como** desarrollador,  
**quiero** pruebas BDD que validen el flujo CAG completo (pregunta → contexto → respuesta),  
**para** garantizar que cada componente integra correctamente y el comportamiento del sistema es el especificado.

| Campo | Valor |
|---|---|
| **Prioridad** | Alta |
| **Estimación** | 5 story points |
| **Sprint** | Sprint 2 |

**Criterios de aceptación:**

1. Dado un escenario BDD escrito en lenguaje Gherkin (Given/When/Then), cuando se ejecuta el suite con `pytest-bdd` (u equivalente), entonces todos los escenarios definidos deben pasar sin errores.
2. Dado que el flujo CAG recibe una pregunta de seguimiento con contexto previo, cuando se ejecuta el escenario BDD correspondiente, entonces la respuesta simulada debe contener datos del turno anterior.
3. Dado que el `ContextStore` está vacío al inicio de un escenario, cuando el escenario lleva a cabo múltiples pasos de conversación, entonces al final el store contiene exactamente los turnos generados por ese escenario.
4. Dado que algún componente del flujo CAG falla (e.g., knowledge base no encontrada), cuando se corre el escenario de error correspondiente, entonces el test valida que el sistema retorna el mensaje de error apropiado y no arroja excepción no manejada.

---

### US-04 — Pruebas TDD unitarias para ContextStore y apply_context

**Como** desarrollador,  
**quiero** pruebas TDD unitarias para `ContextStore` y `apply_context`,  
**para** asegurar que cada función se comporta correctamente de forma aislada y facilitar el refactor seguro del código.

| Campo | Valor |
|---|---|
| **Prioridad** | Alta |
| **Estimación** | 3 story points |
| **Sprint** | Sprint 1 |

**Criterios de aceptación:**

1. Dado un `ContextStore` recién inicializado, cuando se llama a `get_context(session_id)`, entonces retorna una lista vacía sin lanzar excepciones.
2. Dado que se agregan N turnos al `ContextStore` mediante `add_turn`, cuando se llama a `get_context`, entonces retorna exactamente esos N turnos en orden de inserción.
3. Dado que el store alcanza la capacidad máxima definida, cuando se agrega un turno adicional, entonces el turno más antiguo es eliminado y la longitud del historial no supera el límite.
4. Dado una lista de mensajes de historial y un texto de consulta, cuando se llama a `apply_context`, entonces retorna un string que contiene tanto el historial formateado como la consulta original.
5. Dado que `apply_context` recibe un historial vacío, cuando se ejecuta, entonces retorna únicamente la consulta original sin texto adicional de contexto.

---

## Tabla resumen

| ID | Historia | Prioridad | Story Points | Sprint |
|---|---|---|---|---|
| US-01 | Memoria de contexto entre preguntas | Alta | 5 | Sprint 1 |
| US-04 | Pruebas TDD para ContextStore y apply_context | Alta | 3 | Sprint 1 |
| US-03 | Pruebas BDD para flujo CAG completo | Alta | 5 | Sprint 2 |
| US-02 | Preferencias de usuario persistentes | Media | 3 | Sprint 2 |

**Velocidad estimada Sprint 1:** 8 story points  
**Total backlog:** 16 story points
