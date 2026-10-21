"""Bounded traversal of advertised SNIBLI HAL vocabulary children; no HTTP of its own."""

from collections import deque
from urllib.parse import urlsplit

from cataloging_api.dspace.client import DSpaceError


def children_path(href, vocabulary, entry_id):
    """Reject foreign, malformed and unrelated links before any credentialed request."""
    p = urlsplit(href)
    expected = f"/server/api/submission/vocabularyEntryDetails/{entry_id}/children"
    if (
        p.scheme != "https"
        or p.hostname != "www.iifl.unam.mx"
        or p.port not in (None, 443)
        or p.username
        or p.password
        or p.fragment
        or p.query
        or p.path != expected
        or not entry_id.startswith(vocabulary + ":")
    ):
        raise DSpaceError("unsafe_children_link", "Unapproved vocabulary child link")
    return p.path.removeprefix("/server/api")


async def collect_tree(
    vocabulary, roots, fetch, state, *, max_nodes=10000, max_depth=32
):
    """Keep partial normalized nodes/edges while raw pages are persisted by fetch."""
    state.update(status="UNKNOWN", complete=False, nodes=[], edges=[], errors=[])
    pending = deque((node, None, 0) for node in roots)
    seen = set()
    while pending:
        node, parent, depth = pending.popleft()
        identifier = node.get("id")
        if not isinstance(identifier, str) or not identifier.startswith(
            vocabulary + ":"
        ):
            state["errors"].append({"code": "INVALID_NODE_ID"})
            continue
        if identifier in seen:
            state["errors"].append(
                {"code": "CYCLE_OR_DUPLICATE_NODE", "id": identifier}
            )
            continue
        if len(seen) >= max_nodes or depth > max_depth:
            state["errors"].append({"code": "TREE_LIMIT", "id": identifier})
            break
        seen.add(identifier)
        state["nodes"].append(node)
        if parent is not None:
            state["edges"].append({"parent": parent, "child": identifier})
        info = node.get("otherInformation", {})
        has_children = info.get("hasChildren") if isinstance(info, dict) else None
        if not (
            type(has_children) is bool
            or isinstance(has_children, str)
            and has_children in {"true", "false"}
        ):
            state["errors"].append(
                {"code": "UNKNOWN_CHILD_MEMBERSHIP", "id": identifier}
            )
            continue
        if not isinstance(node.get("value"), str) or not isinstance(
            node.get("display"), str
        ):
            state["errors"].append({"code": "INVALID_NODE_VALUE", "id": identifier})
            continue
        if has_children in (False, "false"):
            continue
        href = node.get("_links", {}).get("children", {}).get("href")
        if not isinstance(href, str):
            state["errors"].append({"code": "CHILD_LINK_MISSING", "id": identifier})
            continue
        try:
            path = children_path(href, vocabulary, identifier)
            children = await fetch(identifier, path)
            if children is None or not children:
                state["errors"].append(
                    {"code": "CHILDREN_INCOMPLETE", "id": identifier}
                )
                continue
            pending.extend((child, identifier, depth + 1) for child in children)
        except DSpaceError as exc:
            state["errors"].append({"code": exc.code, "id": identifier})
    state["node_count"] = len(state["nodes"])
    state["edge_count"] = len(state["edges"])
    state["complete"] = not state["errors"] and not pending
    state["status"] = "PASS" if state["complete"] else "UNKNOWN"
    state["scope"] = (
        "Reachable hierarchy exposed by HAL; not server XML byte equivalence"
    )
    return state
