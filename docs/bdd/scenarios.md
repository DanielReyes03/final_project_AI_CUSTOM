# Escenarios BDD — Módulo CAG

**Proyecto:** Sistema CAG con Memoria Contextual  
**Formato:** Gherkin (Given / When / Then)  
**Fecha:** 2026-06-12

---

## Feature: Gestión de contexto de usuario

> Como usuario del sistema CAG,
> quiero que el sistema recuerde mis preferencias y contexto,
> para recibir respuestas adaptadas a mi perfil sin repetir información en cada pregunta.

---

### Escenario 1: Guardar contexto exitosamente

```gherkin
Scenario: El usuario guarda un contexto por primera vez
  Given un usuario identificado como "ana"
  And el sistema no tiene contexto previo para "ana"
  When el usuario envía la preferencia con clave "preferred_style" y valor "explicaciones con analogias"
  Then el sistema confirma que el contexto fue guardado
  And la respuesta tiene código de estado 201
  And el cuerpo de la respuesta contiene "saved": true
```

---

### Escenario 2: Recuperar contexto de usuario existente

```gherkin
Scenario: El usuario recupera su contexto previamente guardado
  Given un usuario identificado como "ana"
  And el sistema tiene guardado el contexto con clave "project" y valor "usa arquitectura monolitica moderna"
  When el usuario solicita su lista de contexto
  Then el sistema retorna el contexto completo del usuario
  And la respuesta tiene código de estado 200
  And el cuerpo incluye "user_id": "ana"
  And el cuerpo incluye el par {"key": "project", "value": "usa arquitectura monolitica moderna"}
```

---

### Escenario 3: Recuperar contexto de usuario sin historial

```gherkin
Scenario: Un usuario nuevo no tiene contexto acumulado
  Given un usuario identificado como "nuevo_usuario_xyz"
  And el sistema no tiene ningún contexto registrado para ese usuario
  When el usuario solicita su lista de contexto
  Then el sistema retorna una respuesta vacía
  And la respuesta tiene código de estado 200
  And el campo "context" de la respuesta es una lista vacía []
```

---

### Escenario 4: Pregunta sin contexto previo retorna respuesta base

```gherkin
Scenario: El sistema responde con información base cuando no hay contexto del usuario
  Given un usuario identificado como "usuario_sin_contexto"
  And el sistema no tiene contexto registrado para ese usuario
  When el usuario pregunta "Que es RAG en el curso?"
  Then el sistema busca la respuesta en la base de conocimiento
  And la respuesta tiene código de estado 200
  And el campo "answer" contiene "RAG recupera"
  And el campo "context_used" es una lista vacía []
  And el campo "sources" contiene "rag"
```

---

### Escenario 5: Pregunta con contexto previo adapta la respuesta

```gherkin
Scenario: El sistema adapta la respuesta según la audiencia guardada en el contexto
  Given un usuario identificado como "luis"
  And el sistema tiene guardado el contexto con clave "audience" y valor "explicar como principiante"
  When el usuario pregunta "Que es CAG?"
  Then el sistema combina la respuesta base con el contexto del usuario
  And la respuesta tiene código de estado 200
  And el campo "answer" contiene la palabra "principiante"
  And el campo "context_used" incluye la clave "audience"
```

---

### Escenario 6: Múltiples contextos acumulados influyen en la respuesta

```gherkin
Scenario: El sistema aplica todos los contextos acumulados del usuario
  Given un usuario identificado como "mario"
  And el sistema tiene guardado el contexto con clave "audience" y valor "explicar como principiante"
  And el sistema tiene guardado el contexto con clave "preferred_style" y valor "usar ejemplos practicos"
  When el usuario pregunta "Que es SDD?"
  Then el sistema construye una respuesta enriquecida con todos los contextos
  And la respuesta tiene código de estado 200
  And el campo "answer" contiene la palabra "principiante"
  And el campo "answer" contiene la frase "usar ejemplos practicos"
  And el campo "context_used" incluye la clave "audience"
  And el campo "context_used" incluye la clave "preferred_style"
```

---

### Escenario 7: Actualizar un contexto ya existente (misma key)

```gherkin
Scenario: El usuario actualiza una preferencia existente con un nuevo valor
  Given un usuario identificado como "sofia"
  And el sistema tiene guardado el contexto con clave "audience" y valor "explicar como principiante"
  When el usuario envía la preferencia con clave "audience" y valor "explicar como experto en sistemas"
  Then el sistema actualiza el valor existente sin duplicar la clave
  And la respuesta tiene código de estado 201
  And la respuesta contiene "saved": true
  When el usuario solicita su lista de contexto
  Then el campo "context" contiene exactamente un elemento con clave "audience"
  And ese elemento tiene valor "explicar como experto en sistemas"
```

---

## Notas de diseño

- Cada escenario es **independiente**: parte de un estado conocido del sistema y no asume el orden de ejecución de otros escenarios.
- Los valores de `user_id` son distintos entre escenarios para evitar contaminación de estado.
- El Escenario 7 usa dos bloques `When/Then` porque verifica tanto la operación de guardado como el estado resultante en una lectura posterior.
