# Auditoría local SNIBLI (Python 3.11+)

## Comparación explícita con la candidata

Desde 2026-10-21, `--candidate` permite seleccionar una referencia local de
revisión junto con `--observed`, sin necesitar un baseline histórico para esa
comparación. No sustituye la comparación con v3.9.2 ni activa el contrato:

```bash
python3 scripts/audit_snibli_migration.py --offline \
  --candidate reports/snibli-migration/reconciliation-proposal/candidate-contract.json \
  --observed reports/snibli-migration/authenticated-20261021T055428Z-8a836a27/export.json \
  --output reports/snibli-migration/candidate-validation-2026-10-21
```

Ejecutar desde el directorio exigido por AGENTS.md y usar rutas absolutas cuando
el checkout se encuentre en otro directorio. Se pueden proporcionar `--baseline`
y `--candidate` simultáneamente para mostrar ambas comparaciones.

La entrada candidata debe conservar las 56 identidades de referencia, claves
literales, dimensiones completas, posiciones únicas, metadatos registrados y
políticas de no escritura y aprobación humana. `adopted` y `runtimeEnabled` deben
ser false. Las candidatas inválidas se rechazan; una coincidencia no acredita
aprobación institucional ni promociona un snapshot. Los controles que comparten
metadataField se comparan como bindings separados.

El reporte muestra por separado los checks `configured_forms_against_v3_9_2`,
`imported_vocabulary_values` y los checks `candidate_*`. `diff.json` preserva la
referencia candidata, sus hashes y la evidencia observada. Las secciones activas
HTTP 204 y una referencia de vocabulario jerárquico UNKNOWN no se convierten en
PASS por elegir una candidata.

La ejecución real dio PASS para 57 controles, 55 claves registrales e identidad
de colección; 17 vocabularios planos coinciden y `srsc` sigue UNKNOWN. Los dos
checks de drift contra v3.9.2 siguen FAIL y el código de salida continúa siendo 1.
Ese código es esperado por las diferencias históricas, no es fallo de login ni
motivo para repetir capturas. El resumen está en
`reports/snibli-migration/candidate-validation-2026-10-21/summary.md`.

## Diagnóstico público y evidencia histórica

La CLI usa exclusivamente GET sin credenciales, cookies ni proxies de entorno.
No deriva la API del frontend, inicia sesión, ejecuta jobs, escribe en PostgreSQL,
promueve baselines ni cambia configuración o artefactos de la skill. No requiere
instalar el paquete API (que exige Python 3.12): importa únicamente sus módulos
puros de contrato y VERTICAL-022 desde este checkout.

Desde PowerShell o CMD en la raíz del repositorio:

```powershell
py -3.11 scripts/audit_snibli_migration.py --offline
py -3.11 scripts/audit_snibli_migration.py --public-url https://www.iifl.unam.mx/SNIBLI/home --timeout 10
```

Solo cuando un operador haya identificado la REST real:

```powershell
py -3.11 scripts/audit_snibli_migration.py --api-base https://HOST-VERIFICADO/REST-VERIFICADA --output reports/snibli-migration
```

El valor de ejemplo no es una ruta sugerida. La CLI prueba la base explícita y
`/core/collections/e9a8f44f-a8d3-4d22-b02a-cf590285bac6`. Verifica UUID y Handle
`123456789/4`, sin usarlos como prueba suficiente de identidad de base de datos.
La sonda pública solo verifica disponibilidad HTTP; no automatiza el navegador.
La comprobación HAL exige HTTP 200, Content-Type `application/hal+json`, JSON
objeto y `_links` objeto. No demuestra identidad DSpace por sí sola.

El timeout es un presupuesto por endpoint, entre 0 y 60 segundos; cada sonda se
ejecuta en un proceso cancelable para limitar también DNS/TLS y servidores lentos.
Como máximo se prueban tres endpoints, cuatro solicitudes por endpoint contando
redirecciones, sin retries. Solo se admiten redirecciones al mismo origen exacto
(esquema, hostname y puerto); cambios de host o downgrade se reportan como FAIL
sin seguirlos. Una redirección institucional legítima entre hosts requiere revisar
su destino e iniciar otra ejecución explícita. El límite de respuesta es 4 MiB.

## Comparación de evidencia de VERTICAL-022

No ejecutar `contract_job` como parte de esta auditoría: aunque es read-only frente
a DSpace, persiste snapshots en PostgreSQL. Tampoco ejecutar el sincronizador de
vocabularios, que modifica el índice local. Si ya existen capturas autorizadas,
exportar sus páginas brutas sin secretos mediante el procedimiento operativo
aprobado y proporcionarlas como archivos:

```powershell
py -3.11 scripts/audit_snibli_migration.py --offline --baseline baseline.json --observed observed.json
```

Ambos archivos usan un envelope JSON con `pages_by_surface`, exactamente las
páginas brutas que consume `build_contract_snapshot` de VERTICAL-022:

