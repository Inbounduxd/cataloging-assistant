> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Cataloging Assistant App Alignment — dspace-cataloger v3.9

## Baseline

Parent skill: `dspace-cataloger v3.8`
SHA-256: `2f373dc9593cbc23f7fd6f32a6e1ae7a10194732841ef4553e4c4d5437cf860e`

Application repository: `keilynrp/cataloging-assistant`
Reviewed `main`: `c57d48bf7ff07e47c6c44e0a625e1f5445e2b33e`

Runtime contract remains frozen independently:

- id: `dspace-cataloger-v3.6`
- fields/bindings: `56`
- SHA-256: `a68fbf9664b7165ea240508da85167058cd57796fbda9c1a9869986afb0178bb`

## What v3.9 changes

v3.9 is an **additive governance/evaluation alignment** after VERTICAL-021.

It does not replace VERTICAL-017/019/020 and does not expand runtime permissions.

### Preserved runtime baseline

- deterministic Evidence Sessions;
- controlled local PDF, text-layer only;
- secure backend-only remote fetch;
- five runtime linguistic fields;
- canonical evidence states:
  `EXTRAÍDO`, `VERIFICADO`, `INFERIDO`, `PENDIENTE`, `GENERADO`;
- `dc.subject.linguiscgroup` literal;
- exact-match controlled-vocabulary behavior;
- session-level staleness against DSpace `source_hash`;
- agent read-only;
- no DSpace write;
- no OCR.

### New governance alignment

- provider-independent LLM candidate contract documented;
- LLM runtime remains OFF/not productively authorized;
- `model_intent` separated from `evidence_state`;
- `INFERRED_VALUE -> INFERIDO`;
- `GENERATED_CONTENT -> GENERADO`;
- model can never originate `EXTRAÍDO` or `VERIFICADO`;
- backend remains authoritative for binding/field/vocabulary semantics;
- inference runs require immutable input provenance;
- egress policy is fail-closed;
- evaluation uses independent review/adjudication;
- `ADJUDICATED_GOLD` remains evaluation-only;
- `registeredLanguage` is explicitly the resource writing/registration language.

## Version separation

`skill package version != application runtime contract version`

Therefore:

`dspace-cataloger v3.9`

coexists intentionally with:

`runtime contract dspace-cataloger-v3.6`

until the application deliberately changes and refreezes the runtime contract.
