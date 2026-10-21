> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Contributor Roles v3.3

## Objetivo

Preservar el rol fuente/canónico aunque DSpace tenga menor expresividad.

## Roles canónicos

- `author`
- `editor`
- `translator`
- `advisor`
- `thesis_committee`
- `examiner`
- `coordinator`
- `collective`
- `institution`
- `other`

## Pipeline

`Source Role → Canonical Role → DSpace Mapping`

## Regla

Si DSpace no tiene un campo específico:

- no perder el rol;
- conservarlo en Evidence Corpus;
- mapear temporalmente a `dc.contributor.other` solo bajo política;
- marcar `POLICY_REVIEW`.

No convertir automáticamente `coordinator` en `editor`.

No asignar `translator` por plausibilidad si la fuente no lo declara.
