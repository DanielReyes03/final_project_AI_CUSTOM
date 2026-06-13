# Sprint 3 — Retrospectiva

**Proyecto:** Sistema CAG con Memoria Contextual  
**Fecha:** 2026-06-12  
**Equipo:** Fredy Reyes

---

## Qué salió bien

1. **16/16 tests pasan sin regresiones.** El sprint cerró con la suite completa verde. Agregar 10 tests nuevos (6 + 4) sin romper los 6 existentes confirma que la arquitectura del módulo CAG es estable y bien delimitada.

2. **Los tests TDD revelaron el diseño correcto de la API.** Escribir `test_save_updates_existing_key` antes de pensar en la implementación aclaró que `ContextStore` debía usar un dict de dicts (no una lista) para garantizar unicidad de keys de forma natural. El test guió la estructura de datos.

3. **El mapeo BDD → Python fue más útil que los escenarios solos.** El `tests/bdd/README.md` no solo documenta lo implementado, sino que identifica exactamente qué comportamientos (escenarios 3, 6 y 7) no tienen cobertura de test. Esa brecha es accionable para el próximo sprint.

4. **El frontend mejoró sin tocar el backend.** Todos los cambios de UI (panel de contexto, badge CAG, formulario de guardado) se implementaron únicamente en `index.html`, `styles.css` y `app.js`. El contrato de la API no cambió, los tests del servidor no se tocaron.

5. **`escapeHtml` previene XSS desde el inicio.** Implementar la sanitización desde el primer momento en que se renderizan datos del usuario en el DOM evita introducir la vulnerabilidad más tarde, cuando el código es más difícil de auditar.

---

## Qué se puede mejorar

1. **Los escenarios BDD no son ejecutables todavía.** `docs/bdd/scenarios.md` está en Gherkin pero no hay un archivo `.feature` ni step definitions en Python. Para que US-03 esté realmente completo según sus criterios de aceptación, se necesita `pytest-bdd` instalado y los archivos correspondientes.

2. **Los tests de contrato comparten estado de servidor.** La instancia de servidor se crea una vez por clase (`setUpClass`) y el contexto guardado en un test puede estar disponible en otro. Funciona porque los `user_id` son distintos, pero es un acoplamiento frágil que debería resolverse con un `setUp` que limpie el store.

3. **El frontend no maneja errores de red visualmente.** Si el backend está caído, el formulario de guardar contexto simplemente no hace nada visible. Un mensaje de error o un estado de "sin conexión" mejoraría la experiencia.

4. **No hay feedback visual al guardar contexto exitosamente.** El botón vuelve a "Guardar Contexto" y el panel se actualiza, pero no hay un mensaje tipo "¡Guardado!" que confirme explícitamente la acción al usuario.

5. **`requirements.txt` mezcla dependencias runtime y dev.** El archivo tiene un comentario que dice "Runtime: ninguna" y luego lista `pytest`. Para un proyecto real sería más correcto separar en `requirements.txt` (runtime) y `requirements-dev.txt` (testing).

---

## Acciones concretas para el próximo sprint

| Acción | Descripción | Prioridad |
|---|---|---|
| Implementar BDD ejecutable | Instalar `pytest-bdd`, crear `tests/bdd/features/cag.feature` y `tests/bdd/test_cag_bdd.py` con step definitions para los 7 escenarios | Alta |
| Cubrir escenarios 3, 6 y 7 | Agregar tests Python para: usuario sin historial, múltiples contextos acumulados y actualización de key existente | Alta |
| Limpiar estado en tests de contrato | Agregar `setUp` en `CagContractTest` que reinicie el `ContextStore` entre tests | Media |
| Feedback visual al guardar contexto | Mostrar un mensaje temporal "Contexto guardado" tras POST exitoso | Baja |
| Separar `requirements-dev.txt` | Mover `pytest` a un archivo de dependencias de desarrollo separado | Baja |
