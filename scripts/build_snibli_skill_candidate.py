"""Build a deterministic, unadopted skill candidate from verified local evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import zipfile
from pathlib import Path

from audit_snibli_migration import ROOT, load_candidate, release_archive

VERSION = "3.9.3-rc.1"
PREFIX = "dspace-cataloger/"
STAMP = "2026-10-21T00:00:00Z"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def build_members(candidate_path: Path, decision_path: Path, runtime: dict):
    candidate, _ = load_candidate(candidate_path)
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    if {c["id"] for c in decision["changes"] if c["approved"] is True} != {
        "C1",
        "C2",
        "C3",
    }:
        raise ValueError("C1_C2_C3_APPROVAL_REQUIRED")
    if decision["proposalId"] != candidate["proposalId"]:
        raise ValueError("APPROVAL_PROPOSAL_MISMATCH")
    blob, parent_hash = release_archive()
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}

    def asset(name):
        return json.loads(members[PREFIX + "assets/" + name])

    contract = asset("dspace-form-contract-v1.json")
    old_fields = {f["bindingId"]: f for f in contract["fields"]}
    fields = []
    for observed in candidate["fields"]:
        field = copy.deepcopy(old_fields.get(observed["referenceBindingId"], {}))
        for key in (
            "formId",
            "formOrder",
            "row",
            "fieldIndex",
            "metadataIndex",
            "renderOrder",
            "metadataField",
            "uiLabel",
            "inputType",
            "required",
            "repeatable",
            "controlledVocabulary",
            "closedVocabulary",
        ):
            field[key] = observed[key]
        field["bindingId"] = observed["observedBindingId"]
        field["referenceBindingId"] = observed["referenceBindingId"]
        field.setdefault("assistantLabel", observed["uiLabel"])
        field.setdefault("visibility", "visible")
        if observed["metadataField"] == "dc.type.genre":
            field["hints"] = "Indique si el recurso es un texto comparativo."
        fields.append(field)
    fields.sort(key=lambda f: f["renderOrder"])
    if [(f["metadataField"], f["uiLabel"]) for f in fields] != [
        (
            f["metadata_field"],
            "Identificador"
            if f["binding_id"]
            in {
                "issn",
                "identifier-other",
                "ismn",
                "govdoc",
                "uri",
                "isbn",
                "eissn",
                "eisbn",
                "handle",
                "doi",
            }
            else f["ui_label"],
        )
        for f in runtime["fields"]
    ]:
        raise ValueError("RUNTIME_MAPPING_MISMATCH")
    for field, current in zip(fields, runtime["fields"], strict=True):
        if (field["required"], field["repeatable"], field["controlledVocabulary"]) != (
            current["required"],
            current["repeatable"],
            current["vocabulary_id"],
        ):
            raise ValueError("RUNTIME_FLAGS_MISMATCH")
    for name, values in runtime["controlled_vocabulary_values"].items():
        if candidate["vocabularies"][name]["values"] != values:
            raise ValueError("RUNTIME_VOCABULARY_MISMATCH")

    coverage = {
        "fullMigrationEquivalence": "UNKNOWN",
        "srscHierarchy": "UNKNOWN",
        "activeSectionsHAL": "UNKNOWN_HTTP_204",
        "guiEvidenceScope": "workspaceitems/2050 only",
        "adopted": False,
        "runtimeEnabled": False,
    }
    provenance = {
        "parentRelease": "3.9.2",
        "parentSha256": parent_hash,
        "candidateSha256": sha(candidate_path.read_bytes()),
        "decisionSha256": sha(decision_path.read_bytes()),
        "captureSha256": candidate["source"]["sha256"],
        "approval": decision,
        "coverage": coverage,
    }
    instance = {
        "name": "Respositorio Ind",
        "dspaceVersion": "7.6.6",
        "ui": "https://www.iifl.unam.mx/SNIBLI",
        "server": "https://www.iifl.unam.mx/server",
        "apiBase": "https://www.iifl.unam.mx/server/api",
        "profileVersion": "3.1",
    }
    contract.update(
        contractVersion="1.1",
        generatedAt=STAMP,
        instance=instance,
        fields=fields,
        forms=candidate["forms"],
        coverage=coverage,
    )
    contract["evidence"] = {
        "primary": "assets/snibli-migration-evidence.json",
        "captureSha256": candidate["source"]["sha256"],
        "contractPolicy": "Literal labels and keys; human-approved mapping; no automatic writes.",
    }
    vocabularies = {
        name: {
            "status": v["status"],
            "values": v["values"],
            "entryCount": len(v["values"]) if v["values"] is not None else None,
            "error": "HIERARCHY_NOT_OBSERVED" if v["values"] is None else None,
        }
        for name, v in candidate["vocabularies"].items()
    }
    for name in ("genrePairs", "common_types"):
        vocabularies[name]["status"] = "HUMAN_APPROVED_LOCAL_MAPPING"
    registry = {
        f["metadata"]: {
            "key": f["metadata"],
            "id": f["id"],
            "scopeNote": f["scopeNote"],
            "element": f["metadata"].split(".")[1],
            "qualifier": ".".join(f["metadata"].split(".")[2:]) or None,
        }
        for f in candidate["metadataRegistryForCandidate"].values()
    }
    forms = {
        form["id"]: {
            "id": form["id"],
            "fields": [
                {
                    "row": f["row"],
                    "fieldIndex": f["fieldIndex"],
                    "metadataIndex": f["metadataIndex"],
                    "metadata": f["metadataField"],
                    "label": f["uiLabel"],
                    "inputType": f["inputType"],
                    "mandatory": f["required"],
                    "repeatable": f["repeatable"],
                    "controlledVocabulary": f["controlledVocabulary"],
                    "closed": f["closedVocabulary"],
                    "hints": f.get("hints"),
                }
                for f in fields
                if f["formId"] == form["id"]
            ],
        }
        for form in candidate["forms"]
    }
    mapping = {}
    for f in fields:
        if f["controlledVocabulary"]:
            values = mapping.setdefault(f["metadataField"], [])
            if f["controlledVocabulary"] not in values:
                values.append(f["controlledVocabulary"])
    profile = {
        "profileVersion": "3.1",
        "generatedAt": STAMP,
        "instance": instance,
        "source": {
            "mode": "LOCAL_EVIDENCE_PROJECTION_NOT_NEW_LIVE_CAPTURE",
            "apiBase": instance["apiBase"],
            "captureSha256": candidate["source"]["sha256"],
        },
        "traditionalForms": forms,
        "fieldToVocabulary": mapping,
        "metadataRegistryForTraditionalForms": registry,
        "vocabularies": vocabularies,
        "coverage": coverage,
        "collection": candidate["collection"],
    }
    target_keys = set(asset("dspace-cataloguing-profile-v3.json")["targetFields"])
    target_keys.add("dc.type.genre")
    profile["targetFields"] = {
        key: {
            "registered": True,
            "metadataField": registry[key],
            "formBindings": [
                {
                    "form": f["formId"],
                    "label": f["uiLabel"],
                    "inputType": f["inputType"],
                    "mandatory": f["required"],
                    "repeatable": f["repeatable"],
                    "controlledVocabulary": f["controlledVocabulary"],
                    "closed": f["closedVocabulary"],
                    "hints": f.get("hints"),
                }
                for f in fields
                if f["metadataField"] == key
            ],
        }
        for key in sorted(target_keys)
    }
    runtime_hash = sha(
        json.dumps(
            runtime, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    )
    lock = {
        "skillVersion": VERSION,
        "runtimeContractVersion": runtime["contract_version"],
        "catalogContractSha256": runtime_hash,
        "hashAlgorithm": "SHA256_CANONICAL_JSON_UTF8",
        "fieldCount": 57,
        "uniqueMetadataCount": 55,
        "applicationRepository": "Inbounduxd/cataloging-assistant",
        "applicationCommit": None,
        "status": "LOCAL_WORKING_TREE_NOT_DEPLOYED",
        "governance": runtime["runtime"],
    }
    manifest = asset("release-manifest.json")
    manifest.update(
        release="v" + VERSION,
        version=VERSION,
        previousRelease="v3.9.2",
        previousVersion="3.9.2",
        releaseDate="2026-10-21",
        generatedAt=STAMP,
        status="LOCAL_CANDIDATE_NOT_ADOPTED",
        formContractVersion="1.1",
        formBindingCount=57,
        uniqueMetadataCount=55,
        profileVersion="3.1",
        profileGeneratedAt=STAMP,
        vocabularyCount=len(vocabularies),
        targetFieldCount=len(target_keys),
        runtimeContractCodeVersion=runtime["contract_version"],
        runtimeContractSha256=runtime_hash,
        coverage=coverage,
        changePolicy="HUMAN_APPROVED_LOCAL_MAPPING_FROM_VERIFIED_V392",
        qa={"migrationEquivalence": "UNKNOWN", "srscHierarchy": "UNKNOWN"},
    )
    manifest["references"].append("references/SNIBLI_MIGRATION_2026.md")
    manifest["parentArtifact"] = {
        "release": "v3.9.2",
        "sha256": parent_hash,
        "verifiedExact": True,
        "provenance": "repository-preserved lossless base64 multipart",
    }
    manifest["goldenSet"]["status"] = (
        "HISTORICAL_FIXTURES_RETAINED_NOT_NEW_ADJUDICATION"
    )
    replacements = {
        "assets/dspace-form-contract-v1.json": encoded(contract),
        "assets/dspace-cataloguing-profile-v3.json": encoded(profile),
        "assets/controlled-vocabulary-index.json": encoded(vocabularies),
        "assets/release-manifest.json": encoded(manifest),
        "assets/runtime-contract-lock-v3.9.json": encoded(lock),
        "SKILL.md": SKILL.encode(),
    }
    for name, value in replacements.items():
        members[PREFIX + "historical-v3.9.2/" + name] = members[PREFIX + name]
        members[PREFIX + name] = value
    members[PREFIX + "assets/snibli-migration-evidence.json"] = encoded(provenance)
    members[PREFIX + "assets/cataloging-runtime-contract.json"] = encoded(runtime)
    members[PREFIX + "references/SNIBLI_MIGRATION_2026.md"] = MIGRATION.encode()
    # Existing references retain their semantic rules; current source takes precedence.
    for name in tuple(members):
        if (
            name.startswith(PREFIX + "references/")
            and name.endswith(".md")
            and not name.endswith("SNIBLI_MIGRATION_2026.md")
        ):
            members[name] = (
                "> Carried forward from v3.9.2. For current SNIBLI instance, form counts, "
                "order, vocabulary values and runtime lock, use "
                "[SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. "
                "Historical release counts and verification claims do not certify this candidate.\n\n"
            ).encode() + members[name]
    return members, provenance


SKILL = """---
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
"""

MIGRATION = """# Current SNIBLI mapping — v3.9.3-rc.1

