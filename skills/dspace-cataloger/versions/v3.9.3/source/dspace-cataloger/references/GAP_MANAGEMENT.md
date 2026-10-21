> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Gap Management v3.3

## Dos clases principales

### Vocabulary Gap

El concepto está bien sustentado, pero el vocabulario cerrado no contiene una
representación exacta.

Ejemplo:
`jach-t’aan` verificado, ausente de `selfDenominationPairs`.

### Schema Gap

La información existe y es relevante, pero el perfil DSpace no ofrece un campo
semánticamente correcto.

Ejemplo:
`volume = 10` sin campo de volumen.

## Estados de mapeo

- `MAPPED`
- `VOCABULARY_GAP`
- `SCHEMA_GAP`
- `POLICY_REVIEW`
- `NOT_APPLICABLE`

## Regla crítica

Un gap no es evidencia insuficiente.

Por ello:

`evidenceStatus = VERIFICADO`
puede coexistir con:
`mappingStatus = VOCABULARY_GAP`.

## Registros

Consultar:

- `assets/vocabulary-gap-registry.json`
- `assets/schema-gap-registry.json`

Nunca sustituir un concepto verificado por un término semánticamente próximo
solo para evitar registrar un gap.
