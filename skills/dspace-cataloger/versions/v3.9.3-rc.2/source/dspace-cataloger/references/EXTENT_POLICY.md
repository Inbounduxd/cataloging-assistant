> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Extent Policy v3.3

## PDF

Preferir extensión bibliográfica sobre conteo físico del archivo.

Ejemplo:

`PDF pages = 456`
`bibliographic extent = xvi, 439 páginas`

Resultado recomendado:
`dc.format.extent = xvi, 439 páginas`

## Artículos paginados

Calcular páginas inclusivamente cuando la fuente publica un rango inequívoco.

## HTML sin paginación

No inventar `1 página`.

Puede proponerse una unidad intelectual explícita y verificable, por ejemplo:

- `2 poemas bilingües`

pero mientras no exista política institucional, usar:

`mappingStatus = POLICY_REVIEW`

## EPUB

No inventar páginas. Preferir una extensión estructural solo si la política
institucional la admite.

## Principio

`dc.format.extent` significa extensión, no necesariamente número de páginas.
