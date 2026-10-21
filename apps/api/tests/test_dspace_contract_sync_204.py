import asyncio
from types import SimpleNamespace

import cataloging_api.dspace.contract_sync_core as core
import pytest
from cataloging_api.dspace.client import DSpaceError


class _Session:
    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


class _Client:
    async def get_submission_definition_for_collection(self, collection_uuid: str) -> dict:
        assert collection_uuid == "collection-uuid"
        return {"name": "traditional"}


async def _raise_204(_session: object, **_: object) -> None:
    raise DSpaceError("invalid_response", "HTTP 204", status_code=204)


def test_active_sections_204_is_persisted_as_unobservable_not_raised(monkeypatch) -> None:
    persisted: list[dict] = []

    async def fake_persist(session, **kwargs):
        persisted.append(kwargs)

    monkeypatch.setattr(core, "persist_page_and_advance_checkpoint", fake_persist)
    monkeypatch.setattr(core, "_collect_surface", _raise_204)

    async def run() -> None:
        session = _Session()
        await core._collect_active_definition(
            session,
            run=SimpleNamespace(),
            client=_Client(),
            collection_uuid="collection-uuid",
            page_size=100,
        )
        assert session.commits == 2

    asyncio.run(run())

    assert len(persisted) == 2
    sections = persisted[1]
    assert sections["surface"] == "active_submission_sections"
    assert sections["raw_payload"]["_observation"] == {
        "observable": False,
        "statusCode": 204,
        "reason": "no_content",
    }
    assert sections["raw_payload"]["page"] == {
        "number": 0,
        "totalPages": 0,
        "totalElements": 0,
    }


@pytest.mark.parametrize("status_code", [401, 403, 500])
def test_non_204_errors_are_not_converted_to_unobservable_sections(
    monkeypatch, status_code
) -> None:
    persisted = []

    async def fake_persist(session, **kwargs):
        persisted.append(kwargs)

    async def fail_sections(session, **kwargs):
        raise DSpaceError("invalid_response", f"HTTP {status_code}", status_code=status_code)

    monkeypatch.setattr(core, "persist_page_and_advance_checkpoint", fake_persist)
    monkeypatch.setattr(core, "_collect_surface", fail_sections)
    session = _Session()
    with pytest.raises(DSpaceError) as caught:
        asyncio.run(
            core._collect_active_definition(
                session,
                run=SimpleNamespace(),
                client=_Client(),
                collection_uuid="collection-uuid",
                page_size=100,
            )
        )
    assert caught.value.status_code == status_code
    assert session.commits == 1
    assert len(persisted) == 1
    assert persisted[0]["surface"] == "active_submission_definition"
