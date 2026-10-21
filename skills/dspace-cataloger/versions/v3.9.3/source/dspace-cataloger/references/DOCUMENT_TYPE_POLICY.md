> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Document Type Policy v3.3

## Regla

El tipo documental se determina por la naturaleza intelectual/documental del
recurso, no por su contenedor.

Ejemplos:

- una reseña en una revista no se convierte automáticamente en `Article`;
- un poema en una revista web no se convierte automáticamente en `Article`;
- un capítulo de libro debe usar `Book chapter` cuando exista coincidencia exacta.

## Vocabulario cerrado

Si el tipo real no existe en `common_types`:

1. conservar la naturaleza real en Evidence Corpus;
2. registrar `VOCABULARY_GAP`;
3. proponer un valor de fallback solo si existe política institucional;
4. requerir revisión humana.

Nunca degradar semántica silenciosamente para lograr un match.
