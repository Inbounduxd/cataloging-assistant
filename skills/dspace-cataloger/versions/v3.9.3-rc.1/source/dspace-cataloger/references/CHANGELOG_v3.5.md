> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# CHANGELOG — dspace-cataloger v3.5

## Estrategia

Actualización aditiva sobre v3.4. No se reemplaza el Golden Set anterior ni se
modifican las 56 bindings del formContract.

## Incorporado

- Gobernanza CLIN/INALI: Familia → Agrupación → Variante.
- Rama lingüística declarada enriquecimiento opcional no-CLIN.
- Separación `registeredLanguage` / `linguiscgroup`.
- Modelo multientidad Familia–Rama?–Agrupación–Variante.
- Política conservadora de variantes y reconciliación de alias.
- Prohibición explícita de sustitución por proximidad en vocabularios cerrados.
- Precedencia del abstract autoral.
- Separación palabras clave autorales / tópicos inferidos.
- Cobertura geográfica separada de `countryFound`.
- Fechas editoriales diferenciadas.
- Dos puntos no implica subtítulo.
- Nuevas reglas QA y Golden Set GR11–GR20.

## Contratos preservados

- UI Fidelity y `bindingId`.
- `dc.subject.linguiscgroup` literal.
- `autoWrite=false`.
- `humanApprovalRequired=true`.
- Golden Set GR01–GR10 sin cambios.
