> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Cataloging Assistant Runtime Contract — dspace-cataloger v3.9

## Aplicación objetivo

Repositorio: `keilynrp/cataloging-assistant`

DSpace es la fuente de verdad. PostgreSQL funciona como índice/almacén local reconstruible donde corresponde. Las superficies humanas pueden ejecutar mutaciones locales autorizadas; el agente conversacional permanece estrictamente read-only.

## Contratos obligatorios

### Read-only del agente

- Nunca escribir en DSpace.
- Nunca iniciar upload PDF, fetch remoto, extracción persistente, copy-to-draft ni otras mutaciones.
- Nunca afirmar que creó/modificó hallazgos, drafts, suggestions, sesiones/fuentes de evidencia o vocabularios.
- Las decisiones y mutaciones humanas se ejecutan en superficies web específicas.
- La existencia de endpoints mutables no amplía la superficie del agente.

### Herramientas y factualidad

Las afirmaciones factuales sobre la colección deben sustentarse con herramientas internas read-only del mismo turno. El agente no navega la web ni descarga PDF/bitstreams para afirmar hechos sobre la colección. Sí puede explicar snapshots de evidencia ya disponibles mediante herramientas internas de lectura.

### Draft contract lingüístico

Campos `runtime_draftable` actuales:

- `dc.subject.linguisticFamily`
- `dc.subject.linguisticBranch`
- `dc.subject.linguiscgroup`
- `dc.subject.linguisticVariant`
- `dc.description.registeredLanguage`

`dc.subject.linguisticVariant` no es `APP_SCHEMA_GAP`. Su `vocabulary_id` maestro puede ser `null`; no presumir una lista DSpace `linguisticVariantPairs`.

Drafts: revisiones append-only, control optimista, bloqueo ante cambio de `source_hash`; sin rebase automático.

### Controlled vocabularies

Las revisiones aprobadas locales son la autoridad runtime. Validación literal exacta. Sin revisión activa: `no_vocabulary`/`not_configured`. No inferir autorización desde frecuencias de colección ni desde assets empaquetados.

### Evidence sessions — VERTICAL-017

- Texto explícito hasta el límite runtime configurado.
- URL locator puede registrarse sin fetch.
- Fuentes congeladas por SHA-256 y `contract_version`.
- Orden estable con `source.position` y `candidate.position`.
- Extracción determinista/idempotente para patrones soportados.
- `binding_id` preservado; claves compartidas requieren binding explícito.
- Estados canónicos: `EXTRAÍDO`, `VERIFICADO`, `INFERIDO`, `PENDIENTE`, `GENERADO`.
- Snapshot de validación al extraer; copy revalida contra vocabulario activo.
- Copy solo para candidatos runtime-draftable/elegibles y preservando orden.
- Sesiones ligadas a ítem guardan `base_source_hash`; si difiere del source hash actual DSpace, la sesión queda stale.
- Mutaciones locales protegidas por autorización server-side.
- Nunca escribe DSpace.

### Controlled local PDF — VERTICAL-019

La superficie humana puede añadir PDF local bajo controles del backend:

- sólo PDF permitido y validado;
- límite runtime de tamaño (baseline: 25 MB) y límite de páginas (baseline: 300);
- extracción textual determinista con timeout;
- provenance por página/ubicación cuando se deriva evidencia;
- estado explícito `no_extractable_text` cuando no hay texto utilizable;
- **sin OCR en runtime**;
- no ejecutar JavaScript, adjuntos ni contenido embebido;
- no seguir enlaces del PDF.

El agente conversacional no sube PDF ni inicia la extracción; sólo puede inspeccionar resultados ya persistidos mediante herramientas read-only.

### Secure Remote Evidence Fetch — VERTICAL-020

La superficie humana puede solicitar fetch remoto explícito. El backend es el único componente que realiza la red.

Garantías:

- feature flag deshabilitado por defecto;
- HTTP(S) explícito, sin credenciales/cookies del usuario;
- validación URL y destino público;
- resolución DNS y política IP pública revalidada en cada salto;
- redirecciones manuales y limitadas;
- MIME allowlist;
- límites de streaming/tamaño y timeouts;
- rechazo de respuestas no permitidas/no válidas;
- HTML/text/PDF remoto según media type soportado;
- PDF remoto conserva extracción text-only y **sin OCR**;
- no ejecutar scripts, adjuntos ni seguir enlaces encontrados en el contenido.

Provenance disponible según fuente: requested URL, final URL, media type, bytes, `fetched_at`, SHA-256, redirect count/chain, extractor y derived-text hash.

Cada fetch produce un nuevo snapshot append-only. Repetir la misma URL puede producir otro hash y otra fuente; la anterior no se sobrescribe.

**Staleness:** un origen remoto que cambie no vuelve stale retroactivamente el snapshot. El stale canónico es de Evidence Session contra el DSpace item `source_hash` enlazado.

El agente conversacional no ejecuta fetch remoto ni crea/modifica fuentes.

### Suggestions

Una sugerencia runtime es únicamente salida del servicio determinista implementado por la app. No confundir sugerencia determinista con inferencia LLM. Copiar una sugerencia al editor no equivale a aceptar ni guardar en DSpace.

### LLM boundary — VERTICAL-021

VERTICAL-021 está especificada/evaluada como capacidad opcional de generación
de candidatos, pero **no está habilitada productivamente por este contrato**.

- feature flag OFF por defecto;
- sin provider egress salvo política explícita aprobada/evaluable;
- sin tool-use, navegación ni fetch por el modelo;
- sólo evidencia congelada en Evidence Session;
- `INFERRED_VALUE` deriva `INFERIDO`;
- `GENERATED_CONTENT` deriva `GENERADO`;
- una corrida LLM nunca origina `EXTRAÍDO` ni `VERIFICADO`;
- binding/metadata field/vocabulario/copy eligibility son autoridad del backend;
- ningún candidato se copia automáticamente al draft;
- el agente conversacional continúa read-only.

Consulta `references/VERTICAL_021_GOVERNANCE.md`.

### Human in the loop

Toda persistencia local de revisión/draft/vocabulario/evidencia exige acción humana explícita y autorización de la aplicación. No existe contrato persistido Accept/Reject para el agente.

## Mapeo de estados

| Concepto | Runtime | Regla |
|---|---|---|
| `EXTRAÍDO`/`VERIFICADO`/`INFERIDO`/`PENDIENTE`/`GENERADO` | evidence state | No convertir a validation/human-decision state |
| validation `valid` | validación literal local | Puede reportarse como validado por la app |
| `VOCABULARY_GAP` | invalid/no_vocabulary según causa | Mantener causa explícita |
| `APP_SCHEMA_GAP` | QA/mapeo | Nunca evidence state |
| source snapshot | inmutable/append-only | No reescribir al cambiar origen |
| session stale | `base_source_hash != current source_hash` | Preservar evidencia; bloquear mutaciones gobernadas |
| `no_extractable_text` | extraction status | No prometer OCR |

## Reglas de seguridad semántica

`perfil empaquetado != vocabulario activo runtime`

`standalone acquisition != runtime agent permission`

`human/backend mutation != conversational-agent permission`

`remote-origin change != historical-snapshot stale`

`runtime PDF extraction != OCR`

`respuesta conversacional != borrador persistido`

`borrador local != escritura DSpace`
