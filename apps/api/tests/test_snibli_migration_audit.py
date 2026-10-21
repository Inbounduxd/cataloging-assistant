import importlib.util
import io
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError

import pytest

from .test_dspace_contract_snapshot import _pages

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "snibli_audit", ROOT / "scripts/audit_snibli_migration.py"
)
audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)


class Response(io.BytesIO):
    def __init__(self, body=b"{}", status=200, headers=None):
        super().__init__(body)
        self.status = status
        self.headers = headers or {"Content-Type": "application/hal+json"}


class Opener:
    def __init__(self, *responses):
        self.responses = iter(responses)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append(request)
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


def test_valid_hal_preserves_raw_and_only_gets():
    payload = {"_links": {"self": {"href": "https://example.org/api"}}, "dspaceVersion": "7.6.6"}
    opener = Opener(Response(json.dumps(payload).encode()))
    response = audit.get_public("https://example.org/api", 1, opener=opener)
    assert audit.inspect_hal(response) == ("PASS", "HAL_RESPONSE_OBSERVED", payload)
    assert response["body"] == json.dumps(payload).encode()
    assert opener.requests[0].get_method() == "GET"
    assert not opener.requests[0].has_header("Authorization")
    assert not opener.requests[0].has_header("Cookie")


def test_html_200_is_not_an_api():
    response = {"http_status": 200, "content_type": "text/html", "body": b"<html>SNIBLI</html>"}
    assert audit.inspect_hal(response)[:2] == ("FAIL", "EXPECTED_HAL_CONTENT_TYPE")


def test_timeout_is_unknown_and_partial_local_results_survive():
    def timeout(url, seconds):
        return audit.get_public(url, seconds, opener=Opener(TimeoutError()))

    args = SimpleNamespace(
        public_url=audit.PUBLIC,
        api_base=None,
        timeout=1,
        offline=False,
        baseline=None,
        observed=None,
    )
    report, diff = audit.run(args, getter=timeout)
    results = {r["check"]: r for r in report["results"]}
    assert results["public_url"]["status"] == "UNKNOWN"
    assert results["public_url"]["detail"] == "TIMEOUT"
    assert results["release_v3.9.2_integrity"]["status"] == "PASS"
    assert results["api_hal"]["status"] == "NOT_TESTED"
    assert diff is None


@pytest.mark.parametrize(
    "target",
    [
        "http://example.org/api",
        "https://evil.org/api",
        "https://user:password@example.org/api",
        "file:///etc/passwd",
    ],
)
def test_unsafe_redirect_never_contacted(target):
    opener = Opener(
        HTTPError("https://example.org/api", 302, "Found", {"Location": target}, io.BytesIO())
    )
    with pytest.raises(audit.ProbeError, match="UNSAFE_REDIRECT"):
        audit.get_public("https://example.org/api", 1, opener=opener)
    assert len(opener.requests) == 1


def test_same_origin_redirect_is_recorded():
    opener = Opener(Response(status=302, headers={"Location": "/next"}), Response())
    response = audit.get_public("https://example.org/api", 1, opener=opener)
    assert response["endpoint"] == "https://example.org/next"
    assert len(response["redirects"]) == 2


def test_redirect_limit():
    opener = Opener(*(Response(status=302, headers={"Location": "/loop"}) for _ in range(4)))
    with pytest.raises(audit.ProbeError, match="REDIRECT_LIMIT"):
        audit.get_public("https://example.org/api", 1, opener=opener)


def export(tmp_path, name, pages):
    path = tmp_path / name
    path.write_text(json.dumps({"pages_by_surface": pages}), encoding="utf-8")
    return path


def test_real_drift_uses_vertical_022(tmp_path):
    old = export(tmp_path, "old.json", _pages(required=False))
    new = export(tmp_path, "new.json", _pages(required=True))
    diff = audit.compare_evidence(old, new)
    assert diff["complete"]
    assert any(c["change_type"] == "REQUIRED_CHANGED" for c in diff["changes"])
    assert diff["baseline_semantic_hash"] != diff["observed_semantic_hash"]


