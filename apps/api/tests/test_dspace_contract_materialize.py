from cataloging_api.dspace.contract_materialize import classify_snapshot_status
from cataloging_api.dspace.contract_snapshot import ContractChange, ContractSnapshotView
from cataloging_api.dspace.contract_snapshot_store import DSpaceContractSnapshot


def _view(*, complete: bool, semantic_hash: str = "new") -> ContractSnapshotView:
    return ContractSnapshotView(
        canonical={},
        semantic_hash=semantic_hash,
        complete=complete,
        warnings=() if complete else ("UNOBSERVABLE_SURFACE:x",),
    )


def test_first_complete_snapshot_requires_baseline_review() -> None:
    assert classify_snapshot_status(None, _view(complete=True), []) == "BASELINE_REVIEW_REQUIRED"


def test_first_incomplete_snapshot_cannot_be_baseline_candidate() -> None:
    assert classify_snapshot_status(None, _view(complete=False), []) == "REVIEW_REQUIRED"


def test_matching_active_hash_is_no_change() -> None:
    active = DSpaceContractSnapshot(semantic_hash="same", effective_hash=None)
    assert (
        classify_snapshot_status(active, _view(complete=True, semantic_hash="same"), [])
        == "NO_CHANGE"
    )


def test_high_severity_change_requires_review() -> None:
    active = DSpaceContractSnapshot(semantic_hash="old", effective_hash=None)
    changes = [ContractChange("REQUIRED_CHANGED", "HIGH", "binding")]
    assert classify_snapshot_status(active, _view(complete=True), changes) == "REVIEW_REQUIRED"


def test_safe_drift_is_detected_without_auto_promotion() -> None:
    active = DSpaceContractSnapshot(semantic_hash="old", effective_hash=None)
    changes = [ContractChange("LABEL_CHANGED", "LOW", "binding")]
    assert classify_snapshot_status(active, _view(complete=True), changes) == "DIFF_DETECTED"


def test_approved_effective_hash_takes_precedence_over_observed_hash() -> None:
    active = DSpaceContractSnapshot(semantic_hash="observed", effective_hash="approved")
    assert (
        classify_snapshot_status(active, _view(complete=True, semantic_hash="approved"), [])
        == "NO_CHANGE"
    )
    assert (
        classify_snapshot_status(active, _view(complete=True, semantic_hash="observed"), [])
        == "DIFF_DETECTED"
    )


def test_matching_hash_never_overrides_incomplete_evidence() -> None:
    active = DSpaceContractSnapshot(semantic_hash="observed", effective_hash="approved")
    assert (
        classify_snapshot_status(active, _view(complete=False, semantic_hash="approved"), [])
        == "REVIEW_REQUIRED"
    )
