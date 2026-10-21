> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# VERTICAL-021 — Evaluation and human adjudication alignment

## Golden Set de evaluación vs Golden Set catalográfico

Los fixtures `GR01–GR20` de la skill prueban **semántica catalográfica**.

La evaluación VERTICAL-021 prueba otra dimensión:

- generación de candidatos asistida por modelo;
- grounding/provenance;
- scorer determinista;
- abstención;
- revisión humana independiente;
- adjudicación;
- construcción controlada de gold.

No sustituir ni mezclar ambos Golden Sets.

## Lifecycle de evaluación

`candidate -> independent reviews -> adjudication when required -> case-level gold`

Estados de evaluación relevantes:

- `READY_FOR_INDEPENDENT_REVIEW`
- `UNDER_INDEPENDENT_REVIEW`
- `AWAITING_ADJUDICATION`
- `ADJUDICATED_GOLD`

`ADJUDICATED_GOLD` es **sólo un estado de evaluación**. No autoriza:

- escritura DSpace;
- activación productiva de LLM;
- egress a proveedores;
- OCR;
- promoción automática a `VERIFICADO`;
- copy-to-draft automático.

## Integridad de reviews

Para casos que avanzan a review/adjudicación deben preservarse de forma relacional:

- mismo `case_id`;
- reviewer autorizado y distinto;
- `binding_id` bajo revisión;
- mismo `evidence_snapshot_sha256`;
- `review_id` único.

Para el estrato A actualmente gobernado por el repositorio se requieren dos
revisores humanos independientes antes de adjudicación.

## Corrección semántica de registeredLanguage

`dc.description.registeredLanguage` representa la lengua en la que el recurso
está escrito/registrado.

Es independiente de:

- lengua objeto;
- lengua de ejemplos;
- lengua citada;
- lengua documentada/estudiada.

La evaluación VERTICAL-021 corrigió un tratamiento histórico que usaba
`Purépecha` como lengua de registro en un recurso escrito en español. El gold
correctivo usa `Español`.

Esto es una corrección semántica de campo, no una operación de alias.

## Gate D

Gate D permanece abierto. Un caso adjudicado no demuestra cobertura empírica
suficiente para todos los bindings lingüísticos críticos ni autoriza runtime
productivo. La promoción debe seguir dependiendo de evidencia empírica
suficiente y gobernanza explícita.