def test_204_is_unobservable_never_empty_active_contract(tmp_path):
    response = {"http_status": 204, "body": b"", "content_type": ""}
    assert audit.inspect_hal(response)[:2] == ("UNKNOWN", "UNOBSERVABLE_SURFACE_HTTP_204")
    old = export(tmp_path, "old.json", _pages())
    pages = _pages()
    pages.pop("active_submission_sections")
    new = export(tmp_path, "new.json", pages)
    diff = audit.compare_evidence(old, new)
    assert not diff["complete"]
    assert diff["warnings"]
    assert not any(
        c["change_type"].endswith("REMOVED") or c["change_type"] == "FORM_STRUCTURE_CHANGED"
        for c in diff["changes"]
    )


def test_offline_never_calls_network_and_removes_stale_diff(tmp_path):
    def forbidden(*args):
        raise AssertionError("Network used in offline mode")

    args = SimpleNamespace(
        public_url=audit.PUBLIC,
        api_base="https://example.org/api",
        timeout=1,
        offline=True,
        baseline=None,
        observed=None,
    )
    report, diff = audit.run(args, getter=forbidden)
    (tmp_path / "diff.json").write_text("stale", encoding="utf-8")
    audit.write_reports(tmp_path, report, diff)
    assert not (tmp_path / "diff.json").exists()
    assert report["endpoints"] == []
    assert (tmp_path / "audit.md").is_file()


@pytest.mark.parametrize(
    "url",
    [
        "https://user:secret@example.org",
        "https://example.org?a=secret",
        "ftp://example.org",
        "https://example.org/#token",
    ],
)
def test_sensitive_or_invalid_urls_rejected(url):
    with pytest.raises(ValueError):
        audit.validate_url(url)


def test_release_hash_failure(tmp_path, monkeypatch):
    folder = tmp_path / "skills/dspace-cataloger/versions/v3.9.2"
    folder.mkdir(parents=True)
    (folder / "manifest.json").write_text(json.dumps({"partsInReconstructionOrder": ["part"]}))
    (folder / "part").write_text("dGFtcGVyZWQ=")
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="RELEASE_HASH_OR_SIZE_MISMATCH"):
        audit.release_check()


def test_204_evidence_preserves_historical_warning(tmp_path):
    pages = _pages()
    pages.pop("active_submission_sections")
    path = tmp_path / "204.json"
    path.write_text(
        json.dumps(
            {
                "pages_by_surface": pages,
                "http_observations": [
                    {"surface": "active_submission_sections", "http_status": 204}
                ],
            }
        )
    )
    _, snapshot, _ = audit.load_evidence(path)
    assert "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204" in snapshot.warnings
    assert not snapshot.complete


def test_collector_native_204_marker_is_preserved(tmp_path):
    pages = _pages()
    pages["active_submission_sections"] = [
        {
            "_observation": {"observable": False, "statusCode": 204, "reason": "no_content"},
            "page": {"number": 0, "totalPages": 0, "totalElements": 0},
        }
    ]
    path = export(tmp_path, "native204.json", pages)
    _, snapshot, _ = audit.load_evidence(path)
    assert not snapshot.complete
    assert "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204" in snapshot.warnings


def test_vocabulary_values_are_literal_and_partial_trees_stay_unknown():
    reference = audit.skill_asset("controlled-vocabulary-index.json")
    name = next(
        n for n, value in reference.items() if value.get("values") and not value.get("error")
    )
    values = reference[name]["values"]
    payload = {
        "_embedded": {"entries": [{"value": v} for v in values]},
        "page": {"number": 0, "totalPages": 1, "totalElements": len(values)},
    }
    evidence = {"vocabulary_evidence": {name: {"hierarchical": False, "pages": [payload]}}}

    def check():
        return next(
            r for r in audit.vocabulary_check(evidence)["results"] if r["vocabulary"] == name
        )

    assert check()["status"] == "PASS"
    payload["_embedded"]["entries"][0]["value"] += " "
    assert check()["status"] == "FAIL"
    evidence["vocabulary_evidence"][name]["hierarchical"] = True
    assert check()["status"] == "UNKNOWN"


