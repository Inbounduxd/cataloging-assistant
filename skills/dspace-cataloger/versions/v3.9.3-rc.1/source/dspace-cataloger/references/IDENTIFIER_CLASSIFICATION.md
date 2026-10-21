> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Identifier classification v3.9.2

Classify identifier-shaped evidence before DSpace mapping.

- `doi`, `issn`, and `isbn` may map only through existing governed bindings.
- `orcid` is evidence-only: retain the complete normalized value and provenance,
  but do not map it to DSpace or a draft until a governed binding is approved.
- Match a complete ORCID (`0000-0000-0000-0000`, including an `X` check digit)
  as one identifier. Do not emit a contained eight-character segment as ISSN.
- A valid ISSN outside that range remains independently extractable.

This is a classification and QA guardrail, not a DSpace schema change. It preserves
human approval, runtime read-only behavior, and the existing 56 bindings.
