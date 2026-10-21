---
name: dspace-cataloger
description: >
  Assist SNIBLI DSpace cataloging with literal form mappings, controlled vocabulary
  checks, source evidence and human review. Use for cataloging proposals and contract
  validation; runtime operation remains read-only.
---

# dspace-cataloger v3.9.3-rc.1

Local release candidate, not adopted, deployed or repository-preserved through Git.
Read [SNIBLI migration](references/SNIBLI_MIGRATION_2026.md) for the current instance,
approved mapping and known coverage limits. The current reference supersedes carried
forward historical instance URLs, field counts and runtime hashes.

## Workflow

Separate extraction → normalization → vocabulary validation → inference → QA → human
approval. Preserve source provenance and distinguish EXTRAÍDO, VERIFICADO, INFERIDO,
PENDIENTE and GENERADO. Never label inferred or generated content as extracted evidence.

Standalone mode prepares evidence-backed proposals without implying persistence.
Application runtime mode follows the application contract and remains read-only: no
ingestion initiation, finding mutation, approvals, vocabulary changes or DSpace writes
by the conversational agent. Runtime OCR and automatic agent mutations remain disabled.
For details use [runtime contract](references/CATALOGING_ASSISTANT_RUNTIME_CONTRACT.md)
and assets/cataloging-runtime-contract.json.

## Form mapping

Use assets/dspace-form-contract-v1.json: 57 bindings, 55 unique metadata keys, preserving
separate controls that share a key. Keep labels, order, mandatory and repeatable flags.
The bindingId is the physical form control; referenceBindingId preserves its historical
identity across the inserted row. Show the metadata key alongside the human label.

dc.type.genre is the optional, single-valued closed question “¿Es un texto comparativo?”.
Its exact genrePairs values are Sí, No and Incluye Datos de Diferentes Lenguas.
Do not reinterpret it as a generic genre field or infer its answer solely from multiple
language mentions. Unknown evidence stays pending; approval of the mapping does not
authorize automatic completion. common_types retains its original 23 values and adds
Códice, Reseña and Documento Colonial. Do not invent synonyms or classify automatically.
For other document-type rules consult references/DOCUMENT_TYPE_POLICY.md.

## Linguistic governance

Preserve dc.subject.linguiscgroup literally. Lengua de registro is the language in
which the resource is recorded; grouping is the language studied. Do not propagate
between these axes. CLIN/INALI governs Familia → Agrupación → Variante; Rama is optional
secondary-authority enrichment. Reconcile variant authorities before assigning values.
Do not substitute a nearby term for a missing closed-vocabulary value; report the gap.
Use references/MEXICAN_INDIGENOUS_LANGUAGE_GOVERNANCE.md and references/LANGUAGE_POLICY.md.

Classify language mentions as PRIMARY_SUBJECT_LANGUAGE, SECONDARY_LANGUAGE_MENTION or
VARIANT_EVIDENCE. Secondary mentions alone cannot produce subject grouping, family,
branch or variant. Preserve GR21–GR22 rules and evidence boundaries.

## Identifiers and evidence

Classify whole identifiers first. ORCID is evidence-only with no approved DSpace binding;
never propose any ORCID fragment as ISSN. Independently occurring valid ISSNs remain
eligible. Read references/IDENTIFIER_CLASSIFICATION.md and preserve GR23.
Use references/EVIDENCE_MODEL.md and references/QA_RULES.md for evidence and QA rules.
Historical Golden Set GR01–GR23 is retained byte-for-byte; it is not a new independent
evaluation of this candidate's mapping changes.

## Partial coverage

The complete srsc hierarchy remains UNKNOWN. A null values list means unavailable,
not empty. Observed configured forms and workspace 2050 do not reconstruct the active
sections endpoint's HTTP 204. Never claim complete migration equivalence or baseline
adoption from this candidate. See assets/snibli-migration-evidence.json for provenance.
