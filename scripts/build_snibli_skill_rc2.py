"""Build an unadopted rc.2 from pinned rc.1 plus verified public srsc HAL evidence."""

from __future__ import annotations

import argparse
import io
import json
import zipfile
from collections import deque
from pathlib import Path

from build_snibli_skill_candidate import PREFIX, ROOT, encoded, package, sha

VERSION = "3.9.3-rc.2"
PARENT_HASH = "d4bcb41c342f31150a1da7244550b319de1ae2a71a83b401bd2f05222feffa49"
API = "https://www.iifl.unam.mx/server/api"


def verify_capture(folder: Path):
    raw_export = (folder / "export.json").read_bytes()
    data = json.loads(raw_export)
    tree_bytes = (folder / "srsc-tree.json").read_bytes()
    tree_document = json.loads(tree_bytes)
    tree = tree_document["tree"]
    if (
        tree_document["source_export_sha256"] != sha(raw_export)
        or tree_document["vocabulary"] != "srsc"
        or tree_document["source_api"] != API
        or data["source_base_url"] != API
        or not data["capture_complete"]
        or data["authenticated"]
        or data["login_post_count"] != 0
        or data["errors"]
        or not tree["complete"]
        or tree["status"] != "PASS"
        or tree["errors"]
        or data["vocabulary_evidence"]["srsc"]["tree"] != tree
    ):
        raise ValueError("INCOMPLETE_OR_INCONSISTENT_CAPTURE")
    files = {}
    observed = {}
    for event in data["captures"]:
        if (
            event["method"] != "GET"
            or event["http_status"] != 200
            or not event["endpoint"].startswith(
                API + "/submission/vocabularyEntryDetails/"
            )
        ):
            raise ValueError("UNEXPECTED_CAPTURE_SCOPE")
        relative = Path(event["raw_file"])
        if (
            len(relative.parts) != 2
            or relative.parts[0] != "raw"
            or ".." in relative.parts
        ):
            raise ValueError("UNSAFE_RAW_PATH")
        path = folder / relative
        if not path.resolve().is_relative_to(folder.resolve()):
            raise ValueError("UNSAFE_RAW_PATH")
        body = path.read_bytes()
        if sha(body) != event["sha256"] or len(body) != event["bytes"]:
            raise ValueError("RAW_HASH_MISMATCH")
        files[relative.as_posix()] = body
        observed.setdefault(event["surface"], []).append(json.loads(body))
    surfaces = {
        key: value
        for key, value in data["pages_by_surface"].items()
        if key == "vocabulary_top:srsc" or key.startswith("vocabulary_children:srsc:")
    }
    if observed != surfaces or set(surfaces) != set(data["surfaces_complete"]):
        raise ValueError("RAW_SURFACE_MISMATCH")
    collections = {}
    for surface, pages in surfaces.items():
        if not pages:
            raise ValueError("EMPTY_PAGE_SEQUENCE")
        total_pages = pages[0]["page"]["totalPages"]
        total_elements = pages[0]["page"]["totalElements"]
        relation = (
            "vocabularyEntryDetails" if surface == "vocabulary_top:srsc" else "children"
        )
        items = []
        for index, page in enumerate(pages):
            if page["page"] != {
                **page["page"],
                "number": index,
                "totalPages": total_pages,
                "totalElements": total_elements,
            }:
                raise ValueError("PAGINATION_CHANGED")
            items.extend(page.get("_embedded", {}).get(relation, []))
        if len(pages) != max(1, total_pages) or len(items) != total_elements:
            raise ValueError("PAGINATION_INCOMPLETE")
        collections[surface] = items
    roots = collections.get("vocabulary_top:srsc", [])
    queue = deque((node, None) for node in roots)
    nodes, edges, seen, expanded = [], [], set(), {"vocabulary_top:srsc"}
    while queue:
        node, parent = queue.popleft()
        identifier = node["id"]
        if identifier in seen or not identifier.startswith("srsc:"):
            raise ValueError("CYCLE_OR_DUPLICATE")
        seen.add(identifier)
        nodes.append(node)
        if parent is not None:
            edges.append({"parent": parent, "child": identifier})
        if type(node.get("selectable")) is not bool:
            raise ValueError("INVALID_SELECTABILITY")
        has_children = node["otherInformation"]["hasChildren"]
        if has_children not in ("true", "false") or not all(
            isinstance(node.get(key), str) for key in ("value", "display")
        ):
            raise ValueError("INVALID_NODE")
        if has_children == "true":
            surface = "vocabulary_children:" + identifier
            children = collections.get(surface)
            if not children:
                raise ValueError("BRANCH_MISSING")
            expanded.add(surface)
            queue.extend((child, identifier) for child in children)
    if (
        expanded != set(surfaces)
        or nodes != tree["nodes"]
        or edges != tree["edges"]
        or tree["node_count"] != len(nodes)
        or tree["edge_count"] != len(edges)
        or tree_document["root_ids"] != [node["id"] for node in roots]
    ):
        raise ValueError("NORMALIZED_TREE_MISMATCH")
    facts = {
        "vocabulary": "srsc",
        "captureStatus": "PASS_REACHABLE_HAL_TREE",
        "nodeCount": len(nodes),
        "edgeCount": len(edges),
        "rootCount": len(roots),
        "rawResponseCount": len(files),
        "exportSha256": sha(raw_export),
        "treeSha256": sha(tree_bytes),
        "capturedAt": data["captured_at"],
        "historicalEquivalence": "UNKNOWN",
        "serverXmlEquivalence": "NOT_TESTED",
    }
    return tree_document, facts, files, raw_export, tree_bytes


