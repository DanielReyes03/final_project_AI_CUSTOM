# Sprint 2 — Retrospectiva

**Proyecto:** Sistema CAG con Memoria Contextual  
**Fecha:** 2026-06-12  
**Equipo:** Daniel Reyes

---

## Qué salió bien

1. **El contrato guió la implementación.** Leer `test_cag_contract.py` antes de escribir código dejó muy claro qué debía retornar cada función y en qué formato. No hubo sorpresas al correr los tests.

2. **La arquitectura base era sólida.** El servidor ya tenía `context_store` instanciado a nivel de módulo y el flujo de handlers bien separado. Integrar el nuevo código requirió cambios mínimos (una sola línea en `server.py`).

3. **El enfoque incremental funcionó.** Implementar y validar en orden (`context_store` → `cag` → `assistant`) permitió detectar exactamente en qué capa estaba el problema en cada momento, sin tener que debuggear el sistema completo de golpe.

4. **Cero regresiones.** Los 3 tests de base siguieron pasando en todo momento. La decisión de pasar `context_store` como parámetro explícito, en lugar de importarlo o crear un singleton nuevo, evitó cualquier efecto secundario en los tests existentes.

---

## Qué se puede mejorar

1. **`apply_context` no es inteligente, solo concatena.** La respuesta enriquecida es mecánica: añade el contexto como texto literal al final. En un sistema real, el contexto debería modificar el tono y el vocabulario de toda la respuesta, no solo pegarse al final.

2. **No hay persistencia entre reinicios del servidor.** El `ContextStore` almacena todo en RAM. Si el servidor se reinicia, el contexto de todos los usuarios se pierde. Para un proyecto real sería necesario serializar a disco o base de datos.

3. **Falta validación de tipos en `save`.** El método acepta cualquier `value` sin verificar que sea serializable o que tenga un formato esperado. Podría causar errores silenciosos con inputs inesperados.

4. **Los tests de contrato comparten estado entre casos.** El servidor se instancia una sola vez por clase de test (`setUpClass`), por lo que el contexto guardado en un test puede "contaminar" otro. Funciona ahora porque los tests usan `user_id` distintos, pero es frágil.

---

## Acciones concretas para el próximo sprint

| Acción | Descripción | Prioridad |
|---|---|---|
| Implementar pruebas TDD unitarias | Crear `tests/unit/test_context_store.py` y `tests/unit/test_apply_context.py` para cubrir US-04 del backlog | Alta |
| Implementar pruebas BDD | Crear escenarios Gherkin para el flujo CAG completo, cubriendo US-03 del backlog | Alta |
| Documentar la API del módulo CAG | Añadir docstrings a `apply_context`, `save` y `list_for_user` con ejemplos de uso | Media |
| Revisar aislamiento de tests | Añadir `setUp` que limpie el `ContextStore` entre tests de contrato para evitar dependencia de orden | Media |
