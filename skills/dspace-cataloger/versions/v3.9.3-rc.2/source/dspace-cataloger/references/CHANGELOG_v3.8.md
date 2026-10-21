> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Changelog — dspace-cataloger v3.8

## Added / aligned

- Alineación con VERTICAL-019: ingestión local PDF controlada por superficie humana, extracción textual determinista y provenance por página.
- Alineación con VERTICAL-020: fetch remoto HTTP(S) explícito y backend-only con mitigación SSRF, revalidación por redirección, allowlist MIME, límites y provenance rica.
- Semántica append-only para snapshots remotos y PDF.
- Distinción explícita entre staleness de Evidence Session y cambios del origen remoto.
- Contrato runtime `no OCR` para PDF local/remoto.
- Separación explícita entre capacidades mutables de superficies humanas y permisos read-only del agente.

## Preserved

- 56 bindings del form contract.
- Literal `dc.subject.linguiscgroup`.
- Cinco campos lingüísticos runtime.
- Estados canónicos `EXTRAÍDO`, `VERIFICADO`, `INFERIDO`, `PENDIENTE`, `GENERADO`.
- Validación exacta de vocabularios activos en runtime.
- Orden estable de fuentes/candidatos.
- Human approval y copy-to-local-draft.
- Sin LLM-assisted extraction.
- Sin escritura DSpace.

## Clarification

La política standalone de adquisición puede contemplar OCR como fallback cuando la ejecución ocurre fuera de Cataloging Assistant Runtime Mode. Esa capacidad **no se traslada** al runtime de la aplicación: VERTICAL-019/020 mantienen PDF text-only y no OCR.
