# Observación autenticada de la interfaz — 2026-10-21

## Alcance

Revisión de lectura en la sesión de Google Chrome iniciada por el usuario.
No se extrajeron credenciales, cookies o tokens. No se pulsaron Guardar,
Agregar plantilla, Nuevo depósito, Eliminar ni acciones de modificación.

## Evidencia observada

- La página de inicio muestra la barra de administración y el menú de perfil
  autenticado. La sesión permite abrir la edición de la colección objetivo.
- La URL `/SNIBLI/collections/3ce3afb3-94ed-4f60-bfda-0a1242c4d689`
  muestra el título **Lingüística Maayat'aan, Maya** y su comunidad
  **Maayat'aan, Maya**. Resultado de identidad visual: PASS.
- El enlace visible «Editar esta colección» lleva a
  `/SNIBLI/collections/3ce3afb3-94ed-4f60-bfda-0a1242c4d689/edit/metadata`.
- Las pestañas visibles son Editar metadatos, Asignar roles, Origen del contenido,
  Curar, Control de acceso, Autorizaciones y Mapeo de ítems. En la pestaña de
  metadatos aparecen Plantilla de ítem, logotipo, nombre, descripción, copyright,
  noticias y licencia. No presenta secciones de depósito ni su orden.
- El menú Editar ofrece Comunidad, Colección e Ítem. El menú Registros ofrece
  Metadatos y Formato. Estas opciones observadas no incluyen un visor de
  formularios de depósito o un explorador de vocabularios controlados.
- Al pulsar «Explora por tema» no se observó un árbol o menú temático adicional.
  Esto no demuestra ausencia de `srsc` en el servidor.

## Resultados pendientes

| Comprobación | Estado | Motivo |
|---|---|---|
| Membresía y orden de las secciones activas | UNKNOWN | No expuestos por las vistas inspeccionadas; el endpoint previamente capturado devolvió 204 |
| Árbol completo de `srsc` | UNKNOWN | No expuesto en las vistas inspeccionadas; el fallback previo solo contiene nodos superiores |
| Intención institucional de `dc.type.genre` y nuevas opciones | PENDIENTE | Requiere respuesta humana, no se deduce de una sesión de administrador |

No se recorrieron todas las pantallas del sistema ni se declara que no exista
otra vista. No se inició un depósito para evitar crear un borrador. Una pantalla
de edición de metadatos de ítem tampoco demostraría el formulario activo.

## Evidencia necesaria para cerrar la auditoría

El responsable de la configuración puede aportar una exportación de lectura de
la definición `traditional`, sus secciones ordenadas y los formularios vinculados,
así como la definición completa de `srsc` con sus relaciones padre-hijo. Debe
identificar instancia, colección, fecha y procedencia. Cualquier secreto debe
excluirse. Esta solicitud queda preparada; no se envió comunicación a terceros.

La candidata conserva su estado de revisión, sin aprobación ni adopción. Se
mantienen los dos FAIL históricos y la equivalencia completa UNKNOWN. No hubo
cambios de código: no se repitieron las 100 pruebas previamente aprobadas.
