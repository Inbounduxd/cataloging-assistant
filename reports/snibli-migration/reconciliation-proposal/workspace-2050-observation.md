# Formulario del borrador 2050 — 2026-10-21

Fuente: https://www.iifl.unam.mx/SNIBLI/workspaceitems/2050/edit,
sesión autenticada de Chrome. Observación de DOM y accesibilidad; no captura HAL.
El usuario indicó expresamente este borrador existente para su inspección.

## Hallazgos

| Comprobación | Evidencia visible | Resultado |
|---|---|---|
| Colección | Lingüística Maayat'aan, Maya; enlace a UUID `3ce3afb3-94ed-4f60-bfda-0a1242c4d689` | PASS |
| Campo adicional | ID DOM `dc_type_genre`, etiqueta «¿Es un texto comparativo?», ayuda «Indique si el recurso es un texto comparativo.» | PASS: coincide con la captura de configuración |
| Opciones del campo | Sí; No; Incluye Datos de Diferentes Lenguas | PASS |
| Presentación | Desplegable único, sin asterisco de obligatoriedad ni botón Añadir más en este control | PASS visual; flags de contrato respaldados por la captura HAL previa |
| Posición | Después de Edicion(No)/Periodicdad y antes de Identificador | PASS |
| Tipos documentales nuevos | En el desplegable Type, ID DOM `31_array-0-dc_type`: Códice; Reseña; Documento Colonial | PASS |
| Secciones renderizadas | `traditionalpageone`, `traditionalpagetwo`, `upload`, `license`, en ese orden | PASS para este borrador |
| Separación lingüística | Lengua de registro y Lengua registrada (Agrupación lingüística) son controles distintos; el segundo conserva `dc_subject_linguiscgroup` en el ID DOM | PASS visual |

Los dos primeros paneles llevan la etiqueta visible Describir; los siguientes,
Subir archivos y Licencia de depósito. Esta es evidencia independiente de las
secciones renderizadas para el borrador 2050 en la colección indicada. No convierte
en observable el endpoint HTTP 204 ni demuestra la configuración de todos los
borradores o de futuros depósitos. No se recertificaron aquí los 57 bindings uno
por uno; su comparación completa sigue siendo la de la captura autenticada.

## Alcance y conservación

Se abrieron los desplegables y se desplazó su lista sin seleccionar opciones,
escribir valores, adjuntar archivos, aceptar licencia, guardar, descartar o
depositar. Al finalizar, el campo comparativo seguía vacío y Guardar figuraba
deshabilitado en la interfaz (clase disabled y control no habilitado).

El árbol completo de `srsc` no fue inspeccionado en esta comprobación y sigue
UNKNOWN. La presencia y ayuda del campo comparativo aclaran su uso presentado
por la interfaz; no sustituyen la confirmación institucional de su semántica ni
constituyen aprobación de C1–C3. No se modifica `decision.json`, el contrato vigente
o la skill v3.9.2. El documento de observación anterior se conserva como registro
del alcance de aquella revisión, ahora complementado por esta evidencia.
