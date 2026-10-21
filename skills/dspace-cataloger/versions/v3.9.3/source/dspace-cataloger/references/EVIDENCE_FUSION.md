> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Evidence Fusion v3.2

## Objetivo

Resolver múltiples fuentes sin mezclar sus niveles de autoridad.

## Matriz recomendada

| Fuente | Contenido | Bibliografía |
|---|---|---|
| PDF editorial | PRIMARY | OFFICIAL |
| XML/JATS editorial | PRIMARY | OFFICIAL |
| EPUB editorial | PRIMARY | OFFICIAL |
| Landing editorial | SUPPORTING | OFFICIAL |
| PDF subido por usuario | PRIMARY | USER_SUPPLIED |
| Hoja de trabajo | SUPPORTING | USER_SUPPLIED |
| DSpace metadata existente | SUPPORTING | OFFICIAL_CURRENT_STATE |
| Bitstream DSpace | PRIMARY | OFFICIAL_CURRENT_STATE |

## Regla de discrepancia

Si dos fuentes difieren:

- conservar ambas;
- no elegir silenciosamente;
- señalar el campo afectado;
- explicar qué fuente tiene mayor autoridad para esa dimensión;
- pedir revisión cuando la discrepancia cambie el significado del registro.

## Ejemplos

### Fecha

PDF:
`2024`

Landing:
`2024-06-28`

Puede proponerse `2024-06-28` porque la landing aporta mayor granularidad
bibliográfica oficial, siempre que no exista contradicción sustantiva.

### Autor

Excel:
`Romero Hernández, Odilia`

Landing:
`Odilia Romero`

No borrar ninguna forma. Conservar evidencia original y proponer una forma
normalizada solo si existe autoridad adicional o política institucional.

### Lengua

Excel:
`Maya`

PDF:
Maya aparece solo en referencias.

Resultado:
no elevar automáticamente a `dc.subject.linguiscgroup`.


## Tipos de discrepancia v3.3

Registrar las discrepancias conforme a `assets/discrepancy.schema.json`.

- `VALUE_CONFLICT`: dos fuentes dan valores materialmente distintos.
- `GRANULARITY_DIFFERENCE`: una fuente ofrece más detalle sin contradecir otra.
- `LABEL_MISMATCH`: etiqueta y valor son estructuralmente incompatibles, p. ej. ISBN-10 con 13 dígitos.
- `ROLE_MISMATCH`: la misma persona/entidad aparece con roles distintos.
- `SOURCE_NORMALIZATION`: forma fuente y forma normalizada difieren sin ser valores contradictorios.
- `STRUCTURAL_MISMATCH`: un concepto fue colocado en una dimensión equivocada, p. ej. volumen tratado como número.

Las discrepancias no se resuelven silenciosamente.
