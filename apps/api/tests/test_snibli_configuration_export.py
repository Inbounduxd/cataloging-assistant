import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs

import httpx
import pytest

from .test_dspace_contract_snapshot import _paged, _pages

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "snibli_export", ROOT / "scripts/export_snibli_configuration.py"
)
exporter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = exporter
spec.loader.exec_module(exporter)

PASSWORD = "test-password-only-in-memory-8382"
TOKEN = "private-token-only-in-memory-8723"
CSRF = "private-csrf-only-in-memory-1938"
COLLECTION = "b9ceaf16-0d56-43b6-8fc0-671dc3293283"


def args(tmp_path, **overrides):
    values = dict(
        api_base=exporter.API,
        output=tmp_path / "run",
        collection_uuid=COLLECTION,
        timeout=2,
        max_seconds=30,
        max_requests=100,
        max_pages=5,
        page_size=100,
        baseline=None,
    )
    values.update(overrides)
    return SimpleNamespace(**values)


def mock_server(
    *,
    login_status=200,
    redirect=False,
    active_204=False,
    field_error=None,
    leak_secret=False,
    html=False,
    missing_cookie=False,
):
    seen = []
    authenticated = False
    pages = _pages()

    async def handler(request):
        nonlocal authenticated
        seen.append(request)
        path = request.url.path.removeprefix("/server/api")
        if path == "/authn/status":
            return httpx.Response(
                200,
                json={"authenticated": authenticated},
                headers={
                    **(
                        {}
                        if missing_cookie
                        else {"Set-Cookie": f"DSPACE-XSRF-COOKIE={CSRF}; Path=/"}
                    )
                },
            )
        if path == "/authn/login":
            assert request.method == "POST"
            assert parse_qs(request.content.decode())["password"] == [PASSWORD]
            assert request.headers["X-XSRF-TOKEN"] == CSRF
            if redirect:
                return httpx.Response(302, headers={"Location": "https://unapproved.example/login"})
            authenticated = login_status == 200
            return httpx.Response(login_status, headers={"Authorization": f"Bearer {TOKEN}"})
        assert request.method == "GET"
        assert request.headers["Authorization"] == f"Bearer {TOKEN}"
        if path == "/core/metadatafields" and field_error:
            if field_error == "timeout":
                raise httpx.ReadTimeout("Simulated timeout", request=request)
            return httpx.Response(field_error, json={"status": field_error})
        if path == "/core/metadatafields" and html:
            return httpx.Response(
                200, text="<html>Frontend</html>", headers={"Content-Type": "text/html"}
            )
        if path == "/core/metadataschemas":
            payload = pages["metadata_schemas"][0]
        elif path in {"/core/metadatafields", "/core/metadatafields/search/bySchema"}:
            payload = json.loads(json.dumps(pages["metadata_fields"][0]))
            if leak_secret:
                payload["_embedded"]["metadatafields"][0]["scopeNote"] = PASSWORD
        elif path == "/config/submissiondefinitions":
            payload = _paged("submissiondefinitions", [{"name": "traditional"}])
        elif path == "/config/submissionforms":
            payload = pages["submission_forms"][0]
        elif path in {
            "/config/submissionsections",
            "/config/submissiondefinitions/traditional/sections",
        }:
            if active_204 and path.endswith("traditional/sections"):
                return httpx.Response(204)
            payload = pages["active_submission_sections"][0]
        elif path == "/core/collections":
            payload = _paged(
                "collections", [{"uuid": COLLECTION, "handle": "123456789/900", "name": "Pilot"}]
            )
        elif path == "/core/collections/" + COLLECTION:
            payload = {"uuid": COLLECTION, "handle": "123456789/900"}
        elif path == "/config/submissiondefinitions/search/findByCollection":
            payload = {"name": "traditional"}
        elif path == "/submission/vocabularies":
            payload = _paged("vocabularies", [{"id": "educationLevelPairs", "hierarchical": False}])
        elif path == "/submission/vocabularies/educationLevelPairs/entries":
            values = exporter.audit.skill_asset("controlled-vocabulary-index.json")[
                "educationLevelPairs"
            ]["values"]
            payload = _paged("entries", [{"value": v} for v in values])
        else:
            raise AssertionError(f"Unexpected endpoint {path}")
        return httpx.Response(
            200,
            json={**payload, "_links": {"self": {"href": str(request.url)}}},
            headers={"Content-Type": "application/hal+json"},
        )

    return httpx.MockTransport(handler), seen