This reference and the current assets supersede historical instance/count/hash claims
in carried-forward references. Historical copies of changed primary assets are under
historical-v3.9.2/; they are provenance, not current operational configuration.

Verified REST: https://www.iifl.unam.mx/server/api. Public UI:
https://www.iifl.unam.mx/SNIBLI/home. Do not infer another API from a frontend URL or send
credentials to redirects. This package does not authorize authenticated operations.

Collection: Lingüística Maayat'aan, Maya, 3ce3afb3-94ed-4f60-bfda-0a1242c4d689,
Handle 123456789/393; definition traditional. Configured forms contain 45 + 12 bindings.
The existing workspace 2050 visibly renders traditionalpageone, traditionalpagetwo,
upload and license. This is scoped GUI evidence; active sections HAL remains UNKNOWN.

Human approval C1–C3 covers the optional dc.type.genre mapping, observed ordering and
the three new common_types values. It does not authorize writes, automatic inference,
baseline promotion or deployment. Full srsc hierarchy and migration equivalence remain
UNKNOWN. No validation result here claims complete compatibility.

The executable application reference is snibli-contract-2026-10-21. Its exact payload
and canonical-JSON hash are included in assets/cataloging-runtime-contract.json and
assets/runtime-contract-lock-v3.9.json (legacy filename retained for compatibility).
The local working tree is not a committed or deployed runtime. Its lock must be
revalidated against the runtime before any future adoption.

