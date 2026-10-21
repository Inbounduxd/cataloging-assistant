#!/usr/bin/env python3
"""Interactive, file-only SNIBLI configuration export. Python 3.11+, httpx 0.28."""

from __future__ import annotations

import argparse
import asyncio
import getpass
import hashlib
import json
import math
import re
import sys
import uuid
import warnings
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api/src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import httpx
except ImportError:
    raise SystemExit(
        'Install dependency: python -m pip install "httpx>=0.28,<0.29"'
    ) from None

import audit_snibli_migration as audit  # noqa: E402
from snibli_vocabulary_tree import collect_tree  # noqa: E402
from cataloging_api.dspace.authenticated_client import ReadAuthenticatedDSpaceClient  # noqa: E402
from cataloging_api.dspace.client import DSpaceError  # noqa: E402
from cataloging_api.dspace.contract_snapshot import build_contract_snapshot  # noqa: E402

API = "https://www.iifl.unam.mx/server/api"
MAX_BYTES = 4 * 1024 * 1024
NAME = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*\Z")


def api_url(value):
    p = urlsplit(value)
    if (
        p.scheme != "https"
        or p.hostname != "www.iifl.unam.mx"
        or p.port not in (None, 443)
        or p.path.rstrip("/") != "/server/api"
        or p.username
        or p.password
        or p.query
        or p.fragment
    ):
        raise ValueError("Only the verified SNIBLI HTTPS API is authorized")
    return API


def safe_name(value):
    if not isinstance(value, str) or not NAME.fullmatch(value):
        raise DSpaceError("unsafe_identifier", "Unsafe configuration identifier")
    return value