@pytest.mark.asyncio
async def test_export_reuses_login_and_only_saves_hal_files(tmp_path):
    transport, seen = mock_server()
    data, report = await exporter.export_configuration(
        args(tmp_path), "operator", PASSWORD, inner=transport
    )
    assert data["authenticated"]
    assert data["capture_complete"]
    assert data["snapshot_complete"]
    assert data["collection_uuid"] == COLLECTION
    assert [r.method for r in seen].count("POST") == 1
    assert all(r.method == "GET" or r.url.path == "/server/api/authn/login" for r in seen)
    assert data["pages_by_surface"]["metadata_fields"][0]["_embedded"]["metadatafields"]
    assert (tmp_path / "run/export.json").is_file()
    assert (tmp_path / "run/audit.md").is_file()
    assert report["configuration"]["credentials_persisted"] is False
    for path in (tmp_path / "run").rglob("*"):
        if path.is_file():
            content = path.read_bytes()
            assert PASSWORD.encode() not in content
            assert TOKEN.encode() not in content
            assert CSRF.encode() not in content
    assert all("authn" not in event["endpoint"] for event in data["captures"])


@pytest.mark.parametrize(
    "method,path",
    [
        ("POST", "/core/items"),
        ("PUT", "/config/submissionforms/test"),
        ("DELETE", "/core/collections/" + COLLECTION),
        ("PATCH", "/authn/login"),
        ("POST", "/authn/login/"),
        ("POST", "/authn/login?other=1"),
        ("GET", "/workflow/workflowitems"),
    ],
)
@pytest.mark.asyncio
async def test_mutations_and_out_of_scope_reads_blocked_before_network(tmp_path, method, path):
    called = []
    inner = httpx.MockTransport(lambda request: called.append(request) or httpx.Response(200))
    boundary = exporter.ReadOnlyTransport(exporter.API, tmp_path, 20, inner=inner)
    with pytest.raises(exporter.DSpaceError):
        await boundary.handle_async_request(httpx.Request(method, exporter.API + path))
    assert not called


@pytest.mark.asyncio
async def test_foreign_host_never_receives_credentials(tmp_path):
    seen = []
    boundary = exporter.ReadOnlyTransport(
        exporter.API,
        tmp_path,
        10,
        inner=httpx.MockTransport(lambda req: seen.append(req) or httpx.Response(200)),
    )
    with pytest.raises(exporter.DSpaceError, match="blocked"):
        await boundary.handle_async_request(
            httpx.Request(
                "POST", "https://unapproved.example/server/api/authn/login", content=PASSWORD
            )
        )
    assert not seen


@pytest.mark.asyncio
async def test_login_redirect_never_followed(tmp_path):
    transport, seen = mock_server(redirect=True)
    data, report = await exporter.export_configuration(
        args(tmp_path), "operator", PASSWORD, inner=transport
    )
    assert not data["authenticated"]
    assert not data["capture_complete"]
    assert all(r.url.host == "www.iifl.unam.mx" for r in seen)
    assert data["errors"][0]["code"] == "redirect_blocked"
    assert not list((tmp_path / "run/raw").iterdir())


@pytest.mark.parametrize("options", [{"login_status": 401}, {"missing_cookie": True}])
@pytest.mark.asyncio
async def test_failed_authentication_never_reads_configuration(tmp_path, options):
    transport, seen = mock_server(**options)
    data, _ = await exporter.export_configuration(
        args(tmp_path), "operator", PASSWORD, inner=transport
    )
    assert not data["authenticated"]
    assert all("/authn/" in r.url.path for r in seen)
    assert not list((tmp_path / "run/raw").iterdir())
    assert not (tmp_path / "run/diff.json").exists()


