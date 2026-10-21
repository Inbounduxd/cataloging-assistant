> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Abstract Policy v3.3

## Abstract original

Solo poblar `dc.description.abstract` con un abstract/resumen presente en la
fuente. Un resumen generado no lo sustituye.

## Ausencia

Si el full text confirma que no existe:

`ABSTRACT_NOT_PRESENT_IN_SOURCE`

y el campo queda vacío.

## Abstracts paralelos

Cuando existan dos o más:

1. conservar todos en Evidence Corpus;
2. registrar lengua y origen;
3. no usar su presencia para inferir bilingüismo;
4. si DSpace no es repetible, aplicar `POL-ABSTRACT-001`;
5. nunca descartar silenciosamente los abstracts no mapeados.

La selección final sigue siendo una PolicyDecision institucional.
