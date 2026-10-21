> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Alineación dspace-cataloger v3.7 ↔ Cataloging Assistant

## Estado de referencia

Alineación posterior a la fusión de VERTICAL-017 en `main`. La aplicación conserva
`CONTRACT_VERSION = dspace-cataloger-v3.6`; v3.7 es una actualización de la skill que
documenta el runtime efectivamente implementado sin alterar por sí sola ese identificador
de contrato de código.

## Decisiones vigentes

1. Se preserva el modo standalone para catalogación desde URL/PDF/hojas.
2. Runtime Mode mantiene precedencia de ADR/Specs y restricciones de la aplicación.
3. DSpace continúa como fuente de verdad; no se habilita escritura DSpace.
4. El agente conversacional continúa estrictamente read-only.
5. El contrato lingüístico runtime comprende cinco campos: familia, rama, agrupación,
   variante y lengua de registro.
6. `dc.subject.linguisticVariant` deja de ser `APP_SCHEMA_GAP`; es draftable/profiled/
   vocabularied local y no presume vocabulario DSpace por pares.
7. `APP_SCHEMA_GAP` queda reservado a QA/mapeo de superficies realmente no soportadas y
   nunca forma parte de los estados de evidencia.
8. Vocabularios empaquetados no equivalen a revisiones activas locales.
9. VERTICAL-017 añade sesiones explícitas de evidencia con snapshot SHA-256, orden lógico
   estable, extracción determinista e idempotente, `binding_id` y staleness por
   `base_source_hash`.
10. `copy-to-draft` revalida contra vocabulario activo en tiempo de copia y solo admite
    `runtime_draftable`.
11. El orden de fuentes y candidatos se representa con `position`; no depende de
    timestamps ni UUID aleatorios.
12. El MVP runtime no descarga URLs, no procesa PDF/binarios y no usa LLM para extraer.
13. La lógica catalográfica sigue desacoplada del proveedor LLM.

## Evolución siguiente recomendada

- Golden Set end-to-end para la nueva superficie de evidencia.
- upload PDF controlado y extracción textual en sandbox con límites de tamaño/MIME/tiempo.
- fetch HTTP seguro con mitigación SSRF, solo en una vertical explícita.
- extracción LLM provider-independent después de establecer métricas de regresión.
- mantener toda ampliación de escritura DSpace fuera de alcance salvo ADR específico.
