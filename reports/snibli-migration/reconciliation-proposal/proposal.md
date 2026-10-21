# Propuesta de conciliación SNIBLI — 2026-10-20

Estado: **CANDIDATA PARA REVISIÓN — NO ADOPTADA**.

La propuesta refleja lo observado en la captura autenticada de la colección
**Lingüística Maayat'aan, Maya**, UUID `3ce3afb3-94ed-4f60-bfda-0a1242c4d689`,
Handle `123456789/393`, definición `traditional`. No modifica DSpace, el contrato
ejecutable, variables de despliegue, baseline ACTIVE o la skill histórica.

## Cambios propuestos

| Aspecto | Referencia v3.9.2 | Candidata observada |
|---|---|---|
| Bindings configurados | 56 | 57; los 56 originales se conservan |
| Claves únicas | 54 | 55 |
| Campo adicional | No incluido | `dc.type.genre` |
| Etiqueta literal | — | ¿Es un texto comparativo? |
| Control | — | Dropdown, opcional, no repetible, cerrado |
| Vocabulario del campo | — | `genrePairs`: Sí; No; Incluye Datos de Diferentes Lenguas |
| `common_types` | 23 valores | 26; añade Códice, Reseña, Documento Colonial |
| Orden | Referencia preservada | 29 posiciones desplazadas por la inserción |

`candidate-contract.json` conserva los 57 controles con posición, label, flags,
tipo y vocabulario literales, registro de sus 55 claves y valores disponibles de
sus vocabularios. Distingue identidad semántica del binding, ID físico observado
y referencia histórica: al insertar una fila, los IDs físicos basados en fila
pueden cambiar. No se reasignan identidades históricas ni se colapsan los controles
que comparten metadataField.

Se conserva literalmente `dc.subject.linguiscgroup`. La lengua de registro y la
lengua objeto de estudio permanecen separadas; la nueva pregunta no autoriza
inferencias o propagaciones automáticas entre esos ejes.

## Revisión semántica necesaria

`dc.type.genre` se presenta con una pregunta de comparación lingüística y opciones
Sí/No/Incluye Datos de Diferentes Lenguas. La captura prueba esa configuración,
pero no define por sí sola la intención institucional del campo. La candidata
conserva exactamente la configuración y deja su significado pendiente de revisión.
No propone renombrar la clave externa ni autocompletar el nuevo control.

Las tres nuevas opciones de tipo documental se proponen como valores literales.
No se añaden sinónimos, equivalencias o reglas de clasificación automática.

## Límites que no se aprueban por esta propuesta

- El endpoint de secciones activas devuelve HTTP 204. Los dos formularios son un
  inventario configurado comparable; no se declara que sean la totalidad del
  formulario activo de la colección. No se inventa una resolución de evidencia.
- `srsc` solo expone el fallback de nodos superiores tras HTTP 422; el árbol
  completo sigue UNKNOWN.
- La referencia es la release preservada, no un snapshot ACTIVE histórico
  exportado del servicio. No se determina cuándo se hicieron las adiciones.

## Decisión revisable

`decision.json` enumera C1–C3: campo adicional, conservación de controles/orden y
tres valores de `common_types`. Estado PENDING_HUMAN_REVIEW; no se rellenaron
aprobador, fecha o intención institucional. La instrucción de continuar permitió
preparar esta propuesta, sin inventar una aprobación institucional de su semántica.

Recomendación: revisar C1–C3 y el significado del nuevo campo; si se aprueban,
preparar un cambio gobernado futuro de contrato y sus pruebas. La numeración de
una futura release queda sin asignar. Mantener v3.9.2 intacta y no promover un
baseline o declarar equivalencia completa sin conservar los warnings y obtener
la evidencia activa correspondiente.

## Validación y procedencia

`validation.json` verifica fidelidad de los 57 controles, identidades únicas,
55 claves registradas, conservación de las 56 referencias, políticas de no
escritura y aprobación humana, hash del export y hashes de todos sus cuerpos
raw. El checksum de la release v3.9.2 se volvió a verificar sin reconstruir ni
modificar archivos. PASS aquí significa fidelidad documental de la candidata,
no aprobación o compatibilidad completa de la migración.

Solo se añadieron artefactos de revisión. No cambió código en esta fase y se
mantienen las 87 pruebas aprobadas; no se repitió la suite sin cambios de código.
Sin nuevas solicitudes HTTP, credenciales, PostgreSQL, commits, PR o despliegues.
