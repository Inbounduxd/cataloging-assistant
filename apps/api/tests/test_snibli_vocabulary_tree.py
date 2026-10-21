import hashlib
import json
from unittest.mock import AsyncMock

import httpx
import pytest

from .test_dspace_contract_snapshot import _paged
from .test_snibli_configuration_export import PASSWORD, TOKEN, args, exporter, mock_server

tree_module = __import__("snibli_vocabulary_tree")


def node(identifier, *, children=False, href=None):
    result = {
        "id": "srsc:" + identifier,
        "value": identifier,
        "display": identifier,
        "selectable": True,
        "otherInformation": {"hasChildren": str(children).lower()},
        "_links": {},
    }
    if children:
        result["_links"]["children"] = {
            "href": href
            or exporter.API + f"/submission/vocabularyEntryDetails/srsc:{identifier}/children"
        }
    return result


def hierarchy_server(mode=None):
    base, _ = mock_server()
    seen = []

    async def handler(request):
        seen.append(request)
        path = request.url.path.removeprefix("/server/api")
        if path == "/submission/vocabularies":
            payload = _paged("vocabularies", [{"id": "srsc", "hierarchical": True}])
        elif path == "/submission/vocabularyEntryDetails/search/top":
            root = node("ROOT", children=True)
            if mode == "unsafe":
                root["_links"]["children"]["href"] = "https://evil.example/children"
            payload = _paged("vocabularyEntryDetails", [root])
        elif path == "/submission/vocabularyEntryDetails/srsc:ROOT/children":
            assert (
                not request.headers.get("Authorization")
                or request.headers["Authorization"] == f"Bearer {TOKEN}"
            )
            if mode == "timeout":
                raise httpx.ReadTimeout("simulated", request=request)
            if mode == "204":
                return httpx.Response(204)
            if mode == "cycle":
                payload = _paged("children", [node("ROOT", children=True)])
            elif mode == "empty":
                payload = {"page": {"number": 0, "totalPages": 0, "totalElements": 0}}
            else:
                number = int(request.url.params["page"])
                payload = {
                    "_embedded": {"children": [node("LEAF" + str(number))]},
                    "page": {"number": number, "totalPages": 2, "totalElements": 2},
                }
                if mode == "bad_count":
                    payload["page"]["totalElements"] = 3
        else:
            return await base.handle_async_request(request)
        return httpx.Response(
            200,
            json={**payload, "_links": {"self": {"href": str(request.url)}}},
            headers={"Content-Type": "application/hal+json"},
        )

    return httpx.MockTransport(handler), seen


@pytest.mark.asyncio
async def test_hierarchy_only_captures_all_children_pages_and_raw_hashes(tmp_path):
    transport, seen = hierarchy_server()
    data, report = await exporter.export_configuration(
        args(tmp_path, hierarchy_only="srsc", collection_uuid=None),
        "operator",
        PASSWORD,
        inner=transport,
    )
    tree = data["vocabulary_evidence"]["srsc"]["tree"]
    assert data["capture_complete"] and tree["complete"]
    assert not data["snapshot_complete"]
    assert report["coverage"] == "AUTHENTICATED_HIERARCHY_ONLY"
    assert tree["node_count"] == 3 and tree["edge_count"] == 2
    assert tree["edges"] == [
        {"parent": "srsc:ROOT", "child": "srsc:LEAF0"},
        {"parent": "srsc:ROOT", "child": "srsc:LEAF1"},
    ]
    assert not any("/core/" in r.url.path or "/entries" in r.url.path for r in seen)
    assert sum(r.method == "POST" for r in seen) == 1
    for event in data["captures"]:
        body = (tmp_path / "run" / event["raw_file"]).read_bytes()
        assert hashlib.sha256(body).hexdigest() == event["sha256"]
        assert PASSWORD.encode() not in body and TOKEN.encode() not in body


@pytest.mark.parametrize("mode", ["timeout", "204", "unsafe", "cycle", "bad_count", "empty"])
@pytest.mark.asyncio
async def test_incomplete_hierarchy_never_passes_and_preserves_roots(tmp_path, mode):
    transport, seen = hierarchy_server(mode)
    data, report = await exporter.export_configuration(
        args(tmp_path, hierarchy_only="srsc", collection_uuid=None),
        "operator",
        PASSWORD,
        inner=transport,
    )
    tree = data["vocabulary_evidence"]["srsc"]["tree"]
    assert tree["status"] == "UNKNOWN" and not tree["complete"]
    assert not data["capture_complete"]
    assert tree["nodes"][0]["id"] == "srsc:ROOT"
    assert all(r.url.host == "www.iifl.unam.mx" for r in seen)
    assert json.loads((tmp_path / "run/export.json").read_text())["vocabulary_evidence"]["srsc"]
    if mode == "unsafe":
        assert not any(r.url.path.endswith("/children") for r in seen)


@pytest.mark.asyncio
async def test_request_budget_retains_partial_hierarchy(tmp_path):
    transport, _ = hierarchy_server()
    data, _ = await exporter.export_configuration(
        args(tmp_path, hierarchy_only="srsc", collection_uuid=None, max_requests=5),
        "operator",
        PASSWORD,
        inner=transport,
    )
    assert not data["capture_complete"]
    assert any(e["code"] == "request_limit" for e in data["errors"])
    assert data["vocabulary_evidence"]["srsc"]["tree"]["status"] == "UNKNOWN"


@pytest.mark.asyncio
async def test_depth_limit_does_not_claim_complete_tree():
    fetch = AsyncMock(return_value=[node("BRANCH", children=True)])
    state = {}
    await tree_module.collect_tree("srsc", [node("ROOT", children=True)], fetch, state, max_depth=0)
    assert state["status"] == "UNKNOWN"
    assert state["errors"][0]["code"] == "TREE_LIMIT"
    fetch.assert_awaited_once()


def test_hierarchy_mode_cannot_be_combined_with_collection(tmp_path):
    with pytest.raises(SystemExit):
        exporter.parse_args(
            [
                "--hierarchy-only",
                "srsc",
                "--collection-uuid",
                "3ce3afb3-94ed-4f60-bfda-0a1242c4d689",
                "--output",
                str(tmp_path / "new"),
            ]
        )


@pytest.mark.asyncio
async def test_public_hierarchy_never_logs_in_or_sends_credentials(tmp_path):
    transport, seen = hierarchy_server()
    data, report = await exporter.export_configuration(
        args(tmp_path, hierarchy_only="srsc", public_hierarchy="srsc", collection_uuid=None),
        None,
        None,
        inner=transport,
    )
    assert data["capture_complete"] and not data["authenticated"]
    assert data["login_post_count"] == 0
    assert report["coverage"] == "PUBLIC_HIERARCHY_ONLY"
    assert all(
        r.method == "GET" and not r.headers.get("Authorization") and not r.headers.get("Cookie")
        for r in seen
    )


@pytest.mark.asyncio
async def test_integer_child_flag_cannot_prove_a_leaf():
    root = node("ROOT")
    root["otherInformation"]["hasChildren"] = 0
    fetch = AsyncMock()
    state = {}
    await tree_module.collect_tree("srsc", [root], fetch, state)
    assert state["status"] == "UNKNOWN"
    assert state["errors"][0]["code"] == "UNKNOWN_CHILD_MEMBERSHIP"
    fetch.assert_not_awaited()