def build_members(parent: Path, capture: Path):
    manifest = json.loads((parent / "manifest.json").read_text())
    blob = (parent / "dspace-cataloger-v3.9.3-rc.1.skill").read_bytes()
    if sha(blob) != PARENT_HASH or manifest["sha256"] != PARENT_HASH:
        raise ValueError("PARENT_HASH_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        if archive.testzip() is not None:
            raise ValueError("PARENT_ZIP_INVALID")
        members = {name: archive.read(name) for name in archive.namelist()}
    tree_doc, facts, raw_files, raw_export, tree_bytes = verify_capture(capture)
    nodes = tree_doc["tree"]["nodes"]
    srsc = {
        "status": "OBSERVED_COMPLETE_HAL_HIERARCHY",
        "hierarchical": True,
        "entryCount": len(nodes),
        "selectableEntryCount": sum(n["selectable"] for n in nodes),
        "values": [n["value"] for n in nodes if n["selectable"]],
        "error": None,
        "treeAsset": "assets/srsc-tree.json",
        "evidence": facts,
    }
    for name in (
        "dspace-form-contract-v1.json",
        "dspace-cataloguing-profile-v3.json",
        "release-manifest.json",
        "snibli-migration-evidence.json",
    ):
        key = PREFIX + "assets/" + name
        value = json.loads(members[key])
        value["coverage"]["srscHierarchy"] = "PASS_CURRENT_HAL_CAPTURE"
        value["coverage"]["srscHistoricalEquivalence"] = "UNKNOWN"
        if name == "dspace-cataloguing-profile-v3.json":
            value["vocabularies"]["srsc"] = srsc
            value["source"]["srscCapture"] = facts
        elif name == "release-manifest.json":
            value.update(
                release="v" + VERSION,
                version=VERSION,
                previousRelease="v3.9.3-rc.1",
                previousVersion="3.9.3-rc.1",
            )
            value["parentArtifact"] = {
                "release": "v3.9.3-rc.1",
                "sha256": PARENT_HASH,
                "status": "LOCAL_CANDIDATE_NOT_ADOPTED",
                "verifiedExact": True,
            }
            value["references"].append("references/SRSC_HAL_EVIDENCE.md")
            value["qa"]["srscHierarchy"] = "PASS_CURRENT_HAL_CAPTURE"
        elif name == "snibli-migration-evidence.json":
            value.update(
                parentRelease="3.9.3-rc.1", parentSha256=PARENT_HASH, srscCapture=facts
            )
            value["srscPreparationApproval"] = {
                "source": "Explicit user approval in this conversation",
                "date": "2026-10-21",
                "scope": "Prepare local rc.2 with captured srsc evidence",
                "adoptionAuthorized": False,
                "deploymentAuthorized": False,
            }
        members[key] = encoded(value)
    vocab_key = PREFIX + "assets/controlled-vocabulary-index.json"
    vocabulary = json.loads(members[vocab_key])
    vocabulary["srsc"] = srsc
    members[vocab_key] = encoded(vocabulary)
    lock_key = PREFIX + "assets/runtime-contract-lock-v3.9.json"
    lock = json.loads(members[lock_key])
    lock["skillVersion"] = VERSION
    members[lock_key] = encoded(lock)
    members[PREFIX + "assets/srsc-tree.json"] = tree_bytes
    members[PREFIX + "evidence/srsc/export.json"] = raw_export
    for relative, body in raw_files.items():
        members[PREFIX + "evidence/srsc/" + relative] = body
    members[PREFIX + "assets/srsc-evidence-validation.json"] = encoded(facts)
    # Keep the current entrypoint explicit; historical documents and fixtures stay intact.
    skill_key = PREFIX + "SKILL.md"
    skill = (
        members[skill_key]
        .decode()
        .replace("dspace-cataloger v3.9.3-rc.1", "dspace-cataloger v" + VERSION)
    )
    skill = skill.replace(
        "The complete srsc hierarchy remains UNKNOWN. A null values list means unavailable,\nnot empty.",
        "The current srsc HAL hierarchy has been captured completely within its exposed scope.\nUse assets/srsc-tree.json and references/SRSC_HAL_EVIDENCE.md; preserve IDs, paths,\nparent-child relations and selectable flags. Values are authorized only when selectable.\nThis capture does not establish historical equivalence. A null values list elsewhere\nmeans unavailable, not empty.",
    )
    members[skill_key] = skill.encode()
    guide_key = PREFIX + "references/SNIBLI_MIGRATION_2026.md"
    guide = members[guide_key].decode().replace("v3.9.3-rc.1", "v" + VERSION)
    guide = guide.replace(
        "Parent: verified v3.9.2", "Preserved ancestor: verified v3.9.2"
    )
    guide = guide.replace(
        "Full srsc hierarchy and migration equivalence remain\nUNKNOWN.",
        "The current srsc HAL hierarchy is now captured; see SRSC_HAL_EVIDENCE.md.\nHistorical srsc equivalence and full migration equivalence remain UNKNOWN.",
    )
    members[guide_key] = guide.encode()
    members[PREFIX + "references/SRSC_HAL_EVIDENCE.md"] = GUIDE.encode()
    return members, facts


GUIDE = """# srsc HAL evidence in v3.9.3-rc.2

The public GET-only traversal captured the hierarchy currently exposed by SNIBLI:
665 nodes, 653 parent-child relations, 12 roots, 126 raw HAL responses, no login.
assets/srsc-tree.json retains literal IDs, labels, values, selectable flags and edges.
The vocabulary index exposes selectable values only; never infer selection permission
from being a parent or leaf. Retain non-selectable nodes as hierarchy context.

Original HAL bodies and export envelope are in evidence/srsc/. Their hashes, pagination
and reconstruction have been checked against the normalized tree. This is not an
atomic database snapshot or proof of nodes the API does not expose. Validate current
vocabulary availability before any future human-controlled copy to DSpace.

The prior UNKNOWN for the current reachable tree is resolved. Historical equivalence
remains UNKNOWN because the preserved historical release lacks the full tree. Active
sections HAL remains UNKNOWN_HTTP_204; full migration equivalence remains UNKNOWN.
This evidence supersedes rc.1's current-tree gap but does not rewrite rc.1 itself.

Human authorization covers preparing rc.2 with this captured evidence, not adopting,
publishing, installing or deploying it. No DSpace writes, automatic inference, agent
mutation, baseline promotion or synchronization are enabled. The application runtime
payload/hash remains unchanged from rc.1, as do the 57 bindings and 55 metadata keys.
Golden Set GR01–GR23 remains byte-for-byte unchanged; no new adjudication is claimed.

Direct binary parent: local v3.9.3-rc.1, verified checksum recorded in the manifests.
The adopted repository pointer still identifies preserved v3.9.2. Without a commit,
rc.2 is a local candidate and must not be described as preserved on GitHub.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parent",
        type=Path,
        default=ROOT / "skills/dspace-cataloger/versions/v3.9.3-rc.1",
    )
    parser.add_argument(
        "--capture",
        type=Path,
        default=ROOT / "reports/snibli-migration/srsc-hal-tree-20261021",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    members, facts = build_members(args.parent, args.capture)
    blob = package(members)
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        if archive.testzip() is not None:
            raise ValueError("INVALID_OUTPUT_ZIP")
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))
    args.output.mkdir(parents=True, exist_ok=False)
    name = f"dspace-cataloger-v{VERSION}.skill"
    (args.output / name).write_bytes(blob)
    for path, body in members.items():
        target = args.output / "source" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
    manifest = {
        "skill": "dspace-cataloger",
        "version": VERSION,
        "artifact": name,
        "status": "LOCAL_CANDIDATE_NOT_ADOPTED_NOT_REPOSITORY_PRESERVED",
        "sha256": sha(blob),
        "sizeBytes": len(blob),
        "packageFileCount": len(members),
        "parentSha256": PARENT_HASH,
        "parentVersion": "3.9.3-rc.1",
        "srscEvidence": facts,
        "memberSha256": {path: sha(body) for path, body in sorted(members.items())},
        "validation": {
            "zipIntegrity": "PASS",
            "jsonValidation": "PASS",
            "jsonFileCount": sum(path.endswith(".json") for path in members),
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
