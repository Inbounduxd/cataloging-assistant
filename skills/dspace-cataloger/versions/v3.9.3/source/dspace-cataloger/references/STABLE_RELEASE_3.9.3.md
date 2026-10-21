# Stable release 3.9.3 — scope and lineage

Direct parent: v3.9.3-rc.2, SHA-256
c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae.
rc.1 and rc.2 are preserved by merged repository PR #87. The stable artifact changes
version/provenance and release guidance only: mapping, vocabularies, raw HAL, runtime
payload, schemas and Golden Set GR01–GR23 remain byte-identical to rc.2.

The user accepted the focused pilot for stable preparation and a pointer PR on
2026-10-21. Its nine technical checks passed. For Handle 123456789/733 the editorial
source supports Article → Reseña; dc.type.genre remains pending. This acceptance
approves the proposal and release preparation, not applying changes to DSpace.
The original pilot proposal/validation remain immutable historical review records;
the later acceptance is a separate evidence document. No independent adjudicated
gold set, full-text validation or complete migration certification is claimed.

The build-time status is STABLE_PREPARED_FOR_REPOSITORY_REVIEW. Repository adoption
takes effect only through review/merge of the complete package and CURRENT_RELEASE.md
pointer. That pointer, rather than immutable build-time coverage flags, identifies
the adopted version. Preparation authorizes neither PR merge nor installation,
deployment, synchronization, baseline promotion or DSpace writes. Every future field
decision still requires human approval. Runtime writes and agent mutations stay off.

Current contract: 57 bindings / 55 unique metadata keys, all original 56 bindings
retained; optional dc.type.genre with exact three genrePairs values; common_types
adds Códice, Reseña and Documento Colonial. The captured srsc tree has 665 nodes,
653 edges and 12 roots, backed by 126 original HAL responses. Historical srsc
equivalence remains UNKNOWN, active sections HAL UNKNOWN_HTTP_204 and complete
migration equivalence UNKNOWN. Do not convert these limits into a PASS.
