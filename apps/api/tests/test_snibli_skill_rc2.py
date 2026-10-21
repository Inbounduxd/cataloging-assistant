import importlib.util
import io
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "skill_rc2", ROOT / "scripts/build_snibli_skill_rc2.py"
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
PARENT = ROOT / "skills/dspace-cataloger/versions/v3.9.3-rc.1"
CAPTURE = ROOT / "reports/snibli-migration/srsc-hal-tree-20261021"


def asset(members, name):
    return json.loads(members[builder.PREFIX + "assets/" + name])


def test_reconstructs_tree_from_original_hal_and_validates_all_raw_hashes():
    tree, facts, raw, _, _ = builder.verify_capture(CAPTURE)
    assert (facts["nodeCount"], facts["edgeCount"], facts["rootCount"]) == (665, 653, 12)
    assert facts["rawResponseCount"] == len(raw) == 126
    assert len(tree["tree"]["nodes"]) == 665
    assert facts["historicalEquivalence"] == "UNKNOWN"


def test_rc2_assets_agree_and_preserve_parent_runtime_and_golden_records():
    members, facts = builder.build_members(PARENT, CAPTURE)
    with zipfile.ZipFile(PARENT / "dspace-cataloger-v3.9.3-rc.1.skill") as archive:
        for index in range(1, 24):
            name = f"dspace-cataloger/tests/golden-set/GR{index:02}.json"
            assert members[name] == archive.read(name)
        name = builder.PREFIX + "assets/cataloging-runtime-contract.json"
        assert members[name] == archive.read(name)
        old_lock = json.loads(
            archive.read(builder.PREFIX + "assets/runtime-contract-lock-v3.9.json")
        )
    contract = asset(members, "dspace-form-contract-v1.json")
    profile = asset(members, "dspace-cataloguing-profile-v3.json")
    vocab = asset(members, "controlled-vocabulary-index.json")["srsc"]
    release = asset(members, "release-manifest.json")
    lock = asset(members, "runtime-contract-lock-v3.9.json")
    assert lock["catalogContractSha256"] == old_lock["catalogContractSha256"]
    assert lock["skillVersion"] == "3.9.3-rc.2"
    assert len(contract["fields"]) == 57
    assert len(profile["metadataRegistryForTraditionalForms"]) == 55
    assert vocab["entryCount"] == 665 and vocab["error"] is None
    assert profile["vocabularies"]["srsc"] == vocab
    nodes = asset(members, "srsc-tree.json")["tree"]["nodes"]
    assert vocab["values"] == [node["value"] for node in nodes if node["selectable"]]
    assert release["qa"]["srscHierarchy"] == "PASS_CURRENT_HAL_CAPTURE"
    assert release["parentArtifact"]["sha256"] == builder.PARENT_HASH
    assert contract["coverage"]["fullMigrationEquivalence"] == "UNKNOWN"
    assert contract["coverage"]["activeSectionsHAL"] == "UNKNOWN_HTTP_204"
    assert not contract["coverage"]["adopted"]
    skill = members[builder.PREFIX + "SKILL.md"].decode()
    assert "The complete srsc hierarchy remains UNKNOWN" not in skill
    assert "SRSC_HAL_EVIDENCE.md" in skill
    assert facts["rawResponseCount"] == 126


def test_rc2_package_deterministic_and_json_valid():
    members, _ = builder.build_members(PARENT, CAPTURE)
    blob = builder.package(members)
    assert blob == builder.package(dict(reversed(list(members.items()))))
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.endswith(".json"):
                json.loads(archive.read(name))


def test_modified_raw_body_is_rejected(tmp_path):
    capture = tmp_path / "capture"
    shutil.copytree(CAPTURE, capture)
    event = json.loads((capture / "export.json").read_text())["captures"][0]
    (capture / event["raw_file"]).write_bytes(b"tampered")
    with pytest.raises(ValueError, match="RAW_HASH_MISMATCH"):
        builder.verify_capture(capture)


def test_normalized_edge_tampering_is_rejected_even_if_envelope_is_rehashed(tmp_path):
    capture = tmp_path / "capture"
    shutil.copytree(CAPTURE, capture)
    data = json.loads((capture / "export.json").read_text())
    tree = json.loads((capture / "srsc-tree.json").read_text())
    tree["tree"]["edges"].pop()
    data["vocabulary_evidence"]["srsc"]["tree"] = tree["tree"]
    raw = builder.encoded(data)
    (capture / "export.json").write_bytes(raw)
    tree["source_export_sha256"] = builder.sha(raw)
    (capture / "srsc-tree.json").write_bytes(builder.encoded(tree))
    with pytest.raises(ValueError, match="NORMALIZED_TREE_MISMATCH"):
        builder.verify_capture(capture)


def test_parent_artifact_cannot_be_silently_replaced(tmp_path):
    parent = tmp_path / "parent"
    parent.mkdir()
    shutil.copyfile(PARENT / "manifest.json", parent / "manifest.json")
    (parent / "dspace-cataloger-v3.9.3-rc.1.skill").write_bytes(b"other parent")
    with pytest.raises(ValueError, match="PARENT_HASH_MISMATCH"):
        builder.build_members(parent, CAPTURE)
