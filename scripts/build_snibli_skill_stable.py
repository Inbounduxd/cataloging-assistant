"""Prepare stable v3.9.3 offline; repository adoption requires review of its pointer PR."""

from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path

from build_snibli_skill_candidate import PREFIX, ROOT, encoded, package, sha

VERSION = "3.9.3"
PARENT_HASH = "c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae"
PROPOSAL_HASH = "45b66afdf39cc2f9777c4e8ce952f11b060b0e1cb9f5186abe6f5b4f5a04accd"
VALIDATION_HASH = "e34eaadc91253dd75c4f0841776cd471f18567b50af9b32cc73720b1d4d33d00"
STATUS = "STABLE_PREPARED_FOR_REPOSITORY_REVIEW"


def build_members(parent: Path, pilot: Path):
    manifest = json.loads((parent / "manifest.json").read_bytes())
    blob = (parent / "dspace-cataloger-v3.9.3-rc.2.skill").read_bytes()
    if sha(blob) != PARENT_HASH or manifest["sha256"] != PARENT_HASH:
        raise ValueError("PARENT_HASH_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        if archive.testzip() is not None:
            raise ValueError("PARENT_ZIP_INVALID")
        members = {name: archive.read(name) for name in archive.namelist()}
    for name, digest in (
        ("proposal.json", PROPOSAL_HASH),
        ("validation.json", VALIDATION_HASH),
    ):
        body = (pilot / name).read_bytes()
        if sha(body) != digest:
            raise ValueError("PILOT_HASH_MISMATCH")
        members[PREFIX + "evidence/functional-pilot/" + name] = body
    acceptance_bytes = (pilot / "acceptance.json").read_bytes()
    acceptance = json.loads(acceptance_bytes)
    if (
        acceptance["status"] != "ACCEPTED_FOR_STABLE_PREPARATION_AND_PR"
        or acceptance["proposalSha256"] != PROPOSAL_HASH
        or acceptance["validationSha256"] != VALIDATION_HASH
        or acceptance["dspaceWriteAuthorized"]
        or acceptance["deploymentAuthorized"]
        or acceptance["prMergeAuthorized"]
    ):
        raise ValueError("INVALID_ACCEPTANCE_SCOPE")
    validation = json.loads((pilot / "validation.json").read_bytes())
    if not validation["checks"] or not all(validation["checks"].values()):
        raise ValueError("PILOT_CHECK_FAILED")
    members[PREFIX + "evidence/functional-pilot/acceptance.json"] = acceptance_bytes
    for name in (
        "dspace-form-contract-v1.json",
        "dspace-cataloguing-profile-v3.json",
        "release-manifest.json",
        "snibli-migration-evidence.json",
    ):
        key = PREFIX + "assets/" + name
        value = json.loads(members[key])
        # Coverage is a build-time record; only the governed repository pointer adopts.
        value["coverage"]["repositoryAdoption"] = "PENDING_POINTER_PR_REVIEW"
        if name == "release-manifest.json":
            value.update(
                release="v" + VERSION,
                version=VERSION,
                previousRelease="v3.9.3-rc.2",
                previousVersion="3.9.3-rc.2",
                status=STATUS,
                parentArtifact={
                    "release": "v3.9.3-rc.2",
                    "sha256": PARENT_HASH,
                    "status": "REPOSITORY_PRESERVED_CANDIDATE_PR_87",
                    "verifiedExact": True,
                },
                functionalPilot={
                    "proposalSha256": PROPOSAL_HASH,
                    "validationSha256": VALIDATION_HASH,
                    "acceptanceSha256": sha(acceptance_bytes),
                    "technicalChecks": len(validation["checks"]),
                    "scope": "One focused case; not independent gold adjudication",
                },
            )
            value["references"].append("references/STABLE_RELEASE_3.9.3.md")
        elif name == "snibli-migration-evidence.json":
            value.update(
                parentRelease="3.9.3-rc.2",
                parentSha256=PARENT_HASH,
                stablePreparationApproval=acceptance,
            )
        members[key] = encoded(value)
    key = PREFIX + "assets/runtime-contract-lock-v3.9.json"
    lock = json.loads(members[key])
    lock["skillVersion"] = VERSION
    members[key] = encoded(lock)
    key = PREFIX + "SKILL.md"
    skill = (
        members[key]
        .decode()
        .replace("# dspace-cataloger v3.9.3-rc.2", "# dspace-cataloger v3.9.3")
    )
    skill = skill.replace(
        "Local release candidate, not adopted, deployed or repository-preserved through Git.",
        "Stable package prepared for repository review. See references/STABLE_RELEASE_3.9.3.md\n"
        "for provenance and adoption scope; CURRENT_RELEASE.md in the repository controls adoption.",
    )
    members[key] = skill.encode()
    key = PREFIX + "references/SNIBLI_MIGRATION_2026.md"
    guide = (
        members[key]
        .decode()
        .replace(
            "# Current SNIBLI mapping — v3.9.3-rc.2",
            "# Current SNIBLI mapping — v3.9.3",
        )
    )
    guide = guide.replace(
        "The local working tree is not a committed or deployed runtime. Its lock must be\nrevalidated against the runtime before any future adoption.",
        "The application contract is preserved by merged PR #87. This is not evidence of\n"
        "a deployed runtime; revalidate its lock before any runtime activation.",
    ).replace(
        "The parent stays unchanged and remains CURRENT. This candidate has no preservation\nor adoption claim until the repository governance transition is completed.",
        "The historical artifacts remain unchanged. Stable preparation derives directly from\n"
        "pinned rc.2. See STABLE_RELEASE_3.9.3.md; repository adoption is controlled by the\n"
        "reviewed root pointer, independently of installation or deployment.",
    )
    members[key] = guide.encode()
    key = PREFIX + "references/SRSC_HAL_EVIDENCE.md"
    guide = members[key].decode()
    guide = guide[: guide.index("Human authorization covers preparing rc.2")]
    members[key] = (
        guide
        + "This evidence was first packaged in rc.2, preserved by merged PR #87.\n"
        "Its original bodies, normalized tree and verified facts remain byte-identical.\n"
        "Stable preparation and repository adoption are described in STABLE_RELEASE_3.9.3.md.\n"
    ).encode()
    members[PREFIX + "references/STABLE_RELEASE_3.9.3.md"] = GUIDE.encode()
    return members


GUIDE = """# Stable release 3.9.3 — scope and lineage

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
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parent",
        type=Path,
        default=ROOT / "skills/dspace-cataloger/versions/v3.9.3-rc.2",
    )
    parser.add_argument(
        "--pilot",
        type=Path,
        default=ROOT / "reports/snibli-migration/functional-pilot-20261021",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    members = build_members(args.parent, args.pilot)
    blob = package(members)
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        if archive.testzip() is not None:
            raise ValueError("OUTPUT_ZIP_INVALID")
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))
    args.output.mkdir(parents=True, exist_ok=False)
    artifact = f"dspace-cataloger-v{VERSION}.skill"
    (args.output / artifact).write_bytes(blob)
    for name, body in members.items():
        target = args.output / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
    manifest = {
        "skill": "dspace-cataloger",
        "version": VERSION,
        "artifact": artifact,
        "status": STATUS,
        "sha256": sha(blob),
        "sizeBytes": len(blob),
        "packageFileCount": len(members),
        "parentVersion": "3.9.3-rc.2",
        "parentSha256": PARENT_HASH,
        "memberSha256": {name: sha(body) for name, body in sorted(members.items())},
        "validation": {
            "zipIntegrity": "PASS",
            "jsonValidation": "PASS",
            "jsonFileCount": sum(name.endswith(".json") for name in members),
            "fullMigrationEquivalence": "UNKNOWN",
        },
    }
    (args.output / "manifest.json").write_bytes(encoded(manifest))
    print(
        json.dumps(
            {
                key: manifest[key]
                for key in ("version", "sha256", "sizeBytes", "packageFileCount")
            }
        )
    )


if __name__ == "__main__":
    main()
