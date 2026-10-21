> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Bibliographic Discovery v3.3

## Cuándo se activa

Cuando una fila/ficha no aporta URL utilizable o la URL está rota.

## Flujo

`metadata hint → discovery → identity matching → source acquisition`

## Señales de identidad

Comparar como mínimo:

- título;
- autor(es);
- año;
- contenedor;
- DOI;
- ISSN/ISBN cuando existan.

## Estados

- `MATCH_HIGH_CONFIDENCE`
- `MATCH_REVIEW`
- `NO_MATCH`

## Regla crítica

Encontrar una página parecida no basta. La fuente recuperada debe coincidir
bibliográficamente antes de entrar al Evidence Corpus como representación del
mismo recurso.

## Sin URL no significa sin full text

No declarar `FULLTEXT_UNAVAILABLE` hasta intentar recuperación bibliográfica
cuando existan suficientes claves de identidad.

## Trazabilidad

Registrar:

- consulta usada;
- fuente candidata;
- señales coincidentes;
- señales discrepantes;
- estado de match;
- fuente finalmente seleccionada.
