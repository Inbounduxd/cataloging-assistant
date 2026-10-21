# Revisión de captura por colección SNIBLI — 2026-10-20

**La sesión y la identidad de la colección se confirmaron. La configuración
presenta drift frente a v3.9.2; la equivalencia completa permanece UNKNOWN.**

Colección: **Lingüística Maayat'aan, Maya**, UUID
`3ce3afb3-94ed-4f60-bfda-0a1242c4d689`, Handle `123456789/393`.
La consulta autenticada `findByCollection` devuelve la definición **traditional**.
El endpoint enlazado `traditional/sections` responde **HTTP 204**, que se conserva
como `ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204` y no como secciones vacías.
Esto coincide con la limitación documentada históricamente en VERTICAL-022.

## Diagnóstico de los flags

El login fue confirmado y hubo 67 peticiones: un POST de autenticación y GET de
lectura. `capture_complete: false` conserva los HTTP 204 de secciones activas y
422 de `srsc/entries`; el fallback de `srsc` solo captura nodos superiores.
`snapshot_complete: false` refleja que no se observó la pertenencia/orden completo
de secciones activas. Los dos FAIL corresponden a drift real en formularios y
vocabularios; no a un problema de contraseña.

No conviene repetir exportaciones idénticas para intentar obtener PASS: las
limitaciones actuales no se resuelven cambiando los límites o las aserciones.

## Comparación con v3.9.2

- Las 54 claves originales están presentes con IDs y scopeNote coincidentes.
- Los dos formularios configurados contienen 57 bindings y 55 claves: los 56
  bindings originales más `dc.type.genre`, etiqueta «¿Es un texto comparativo?»,
  dropdown cerrado y opcional, no repetible, vocabulario `genrePairs`.
- VERTICAL-022 identifica un `BINDING_ADDED` y 29 `ORDER_CHANGED` en el subconjunto
  configurado. No hay eliminaciones ni otros cambios en los controles compartidos.
- `common_types` añade `Códice`, `Reseña` y `Documento Colonial`, conservando los
  23 valores anteriores. De los 21 vocabularios de referencia: 19 PASS, uno FAIL
  y `srsc` UNKNOWN.
- La captura nueva reproduce exactamente los controles configurados y los
  resultados de comparación de vocabularios de la captura anterior. Las
  diferencias no son consecuencia de haber seleccionado ahora la colección.

`review.diff.json` utiliza el motor de diff de VERTICAL-022 para los controles
configurados y declara su alcance acotado. Su baseline es el artefacto preservado
v3.9.2; no se presenta como el snapshot ACTIVE desplegado ni determina cuándo
ocurrieron los cambios. La asignación de `traditional` está observada, pero no se
afirma que los dos formularios comparados sean la totalidad de sus secciones
activas mientras su enlace devuelva 204.

## Siguiente decisión humana

1. Revisar si el nuevo campo y las tres opciones son cambios institucionales
   intencionales y si deben proponerse para el contrato futuro. Conservar la
   release histórica v3.9.2 intacta.
2. Para resolver pertenencia activa, aportar evidencia autorizada de la
   configuración de esa definición o de su renderizado real. No usar el inventario
   global de secciones como sustituto automático de la asociación a la colección.
3. Si se necesita certificar todo el árbol `srsc`, obtener evidencia completa
   mediante una superficie de lectura admitida o una exportación del operador.

Los datos ya permiten documentar el drift para revisión sin repetir credenciales.
No se promovió baseline, modificó DSpace/PostgreSQL/skill/despliegue ni activó cron.

## Procedencia

Los archivos originales `export.json`, `audit.json`, `audit.md`, `diff.json` y
`raw/` permanecen intactos. Esta revisión offline añade `review.audit.json`,
`review.diff.json` y este documento. Los JSON contienen hashes SHA-256 de ambas
capturas y los indicadores de comparación. No hubo acceso a contraseñas o tokens.
No cambió código en esta revisión; se mantienen las 87 pruebas aprobadas.
