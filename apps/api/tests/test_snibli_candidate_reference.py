import copy
import json
from collections import defaultdict
from types import SimpleNamespace

import pytest

from .test_dspace_contract_snapshot import _paged
from .test_snibli_migration_audit import audit

COLLECTION = "f5da6fa3-cd05-4613-ae5a-e71512bda467"


@pytest.fixture
def candidate_and_evidence(tmp_path):
    release = audit.skill_asset("dspace-form-contract-v1.json")
    profile = audit.skill_asset("dspace-cataloguing-profile-v3.json")
    fields = copy.deepcopy(release["fields"])
    for field in fields:
        if field["formId"] == "traditionalpageone" and field["row"] >= 13:
            field["row"] += 1
    fields.append(
        {
            "formId": "traditionalpageone",
            "formOrder": 1,
            "row": 13,
            "fieldIndex": 0,
            "metadataIndex": 0,
            "metadataField": "dc.type.genre",
            "uiLabel": "¿Es un texto comparativo?",
            "inputType": "dropdown",
            "required": False,
            "repeatable": False,
            "controlledVocabulary": "genrePairs",
            "closedVocabulary": True,
        }
    )
    fields.sort(
        key=lambda f: tuple(f[k] for k in ("formOrder", "row", "fieldIndex", "metadataIndex"))
    )
    occurrences = defaultdict(int)
    for order, field in enumerate(fields, 1):
        pair = field["formId"], field["metadataField"]
        field["bindingKey"] = f"{pair[0]}:{pair[1]}:{occurrences[pair]}"
        occurrences[pair] += 1
        field["observedBindingId"] = (
            f"{field['formId']}:r{field['row']}:f{field['fieldIndex']}:m{field['metadataIndex']}"
        )
        field["renderOrder"] = order
    registry = {
        key: {"metadata": key, "id": field["id"], "scopeNote": field.get("scopeNote")}
        for key, field in profile["metadataRegistryForTraditionalForms"].items()
    }
    registry["dc.type.genre"] = {
        "metadata": "dc.type.genre",
        "id": 293,
        "scopeNote": "Genero del recurso",
    }
    vocabulary_reference = audit.skill_asset("controlled-vocabulary-index.json")
    vocabularies, vocabulary_evidence = {}, {}
    for name in {f["controlledVocabulary"] for f in fields if f["controlledVocabulary"]}:
        if name == "srsc":
            vocabularies[name] = {"status": "UNKNOWN", "values": None}
            vocabulary_evidence[name] = {"hierarchical": True, "pages": []}
            continue
        values = (
            ["Sí", "No", "Incluye Datos de Diferentes Lenguas"]
            if name == "genrePairs"
            else copy.deepcopy(vocabulary_reference[name]["values"])
        )
        if name == "common_types":
            values += ["Códice", "Reseña", "Documento Colonial"]
        vocabularies[name] = {"status": "OBSERVED_NOT_APPROVED", "values": values}
        vocabulary_evidence[name] = {
            "hierarchical": False,
            "pages": [_paged("entries", [{"value": value} for value in values])],
        }
    forms = []
    for form in release["forms"]:
        selected = [f for f in fields if f["formId"] == form["id"]]
        rows = [{"fields": []} for _ in range(max(f["row"] for f in selected) + 1)]
        for field in selected:
            controls = rows[field["row"]]["fields"]
            while len(controls) <= field["fieldIndex"]:
                controls.append({})
            control = controls[field["fieldIndex"]]
            if not control:
                control.update(
                    {
                        "label": field["uiLabel"],
                        "mandatory": field["required"],
                        "repeatable": field["repeatable"],
                        "input": {"type": field["inputType"]},
                        "selectableMetadata": [],
                    }
                )
            control["selectableMetadata"].append(
                {
                    "metadata": field["metadataField"],
                    "controlledVocabulary": field["controlledVocabulary"],
                    "closed": field["closedVocabulary"],
                }
            )
        forms.append({"id": form["id"], "rows": rows})
    raw_fields = []
    for key, field in registry.items():
        prefix, element, *qualifier = key.split(".")
        raw_fields.append(
            {
                "id": field["id"],
                "element": element,
                "qualifier": qualifier[0] if qualifier else None,
                "scopeNote": field["scopeNote"],
                "_embedded": {"schema": {"prefix": prefix}},
            }
        )
    prefixes = sorted({key.split(".")[0] for key in registry})
    pages = {
        "metadata_schemas": [
            _paged("metadataschemas", [{"prefix": p, "id": i} for i, p in enumerate(prefixes, 1)])
        ],
        "metadata_fields": [_paged("metadatafields", raw_fields)],
        "submission_forms": [_paged("submissionforms", forms)],
        "active_submission_definition": [{"name": "traditional"}],
        "active_submission_sections": [
            {
                "_observation": {"observable": False, "statusCode": 204},
                "page": {"number": 0, "totalPages": 0, "totalElements": 0},
            }
        ],
    }
    for prefix in prefixes:
        pages["metadata_fields_by_schema:" + prefix] = [
            _paged(
                "metadatafields",
                [field for field in raw_fields if field["_embedded"]["schema"]["prefix"] == prefix],
            )
        ]
    candidate = {
        "proposalId": "test-candidate",
        "status": "CANDIDATE_REVIEW_REQUIRED",
        "adopted": False,
        "runtimeEnabled": False,
        "reference": {"sha256": audit.RELEASE_HASH},
        "writePolicy": release["writePolicy"],
        "governance": {
            "humanApprovalRequired": True,
            "automaticPromotion": False,
            "dspaceWriteEnabled": False,
            "newBindingAutomaticInferenceEnabled": False,
            "newVocabularyAutomaticClassificationEnabled": False,
        },
        "forms": release["forms"],
        "fields": fields,
        "counts": {
            "bindings": 57,
            "uniqueMetadataKeys": 55,
            "referenceBindingsRetained": 56,
            "additionalBindings": 1,
        },
        "collection": {"uuid": COLLECTION, "handle": "123456789/999"},
        "metadataRegistryForCandidate": registry,
        "vocabularies": vocabularies,
    }
    evidence = {
        "source_base_url": "https://www.iifl.unam.mx/server/api",
        "collection_uuid": COLLECTION,
        "collection_handle": "123456789/999",
        "pages_by_surface": pages,
        "vocabulary_evidence": vocabulary_evidence,
    }
    cpath, epath = tmp_path / "candidate.json", tmp_path / "observed.json"

    def save():
        cpath.write_text(json.dumps(candidate), encoding="utf-8")
        epath.write_text(json.dumps(evidence), encoding="utf-8")

    save()
    return candidate, evidence, cpath, epath, save


