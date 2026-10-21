import copy
import importlib.util
import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

from cataloging_api.cataloging_contract import contract_payload

SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location(
    "snibli_skill_builder", SCRIPTS / "build_snibli_skill_candidate.py"
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PROPOSAL = SCRIPTS.parent / "reports/snibli-migration/reconciliation-proposal"


@pytest.fixture
def members():
    return builder.build_members(
        PROPOSAL / "candidate-contract.json", PROPOSAL / "decision.json", contract_payload()
    )[0]


def asset(members, name):
    return json.loads(members[builder.PREFIX + "assets/" + name])


def test_candidate_retains_all_original_golden_records_byte_for_byte(members):
    parent, _ = builder.release_archive()
    with zipfile.ZipFile(io.BytesIO(parent)) as archive:
        for i in range(1, 24):
            name = f"dspace-cataloger/tests/golden-set/GR{i:02}.json"
            assert members[name] == archive.read(name)
    assert "ORCID" in members[builder.PREFIX + "SKILL.md"].decode()


def test_candidate_contract_profile_vocab_and_runtime_lock_agree(members):
    manifest = asset(members, "release-manifest.json")
    assert manifest["parentArtifact"]["release"] == "v3.9.2"
    assert manifest["parentArtifact"]["sha256"] == builder.release_archive()[1]
    form = asset(members, "dspace-form-contract-v1.json")
    profile = asset(members, "dspace-cataloguing-profile-v3.json")
    vocab = asset(members, "controlled-vocabulary-index.json")
    runtime = asset(members, "cataloging-runtime-contract.json")
    lock = asset(members, "runtime-contract-lock-v3.9.json")
    assert len(form["fields"]) == 57
    assert len(profile["metadataRegistryForTraditionalForms"]) == 55
    assert [
        len(profile["traditionalForms"][f]["fields"])
        for f in ("traditionalpageone", "traditionalpagetwo")
    ] == [45, 12]
    assert profile["targetFields"]["dc.type.genre"]["metadataField"]["id"] == 293
    assert vocab["genrePairs"]["values"] == ["Sí", "No", "Incluye Datos de Diferentes Lenguas"]
    assert vocab["common_types"]["values"][-3:] == ["Códice", "Reseña", "Documento Colonial"]
    assert vocab["common_types"]["entryCount"] == 26
    assert vocab["srsc"]["values"] is None and vocab["srsc"]["entryCount"] is None
    assert lock["catalogContractSha256"] == builder.sha(
        json.dumps(runtime, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )
    assert runtime["runtime"]["dspace_write_enabled"] is False
    assert runtime["runtime"]["human_approval_required"] is True
    assert form["coverage"]["fullMigrationEquivalence"] == "UNKNOWN"
    assert not form["coverage"]["adopted"]


def test_package_is_deterministic_and_valid(members):
    first = builder.package(members)
    assert first == builder.package(dict(reversed(list(members.items()))))
    with zipfile.ZipFile(io.BytesIO(first)) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))


def test_build_rejects_missing_approval(tmp_path):
    decision = json.loads((PROPOSAL / "decision.json").read_text())
    decision["changes"][1]["approved"] = None
    path = tmp_path / "decision.json"
    path.write_text(json.dumps(decision))
    with pytest.raises(ValueError, match="C1_C2_C3_APPROVAL_REQUIRED"):
        builder.build_members(PROPOSAL / "candidate-contract.json", path, contract_payload())


def test_build_rejects_runtime_vocab_drift():
    runtime = copy.deepcopy(contract_payload())
    runtime["controlled_vocabulary_values"]["genrePairs"][0] = "Si"
    with pytest.raises(ValueError, match="RUNTIME_VOCABULARY_MISMATCH"):
        builder.build_members(
            PROPOSAL / "candidate-contract.json", PROPOSAL / "decision.json", runtime
        )
