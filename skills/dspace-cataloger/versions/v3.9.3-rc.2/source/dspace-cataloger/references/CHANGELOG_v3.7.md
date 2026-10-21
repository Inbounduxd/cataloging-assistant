> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Changelog — dspace-cataloger v3.7

## Alineación runtime
- Reconciliado el contrato de la skill con Cataloging Assistant después de VERTICAL-017.
- `dc.subject.linguisticVariant` deja de tratarse como `APP_SCHEMA_GAP` y se reconoce como
  campo runtime draftable/profiled/vocabularied.
- `APP_SCHEMA_GAP` se excluye explícitamente de los estados de evidencia.
- Se mantienen exactamente cinco estados canónicos: `EXTRAÍDO`, `VERIFICADO`,
  `INFERIDO`, `PENDIENTE`, `GENERADO`.

## Evidencia externa controlada
- Documentadas sesiones de evidencia con fuente URL locator y/o texto explícito.
- Snapshot SHA-256, `contract_version` y `base_source_hash` cuando hay ítem DSpace.
- Extracción determinista e idempotente.
- Conservación obligatoria de `binding_id` para los 56 bindings y claves compartidas.
- Orden estable mediante `source.position` y `candidate.position`, únicos por sesión.
- Revalidación de vocabulario activo al copiar a draft.
- Sin fetch remoto, PDF/binarios ni LLM-assisted extraction en el MVP.
- Ningún cambio habilita escritura DSpace ni mutaciones del agente conversacional.

## Compatibilidad
- Se preservan GR01–GR20.
- Se preservan 56 bindings del form contract.
- Se preserva literalmente `dc.subject.linguiscgroup`.
- Cambio aditivo sobre v3.6.
