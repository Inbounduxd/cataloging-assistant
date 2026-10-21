#!/usr/bin/env python3
"""Read-only public probes and offline VERTICAL-022 evidence review (Python 3.11+)."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
import multiprocessing
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api/src"))
from cataloging_api.cataloging_contract import contract_payload  # noqa: E402
from cataloging_api.dspace.contract_snapshot import (  # noqa: E402
    _canonical_bindings,
    _surface_items,
    build_contract_snapshot,
    diff_contract_snapshots,
)

PUBLIC = "https://www.iifl.unam.mx/SNIBLI/home"
PILOT = "e9a8f44f-a8d3-4d22-b02a-cf590285bac6"
RELEASE_HASH = "b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede"
MAX_BYTES = 4 * 1024 * 1024


def validate_url(url):
    p = urllib.parse.urlsplit(url)
    if (
        p.scheme not in {"http", "https"}
        or not p.hostname
        or p.username
        or p.password
        or p.query
        or p.fragment
    ):
        raise ValueError("URL must be HTTP(S), without credentials, query or fragment")
    _ = p.port
    return url.rstrip("/")


def origin(url):
    p = urllib.parse.urlsplit(url)
    return p.scheme, p.hostname, p.port or (443 if p.scheme == "https" else 80)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ProbeError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def get_public(url, timeout, *, opener=None):
    """No cookies, credentials, netrc or environment proxies; bounded same-origin GET."""
    validate_url(url)
    opener = opener or urllib.request.build_opener(
        urllib.request.ProxyHandler({}), NoRedirect()
    )
    deadline = time.monotonic() + timeout
    initial = origin(url)
    chain = []
    for _ in range(4):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProbeError("TIMEOUT")
        request = urllib.request.Request(
            url, headers={"Accept": "application/hal+json"}
        )
        try:
            response = opener.open(request, timeout=remaining)
        except urllib.error.HTTPError as exc:
            response = exc
        except TimeoutError:
            raise ProbeError("TIMEOUT") from None
        except urllib.error.URLError as exc:
            raise ProbeError(
                "TIMEOUT" if isinstance(exc.reason, TimeoutError) else "NETWORK_ERROR"
            ) from None
        with response:
            status = response.status
            chain.append({"url": url, "status": status})
            if status in {301, 302, 303, 307, 308}:
                target = urllib.parse.urljoin(url, response.headers.get("Location", ""))
                try:
                    validate_url(target)
                except ValueError:
                    raise ProbeError("UNSAFE_REDIRECT") from None
                if origin(target) != initial:
                    raise ProbeError("UNSAFE_REDIRECT")
                url = target
                continue
            # Read chunks so a slow stream cannot reset the full execution budget.
            content = bytearray()
            while True:
                if time.monotonic() >= deadline:
                    raise ProbeError("TIMEOUT")
                try:
                    chunk = response.read(65536)
                except TimeoutError:
                    raise ProbeError("TIMEOUT") from None
                if not chunk:
                    break
                content.extend(chunk)
                if len(content) > MAX_BYTES:
                    raise ProbeError("RESPONSE_TOO_LARGE")
            return {
                "endpoint": url,
                "redirects": chain,
                "http_status": status,
                "content_type": response.headers.get("Content-Type", ""),
                "body": bytes(content),
            }
    raise ProbeError("REDIRECT_LIMIT")


def inspect_hal(response):
    status = response["http_status"]
    if status == 204:
        return "UNKNOWN", "UNOBSERVABLE_SURFACE_HTTP_204", None
    if status in {401, 403}:
        return "UNKNOWN", "AUTHORIZATION_REQUIRED", None
    if status != 200:
        return "FAIL", f"HTTP_{status}", None
    if response["content_type"].split(";")[0].lower() != "application/hal+json":
        return "FAIL", "EXPECTED_HAL_CONTENT_TYPE", None
    try:
        payload = json.loads(response["body"])
    except (ValueError, UnicodeError):
        return "FAIL", "INVALID_JSON", None
    if not isinstance(payload, dict) or not isinstance(payload.get("_links"), dict):
        return "FAIL", "INVALID_HAL_STRUCTURE", None
    return "PASS", "HAL_RESPONSE_OBSERVED", payload


def _probe_worker(connection, url, timeout):
    try:
        connection.send((True, get_public(url, timeout)))
    except ProbeError as exc:
        connection.send((False, exc.code))
    except Exception:
        connection.send((False, "NETWORK_ERROR"))
    finally:
        connection.close()


def bounded_get_public(url, timeout):
    """Enforce wall-clock budget including DNS/TLS and slow response streams."""
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(
        target=_probe_worker, args=(sender, url, timeout), daemon=True
    )
    try:
        process.start()
        sender.close()
        if not receiver.poll(timeout):
            raise ProbeError("TIMEOUT")
        try:
            success, value = receiver.recv()
        except EOFError:
            raise ProbeError("NETWORK_ERROR") from None
        if not success:
            raise ProbeError(value)
        return value
    finally:
        receiver.close()
        sender.close()
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
            process.join(timeout=1)


def release_archive():
    folder = ROOT / "skills/dspace-cataloger/versions/v3.9.2"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    encoded = "".join(
        (folder / name).read_text(encoding="ascii")
        for name in manifest["partsInReconstructionOrder"]
    )
    blob = base64.b64decode("".join(encoded.split()), validate=True)
    digest = hashlib.sha256(blob).hexdigest()
    if digest != RELEASE_HASH or len(blob) != 118470:
        raise ValueError("RELEASE_HASH_OR_SIZE_MISMATCH")
    return blob, digest


def skill_asset(name):
    blob, _ = release_archive()
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        return json.loads(archive.read("dspace-cataloger/assets/" + name))


def release_check():
    blob, digest = release_archive()
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        if archive.testzip():
            raise ValueError("RELEASE_ZIP_CRC_FAILURE")
        files = [n for n in archive.namelist() if not n.endswith("/")]
        json_files = [n for n in files if n.endswith(".json")]
        for name in json_files:
            json.loads(archive.read(name))
        if len(files) != 86 or len(json_files) != 36:
            raise ValueError("RELEASE_FILE_COUNTS_MISMATCH")
    return {
        "sha256": digest,
        "bytes": len(blob),
        "files": len(files),
        "json_files": len(json_files),
    }


def configured_form_check(evidence, contract=None):
    """Compare configured controls, explicitly independent of active membership."""
    pages = evidence["pages_by_surface"]
    preserved_reference = contract is None
    contract = (
        contract
        if contract is not None
        else skill_asset("dspace-form-contract-v1.json")
    )
    expected = contract["fields"]
    warnings = []
    forms = _surface_items("submission_forms", pages.get("submission_forms", []))
    registry = {
        field["metadata"]
        for field in build_contract_snapshot(pages).canonical["fields"]
    }
    actual = _canonical_bindings(
        forms,
        [f["id"] for f in contract["forms"]],
        registry or {f["metadataField"] for f in expected},
        warnings,
    )

    def normalize_expected(f):
        return {
            "form": f["formId"],
            "metadata": f["metadataField"],
            "position": [
                f["formOrder"] - 1,
                f["row"],
                f["fieldIndex"],
                f["metadataIndex"],
            ],
            "label": f["uiLabel"],
            "required": f["required"],
            "repeatable": f["repeatable"],
            "inputType": f["inputType"],
            "controlledVocabulary": f["controlledVocabulary"],
            "closed": bool(f["closedVocabulary"]),
        }

    reference = [normalize_expected(f) for f in expected]
    observed = [
        {key: (bool(f[key]) if key == "closed" else f[key]) for key in reference[0]}
        for f in actual
    ]

    def order(f):
        return f["position"]

    matches = sorted(reference, key=order) == sorted(observed, key=order)
    present = {f["id"] for f in forms}
    missing = {f["id"] for f in contract["forms"]} - present
    unobservable = missing or any(
        w.startswith("UNRESOLVED_FORM_ROWS:") for w in warnings
    )
    result = {
        "status": "UNKNOWN" if unobservable else ("PASS" if matches else "FAIL"),
        "bindings": len(actual),
        "unique_keys": len({f["metadata"] for f in actual}),
        "matches_reference": matches,
        "warnings": warnings,
        "expected": sorted(reference, key=order),
        "observed": sorted(observed, key=order),
        "scope": "Configured forms only; does not establish active collection membership",
    }
    if preserved_reference:
        result["matches_release_v3_9_2"] = matches
    return result


def vocabulary_check(evidence, reference=None):
    """Review supplied raw entry pages; hierarchical top-only pages are incomplete."""
    preserved_reference = reference is None
    reference = (
        reference
        if reference is not None
        else skill_asset("controlled-vocabulary-index.json")
    )
    supplied = evidence.get("vocabulary_evidence", {})
    results = []
    for name, expected in reference.items():
        entry = supplied.get(name) if isinstance(supplied, dict) else None
        status, detail = "UNKNOWN", "No complete raw vocabulary evidence"
        if isinstance(entry, dict) and entry.get("hierarchical") is False:
            pages = entry.get("pages", [])
            try:
                ordered = sorted(pages, key=lambda p: p["page"]["number"])
                total = ordered[0]["page"]["totalPages"]
                values = [
                    v["value"] for page in ordered for v in page["_embedded"]["entries"]
                ]
                valid = (
                    type(total) is int
                    and total >= 1
                    and [p["page"]["number"] for p in ordered] == list(range(total))
                    and all(
                        p["page"]["totalPages"] == total
                        and p["page"]["totalElements"] == len(values)
                        for p in ordered
                    )
                    and all(isinstance(v, str) for v in values)
                )
                if valid and expected.get("error") is None:
                    status = "PASS" if values == expected["values"] else "FAIL"
                    detail = {
                        "observed_values": values,
                        "expected_values": expected["values"],
                    }
            except (KeyError, IndexError, TypeError):
                pass
        results.append({"vocabulary": name, "status": status, "detail": detail})
    status = (
        "FAIL"
        if any(r["status"] == "FAIL" for r in results)
        else (
            "PASS"
            if results and all(r["status"] == "PASS" for r in results)
            else "UNKNOWN"
        )
    )
    return {
        "status": status,
        "results": results,
        "scope": (
            "Literal values against preserved release; no normalization or fuzzy match"
            if preserved_reference
            else "Literal values against explicit candidate; no normalization"
        ),
    }


def load_candidate(path):
    """Validate a review-only reference; its flags can never enable runtime writes."""
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("CANDIDATE_TOO_LARGE")
    raw = path.read_bytes()
    candidate = json.loads(raw)
    if not isinstance(candidate, dict):
        raise ValueError("INVALID_CANDIDATE")
    if (
        candidate.get("status") != "CANDIDATE_REVIEW_REQUIRED"
        or candidate.get("adopted") is not False
        or candidate.get("runtimeEnabled") is not False
    ):
        raise ValueError("CANDIDATE_MUST_REMAIN_REVIEW_ONLY")
    policy = candidate.get("writePolicy", {})
    governance = candidate.get("governance", {})
    if not isinstance(policy, dict) or not isinstance(governance, dict):
        raise ValueError("INVALID_CANDIDATE_GOVERNANCE")
    if (
        policy.get("autoWrite") is not False
        or policy.get("humanApprovalRequired") is not True
        or policy.get("preserveUnknowns") is not True
        or governance.get("humanApprovalRequired") is not True
        or governance.get("automaticPromotion") is not False
        or governance.get("dspaceWriteEnabled") is not False
        or governance.get("newBindingAutomaticInferenceEnabled") is not False
        or governance.get("newVocabularyAutomaticClassificationEnabled") is not False
    ):
        raise ValueError("UNSAFE_CANDIDATE_GOVERNANCE")
    if (
        not isinstance(candidate.get("reference"), dict)
        or candidate["reference"].get("sha256") != RELEASE_HASH
    ):
        raise ValueError("CANDIDATE_REFERENCE_RELEASE_MISMATCH")
    preserved = skill_asset("dspace-form-contract-v1.json")
    if candidate.get("forms") != preserved["forms"]:
        raise ValueError("CANDIDATE_FORM_IDENTITY_MISMATCH")
    fields = candidate.get("fields")
    if (
        not isinstance(fields, list)
        or not fields
        or not all(isinstance(f, dict) for f in fields)
    ):
        raise ValueError("INVALID_CANDIDATE_FIELDS")
    required = {
        "formId",
        "formOrder",
        "row",
        "fieldIndex",
        "metadataIndex",
        "metadataField",
        "uiLabel",
        "inputType",
        "required",
        "repeatable",
        "controlledVocabulary",
        "closedVocabulary",
        "bindingKey",
        "observedBindingId",
        "renderOrder",
    }
    form_order = {f["id"]: f["order"] for f in preserved["forms"]}
    positions, identities = set(), set()
    for field in fields:
        if not required <= field.keys():
            raise ValueError("CANDIDATE_FIELD_DIMENSIONS_MISSING")
        if any(
            type(field[k]) is not int or field[k] < 0
            for k in ("formOrder", "row", "fieldIndex", "metadataIndex", "renderOrder")
        ):
            raise ValueError("INVALID_CANDIDATE_POSITION")
        if (
            field["formId"] not in form_order
            or field["formOrder"] != form_order[field["formId"]]
        ):
            raise ValueError("INVALID_CANDIDATE_FORM")
        if any(
            not isinstance(field[k], str) or not field[k]
            for k in (
                "metadataField",
                "uiLabel",
                "inputType",
                "bindingKey",
                "observedBindingId",
            )
        ):
            raise ValueError("INVALID_CANDIDATE_FIELD")
        if any(
            type(field[k]) is not bool
            for k in ("required", "repeatable", "closedVocabulary")
        ):
            raise ValueError("INVALID_CANDIDATE_FLAGS")
        if field["controlledVocabulary"] is not None and not isinstance(
            field["controlledVocabulary"], str
        ):
            raise ValueError("INVALID_CANDIDATE_VOCABULARY")
        position = tuple(
            field[k] for k in ("formOrder", "row", "fieldIndex", "metadataIndex")
        )
        expected_id = f"{field['formId']}:r{field['row']}:f{field['fieldIndex']}:m{field['metadataIndex']}"
        if (
            position in positions
            or field["bindingKey"] in identities
            or field["observedBindingId"] != expected_id
        ):
            raise ValueError("DUPLICATE_OR_INVALID_CANDIDATE_BINDING")
        positions.add(position)
        identities.add(field["bindingKey"])

    def identity_set(values, *, candidate_fields):
        occurrences = {}
        result = set()
        ordered = sorted(
            values,
            key=lambda f: tuple(
                f[k] for k in ("formOrder", "row", "fieldIndex", "metadataIndex")
            ),
        )
        for index, field in enumerate(ordered, 1):
            pair = field["formId"], field["metadataField"]
            occurrence = occurrences.get(pair, 0)
            occurrences[pair] = occurrence + 1
            key = f"{pair[0]}:{pair[1]}:{occurrence}"
            if candidate_fields and (
                field["bindingKey"] != key or field["renderOrder"] != index
            ):
                raise ValueError("INVALID_CANDIDATE_BINDING_ORDER")
            result.add(key)
        return result

    preserved_ids = identity_set(preserved["fields"], candidate_fields=False)
    current_ids = identity_set(fields, candidate_fields=True)
    keys = {f["metadataField"] for f in fields}
    if not preserved_ids <= current_ids or "dc.subject.linguiscgroup" not in keys:
        raise ValueError("ORIGINAL_BINDINGS_OR_LITERAL_KEY_NOT_PRESERVED")
    counts = candidate.get("counts", {})
    if not isinstance(counts, dict) or not isinstance(
        candidate.get("collection"), dict
    ):
        raise ValueError("INVALID_CANDIDATE_COUNTS_OR_COLLECTION")
    if (
        counts.get("bindings") != len(fields)
        or counts.get("uniqueMetadataKeys") != len(keys)
        or counts.get("referenceBindingsRetained") != len(preserved_ids)
        or counts.get("additionalBindings") != len(current_ids - preserved_ids)
    ):
        raise ValueError("CANDIDATE_COUNTS_MISMATCH")
    registry = candidate.get("metadataRegistryForCandidate")
    if not isinstance(registry, dict) or set(registry) != keys:
        raise ValueError("CANDIDATE_REGISTRY_MISMATCH")
    for key, field in registry.items():
        if (
            not isinstance(field, dict)
            or field.get("metadata") != key
            or type(field.get("id")) is not int
            or field.get("scopeNote") is not None
            and not isinstance(field.get("scopeNote"), str)
        ):
            raise ValueError("INVALID_CANDIDATE_REGISTRY_FIELD")
    vocabularies = candidate.get("vocabularies")
    if not isinstance(vocabularies, dict):
        raise ValueError("INVALID_CANDIDATE_VOCABULARIES")
    referenced = {
        f["controlledVocabulary"] for f in fields if f["controlledVocabulary"]
    }
    if not referenced <= vocabularies.keys():
        raise ValueError("CANDIDATE_VOCABULARY_MISSING")
    for entry in vocabularies.values():
        if not isinstance(entry, dict) or entry.get("status") not in {
            "UNKNOWN",
            "OBSERVED_NOT_APPROVED",
        }:
            raise ValueError("INVALID_CANDIDATE_VOCABULARY_STATUS")
        values = entry.get("values")
        if entry["status"] == "UNKNOWN":
            if values is not None:
                raise ValueError("UNKNOWN_CANDIDATE_VALUES_MUST_STAY_UNKNOWN")
        elif not isinstance(values, list) or not all(
            isinstance(v, str) for v in values
        ):
            raise ValueError("INVALID_CANDIDATE_LITERAL_VALUES")
    return candidate, hashlib.sha256(raw).hexdigest()


def compare_candidate(candidate_path, observed_path):
    candidate, candidate_hash = load_candidate(candidate_path)
    observed, snapshot, observed_hash = load_evidence(observed_path)
    forms = configured_form_check(observed, contract=candidate)
    reference = {
        name: {
            "values": entry["values"],
            "error": None if entry["values"] is not None else "UNOBSERVED_REFERENCE",
        }
        for name, entry in candidate["vocabularies"].items()
    }
    vocabularies = vocabulary_check(observed, reference=reference)
    registry = {f["metadata"]: f for f in snapshot.canonical["fields"]}
    mismatches = {
        key: {"expected": field, "observed": registry.get(key)}
        for key, field in candidate["metadataRegistryForCandidate"].items()
        if registry.get(key) != field
    }
    # Presence and ID/scope-note comparisons do not assert global registry coverage.
    observed_mismatch = any(key in registry for key in mismatches)
    registry_status = (
        "FAIL"
        if mismatches and (snapshot.complete or observed_mismatch)
        else ("UNKNOWN" if mismatches else "PASS")
    )
    expected_collection = candidate.get("collection", {})
    actual_uuid, actual_handle = (
        observed.get("collection_uuid"),
        observed.get("collection_handle"),
    )
    collection_status = (
        "UNKNOWN"
        if not actual_uuid or not actual_handle
        else (
            "PASS"
            if actual_uuid == expected_collection.get("uuid")
            and actual_handle == expected_collection.get("handle")
            else "FAIL"
        )
    )
    return {
        "scope": "EXPLICIT_REVIEW_ONLY_CANDIDATE",
        "candidate_file_sha256": candidate_hash,
        "observed_file_sha256": observed_hash,
        "proposal_id": candidate.get("proposalId"),
        "human_approved": False,
        "runtime_enabled": False,
        "full_migration_equivalence": "UNKNOWN",
        "configured_forms": forms,
        "vocabularies": vocabularies,
        "registry": {
            "status": registry_status,
            "compared_keys": len(candidate["metadataRegistryForCandidate"]),
            "mismatches": mismatches,
        },
        "collection": {
            "status": collection_status,
            "expected_uuid": expected_collection.get("uuid"),
            "observed_uuid": actual_uuid,
            "observed_handle": actual_handle,
        },
        "active_membership": {
            "status": "PASS" if snapshot.complete else "UNKNOWN",
            "warnings": list(snapshot.warnings),
        },
        "candidate": candidate,
        "raw_observed_evidence": observed,
    }


def load_evidence(path):
    """Require raw VERTICAL-022 surface pages, never trust a supplied complete flag."""
    raw = path.read_bytes()
    if len(raw) > 32 * MAX_BYTES:
        raise ValueError("EVIDENCE_TOO_LARGE")
    data = json.loads(raw)
    if not isinstance(data, dict) or not isinstance(data.get("pages_by_surface"), dict):
        raise ValueError("Expected pages_by_surface from VERTICAL-022 raw export")
    for pages in data["pages_by_surface"].values():
        if not isinstance(pages, list) or not all(isinstance(p, dict) for p in pages):
            raise ValueError("Invalid raw surface pages")
    if data.get("source_base_url"):
        validate_url(data["source_base_url"])
    snapshot = build_contract_snapshot(data["pages_by_surface"])
    active_pages = data["pages_by_surface"].get("active_submission_sections", [])
    if any(not isinstance(p.get("_observation", {}), dict) for p in active_pages):
        raise ValueError("Invalid HTTP observation")
    observations = data.get("http_observations", [])
    if not isinstance(observations, list) or not all(
        isinstance(o, dict) for o in observations
    ):
        raise ValueError("Invalid HTTP observations")
    raw_204 = any(
        p.get("_observation", {}).get("statusCode") == 204 for p in active_pages
    )
    if raw_204:
        snapshot = replace(
            snapshot,
            complete=False,
            warnings=tuple(
                sorted(
                    set(
                        snapshot.warnings
                        + ("ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204",)
                    )
                )
            ),
        )
    for observation in observations:
        if (
            observation.get("surface") == "active_submission_sections"
            and observation.get("http_status") == 204
        ):
            if data["pages_by_surface"].get("active_submission_sections"):
                raise ValueError("Conflicting HTTP 204 and active section pages")
            snapshot = replace(
                snapshot,
                complete=False,
                warnings=tuple(
                    sorted(
                        set(
                            snapshot.warnings
                            + ("ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204",)
                        )
                    )
                ),
            )
    return data, snapshot, hashlib.sha256(raw).hexdigest()


def compare_evidence(baseline_path, observed_path):
    baseline, old, old_hash = load_evidence(baseline_path)
    observed, new, new_hash = load_evidence(observed_path)
    changes = [asdict(c) for c in diff_contract_snapshots(old, new)]
    # VERTICAL-022 emits section changes even on incomplete snapshots. Retain
    # evidence but suppress absence-derived destruction on unobservable surfaces.
    if not new.complete or not old.complete:
        changes = [
            c
            for c in changes
            if c["change_type"]
            not in {
                "SCHEMA_REMOVED",
                "FIELD_REMOVED",
                "BINDING_REMOVED",
                "FORM_STRUCTURE_CHANGED",
            }
        ]
    if not old.complete:
        changes = [
            c
            for c in changes
            if c["change_type"] not in {"SCHEMA_ADDED", "FIELD_ADDED", "BINDING_ADDED"}
        ]
    form_check = configured_form_check(observed)
    return {
        "baseline_file_sha256": old_hash,
        "observed_file_sha256": new_hash,
        "baseline_semantic_hash": old.semantic_hash,
        "observed_semantic_hash": new.semantic_hash,
        "complete": old.complete and new.complete,
        "baseline_warnings": list(old.warnings),
        "warnings": list(new.warnings),
        "changes": changes,
        "canonical": new.canonical,
        "configured_forms": form_check,
        "vocabularies": vocabulary_check(observed),
        "raw_evidence": {"baseline": baseline, "observed": observed},
        "source": {
            key: observed.get(key)
            for key in (
                "source_base_url",
                "captured_at",
                "collection_uuid",
                "collection_handle",
            )
        },
    }


def local_contract_check(contract):
    """Check the declared local revision; do not equate it with the preserved skill."""
    fields = contract["fields"]
    keys = {f["metadata_field"] for f in fields}
    approved = contract["contract_version"] == "snibli-contract-2026-10-21"
    try:
        expected = list(skill_asset("dspace-form-contract-v1.json")["fields"])
    except (OSError, ValueError, KeyError, zipfile.BadZipFile):
        return {
            "status": "UNKNOWN",
            "bindings": len(fields),
            "unique_metadata_keys": len(keys),
            "contract_version": contract["contract_version"],
            "reason": "PRESERVED_REFERENCE_UNAVAILABLE",
        }
    if approved:
        expected.insert(
            15,
            {
                "metadataField": "dc.type.genre",
                "required": False,
                "repeatable": False,
                "controlledVocabulary": "genrePairs",
            },
        )
    dimensions = ("metadata_field", "required", "repeatable", "vocabulary_id")
    reference_dimensions = (
        "metadataField",
        "required",
        "repeatable",
        "controlledVocabulary",
    )
    matches = [tuple(f[k] for k in dimensions) for f in fields] == [
        tuple(f[k] for k in reference_dimensions) for f in expected
    ]
    return {
        "status": "PASS" if matches and "dc.subject.linguiscgroup" in keys else "FAIL",
        "bindings": len(fields),
        "unique_metadata_keys": len(keys),
        "contract_version": contract["contract_version"],
        "reference": "APPROVED_LOCAL_SNIBLI_REVISION"
        if approved
        else "PRESERVED_V3_9_2",
        "expected_bindings": len(expected),
        "expected_unique_metadata_keys": len({f["metadataField"] for f in expected}),
        "scope": "Local mapping only; does not certify the live instance or skill adoption",
    }


def run(args, *, getter=bounded_get_public):
    candidate_path = getattr(args, "candidate", None)
    report = {
        "captured_at": datetime.now(UTC).isoformat(),
        "configuration": {
            "public_url": args.public_url,
            "api_base": args.api_base,
            "timeout": args.timeout,
            "offline": args.offline,
            "credentials_used": False,
            "max_response_bytes": MAX_BYTES,
            "max_requests_per_endpoint": 4,
            "baseline_supplied": args.baseline is not None,
            "observed_supplied": args.observed is not None,
            "candidate_supplied": candidate_path is not None,
        },
        "coverage": "LOCAL_ONLY" if args.offline else "LOCAL_AND_PUBLIC_PARTIAL",
        "results": [],
        "endpoints": [],
        "errors": [],
        "warnings": ["No full migration equivalence established."],
    }

    def result(name, status, detail):
        report["results"].append({"check": name, "status": status, "detail": detail})

    try:
        result("release_v3.9.2_integrity", "PASS", release_check())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        result("release_v3.9.2_integrity", "FAIL", type(exc).__name__)
        report["errors"].append("Release integrity verification failed")
    contract = contract_payload()
    fields = contract["fields"]
    keys = {f["metadata_field"] for f in fields}
    runtime = contract["runtime"]
    local = local_contract_check(contract)
    result("local_master_contract", local["status"], local)
    result(
        "local_governance",
        "PASS"
        if runtime["human_approval_required"] and not runtime["dspace_write_enabled"]
        else "FAIL",
        runtime,
    )
    result(
        "local_language_separation",
        "PASS"
        if runtime["registered_language_is_independent"]
        and "dc.description.registeredLanguage" in keys
        and "dc.subject.linguiscgroup" in keys
        else "FAIL",
        "Local contract only; no live semantic equivalence asserted",
    )
    report["warnings"].append(
        "Executable contract declares "
        + contract["contract_version"]
        + "; current preserved release is v3.9.2. Review version alignment separately."
    )

    targets = [("public_url", args.public_url, False)]
    if args.api_base:
        targets.extend(
            [
                ("api_hal", args.api_base, True),
                (
                    "pilot_collection",
                    args.api_base + "/core/collections/" + PILOT,
                    True,
                ),
            ]
        )
    else:
        result("api_hal", "NOT_TESTED", "API base not supplied; no route inferred")
    for name, url, hal in targets:
        if args.offline:
            result(name, "NOT_TESTED", "Offline: no HTTP request")
            continue
        try:
            response = getter(url, args.timeout)
            body = response.pop("body")
            response["body_sha256"] = hashlib.sha256(body).hexdigest()
            report["endpoints"].append(response)
            response["body"] = body
            if hal:
                status, detail, payload = inspect_hal(response)
                if payload is not None:
                    # Preserve raw HAL alongside public observation, no normalization loss.
                    response["raw_hal"] = payload
                if name == "pilot_collection" and status == "PASS":
                    status = (
                        "PASS"
                        if payload.get("uuid") == PILOT
                        and payload.get("handle") == "123456789/4"
                        else "FAIL"
                    )
                    detail = "UUID and handle comparison only; database identity remains UNKNOWN"
            else:
                status = "PASS" if response["http_status"] == 200 else "FAIL"
                detail = "Public HTTP reachability only"
            response.pop("body")
            result(name, status, detail)
        except (ProbeError, OSError) as exc:
            code = exc.code if isinstance(exc, ProbeError) else "NETWORK_ERROR"
            result(
                name,
                "FAIL" if code in {"UNSAFE_REDIRECT", "REDIRECT_LIMIT"} else "UNKNOWN",
                code,
            )
            report["errors"].append({"endpoint": url, "code": code})
    result(
        "instance_identity",
        "UNKNOWN",
        "UUID/handle alone cannot prove database identity",
    )
    diff = None
    if args.baseline and args.observed:
        try:
            diff = compare_evidence(args.baseline, args.observed)
            report["coverage"] = "OFFLINE_VERTICAL_022_EVIDENCE"
            drift = any(
                c["change_type"] != "UNOBSERVABLE_SURFACE" for c in diff["changes"]
            )
            status = (
                "FAIL" if drift else ("UNKNOWN" if not diff["complete"] else "PASS")
            )
            result(
                "vertical_022_comparison",
                status,
                {
                    k: v
                    for k, v in diff.items()
                    if k
                    not in {
                        "canonical",
                        "configured_forms",
                        "vocabularies",
                        "raw_evidence",
                    }
                },
            )
            check = diff["configured_forms"]
            result(
                "configured_forms_against_v3_9_2",
                check["status"],
                {k: v for k, v in check.items() if k not in {"expected", "observed"}},
            )
            vocab = diff["vocabularies"]
            result("imported_vocabulary_values", vocab["status"], vocab)
            expected_keys = {
                f["metadataField"]
                for f in skill_asset("dspace-form-contract-v1.json")["fields"]
            }
            actual_keys = {f["metadata"] for f in diff["canonical"]["fields"]}
            missing = sorted(expected_keys - actual_keys)
            result(
                "imported_54_registry_keys",
                "PASS" if not missing else ("FAIL" if diff["complete"] else "UNKNOWN"),
                {"missing": missing},
            )
            report["warnings"].extend(diff["warnings"])
            report["warnings"].append(
                "Imported evidence is not a new authenticated capture."
            )
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result("vertical_022_comparison", "UNKNOWN", type(exc).__name__)
            report["errors"].append("Evidence could not be compared")
    else:
        result(
            "vertical_022_comparison",
            "NOT_TESTED",
            "Supply --baseline and --observed raw exports; no database job executed",
        )
    if candidate_path:
        try:
            candidate_result = compare_candidate(candidate_path, args.observed)
            observed = candidate_result["raw_observed_evidence"]
            if not args.baseline:
                released_forms = configured_form_check(observed)
                released_vocab = vocabulary_check(observed)
                result(
                    "configured_forms_against_v3_9_2",
                    released_forms["status"],
                    {
                        k: v
                        for k, v in released_forms.items()
                        if k not in {"expected", "observed"}
                    },
                )
                result(
                    "imported_vocabulary_values",
                    released_vocab["status"],
                    released_vocab,
                )
            report["coverage"] = "OFFLINE_RELEASE_AND_EXPLICIT_CANDIDATE_COMPARISON"
            result(
                "candidate_reference_format",
                "PASS",
                {
                    "sha256": candidate_result["candidate_file_sha256"],
                    "proposal_id": candidate_result["proposal_id"],
                    "human_approved": False,
                    "runtime_enabled": False,
                },
            )
            for name, key in (
                ("candidate_configured_forms", "configured_forms"),
                ("candidate_vocabulary_values", "vocabularies"),
                ("candidate_registry", "registry"),
                ("candidate_collection_identity", "collection"),
                ("candidate_active_membership", "active_membership"),
            ):
                check = candidate_result[key]
                detail = {
                    k: v for k, v in check.items() if k not in {"expected", "observed"}
                }
                result(name, check["status"], detail)
            report["warnings"].extend(candidate_result["active_membership"]["warnings"])
            report["warnings"].append(
                "Candidate matches do not grant approval, promotion or full migration equivalence."
            )
            diff = (
                diff
                if diff is not None
                else {
                    "scope": "RELEASE_AND_EXPLICIT_REVIEW_ONLY_CANDIDATE",
                    "full_migration_equivalence": "UNKNOWN",
                    "release_sha256": RELEASE_HASH,
                    "release_configured_forms": configured_form_check(observed),
                    "release_vocabularies": vocabulary_check(observed),
                }
            )
            diff["candidate_comparison"] = candidate_result
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result("candidate_reference_format", "FAIL", type(exc).__name__)
            report["errors"].append(
                "Candidate or observed evidence could not be validated"
            )
    for name in (
        "live_56_bindings_54_keys",
        "live_form_order_labels_controls",
        "live_vocabulary_values",
        "live_language_rules",
        "golden_GR01_GR23",
    ):
        result(
            name,
            "NOT_TESTED",
            "Requires dedicated contract/semantic evidence; public HAL is insufficient",
        )
    report["status_counts"] = {
        s: sum(r["status"] == s for r in report["results"])
        for s in ("PASS", "FAIL", "UNKNOWN", "NOT_TESTED")
    }
    return report, diff


def write_reports(output, report, diff):
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# SNIBLI migration audit",
        "",
        report["captured_at"],
        "",
        "Coverage: " + report["coverage"],
        "",
        "PASS applies only to the named check, never to full migration equivalence.",
        "",
    ]
    for row in report["results"]:
        lines.extend(
            [
                f"- **{row['status']}** `{row['check']}`: "
                + json.dumps(row["detail"], ensure_ascii=False)
            ]
        )
    lines.extend(["", "## Warnings", ""] + ["- " + w for w in report["warnings"]])
    lines.extend(
        [
            "",
            "## Configuration, endpoints and errors",
            "",
            "```json",
            json.dumps(
                {k: report[k] for k in ("configuration", "endpoints", "errors")},
                ensure_ascii=False,
                indent=2,
            ),
            "```",
            "",
        ]
    )
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    if diff is not None:
        (output / "diff.json").write_text(
            json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    elif (output / "diff.json").exists():
        # Never leave an earlier diff apparently associated with a partial run.
        (output / "diff.json").unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-url", default=PUBLIC)
    parser.add_argument("--api-base")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument(
        "--candidate",
        type=Path,
        help="Explicit review-only local reference; never promotes a baseline",
    )
    parser.add_argument(
        "--observed", type=Path, help="Raw VERTICAL-022 export for offline comparison"
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports/snibli-migration"
    )
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args(argv)
    try:
        args.public_url = validate_url(args.public_url)
        if args.api_base:
            args.api_base = validate_url(args.api_base)
    except ValueError:
        parser.error("URLs must use HTTP(S), without credentials, query or fragment")
    if not math.isfinite(args.timeout) or not 0 < args.timeout <= 60:
        parser.error("--timeout must be finite and in (0, 60] seconds per endpoint")
    if args.observed and not (args.baseline or args.candidate):
        parser.error("--observed requires --baseline or --candidate")
    if args.candidate and not args.observed:
        parser.error("--candidate requires --observed")
    report, diff = run(args)
    write_reports(args.output, report, diff)
    print(
        json.dumps({"coverage": report["coverage"], "counts": report["status_counts"]})
    )
    return 1 if report["status_counts"]["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
