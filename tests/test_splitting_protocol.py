"""
Tests for Official Splitting Protocol (Sprint 3.a.3).
"""

from pathlib import Path
import json
import pytest
from src.validation.splitting_protocol import (
    audit_grouped_fold_distributions,
    get_official_validation_protocol,
    get_cv_splits,
    PROTOCOL_JSON_PATH
)


def test_audit_grouped_fold_distributions():
    """Verify GroupKFold distribution properties and balance assessment."""
    audit = audit_grouped_fold_distributions(n_splits=5)
    
    assert audit["n_splits"] == 5
    assert len(audit["folds"]) == 5
    assert audit["balance_assessment"]["is_balanced"] is True
    
    # Check that each fold has at least 3 validation samples
    for fold in audit["folds"]:
        assert fold["validation_sample_count"] >= 3
        assert fold["training_sample_count"] >= 14
        assert fold["target_max_log10_rc"] > fold["target_min_log10_rc"]


def test_get_official_validation_protocol():
    """Verify serialization and guidelines of the official protocol."""
    protocol = get_official_validation_protocol()
    
    assert protocol["primary_cv_scheme"]["scheme"] == "GroupKFold"
    assert protocol["primary_cv_scheme"]["grouping_variable"] == "source_uid"
    assert protocol["secondary_benchmark_scheme"]["scheme"] == "LeaveOneGroupOut (LOGO)"
    assert len(protocol["prohibited_practices"]) >= 3
    
    assert PROTOCOL_JSON_PATH.exists()
    with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["title"] == protocol["title"]


def test_get_cv_splits():
    """Verify drop-in CV split generator supports grouped_5fold and logo."""
    splits_g5 = get_cv_splits(scheme="grouped_5fold")
    assert len(splits_g5) == 5
    
    splits_logo = get_cv_splits(scheme="logo")
    assert len(splits_logo) >= 10
    
    with pytest.raises(ValueError):
        get_cv_splits(scheme="invalid_scheme")

