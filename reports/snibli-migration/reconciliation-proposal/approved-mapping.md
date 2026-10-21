# Mapeo aprobado para el cambio propuesto — 2026-10-21

El usuario confirmó explícitamente en esta conversación:

> Debe incorporarse al contrato porque es nuevo campo a mapear.

> Deben aceptarse Códice, Reseña y Documento Colonial como tipos documentales.

La aprobación inicial corresponde a C1 y C3 de `decision.json`. Posteriormente,
el usuario respondió «Acepto» a la confirmación del orden observado (C2) y a la
preparación del cambio local. C1–C3 quedan aprobados para ese alcance. No se
atribuye un nombre o cargo institucional que el usuario no haya declarado.

## Incorporación al contrato propuesto

| Atributo | Mapeo |
|---|---|
| Clave literal | `dc.type.genre` |
| Etiqueta | ¿Es un texto comparativo? |
| Formulario | `traditionalpageone` |
| Posición observada | Fila 13 (base cero), después de Edicion(No)/Periodicdad y antes de Identificador |
| Control | Desplegable cerrado, opcional y no repetible |
| Vocabulario | `genrePairs` |
| Valores literales | Sí; No; Incluye Datos de Diferentes Lenguas |
| Ayuda observada | Indique si el recurso es un texto comparativo. |

El contrato propuesto pasa de 56 a 57 bindings y de 54 a 55 claves únicas.
Se retienen los 56 bindings originales. No se cambia el nombre externo del campo
ni se interpreta como un género documental distinto de la pregunta observada.
La aprobación de incorporación no define reglas nuevas para inferir respuestas:
un valor desconocido sigue sin completarse automáticamente.

Para `dc.type`, añadir literalmente **Códice**, **Reseña** y
**Documento Colonial** a `common_types`, conservando los 23 valores anteriores:
total 26. No añadir sinónimos o equivalencias automáticas.

El detalle verificable de los 57 controles y sus valores ya está incluido en
`candidate-contract.json`. Ese archivo se conserva sin cambios para preservar su
hash y las comparaciones offline anteriores; esta decisión documenta la aprobación
posterior de dos cambios concretos. No debe interpretarse su antiguo estado de
revisión como ausencia de la aprobación C1/C3 registrada aquí.

## Pendientes y límites

- `srsc` completo sigue UNKNOWN.
- La interfaz prueba las secciones del borrador 2050 de la colección piloto;
  el endpoint de secciones continúa sin evidencia HAL observable (HTTP 204).
- C2 fue aprobado posteriormente; se conserva el orden observado.
- Se mantienen la aprobación humana y la prohibición de escritura automática;
  se conserva literalmente `dc.subject.linguiscgroup` y la separación de ejes
  lingüísticos.

El cambio local del contrato ejecutable se preparó como `snibli-contract-2026-10-21`,
para revisión sin despliegue. No modifica DSpace, la release v3.9.2, el baseline
activo o el despliegue. No se asigna una versión de skill futura ni se declara
la migración completamente validada.