def test_candidate_match_keeps_unobservable_surfaces_unknown(candidate_and_evidence):
    _, _, cpath, epath, _ = candidate_and_evidence
    result = audit.compare_candidate(cpath, epath)
    assert result["configured_forms"]["status"] == "PASS"
    assert result["configured_forms"]["bindings"] == 57
    assert result["registry"]["status"] == "PASS"
    assert result["registry"]["compared_keys"] == 55
    assert result["collection"]["status"] == "PASS"
    assert result["vocabularies"]["status"] == "UNKNOWN"
    assert result["active_membership"]["status"] == "UNKNOWN"
    assert (
        "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204" in result["active_membership"]["warnings"]
    )
    assert result["full_migration_equivalence"] == "UNKNOWN"
    assert result["human_approved"] is result["runtime_enabled"] is False


def test_explicit_reference_does_not_hide_release_drift_or_use_network(candidate_and_evidence):
    _, _, cpath, epath, _ = candidate_and_evidence
    original_candidate, original_observed = cpath.read_bytes(), epath.read_bytes()
    args = SimpleNamespace(
        public_url=audit.PUBLIC,
        api_base=None,
        timeout=1,
        offline=True,
        baseline=None,
        observed=epath,
        candidate=cpath,
    )

    def forbidden(*args):
        raise AssertionError("Network used for offline comparison")

    report, diff = audit.run(args, getter=forbidden)
    checks = {r["check"]: r["status"] for r in report["results"]}
    assert checks["configured_forms_against_v3_9_2"] == "FAIL"
    assert checks["imported_vocabulary_values"] == "FAIL"
    assert checks["candidate_configured_forms"] == "PASS"
    assert checks["candidate_active_membership"] == "UNKNOWN"
    assert diff["candidate_comparison"]["runtime_enabled"] is False
    assert cpath.read_bytes() == original_candidate
    assert epath.read_bytes() == original_observed


