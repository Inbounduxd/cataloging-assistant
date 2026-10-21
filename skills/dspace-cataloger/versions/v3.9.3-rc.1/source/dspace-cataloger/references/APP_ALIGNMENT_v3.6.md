> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Alineación dspace-cataloger v3.6 ↔ Cataloging Assistant

> **Histórico / superseded:** este documento describe el runtime v3.6 previo a la alineación v3.7. Para estado vigente consulte `references/APP_ALIGNMENT_v3.7.md` y `tests/v3.7-acceptance.md`.
## Decisiones

1. Se preserva el modo standalone para catalogación desde URL/PDF/hojas.
2. Se añade Runtime Mode para la aplicación web con precedencia de sus ADR/Specs.
3. DSpace es fuente de verdad; PostgreSQL es índice local reconstruible.
4. El agente runtime es estrictamente read-only y no genera drafts/suggestions.
5. El contrato local de draft/vocabulario cubre 4 campos lingüísticos.
6. `dc.subject.linguisticVariant` queda como `APP_SCHEMA_GAP` hasta nueva vertical/ADR.
7. Vocabularios empaquetados no equivalen a revisiones activas locales.
8. Se respeta `source_hash`, versionado append-only y ausencia de rebase automático.
9. Sugerencias runtime se reservan al mecanismo determinista de la app.
10. La lógica catalográfica sigue desacoplada del proveedor LLM.

## Próxima evolución recomendada de la aplicación (no implementada por esta skill)

- ampliar el draft contract a `dc.subject.linguisticVariant`;
- representar relaciones Familia→Rama?→Agrupación→Variante en una estructura
  multientidad sin inferir jerarquías desde listas planas;
- importar/promover de manera gobernada el perfil/vocabularios DSpace a revisiones
  locales;
- definir una vertical separada si se desea ingestión de evidencia externa
  (URL/PDF) dentro de la aplicación.