```json
{
  "source_base_url": "https://HOST-VERIFICADO/REST-VERIFICADA",
  "captured_at": "2026-10-20T20:00:00Z",
  "collection_uuid": "e9a8f44f-a8d3-4d22-b02a-cf590285bac6",
  "collection_handle": "123456789/4",
  "pages_by_surface": {
    "metadata_schemas": [],
    "metadata_fields": [],
    "metadata_fields_by_schema:dc": [],
    "submission_forms": [],
    "active_submission_definition": [],
    "active_submission_sections": []
  }
}
```

Las listas vacías ilustran el formato, **no son evidencia completa**. Incluir todas
las páginas y todos los esquemas observados. El normalizador existente verifica
paginación y cobertura; no se acepta un flag `complete` aportado por el usuario.
Se guardan hashes de ambos archivos, evidencia bruta y snapshots normalizados en
`diff.json`. Los archivos de entrada no se modifican. El reporte indica que son
capturas importadas, no live.

La CLI compara además los dos formularios configurados contra el contrato incluido
en el ZIP verificado v3.9.2: bindings (con multiplicidad), 54 claves, posición,
etiqueta literal, required, repeatable, inputType, controlledVocabulary y closed.
Conserva campos esperados y observados en `diff.json` para revisión humana.
Esa comparación es independiente de la pertenencia activa de los formularios.

Para HTTP 204 en secciones activas, conservar el marcador nativo `_observation`
del collector (`observable: false`, `statusCode: 204`) o añadir al envelope
`http_observations: [{"surface": "active_submission_sections", "http_status": 204}]`
omitiendo las páginas inexistentes. Se preserva
`ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204` y se obtiene UNKNOWN y
`UNOBSERVABLE_SURFACE`; no se interpreta como contrato vacío ni se publican
eliminaciones o cambios de estructura derivados de esa ausencia. No se aplica el
fallback de secciones globales como evidencia de pertenencia activa.

Opcionalmente, el envelope observado puede incluir `vocabulary_evidence`, indexado
por ID de vocabulario. Cada entrada contiene `hierarchical: false` y `pages`, las
respuestas HAL brutas de entries con `_embedded.entries[].value` y los campos
`page.number`, `page.totalPages`, `page.totalElements`. La CLI exige secuencia y
recuentos completos y compara valores literales (incluyendo orden y duplicados)
contra `controlled-vocabulary-index.json` del ZIP v3.9.2. Capturas jerárquicas o
solo de nodos superiores quedan UNKNOWN; no se infiere cobertura del árbol.
El collector VERTICAL-022 actual no captura esos valores: no confundir su snapshot
estructural con cobertura de vocabularios.

## Resultados y límites

- `audit.json` y `audit.md`: fecha UTC, configuración no sensible, endpoints,
  redirecciones, HAL público bruto, resultados, errores y cobertura.
- `diff.json`: solo si se cargaron ambos archivos de evidencia. Una ejecución
  parcial elimina el diff anterior del mismo directorio para evitar asociarlo con
  la nueva auditoría. Usar directorios distintos para conservar ejecuciones.
- PASS: comprobación específica satisfecha; FAIL: contradicción observable;
  UNKNOWN: incertidumbre/error de acceso/superficie incompleta;
  NOT_TESTED: comprobación no ejecutada.
- Salida 1 si hay algún FAIL; salida 0 puede incluir UNKNOWN y NOT_TESTED.
  Ninguno de esos códigos declara compatible la migración completa.
- `--baseline` solo no activa comparación. `--observed` requiere `--baseline`.
- No se aceptan URLs con usuario, contraseña, query o fragmento. No proporcionar
  secretos en los archivos de evidencia: su contenido forma parte del expediente.

La comprobación de integridad decodifica en memoria, verifica SHA-256 y tamaño
fijados para v3.9.2, CRC ZIP, 86 archivos y 36 JSON; no reempaqueta la release.
El contrato Python aún declara v3.9.1: se reporta un warning, sin cambiarlo.
La separación de lengua de registro y lengua objeto, aprobación humana y bloqueo
de escritura se comprueban como invariantes **locales**. El comportamiento live,
los permisos, ítems, bitstreams y Golden Set GR01–GR23 requieren validación
operativa adicional; no se declara que hayan pasado por existir en la release.

## Pruebas en WSL

Desde `/home/keilyn/cat`, con `REPO` apuntando al checkout correcto:

```bash
REPO=/home/keilyn/snibli-migration-audit
PYTHONPATH="$REPO/apps/api/src" python3 -m pytest \
  "$REPO/apps/api/tests/test_snibli_migration_audit.py" \
  "$REPO/apps/api/tests/test_cataloging_contract.py" \
  "$REPO/apps/api/tests/test_dspace_contract_snapshot.py" \
  "$REPO/apps/api/tests/test_dspace_contract_live_reconciliation.py" -q
```