class ReadOnlyTransport(httpx.AsyncBaseTransport):
    """Final network boundary, including calls made by the existing login client."""

    def __init__(self, base, output, max_requests, *, inner=None, secrets=()):
        self.base = urlsplit(api_url(base))
        self.output = output
        self.max_requests = max_requests
        self.inner = inner or httpx.AsyncHTTPTransport(trust_env=False, retries=0)
        self.secrets = [s.encode() for s in secrets if s]
        self.events = []
        self.requests = 0
        self.login_requests = 0
        self.surface = "authentication"

    async def aclose(self):
        await self.inner.aclose()

    def check(self, request):
        url = request.url
        if (
            url.scheme != "https"
            or url.host != self.base.hostname
            or url.port not in (None, 443)
            or url.userinfo
            or url.fragment
        ):
            raise DSpaceError(
                "unauthorized_origin", "Request blocked before network access"
            )
        prefix = "/server/api"
        path = url.path
        if not path.startswith(prefix + "/"):
            raise DSpaceError("unauthorized_endpoint", "Endpoint outside export scope")
        relative = path[len(prefix) :]
        if request.method == "POST":
            if relative != "/authn/login" or url.query or self.login_requests:
                raise DSpaceError(
                    "write_blocked", "Only one exact session login is permitted"
                )
            self.login_requests += 1
        elif request.method == "GET":
            fixed = {
                "/authn/status",
                "/core/metadataschemas",
                "/core/metadatafields",
                "/core/metadatafields/search/bySchema",
                "/core/collections",
                "/config/submissiondefinitions",
                "/config/submissionforms",
                "/config/submissionsections",
                "/config/submissiondefinitions/search/findByCollection",
                "/submission/vocabularies",
                "/submission/vocabularyEntryDetails/search/top",
            }
            dynamic = (
                re.fullmatch(r"/core/collections/[0-9a-f-]{36}", relative)
                or re.fullmatch(
                    r"/config/submissiondefinitions/[A-Za-z0-9_.-]+/sections", relative
                )
                or re.fullmatch(
                    r"/submission/vocabularies/[A-Za-z0-9_.-]+/entries", relative
                )
                or re.fullmatch(
                    r"/submission/vocabularyEntryDetails/[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+/children",
                    relative,
                )
            )
            if relative not in fixed and not dynamic:
                raise DSpaceError(
                    "unauthorized_endpoint", "GET outside configuration inventory"
                )
            if set(url.params) - {"page", "size", "schema", "uuid", "vocabulary"}:
                raise DSpaceError("unauthorized_query", "Unexpected query parameter")
        else:
            raise DSpaceError("write_blocked", "DSpace mutations are prohibited")
        self.requests += 1
        if self.requests > self.max_requests:
            raise DSpaceError("request_limit", "Request budget exhausted")

    async def handle_async_request(self, request):
        self.check(request)
        async with asyncio.timeout(30):
            response = await self.inner.handle_async_request(request)
            response.request = request
            try:
                if 300 <= response.status_code < 400:
                    raise DSpaceError("redirect_blocked", "Redirects are not followed")
                chunks = []
                size = 0
                async for chunk in response.aiter_bytes():
                    size += len(chunk)
                    if size > MAX_BYTES:
                        raise DSpaceError("response_limit", "Response exceeds 4 MiB")
                    chunks.append(chunk)
                body = b"".join(chunks)
                # Tokens and cookies remain in memory and are never exported.
                authorization = response.headers.get("authorization")
                if authorization:
                    self.secrets.extend(
                        [authorization.encode(), authorization.split()[-1].encode()]
                    )
                for cookie in response.cookies.values():
                    if cookie:
                        self.secrets.extend([cookie.encode(), unquote(cookie).encode()])
                is_auth = request.url.path.startswith("/server/api/authn/")
                if not is_auth:
                    if any(secret in body for secret in self.secrets):
                        raise DSpaceError(
                            "sensitive_body",
                            "Authentication material detected; body not saved",
                        )
                    event = {
                        "surface": self.surface,
                        "endpoint": str(request.url),
                        "method": "GET",
                        "captured_at": datetime.now(UTC).isoformat(),
                        "http_status": response.status_code,
                        "content_type": response.headers.get("content-type", ""),
                        "sha256": hashlib.sha256(body).hexdigest(),
                        "bytes": size,
                    }
                    payload = None
                    if body:
                        try:
                            payload = json.loads(body)
                        except (ValueError, UnicodeError):
                            pass
                    if response.status_code == 200 and (
                        response.headers.get("content-type", "").split(";")[0].lower()
                        != "application/hal+json"
                        or not isinstance(payload, dict)
                        or not isinstance(payload.get("_links"), dict)
                    ):
                        self.events.append(event)
                        raise DSpaceError(
                            "invalid_hal", "Expected HAL object; invalid body not saved"
                        )
                    filename = f"raw/{self.requests:04}-{event['sha256']}.response"
                    with (self.output / filename).open("xb") as handle:
                        handle.write(body)
                    event["raw_file"] = filename
                    self.events.append(event)
                headers = [
                    (k, v)
                    for k, v in response.headers.multi_items()
                    if k.lower() not in {"content-encoding", "content-length"}
                ]
                return httpx.Response(
                    response.status_code, headers=headers, content=body, request=request
                )
            finally:
                await response.aclose()


class ConfigurationClient(ReadAuthenticatedDSpaceClient):
    """Additional explicit GET surfaces; no public generic HTTP method."""

    async def get_collections_page(self, *, page, size):
        return await self._get_collection_page(
            "/core/collections", "collections", page=page, size=size
        )

    async def get_vocabularies_page(self, *, page, size):
        return await self._get_collection_page(
            "/submission/vocabularies", "vocabularies", page=page, size=size
        )

    async def get_vocabulary_entries_page(self, vocabulary, *, page, size):
        name = safe_name(vocabulary)
        return await self._get_collection_page(
            f"/submission/vocabularies/{name}/entries", "entries", page=page, size=size
        )

    async def get_vocabulary_top_page(self, vocabulary, *, page, size):
        return await self._get_collection_page(
            "/submission/vocabularyEntryDetails/search/top",
            "vocabularyEntryDetails",
            page=page,
            size=size,
            extra_params={"vocabulary": safe_name(vocabulary)},
        )

    async def get_vocabulary_children_page(self, path, *, page, size):
        # The traversal validates the exact advertised origin, path and parent ID;
        # ReadOnlyTransport independently enforces the network boundary.
        return await self._get_collection_page(path, "children", page=page, size=size)


def save_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


