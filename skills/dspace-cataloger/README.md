# dspace-cataloger — Version Registry

Status: **GOVERNED — REPOSITORY SOURCE OF TRUTH**

`v3.9.3` is proposed as current by the reviewed pointer PR; this change takes
effect on main only after merge. Repository adoption does not install or deploy
the skill or authorize DSpace writes. The failed `v3.9.1` package
remains preserved as historical recovery evidence and is not an adoptable binary
parent.

Canonical root: `skills/dspace-cataloger/`

Governed by: [`docs/governance/PROJECT-GOVERNANCE-CONTRACT-v1.1-SKILL-VERSIONING-AMENDMENT.md`](../../docs/governance/PROJECT-GOVERNANCE-CONTRACT-v1.1-SKILL-VERSIONING-AMENDMENT.md)

## Purpose

This directory is the canonical GitHub location for preserving complete, versioned `dspace-cataloger` skill artifacts and their supporting audit or migration evidence.

A skill version is considered repository-preserved only when its complete artifact, or a complete lossless representation, exists in this directory tree and is traceable through Git history.

## Canonical layout

```text
skills/dspace-cataloger/
  README.md
  CURRENT_RELEASE.md
  versions/
  audits/
  migrations/
```

## Current repository-preserved version

**3.9.3 — CURRENT ON MERGE / COMPLETE STABLE PACKAGE**

Canonical preservation representation:

`skills/dspace-cataloger/versions/v3.9.3/`

Artifact identity:

- canonical artifact name: `dspace-cataloger-v3.9.3.skill`;
- representation: complete ZIP artifact plus exact extracted source and member hashes;
- size: `407637` bytes;
- SHA-256: `4ff74baa59049fd9ac9edd1b50458c58493bd2eb9c1482c4a6846f3456ad616e`;
- ZIP integrity: `PASS`;
- JSON validation: `PASS` (`49` JSON members);
- package files: `229`;
- form bindings: `57`, preserving `56` originals; unique metadata keys: `55`;
- Golden Set: `GR01–GR23` present.

Canonical evidence:

- [`CURRENT_RELEASE.md`](CURRENT_RELEASE.md)
- [`versions/v3.9.3/manifest.json`](versions/v3.9.3/manifest.json)
- [Stable release evidence and reproduction](../../reports/snibli-migration/stable-release-20261021.md)

The direct parent is checksum-pinned v3.9.3-rc.2, preserved with rc.1 by merged
PR #87. Its operational assets, raw HAL and historical Golden Set remain unchanged.
The accepted focused pilot supports release preparation, not DSpace corrections.
Full migration equivalence and historical srsc equivalence remain UNKNOWN;
active sections HAL remains UNKNOWN_HTTP_204.

v3.9.2 is a verified re-derivation from the user-provided v3.9 artifact
(`76fdc467…e01c06c`). It carries the documented v3.9.1 semantics forward but
does not claim that the v3.9.1 binary is valid. The preservation incident remains
recorded in [`audits/dspace-cataloger-v3.9.1-integrity-recheck-2026-09-09.md`](audits/dspace-cataloger-v3.9.1-integrity-recheck-2026-09-09.md).

## Preserved versions

| Version | Artifact | GitHub preservation status |
| --- | --- | --- |
| 3.5 | `dspace-cataloger-v3.5.skill` | `PENDING_MIGRATION` |
| 3.6 | `dspace-cataloger-v3.6.skill` | `PENDING_MIGRATION` |
| 3.8 | `dspace-cataloger-v3.8.skill` | `PENDING_MIGRATION` |
| 3.9 | `dspace-cataloger-v3.9.skill` | `SUPERSEDED / REPOSITORY-PRESERVED` |
| 3.9.1 | `dspace-cataloger-v3.9.1.skill` | `PRESERVED / INTEGRITY FAILURE / RECOVERY REQUIRED` |
| 3.9.2 | `dspace-cataloger-v3.9.2.skill` | `VERIFIED RE-DERIVATION / REPOSITORY-PRESERVED / SUPERSEDED ON POINTER MERGE` |
| 3.9.3-rc.1 | `dspace-cataloger-v3.9.3-rc.1.skill` | `REPOSITORY-PRESERVED CANDIDATE / PR #87` |
| 3.9.3-rc.2 | `dspace-cataloger-v3.9.3-rc.2.skill` | `REPOSITORY-PRESERVED CANDIDATE / DIRECT STABLE PARENT / PR #87` |
| 3.9.3 | `dspace-cataloger-v3.9.3.skill` | `COMPLETE STABLE PACKAGE / CURRENT ON REVIEWED POINTER MERGE` |

The v3.9.1 audit records `SOURCE_VARIANCE_RECORDED`: the local v3.9 artifact used as the direct patch base and the repository-preserved v3.9 artifact do not share the same SHA-256. The repository does not claim byte-identical lineage between those two v3.9 artifacts.

## Preservation requirements

When a historical or new version is added, record at minimum:

- version identifier;
- artifact filename;
- provenance/source;
- preservation status;
- checksum when available;
- audit or validation status when available;
- predecessor/successor relationship when relevant;
- whether the artifact is original, reconstructed, or derived.

## Adoption rule

Discussion in ChatGPT, local notes, memory, or temporary files does not constitute adoption of a skill version.

The governed path is:

```text
finding or proposal
    -> versioned skill artifact
    -> GitHub commit / PR
    -> verification
    -> adoption
```

This registry must be updated whenever the repository-preserved current version changes.
