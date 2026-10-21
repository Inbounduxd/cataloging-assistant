> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Cataloging Assistant App Alignment — dspace-cataloger v3.8

## Baseline

Alineación aditiva de la skill con el runtime de `keilynrp/cataloging-assistant` posterior a VERTICAL-020.

La v3.8 no amplía permisos del agente ni autoriza escritura DSpace. Reconoce que las superficies humanas/backend ya admiten evidencia PDF local controlada y fetch remoto seguro, mientras el agente conversacional continúa estrictamente read-only.

## Decisiones vigentes

1. DSpace continúa como fuente de verdad; PostgreSQL sigue siendo índice/almacén local reconstruible donde aplique.
2. El agente solo usa herramientas internas read-only y no hereda permisos de las superficies humanas mutables.
3. El contrato lingüístico runtime conserva cinco campos: familia, rama, agrupación, variante y lengua de registro.
4. `dc.subject.linguiscgroup` se conserva literalmente.
5. Estados de evidencia canónicos: `EXTRAÍDO`, `VERIFICADO`, `INFERIDO`, `PENDIENTE`, `GENERADO`.
6. VERTICAL-017 mantiene sesiones explícitas, snapshots SHA-256, `binding_id`, orden estable, extracción determinista, idempotencia, revalidación de vocabulario y staleness por `base_source_hash`.
7. VERTICAL-019 incorpora ingestión local PDF controlada en la superficie humana: PDF de texto, límites de tamaño/páginas/tiempo, extracción determinista y provenance por página. Runtime **no usa OCR**; `no_extractable_text` queda explícito y no dispara OCR automático.
8. VERTICAL-020 incorpora fetch remoto HTTP(S) explícito, backend-only y deshabilitado por defecto mediante feature flag. Se mantienen mitigaciones SSRF, validación DNS/IP pública por salto, redirecciones manuales/limitadas, MIME allowlist, límites de streaming y timeouts.
9. Cada fetch remoto produce un snapshot append-only. Repetir una URL crea una nueva fuente; nunca reescribe snapshots históricos.
10. El cambio del origen remoto no vuelve stale un snapshot previo. El stale canónico sigue siendo de Evidence Session contra el `source_hash` del ítem DSpace enlazado.
11. Provenance remota preserva, según disponibilidad runtime: requested URL, final URL, media type, bytes, fetched_at, SHA-256, redirect count/chain, extractor y derived-text hash.
12. PDF remoto usa las mismas garantías de extracción textual segura; no ejecuta JS, adjuntos ni enlaces y no habilita OCR.
13. `copy-to-draft` continúa revalidando contra vocabulario activo y solo admite candidatos `runtime_draftable` elegibles.
14. No existe persisted Accept/Reject como contrato runtime del agente.
15. No existe LLM-assisted extraction en el baseline v3.8. `INFERIDO`/`GENERADO` siguen siendo estados canónicos, pero no deben presentarse como salida LLM actual hasta un vertical posterior.
16. No se habilita escritura, submission, workflow ni administración DSpace.

## Separación de capacidades

`standalone acquisition != runtime agent permission`

`human/backend evidence ingestion != conversational-agent mutation`

`remote origin change != snapshot staleness`

`runtime PDF extraction != OCR`

`local draft != DSpace write`

## Evolución siguiente recomendada

- ejecutar UX-PROMPT-002 y cerrar UX-ALIGNMENT-001;
- congelar el contrato UX del Evidence Workspace;
- especificar una futura vertical LLM provider-independent solo después del freeze UX;
- mantener OCR y cualquier DSpace write fuera de alcance salvo vertical/ADR explícito.
