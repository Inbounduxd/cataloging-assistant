import io
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import build_snibli_skill_stable as builder  # noqa: E402

PARENT = ROOT / "skills/dspace-cataloger/versions/v3.9.3-rc.2"
PILOT = ROOT / "reports/snibli-migration/functional-pilot-20261021"


def test_stable_preserves_all_operational_assets_and_raw_evidence():
    members = builder.build_members(PARENT, PILOT)
    allowed = {
        "SKILL.md",
        "assets/dspace-form-contract-v1.json",
        "assets/dspace-cataloguing-profile-v3.json",
        "assets/release-manifest.json",
        "assets/snibli-migration-evidence.json",
        "assets/runtime-contract-lock-v3.9.json",
        "references/SNIBLI_MIGRATION_2026.md",
        "references/SRSC_HAL_EVIDENCE.md",
    }
    with zipfile.ZipFile(PARENT / "dspace-cataloger-v3.9.3-rc.2.skill") as archive:
        for name in archive.namelist():
            if name.removeprefix(builder.PREFIX) not in allowed:
                assert members[name] == archive.read(name), name
        for name in ("dspace-form-contract-v1.json", "dspace-cataloguing-profile-v3.json"):
            path = builder.PREFIX + "assets/" + name
            original = json.loads(archive.read(path))
            stable = json.loads(members[path])
            stable["coverage"].pop("repositoryAdoption")
            assert stable == original
        path = builder.PREFIX + "assets/runtime-contract-lock-v3.9.json"
        original = json.loads(archive.read(path))
        stable = json.loads(members[path])
        stable["skillVersion"] = original["skillVersion"]
        assert stable == original
    release = json.loads(members[builder.PREFIX + "assets/release-manifest.json"])
    assert release["parentArtifact"]["sha256"] == builder.PARENT_HASH
    assert release["version"] == "3.9.3"
    assert release["humanApprovalRequired"]
    assert not release["runtimeDspaceWrite"]
    assert not release["runtimeAgentMutations"]
    assert release["coverage"]["fullMigrationEquivalence"] == "UNKNOWN"
    assert release["coverage"]["activeSectionsHAL"] == "UNKNOWN_HTTP_204"
    assert release["coverage"]["srscHistoricalEquivalence"] == "UNKNOWN"


def test_stable_matches_preserved_package_and_all_member_hashes():
    members = builder.build_members(PARENT, PILOT)
    folder = ROOT / "skills/dspace-cataloger/versions/v3.9.3"
    manifest = json.loads((folder / "manifest.json").read_bytes())
    blob = builder.package(members)
    assert blob == (folder / manifest["artifact"]).read_bytes()
    assert manifest["sha256"] == builder.sha(blob)
    assert manifest["memberSha256"] == {name: builder.sha(body) for name, body in members.items()}
    for name, body in members.items():
        assert (folder / "source" / name).read_bytes() == body
    assert blob == builder.package(dict(reversed(list(members.items()))))
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))


def test_tampered_parent_is_rejected(tmp_path):
    shutil.copyfile(PARENT / "manifest.json", tmp_path / "manifest.json")
    (tmp_path / "dspace-cataloger-v3.9.3-rc.2.skill").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="PARENT_HASH_MISMATCH"):
        builder.build_members(tmp_path, PILOT)


def test_tampered_pilot_is_rejected(tmp_path):
    shutil.copytree(PILOT, tmp_path / "pilot")
    (tmp_path / "pilot/proposal.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="PILOT_HASH_MISMATCH"):
        builder.build_members(PARENT, tmp_path / "pilot")


@pytest.mark.parametrize(
    "permission", ["dspaceWriteAuthorized", "deploymentAuthorized", "prMergeAuthorized"]
)
def test_acceptance_cannot_expand_to_execution_permissions(tmp_path, permission):
    shutil.copytree(PILOT, tmp_path / "pilot")
    path = tmp_path / "pilot/acceptance.json"
    acceptance = json.loads(path.read_bytes())
    acceptance[permission] = True
    path.write_bytes(builder.encoded(acceptance))
    with pytest.raises(ValueError, match="INVALID_ACCEPTANCE_SCOPE"):
        builder.build_members(PARENT, tmp_path / "pilot")
