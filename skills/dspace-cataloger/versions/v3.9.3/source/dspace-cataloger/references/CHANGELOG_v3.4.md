> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# dspace-cataloger v3.4 — Cambios sobre v3.3

## Política de actualización

Actualización estrictamente aditiva. El Golden Set v3.3, las políticas de evidencia,
abstract, lenguas, roles, gaps, adquisición full text y aprobación humana se conservan.

## Añadido

- `assets/dspace-form-contract-v1.json` con 56 bindings visuales.
- `references/UI_FIDELITY_CONTRACT.md`.
- UI Fidelity Mode para salida humana.
- Identidad `bindingId + uiLabel + metadataField`.
- `assistantLabel` para desambiguación sin alterar la UI.
- Estado de evidencia `GENERADO`.
- Validación por binding para claves compartidas.
- Reglas QA `CAT-UI-*` y `CAT-GEN-*`.
- `tests/form-contract-acceptance.md`.
- Extensión de `catalog-draft.schema.json` con datos de binding.

## Preservado

- 10 fixtures del Golden Set v3.3 sin modificaciones.
- `dc.subject.linguiscgroup` como clave contractual literal.
- `ABSTRACT_POLICY.md`: contenido generado no sustituye abstract original.
- Human-in-the-loop y no escritura por defecto.
- Todas las anomalías y políticas v3.3 previas.
