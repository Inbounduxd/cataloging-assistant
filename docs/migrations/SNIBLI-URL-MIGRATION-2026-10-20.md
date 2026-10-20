# SNIBLI — Migración de URL pública y preservación del contrato catalográfico

Fecha: 2026-10-20
Estado: ADOPTADA PARA URL PÚBLICA / VERIFICACIÓN PENDIENTE PARA API Y EQUIVALENCIA RUNTIME
Ámbito: SNIBLI, DSpace Cataloging Assistant, skill dspace-cataloger

## Decisión

La URL pública canónica del proyecto SNIBLI es:
https://www.iifl.unam.mx/SNIBLI/home

La antigua UI `http://132.248.101.240:4000/home` se conserva solo como referencia histórica, no como URL pública recomendada. No se interpreta el cambio de hostname/ruta de UI como evidencia de un cambio de API, metadatos, vocabularios o persistencia.

La dirección REST histórica es `http://132.248.101.240:8080/server/api` y la nueva REST queda **NO VERIFICADA**. En particular, no suponer `https://www.iifl.unam.mx/SNIBLI/server/api` hasta comprobar una respuesta HAL de DSpace, autenticación de solo lectura y compatibilidad. No sustituir `DSpace_BASE_URL` automáticamente ni reconfigurar jobs de ingesta/sync.

## Invariantes de catálogo

1. Mantener la release vigente del registro `skills/dspace-cataloger/CURRENT_RELEASE.md`: v3.9.2 (hash y artefacto sin modificaciones).
2. Preservar los 56 bindings y los formularios `traditionalpageone` y `traditionalpagetwo`, su orden `formOrder → row → fieldIndex → metadataIndex`, sus etiquetas literales, flags required/repeatable y los metadatos canónicos.
3. No normalizar ni renombrar claves externas, especialmente `dc.subject.linguiscgroup`.
4. Preservar vocabularios controlados y las reglas CLIN/INALI: familia→agrupación→variante; rama opcional no CLIN. Mantener separados lengua de registro, lengua objeto de estudio y uso de la lengua.
5. Mantener estados de evidencia y QA fuera de los metadatos, sin inferencias por plausibilidad ni aproximación de valores cerrados.
6. Mantener `autoWrite=false`, acceso agente read-only y aprobación humana obligatoria; no depositar ni mutar DSpace.
7. Conservar Golden Set GR01–GR23 y la protección ORCID evidence-only de v3.9.2.
8. Conservar UUID y Handle de colecciones salvo que la API de la instancia migrada pruebe un cambio. No inferir equivalencia de bases a partir de URLs.

## Distinción de configuración

- `SNIBLI_PUBLIC_HOME_URL=https://www.iifl.unam.mx/SNIBLI/home` — dirección pública canónica documental; configuración propuesta, no variable runtime existente.
- `DSpace_UI_BASE_URL` — base frontend de DSpace; validar rutas e identificadores antes de asignar; **pendiente de comprobación**.
- `DSpace_BASE_URL` — raíz REST API: **pendiente de comprobación**.
- `DSpace_WORKFLOW_UI_URL` — no derivar por concatenación; verificar por separado.

## Criterios de aceptación para declarar migración compatible

- Abrir UI, ítem y colección representativos; comprobar enlaces persistentes, inicio de sesión y permisos.
- Descubrir REST real por configuración del frontend o HAL /server/api y revisar CORS/CSRF, authn/status, metadatos y bitstreams; solo llamadas read-only.
- Exportar nuevo snapshot de formularios/campos/vocabularios y comparar contra baseline versionada con hash; no activar automáticamente si hay drift.
- Comparar recuento, binding IDs, orden, etiquetas, required/repeatable, closed vocabularies, nombres literales, tipos y valores.
- Ejecutar GR01–GR23 y pruebas de regresión del flujo de sincronización/informes.
- Si todo coincide: cambiar configuraciones runtime vía despliegue revisado, nunca mutando el artefacto de la skill histórica.
- Ante cualquier diferencia: registrar `SCHEMA_DRIFT` o `VOCABULARY_DRIFT`, requerir revisión humana, no afirmar equivalencia.

## Evidencia disponible a la fecha

La nueva página pública es recuperable. No se verificó una REST API bajo `/SNIBLI/server/api`. El repositorio contiene referencias IP antiguas en `.env.example`, `apps/api/src/cataloging_api/config.py` y runbooks; se dejan sin modificar hasta establecer la nueva URL API. La release v3.9.2 declara 56 bindings, Golden Set GR01–GR23, 86 archivos y checksum SHA-256 `b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede`.

Este registro de migración es un cambio documental aditivo; no constituye prueba de equivalencia funcional ni reemplaza los contratos estructurales de la skill.

## Revisión técnica adicional — 2026-10-20

- Se confirmó que el repositorio ya implementa un mecanismo de snapshot y drift, VERTICAL-022; reutilizarlo, no reemplazarlo.
- Baseline documentada en `docs/vertical-022-live-contract-reconciliation.md` (2026-08-26): 18 schemas, 292 metadata fields, 12 submission definitions, 46 sections, 15 configured forms, 179 global bindings y 56 bindings de los dos formularios relevantes.
- La conciliación histórica presentó `STRUCTURAL_MATCH_100_PERCENT` de 56/56 y `REGISTRY_MATCH_100_PERCENT` de 54/54; **no son resultados de la migración actual**.
- Advertencia heredada: el endpoint `/config/submissiondefinitions/traditional/sections` retornó HTTP 204 en el snapshot original; mantener `ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204` si persiste.
- Los intentos de acceder desde el entorno de verificación a la URL web y a los candidatos `/SNIBLI/server/api` y `/server/api` no permitieron constatar una API REST. Estos candidatos no se aprueban como configuración.
- No se cambió `DSpace_BASE_URL`, `DSpace_UI_BASE_URL`, ni las variables de despliegue; no se ejecutaron pruebas end-to-end ni el Golden Set sobre la instancia nueva.

### Continuación segura en el entorno de despliegue

1. Inspeccionar la configuración pública del frontend institucional para determinar el REST base y confirmar con un GET de solo lectura a `/core/metadataschemas`, sin asumir rutas.
2. Usar las credenciales read-only y el collector existente de VERTICAL-022 para preservar HAL+JSON y generar snapshot, sin promover baseline.
3. Comparar el snapshot con el ACTIVE previo y el contrato de 56 bindings; evaluar también 54 claves de metadatos, 23 golden tests, vocabularios, collection UUID y handle.
4. Si no hay drift ni warning nuevo, solicitar aprobación humana para configurar la URL REST real y lanzar pruebas de regresión. Si aparece drift, detener promoción, mantener el baseline y generar reporte de diferencias.
5. No alterar ni reconstruir `skills/dspace-cataloger/versions/v3.9.2/` a causa de una mera migración de URL.

### Integridad de numeración

El ADR-013 original del proyecto es `docs/adr/ADR-013-contrato-maestro-catalogacion.md`. Este registro SNIBLI reside en `docs/migrations/` para evitar reutilizar ese identificador de decisión.
