> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# CHANGELOG — dspace-cataloger v3.9

## Type

Additive governance/evaluation alignment. No Golden Set replacement.

## Added

- `assets/runtime-contract-lock-v3.9.json`
- `references/APP_ALIGNMENT_v3.9.md`
- `references/VERTICAL_021_GOVERNANCE.md`
- `references/VERTICAL_021_EVALUATION.md`
- `tests/v3.9-acceptance.md`
- VERTICAL-021 governance QA rules.
- explicit `registeredLanguage = resource writing/registration language` rule.
- runtime contract SHA-256 lock and skill/runtime version separation.

## Updated

- `SKILL.md`
- `assets/release-manifest.json`
- `assets/policy-decisions.json`
- `references/CATALOGING_ASSISTANT_RUNTIME_CONTRACT.md`
- `references/LANGUAGE_POLICY.md`
- `references/QA_RULES.md`

## Intentionally unchanged

- DSpace form contract: 56 bindings.
- DSpace profile snapshot.
- Golden Set GR01–GR20 and its index.
- Canonical DSpace keys, including literal `dc.subject.linguiscgroup`.
- Runtime LLM extraction remains disabled/not authorized.
- OCR remains disabled in runtime.
- DSpace remains read-only.
- Conversational agent remains non-mutating.