def test_missing_vocabulary_page_cannot_pass():
    reference = audit.skill_asset("controlled-vocabulary-index.json")
    name = next(iter(reference))
    evidence = {
        "vocabulary_evidence": {
            name: {
                "hierarchical": False,
                "pages": [
                    {
                        "_embedded": {"entries": []},
                        "page": {"number": 1, "totalPages": 2, "totalElements": 0},
                    }
                ],
            }
        }
    }
    assert audit.vocabulary_check(evidence)["status"] == "UNKNOWN"


def test_incomplete_baseline_cannot_prove_new_bindings(tmp_path):
    pages = _pages()
    pages.pop("active_submission_sections")
    old = export(tmp_path, "old.json", pages)
    new = export(tmp_path, "new.json", _pages())
    diff = audit.compare_evidence(old, new)
    assert not diff["complete"]
    assert not any(c["change_type"].endswith("ADDED") for c in diff["changes"])
    assert diff["raw_evidence"]["baseline"]["pages_by_surface"] == pages


def test_registered_additional_binding_is_drift_not_unobservable():
    pages = _pages()
    pages["submission_forms"][0]["_embedded"]["submissionforms"].append(
        {"id": "traditionalpagetwo", "rows": []}
    )
    pages["submission_forms"][0]["page"]["totalElements"] = 2
    pages["submission_forms"][0]["_embedded"]["submissionforms"][0]["rows"].append(
        {
            "fields": [
                {
                    "label": "¿Es un texto comparativo?",
                    "mandatory": False,
                    "repeatable": False,
                    "input": {"type": "dropdown"},
                    "selectableMetadata": [
                        {
                            "metadata": "dc.type.genre",
                            "controlledVocabulary": "genrePairs",
                            "closed": True,
                        }
                    ],
                }
            ]
        }
    )
    for surface in ("metadata_fields", "metadata_fields_by_schema:dc"):
        page = pages[surface][0]
        page["_embedded"]["metadatafields"].append(
            {"id": 293, "element": "type", "qualifier": "genre", "scopeNote": "Genero del recurso"}
        )
        page["page"]["totalElements"] = 3
    check = audit.configured_form_check({"pages_by_surface": pages})
    assert check["status"] == "FAIL"
    assert "BINDING_METADATA_NOT_IN_REGISTRY:dc.type.genre" not in check["warnings"]
    assert any(b["metadata"] == "dc.type.genre" for b in check["observed"])


def test_binding_drift_stays_observable_when_registry_capture_is_missing():
    pages = _pages()
    pages["submission_forms"][0]["_embedded"]["submissionforms"].append(
        {"id": "traditionalpagetwo", "rows": []}
    )
    pages["submission_forms"][0]["_embedded"]["submissionforms"][0]["rows"][0]["fields"][0][
        "selectableMetadata"
    ][0]["metadata"] = "dc.type.genre"
    check = audit.configured_form_check({"pages_by_surface": pages})
    assert check["status"] == "FAIL"
    assert "BINDING_METADATA_NOT_IN_REGISTRY:dc.type.genre" in check["warnings"]


def test_local_approved_contract_is_not_compared_to_historical_counts():
    check = audit.local_contract_check(audit.contract_payload())
    assert check["status"] == "PASS"
    assert check["reference"] == "APPROVED_LOCAL_SNIBLI_REVISION"
    assert (check["bindings"], check["unique_metadata_keys"]) == (57, 55)
    assert check["expected_bindings"] == 57
    assert len(audit.skill_asset("dspace-form-contract-v1.json")["fields"]) == 56


@pytest.mark.parametrize(
    "dimension,value",
    [
        ("metadata_field", "dc.type.other"),
        ("repeatable", True),
        ("required", True),
        ("vocabulary_id", "common_types"),
    ],
)
def test_local_revision_still_rejects_drift(dimension, value):
    contract = deepcopy(audit.contract_payload())
    field = next(f for f in contract["fields"] if f["metadata_field"] == "dc.type.genre")
    field[dimension] = value
    assert audit.local_contract_check(contract)["status"] == "FAIL"


def test_local_contract_reference_failure_remains_partial(monkeypatch):
    def missing(_name):
        raise FileNotFoundError()

    monkeypatch.setattr(audit, "skill_asset", missing)
    check = audit.local_contract_check(audit.contract_payload())
    assert check["status"] == "UNKNOWN"
    assert check["reason"] == "PRESERVED_REFERENCE_UNAVAILABLE"