async def export_configuration(args, username, password, *, inner=None):
    """No network is used until endpoint, directory and credentials are validated."""
    api_url(args.api_base)
    hierarchy_only = getattr(args, "hierarchy_only", None)
    public_hierarchy = getattr(args, "public_hierarchy", None)
    if not public_hierarchy and (not username or not password):
        raise ValueError("Credentials are required")
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "raw").mkdir()
    transport = ReadOnlyTransport(
        args.api_base, args.output, args.max_requests, inner=inner, secrets=(password,)
    )
    data = {
        "source_base_url": args.api_base,
        "captured_at": datetime.now(UTC).isoformat(),
        "requested_collection_uuid": args.collection_uuid,
        "collection_uuid": None,
        "collection_handle": None,
        "authenticated": False,
        "pages_by_surface": {},
        "vocabulary_evidence": {},
        "surfaces_complete": [],
        "errors": [],
        "warnings": [],
        "captures": transport.events,
        "capture_complete": False,
        "limits": {
            key: getattr(args, key)
            for key in (
                "timeout",
                "max_seconds",
                "max_requests",
                "max_pages",
                "page_size",
            )
        },
    }
    output = args.output / "export.json"
    save_json(output, data)

    async def paginate(surface, loader):
        transport.surface = surface
        pages = data["pages_by_surface"].setdefault(surface, [])
        items = []
        totals = None
        for number in range(args.max_pages):
            async with asyncio.timeout(args.timeout):
                page = await loader(page=number, size=args.page_size)
            if page.page != number or page.total_pages > args.max_pages:
                raise DSpaceError(
                    "pagination_limit", "Invalid or over-budget pagination"
                )
            if totals is None:
                totals = (page.total_pages, page.total_elements)
            elif totals != (page.total_pages, page.total_elements):
                raise DSpaceError(
                    "pagination_changed", "Pagination changed during export"
                )
            pages.append(page.raw_payload)
            items.extend(page.items)
            save_json(output, data)
            if number + 1 >= page.total_pages:
                if len(items) != page.total_elements:
                    raise DSpaceError(
                        "incomplete_surface", "Page counts do not cover the inventory"
                    )
                data["surfaces_complete"].append(surface)
                save_json(output, data)
                return items
        raise DSpaceError("pagination_limit", "Page budget exhausted")

    async def attempt(surface, loader):
        try:
            return await paginate(surface, loader)
        except (DSpaceError, TimeoutError) as exc:
            data["errors"].append(
                {
                    "surface": surface,
                    "code": exc.code if isinstance(exc, DSpaceError) else "TIMEOUT",
                    "http_status": getattr(exc, "status_code", None),
                }
            )
            save_json(output, data)
            return None

    try:
        async with asyncio.timeout(args.max_seconds):
            async with ConfigurationClient(
                args.api_base,
                max_retries=0,
                timeout_seconds=args.timeout,
                transport=transport,
            ) as client:
                if not public_hierarchy:
                    async with asyncio.timeout(args.timeout):
                        await client.authenticate(username, password)
                    data["authenticated"] = True
                schemas = (
                    []
                    if hierarchy_only
                    else await attempt(
                        "metadata_schemas", client.get_metadata_schemas_page
                    )
                )
                if not hierarchy_only:
                    await attempt("metadata_fields", client.get_metadata_fields_page)
                for schema in schemas or []:
                    prefix = safe_name(schema.get("prefix"))

                    async def schema_loader(*, page, size, prefix=prefix):
                        return await client.get_metadata_fields_by_schema_page(
                            prefix, page=page, size=size
                        )

                    await attempt("metadata_fields_by_schema:" + prefix, schema_loader)
                for surface, loader in (
                    ()
                    if hierarchy_only
                    else (
                        (
                            "submission_definitions",
                            client.get_submission_definitions_page,
                        ),
                        ("submission_sections", client.get_submission_sections_page),
                        ("submission_forms", client.get_submission_forms_page),
                        ("collections", client.get_collections_page),
                    )
                ):
                    await attempt(surface, loader)
                if args.collection_uuid:
                    try:
                        transport.surface = "pilot_collection"
                        async with asyncio.timeout(args.timeout):
                            collection = await client.get_collection(
                                args.collection_uuid
                            )
                        if collection.get("uuid") != args.collection_uuid:
                            raise DSpaceError(
                                "collection_identity_mismatch",
                                "Collection UUID differs",
                            )
                        data["collection_uuid"] = collection["uuid"]
                        data["collection_handle"] = collection.get("handle")
                        transport.surface = "active_submission_definition"
                        async with asyncio.timeout(args.timeout):
                            definition = (
                                await client.get_submission_definition_for_collection(
                                    args.collection_uuid
                                )
                            )
                        data["pages_by_surface"]["active_submission_definition"] = [
                            definition
                        ]
                        name = safe_name(definition.get("name"))

                        async def sections_loader(*, page, size):
                            return await client.get_submission_definition_sections_page(
                                name, page=page, size=size
                            )

                        sections = await attempt(
                            "active_submission_sections", sections_loader
                        )
                        if (
                            sections is None
                            and data["errors"][-1].get("http_status") == 204
                        ):
                            data["pages_by_surface"]["active_submission_sections"] = [
                                {
                                    "_observation": {
                                        "observable": False,
                                        "statusCode": 204,
                                        "reason": "no_content",
                                    },
                                    "page": {
                                        "number": 0,
                                        "totalPages": 0,
                                        "totalElements": 0,
                                    },
                                }
                            ]
                            data["warnings"].append(
                                "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204"
                            )
                    except (DSpaceError, TimeoutError) as exc:
                        data["errors"].append(
                            {
                                "surface": transport.surface,
                                "code": getattr(exc, "code", "TIMEOUT"),
                                "http_status": getattr(exc, "status_code", None),
                            }
                        )
                else:
                    data["warnings"].append(
                        "Collection not selected; active membership is NOT_TESTED"
                    )
                vocabularies = (
                    [{"id": public_hierarchy, "hierarchical": True}]
                    if public_hierarchy
                    else await attempt("vocabularies", client.get_vocabularies_page)
                )
                if hierarchy_only:
                    vocabularies = [
                        v for v in vocabularies or [] if v.get("id") == hierarchy_only
                    ]
                    if not vocabularies:
                        data["errors"].append(
                            {"surface": "vocabularies", "code": "VOCABULARY_NOT_FOUND"}
                        )
                for vocabulary in vocabularies or []:
                    name = safe_name(vocabulary.get("id"))

                    if vocabulary.get("hierarchical") is True:

                        async def top_loader(*, page, size, name=name):
                            return await client.get_vocabulary_top_page(
                                name, page=page, size=size
                            )

                        surface = "vocabulary_top:" + name
                        roots = await attempt(surface, top_loader)
                        evidence = {
                            "hierarchical": True,
                            "top_only": True,
                            "pages": data["pages_by_surface"].get(surface, []),
                            "tree": {"status": "UNKNOWN", "complete": False},
                        }
                        data["vocabulary_evidence"][name] = evidence

                        async def fetch_children(identifier, path):
                            async def loader(*, page, size):
                                return await client.get_vocabulary_children_page(
                                    path, page=page, size=size
                                )

                            return await attempt(
                                "vocabulary_children:" + identifier, loader
                            )

                        if roots is not None:
                            await collect_tree(
                                name, roots, fetch_children, evidence["tree"]
                            )
                            evidence["top_only"] = not evidence["tree"]["complete"]
                        if not evidence["tree"]["complete"]:
                            data["warnings"].append("HIERARCHY_INCOMPLETE:" + name)
                        save_json(output, data)
                        continue

                    async def entries_loader(*, page, size, name=name):
                        return await client.get_vocabulary_entries_page(
                            name, page=page, size=size
                        )

                    surface = "vocabulary_entries:" + name
                    entries = await attempt(surface, entries_loader)
                    top_only = False
                    if (
                        entries is None
                        and vocabulary.get("hierarchical")
                        and data["errors"][-1].get("http_status") in {404, 422}
                    ):
                        top_only = True

                        async def top_loader(*, page, size, name=name):
                            return await client.get_vocabulary_top_page(
                                name, page=page, size=size
                            )

                        surface = "vocabulary_top:" + name
                        await attempt(surface, top_loader)
                    data["vocabulary_evidence"][name] = {
                        "hierarchical": vocabulary.get("hierarchical") is not False,
                        "top_only": top_only,
                        "pages": data["pages_by_surface"].get(surface, [])
                        if surface in data["surfaces_complete"]
                        else [],
                    }
                data["capture_complete"] = not data["errors"] and not any(
                    e.get("hierarchical") and not e.get("tree", {}).get("complete")
                    for e in data["vocabulary_evidence"].values()
                )
    except (DSpaceError, TimeoutError) as exc:
        data["errors"].append(
            {
                "surface": transport.surface,
                "code": getattr(exc, "code", "TIMEOUT"),
                "http_status": getattr(exc, "status_code", None),
            }
        )
    except Exception:
        # Never print a transport traceback or exception that might include secrets.
        data["errors"].append(
            {"surface": transport.surface, "code": "EXPORT_INTERRUPTED"}
        )
    finally:
        await transport.aclose()
        data["request_count"] = transport.requests
        data["login_post_count"] = transport.login_requests
        save_json(output, data)

    view = build_contract_snapshot(data["pages_by_surface"])
    data["snapshot_complete"] = view.complete
    data["snapshot_warnings"] = list(view.warnings)
    save_json(output, data)
    checks = [
        {
            "check": "public_read_only" if public_hierarchy else "authenticated",
            "status": "PASS" if public_hierarchy or data["authenticated"] else "FAIL",
            "detail": "No credentials or login used"
            if public_hierarchy
            else "Existing CSRF/login/confirmation client; credentials not exported",
        }
    ]
    for name, evidence in data["vocabulary_evidence"].items():
        if evidence.get("hierarchical"):
            checks.append(
                {
                    "check": "hierarchy_capture:" + name,
                    "status": evidence.get("tree", {}).get("status", "UNKNOWN"),
                    "detail": {
                        k: v
                        for k, v in evidence.get("tree", {}).items()
                        if k not in {"nodes", "edges"}
                    },
                }
            )
    diff = None
    try:
        forms = audit.configured_form_check(data)
        vocab = audit.vocabulary_check(data)
        checks.extend(
            [
                {
                    "check": "configured_forms_vs_v3_9_2",
                    "status": forms["status"],
                    "detail": {
                        k: v
                        for k, v in forms.items()
                        if k not in {"expected", "observed"}
                    },
                },
                {
                    "check": "vocabulary_values_vs_v3_9_2",
                    "status": vocab["status"],
                    "detail": vocab,
                },
            ]
        )
        diff = {
            "scope": "CONFIGURED_FORMS_AND_VOCABULARIES_VS_PRESERVED_RELEASE",
            "full_migration_equivalence": False,
            "baseline_release_sha256": audit.RELEASE_HASH,
            "configured_forms": forms,
            "vocabularies": vocab,
            "raw_export": "export.json",
        }
        if forms["status"] == "UNKNOWN" and not any(
            entry["status"] in {"PASS", "FAIL"} for entry in vocab["results"]
        ):
            diff = None
        if args.baseline and any(data["pages_by_surface"].values()):
            diff = audit.compare_evidence(args.baseline, output)
            checks.append(
                {
                    "check": "baseline_comparison",
                    "status": "UNKNOWN"
                    if not diff["complete"]
                    else ("FAIL" if diff["changes"] else "PASS"),
                    "detail": "VERTICAL-022 diff; see diff.json and observability warnings",
                }
            )
    except (OSError, ValueError, KeyError, TypeError):
        data["warnings"].append(
            "Reference comparison unavailable; raw export preserved"
        )
    checks.extend(
        [
            {
                "check": "active_collection_membership",
                "status": "PASS" if view.complete else "UNKNOWN",
                "detail": list(view.warnings),
            },
            {
                "check": "full_migration_equivalence",
                "status": "NOT_TESTED",
                "detail": "Requires approved baseline, identity review and semantic validation",
            },
        ]
    )
    report = {
        "captured_at": data["captured_at"],
        "coverage": "PUBLIC_HIERARCHY_ONLY"
        if public_hierarchy
        else "AUTHENTICATED_HIERARCHY_ONLY"
        if hierarchy_only
        else "AUTHENTICATED_LOCAL_FILE_EXPORT",
        "configuration": {
            "api_base": args.api_base,
            "hierarchy_only": hierarchy_only,
            "public_hierarchy": public_hierarchy,
            "requested_collection_uuid": args.collection_uuid,
            "limits": data["limits"],
            "credentials_persisted": False,
            "allowed_methods": ["GET", "POST /authn/login once"],
        },
        "results": checks,
        "endpoints": transport.events,
        "errors": data["errors"],
        "warnings": data["warnings"]
        + list(view.warnings)
        + [
            "Administrative account privileges do not authorize any data mutation.",
            "Global configured forms do not prove active collection membership.",
        ],
    }
    report["status_counts"] = {
        s: sum(r["status"] == s for r in checks)
        for s in ("PASS", "FAIL", "UNKNOWN", "NOT_TESTED")
    }
    audit.write_reports(args.output, report, diff)
    return data, report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-base", default=API)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "reports/snibli-migration"
        / (
            "authenticated-"
            + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
            + "-"
            + uuid.uuid4().hex[:8]
        ),
    )
    parser.add_argument("--collection-uuid", type=lambda value: str(uuid.UUID(value)))
    parser.add_argument("--baseline", type=Path)
    parser.add_argument(
        "--public-hierarchy",
        type=safe_name,
        help="GET-only hierarchy capture without credentials",
    )
    parser.add_argument(
        "--hierarchy-only",
        type=safe_name,
        help="Only capture this vocabulary's reachable HAL hierarchy",
    )
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--max-seconds", type=float, default=180)
    parser.add_argument("--max-requests", type=int, default=200)
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--page-size", type=int, default=100)
    args = parser.parse_args(argv)
    if args.public_hierarchy:
        if args.hierarchy_only and args.hierarchy_only != args.public_hierarchy:
            parser.error("Hierarchy vocabulary names must agree")
        args.hierarchy_only = args.public_hierarchy
    if args.hierarchy_only and (args.collection_uuid or args.baseline):
        parser.error(
            "--hierarchy-only cannot be combined with --collection-uuid or --baseline"
        )
    try:
        args.api_base = api_url(args.api_base)
    except ValueError:
        parser.error(
            "Only https://www.iifl.unam.mx/server/api is authorized; no credentials in URLs"
        )
    if (
        not math.isfinite(args.timeout)
        or not 0 < args.timeout <= 30
        or not math.isfinite(args.max_seconds)
        or not 0 < args.max_seconds <= 600
        or not 1 <= args.max_requests <= 500
        or not 1 <= args.max_pages <= 100
        or not 1 <= args.page_size <= 100
    ):
        parser.error(
            "Limits: timeout (0,30], total (0,600], requests 1..500, pages 1..100, size 1..100"
        )
    if args.output.exists():
        parser.error(
            "Output directory already exists; choose a new directory to preserve evidence"
        )
    return args