Parent: verified v3.9.2 b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede.
The parent stays unchanged and remains CURRENT. This candidate has no preservation
or adoption claim until the repository governance transition is completed.
"""


def package(members):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, value in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    proposal = ROOT / "reports/snibli-migration/reconciliation-proposal"
    parser.add_argument(
        "--candidate", type=Path, default=proposal / "candidate-contract.json"
    )
    parser.add_argument("--decision", type=Path, default=proposal / "decision.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from cataloging_api.cataloging_contract import contract_payload

    members, provenance = build_members(
        args.candidate, args.decision, contract_payload()
    )
    artifact = package(members)
    with zipfile.ZipFile(io.BytesIO(artifact)) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))
    args.output.mkdir(parents=True, exist_ok=False)
    artifact_name = f"dspace-cataloger-v{VERSION}.skill"
    (args.output / artifact_name).write_bytes(artifact)
    for name, value in members.items():
        target = args.output / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(value)
    manifest = {
        "skill": "dspace-cataloger",
        "version": VERSION,
        "artifact": artifact_name,
        "status": "LOCAL_CANDIDATE_NOT_ADOPTED_NOT_REPOSITORY_PRESERVED",
        "sha256": sha(artifact),
        "sizeBytes": len(artifact),
        "packageFileCount": len(members),
        "memberSha256": {name: sha(value) for name, value in sorted(members.items())},
        "validation": {
            "zipIntegrity": "PASS",
            "jsonValidation": "PASS",
            "jsonFileCount": sum(name.endswith(".json") for name in members),
            "formBindingCount": 57,
            "uniqueMetadataCount": 55,
            "fullMigrationEquivalence": "UNKNOWN",
        },
        "provenance": provenance,
    }
    (args.output / "manifest.json").write_bytes(encoded(manifest))
    print(
        json.dumps(
            {k: manifest[k] for k in ("version", "status", "sha256", "sizeBytes")}
        )
    )


if __name__ == "__main__":
    main()
