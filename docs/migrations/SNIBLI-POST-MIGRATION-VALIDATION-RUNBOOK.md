# SNIBLI — Runbook de verificación posmigración (2026-10-20)

Estado: READY_FOR_OPERATOR / NOT EXECUTED
Origen: URL institucional pública comunicada por el proyecto, https://www.iifl.unam.mx/SNIBLI/home
Contrato: `docs/adr/ADR-013-contrato-maestro-catalogacion.md`
Migración: `docs/migrations/SNIBLI-URL-MIGRATION-2026-10-20.md`
Skill canónica: `skills/dspace-cataloger/CURRENT_RELEASE.md` (v3.9.2)
Motor existente: VERTICAL-022. No crear collector paralelo.

## 0. Alcance y restricciones

Esta guía no supone equivalencia entre la URL frontend y la REST API. Ejecutar desde el host/servicio API de Dokploy con credenciales read-only ya autorizadas. No revelar secretos en CLI, tickets, logs ni Git. No ejecutar migraciones de base de datos ni habilitar cron como parte del diagnóstico. El collector escribe *solo snapshots/auditoría en PostgreSQL local*; no escribe en DSpace. Los endpoints de autenticación pueden utilizar POST /authn/login para obtener sesión de lectura.

## 1. Identificar la REST API real — solo lectura

Inspeccionar configuración Angular/DSpace del frontend en herramientas de red o configuración de despliegue, sin asumir que el API comparte `/SNIBLI`. Confirmar hostname, esquema HTTPS, puerto y prefijo exacto. Desde un entorno autorizado:

```bash
# Ejemplo: sustituir el valor únicamente después de descubrirlo y aprobarlo.
# Nunca derivar de la URL /SNIBLI/home por concatenación.
API_BASE="<REST_BASE_CONFIRMADA>"
curl -fsS --max-time 20 -H 'Accept: application/hal+json' "$API_BASE/core/metadataschemas?page=0&size=1"
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' --max-time 20 "$API_BASE/authn/status"
```

Exigir HAL JSON coherente con DSpace, redirecciones controladas y certificados válidos. Un HTTP 200 con HTML de la web no demuestra que exista REST. No hacer cambios de configuración hasta comprobar API y autenticación con la cuenta aprobada.

## 2. Preservar el estado previo

Antes de tocar `DSpace_BASE_URL` verificar y registrar de forma privada, sin credenciales: release hash `b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede`, snapshot ACTIVE actual y su hash, URL REST previa, UUID `e9a8f44f-a8d3-4d22-b02a-cf590285bac6`, Handle `123456789/4`, versión y commit desplegados.

Si el nuevo entorno representa otra base de datos, detener: UUID/Handle no prueban por sí solos equivalencia de colección. Confirmar primero el item/collection identity.

## 3. Ejecutar un único ciclo de observación

El administrador actualiza `DSpace_BASE_URL` en la configuración del **servicio API de staging** (preferible) o en una ventana aprobada, tras verificar `API_BASE`, sin editar los defaults de `apps/api/src/cataloging_api/config.py`. Mantener secretos `DSPACE_READ_USERNAME` y `DSPACE_READ_PASSWORD` bajo el gestor de secretos. En el runtime ya migrado, con esquema SQL al menos 0024:

```bash
make contract-sync
# alternativa:
docker compose run --rm api python -m cataloging_api.dspace.contract_job
```

Nota: `docker compose run` crea un contenedor nuevo y podría no heredar todas las variables de Dokploy; comprobar la inyección de secretos de la misma manera que en el servicio API antes de ejecutar. El comando persiste snapshots locales append-only y debe ejecutarse solo con autorización operativa.

Guardar el JSON devuelto y revisar `run_id`, `snapshot_id`, `observed_hash`, `effective_hash`, `governed_hash`, `resolution_inherited`, `contract_health`, `warning_count`.

## 4. Comparar con la baseline documentada

Snapshot histórico de 2026-08-26 (`docs/vertical-022-live-contract-reconciliation.md`):
- 18 metadata schemas
- 292 campos metadata globales
- 12 submission definitions
- 46 submission sections
- 15 submission forms
- 179 global bindings
- `traditionalpageone` 44 + `traditionalpagetwo` 12 = 56 bindings
- 54 claves metadata únicas
- export semantic hash `8260b2023b7b417f3056d3724664869f96cb613371c673517d6b7400af2a0b1c`
- 56-binding normalized comparison hash `5b549a16307354b84b9327325532755877a622e323573616e92c8a0dee93ea92`
- historical effective canonical hash `336972fc4461fce821ef8f9625087de864102ce2b2e7d411cd0daadaf3d9014d`

Los recuentos/hash históricos se usan como señales diagnósticas, **no** como única prueba de compatibilidad. Comparar semánticamente IDs, metadataField, uiLabel, required, repeatable, type, vocabulary, closed, formOrder, renderOrder, valores controlados y cobertura registral. Mantener `dc.subject.linguiscgroup` literal.

## 5. Interpretación fail-closed

- `SYNCED` + `NO_CHANGE` + `resolution_inherited=true`: sin diferencia observable respecto al baseline ACTIVE, siempre sujeto a warnings de observabilidad.
- `BASELINE_REQUIRED`: requiere revisión humana, no promover automáticamente.
- `REVIEW_REQUIRED` / `DRIFT_DETECTED`: no promover ni activar scheduler; exportar diff.
- Error de red/auth o snapshot incompleto: conservar baseline anterior y no inferir eliminaciones.
- `/config/submissiondefinitions/traditional/sections` HTTP 204: `UNOBSERVABLE_SURFACE`, **no** sección vacía.

## 6. Regresión y aprobación

Ejecutar suite de contrato y Golden Set GR01–GR23 en el entorno de pruebas; la existencia de dichos tests no significa que se hayan ejecutado. Comprobar ítem/colección, bitstreams, URLs persistentes, permisos, reporting y vocabularios. Solo tras evidencia equivalente y aprobación humana: promover snapshot mediante flujo gobernado, actualizar URL API en producción y habilitar scheduler si procede. Nunca modificar ni reempaquetar skill v3.9.2 solo por cambio de dominio.

## Estado al 2026-10-20

- Nueva URL pública: declarada por el proyecto.
- Descubrimiento de REST real: PENDIENTE (acceso externo no disponible en esta sesión).
- Collector live ejecutado: NO.
- Pruebas Golden Set live: NO.
- Drift live: DESCONOCIDO.
- Cambios en entorno productivo: NINGUNO.