def main(argv=None):
    args = parse_args(argv)
    print(
        "SNIBLI: local JSON/HAL export. GET only, except session login; no database access."
    )
    try:
        username = password = None
        if not args.public_hierarchy:
            username = input("Usuario DSpace: ").strip()
            with warnings.catch_warnings():
                warnings.simplefilter("error", getpass.GetPassWarning)
                password = getpass.getpass("Contraseña DSpace (oculta): ")
            if not username or not password:
                print("No credentials supplied; no request made.", file=sys.stderr)
                return 2
        data, report = asyncio.run(export_configuration(args, username, password))
    except (EOFError, getpass.GetPassWarning):
        print(
            "An interactive terminal with hidden password input is required.",
            file=sys.stderr,
        )
        return 2
    except (OSError, ValueError):
        print(
            "Export could not start or save files; check the output directory.",
            file=sys.stderr,
        )
        return 2
    except KeyboardInterrupt:
        print(
            "Interrupted. Preserve any partial export; do not treat it as complete.",
            file=sys.stderr,
        )
        return 2
    print(
        json.dumps(
            {
                "output": str(args.output),
                "capture_complete": data["capture_complete"],
                "snapshot_complete": data["snapshot_complete"],
                "counts": report["status_counts"],
            }
        )
    )
    return (
        1 if report["status_counts"]["FAIL"] else (0 if data["capture_complete"] else 2)
    )


if __name__ == "__main__":
    raise SystemExit(main())
