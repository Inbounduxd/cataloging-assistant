# Current repository-preserved release

## `dspace-cataloger v3.9.3`

Status: **CURRENT ON MERGE OF THE REVIEWED POINTER PR**

This pointer change proposes repository adoption of the complete stable package.
On the PR branch it remains a proposal; main retains v3.9.2 until review and merge.
Repository adoption does not install the skill, deploy the application, promote a
runtime baseline, activate synchronization or authorize DSpace writes.

Canonical directory: `skills/dspace-cataloger/versions/v3.9.3/`.

- Artifact: `dspace-cataloger-v3.9.3.skill`
- SHA-256: `4ff74baa59049fd9ac9edd1b50458c58493bd2eb9c1482c4a6846f3456ad616e`
- Size: `407637` bytes; `229` ZIP members; `49` JSON members.
- Direct parent: v3.9.3-rc.2, SHA-256
  `c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae`.
- Preserved ancestor: v3.9.2, SHA-256
  `b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede`.

Contract: **57 bindings / 55 unique metadata keys**. All original 56 bindings remain.
The new optional `dc.type.genre` asks «¿Es un texto comparativo?» with the exact
`genrePairs` values. `common_types` adds Códice, Reseña and Documento Colonial.
The current `srsc` HAL tree has 665 nodes, 653 edges and 12 roots, with 126 original
responses preserved. Golden Set GR01–GR23 remains byte-identical to the parent.

The accepted focused pilot supports an Article → Reseña proposal while leaving
the comparative field pending; no record was changed. Its nine checks are technical
validation of one case, not independent gold adjudication or global certification.

Known limits: full migration equivalence and historical `srsc` equivalence remain
UNKNOWN; active sections HAL remains UNKNOWN_HTTP_204. Coverage adoption flags in
the immutable package record build-time state; this governed pointer controls
repository adoption. Human review remains required for every future record change.

Application alignment: `snibli-contract-2026-10-21`, canonical payload hash
`fb9473e926eefe0c7d119944422cf26c364d9f95afcda618851782544563b106`.
This records the source contract, not the configuration of a deployed runtime.

See [release evidence](../../reports/snibli-migration/stable-release-20261021.md),
[manifest](versions/v3.9.3/manifest.json) and the packaged
`references/STABLE_RELEASE_3.9.3.md` for scope, lineage and reconstruction.
v3.9.2 and both release candidates remain unchanged. The v3.9.1 integrity incident
remains documented in the historical audits; its binary is not a valid parent.
