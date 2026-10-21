> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# CHANGELOG v3.6

- Añade `Cataloging Assistant Runtime Mode`.
- Alinea la skill con ADR-005/006/008/010 y VERTICAL-006/008/010/011 del repositorio web.
- Introduce `APP_SCHEMA_GAP` y `CAT-APP-001` para `dc.subject.linguisticVariant` fuera del contrato local actual.
- Separa vocabulario de referencia de la skill de vocabulario activo aprobado en la aplicación.
- Incorpora reglas de `source_hash`, drafts stale y ausencia de rebase automático.
- Reserva el término “sugerencia runtime” al mecanismo determinista de la aplicación.
- Preserva Standalone Evidence Cataloging Mode y Golden Set v3.5.
