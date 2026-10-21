> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# VERTICAL-021 — Provider-independent LLM-assisted evidence governance

## Estado

**Diseñado y evaluado; NO habilitado productivamente por dspace-cataloger v3.9.**

La vertical introduce un contrato opcional de generación de candidatos sobre
evidencia ya congelada, sin sustituir el extractor determinista y sin conceder
autoridad catalográfica al modelo.

Flujo conceptual:

`SOURCE SNAPSHOT -> DETERMINISTIC EXTRACTION -> OPTIONAL LLM RUN -> CANDIDATES -> BACKEND VALIDATION -> HUMAN REVIEW -> LOCAL DRAFT`

## Principios no negociables

1. Dominio independiente del proveedor.
2. Feature flag OFF por defecto.
3. Sin escritura DSpace.
4. Sin OCR.
5. Sin navegación ni fetch por el modelo.
6. Sólo snapshots de evidencia inmutables.
7. Human-in-the-loop obligatorio.
8. Backend authoritative para bindings, metadata fields, vocabularios, staleness,
   evidence state, draftability y copy eligibility.
9. La evidencia se trata como datos no confiables frente a prompt injection.
10. Data egress fail-closed: sin política explícita aprobada/evaluable no existe
    tráfico hacia un proveedor.
11. Persistencia atómica: fallo de proveedor/parseo/schema no deja candidatos parciales.
12. El agente conversacional permanece read-only.

## model_intent != evidence_state

VERTICAL-021 sólo admite dos intenciones de candidato LLM:

- `INFERRED_VALUE` -> el backend deriva `INFERIDO`.
- `GENERATED_CONTENT` -> el backend deriva `GENERADO`.

Un modelo nunca origina:

- `EXTRAÍDO`;
- `VERIFICADO`.

`PENDIENTE` continúa siendo un estado de workflow y no un intent de salida LLM.

## Binding authority

El proveedor puede proponer únicamente un `binding_id` permitido por el contrato
suministrado. El backend resuelve:

- `metadata_field`;
- labels;
- evidence state;
- vocabulario/control literal;
- runtime draftability;
- copy eligibility.

Un binding inexistente/no permitido invalida el candidato.

## Provenance mínima de inference run

Conservar:

- `inference_run_id`;
- `session_id`;
- provider adapter id/version;
- provider/model normalizados;
- prompt/template version;
- input manifest ordenado;
- source/snapshot hashes;
- fragment hashes y selectores/rangos;
- runtime contract version;
- request/config hash;
- response/output hash;
- timestamps;
- status/error sanitizado.

Nunca persistir credenciales ni secretos del proveedor.

## Separación de permisos

`LLM candidate != cataloguing truth`

`LLM candidate != verified metadata`

`LLM run != DSpace write`

`provider capability != data-egress authorization`

`standalone skill capability != runtime agent permission`