@pytest.mark.asyncio
async def test_active_204_remains_unobservable(tmp_path):
    transport, _ = mock_server(active_204=True)
    data, report = await exporter.export_configuration(
        args(tmp_path), "operator", PASSWORD, inner=transport
    )
    assert not data["snapshot_complete"]
    assert "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204" in data["warnings"]
    _, view, _ = exporter.audit.load_evidence(tmp_path / "run/export.json")
    assert not view.complete
    assert "ACTIVE_SUBMISSION_SECTIONS_UNRESOLVED_HTTP_204" in view.warnings
    assert (
        next(r for r in report["results"] if r["check"] == "active_collection_membership")["status"]
        == "UNKNOWN"
    )


@pytest.mark.parametrize(
    "options,code",
    [
        ({"field_error": "timeout"}, "timeout"),
        ({"field_error": 403}, "invalid_response"),
        ({"html": True}, "invalid_hal"),
        ({"leak_secret": True}, "sensitive_body"),
    ],
)
@pytest.mark.asyncio
async def test_partial_failures_preserve_evidence_without_secrets(tmp_path, options, code):
    transport, _ = mock_server(**options)
    data, _ = await exporter.export_configuration(
        args(tmp_path), "operator", PASSWORD, inner=transport
    )
    assert not data["capture_complete"]
    assert not data["snapshot_complete"]
    assert any(error["code"] == code for error in data["errors"])
    assert (tmp_path / "run/export.json").exists()
    assert all(
        PASSWORD.encode() not in p.read_bytes()
        for p in (tmp_path / "run").rglob("*")
        if p.is_file()
    )


@pytest.mark.asyncio
async def test_no_collection_never_assumes_historical_uuid(tmp_path):
    transport, seen = mock_server()
    data, _ = await exporter.export_configuration(
        args(tmp_path, collection_uuid=None), "operator", PASSWORD, inner=transport
    )
    assert data["collection_uuid"] is None
    assert not data["snapshot_complete"]
    assert not any("findByCollection" in str(r.url) for r in seen)
    assert not any(exporter.audit.PILOT in str(r.url) for r in seen)


@pytest.mark.asyncio
async def test_request_limit_stops_network_and_keeps_partial_export(tmp_path):
    transport, seen = mock_server()
    data, _ = await exporter.export_configuration(
        args(tmp_path, max_requests=3), "operator", PASSWORD, inner=transport
    )
    assert len(seen) == 3
    assert not data["capture_complete"]
    assert any(e["code"] == "request_limit" for e in data["errors"])


@pytest.mark.asyncio
async def test_missing_credentials_or_existing_output_never_connects(tmp_path):
    transport, seen = mock_server()
    with pytest.raises(ValueError):
        await exporter.export_configuration(args(tmp_path), "operator", "", inner=transport)
    assert not seen
    (tmp_path / "run").mkdir()
    with pytest.raises(FileExistsError):
        await exporter.export_configuration(args(tmp_path), "operator", PASSWORD, inner=transport)
    assert not seen


@pytest.mark.asyncio
async def test_second_login_is_blocked(tmp_path):
    seen = []
    boundary = exporter.ReadOnlyTransport(
        exporter.API,
        tmp_path,
        10,
        inner=httpx.MockTransport(lambda req: seen.append(req) or httpx.Response(200)),
    )
    request = httpx.Request("POST", exporter.API + "/authn/login")
    await boundary.handle_async_request(request)
    with pytest.raises(exporter.DSpaceError, match="Only one"):
        await boundary.handle_async_request(request)
    assert len(seen) == 1


@pytest.mark.asyncio
async def test_oversized_response_is_not_persisted(tmp_path):
    (tmp_path / "raw").mkdir()
    boundary = exporter.ReadOnlyTransport(
        exporter.API,
        tmp_path,
        10,
        inner=httpx.MockTransport(
            lambda req: httpx.Response(200, content=b"x" * (exporter.MAX_BYTES + 1))
        ),
    )
    with pytest.raises(exporter.DSpaceError, match="4 MiB"):
        await boundary.handle_async_request(
            httpx.Request("GET", exporter.API + "/core/metadatafields")
        )
    assert not list((tmp_path / "raw").iterdir())


def test_cli_rejects_foreign_api_before_prompting(tmp_path):
    with pytest.raises(SystemExit) as caught:
        exporter.parse_args(
            [
                "--api-base",
                "https://unapproved.example/server/api",
                "--output",
                str(tmp_path / "run"),
            ]
        )
    assert caught.value.code == 2