@pytest.mark.parametrize(
    "section,key",
    [
        ("writePolicy", "autoWrite"),
        ("governance", "dspaceWriteEnabled"),
        ("governance", "automaticPromotion"),
        ("governance", "newBindingAutomaticInferenceEnabled"),
    ],
)
def test_unsafe_candidate_governance_is_rejected(candidate_and_evidence, section, key):
    candidate, _, cpath, _, save = candidate_and_evidence
    candidate[section][key] = True
    save()
    with pytest.raises(ValueError, match="UNSAFE_CANDIDATE_GOVERNANCE"):
        audit.load_candidate(cpath)


def test_duplicate_binding_identity_is_rejected(candidate_and_evidence):
    candidate, _, cpath, _, save = candidate_and_evidence
    candidate["fields"][1]["bindingKey"] = candidate["fields"][0]["bindingKey"]
    save()
    with pytest.raises(ValueError, match="DUPLICATE_OR_INVALID"):
        audit.load_candidate(cpath)


def test_original_literal_metadata_key_cannot_be_renamed(candidate_and_evidence):
    candidate, _, cpath, _, save = candidate_and_evidence
    field = next(f for f in candidate["fields"] if f["metadataField"] == "dc.subject.linguiscgroup")
    field["metadataField"] = "dc.subject.linguisticGroup"
    save()
    with pytest.raises(ValueError):
        audit.load_candidate(cpath)


def test_unknown_reference_tree_cannot_be_declared_empty(candidate_and_evidence):
    candidate, _, cpath, _, save = candidate_and_evidence
    candidate["vocabularies"]["srsc"]["values"] = []
    save()
    with pytest.raises(ValueError, match="MUST_STAY_UNKNOWN"):
        audit.load_candidate(cpath)


def test_registry_id_drift_is_fail_even_with_active_sections_204(candidate_and_evidence):
    _, evidence, cpath, epath, save = candidate_and_evidence
    for page in evidence["pages_by_surface"]["metadata_fields_by_schema:dc"]:
        page["_embedded"]["metadatafields"][0]["id"] = 99999
    save()
    result = audit.compare_candidate(cpath, epath)
    assert result["registry"]["status"] == "FAIL"
    assert result["active_membership"]["status"] == "UNKNOWN"


def test_literal_vocabulary_drift_is_not_normalized(candidate_and_evidence):
    _, evidence, cpath, epath, save = candidate_and_evidence
    pages = evidence["vocabulary_evidence"]["common_types"]["pages"]
    pages[0]["_embedded"]["entries"][-3]["value"] = "Codice"
    save()
    result = audit.compare_candidate(cpath, epath)
    entry = next(v for v in result["vocabularies"]["results"] if v["vocabulary"] == "common_types")
    assert entry["status"] == "FAIL"


def test_shared_metadata_controls_are_not_collapsed(candidate_and_evidence):
    _, evidence, cpath, epath, save = candidate_and_evidence
    forms = evidence["pages_by_surface"]["submission_forms"][0]["_embedded"]["submissionforms"]
    for form in forms:
        removed = False
        for row in form["rows"]:
            for field in row["fields"]:
                options = field["selectableMetadata"]
                match = next((o for o in options if o["metadata"] == "dc.format.medium"), None)
                if match:
                    options.remove(match)
                    removed = True
                    break
            if removed:
                break
        if removed:
            break
    save()
    check = audit.compare_candidate(cpath, epath)["configured_forms"]
    assert check["status"] == "FAIL"
    assert check["bindings"] == 56
    assert check["unique_keys"] == 55


def test_cli_rejects_candidate_without_observed_evidence(tmp_path):
    with pytest.raises(SystemExit) as caught:
        audit.main(["--offline", "--candidate", str(tmp_path / "candidate.json")])
    assert caught.value.code == 2
