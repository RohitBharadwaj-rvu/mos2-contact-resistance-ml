"""
Tests for Data Leakage Risk Analysis (Sprint 3.a.1).
"""

from pathlib import Path
import json
import pytest
from src.validation.leakage_analyzer import (
    quantify_leakage_risk,
    LEAKAGE_JSON_PATH
)


def test_quantify_leakage_risk():
    """Verify statistical detection of cluster leakage under random K-fold splits."""
    report = quantify_leakage_risk()
    
    summary = report["dataset_summary"]
    assert summary["total_samples"] >= 20
    assert summary["total_distinct_papers"] >= 10
    assert summary["multi_device_papers_count"] >= 3
    
    sim = report["random_5fold_simulation"]
    # In random splits with 11 multi-point records across 5 folds, leakage should occur in multiple folds
    assert sim["folds_with_intra_study_leakage"] >= 3
    assert sim["leakage_fold_percentage"] > 50.0
    
    assert LEAKAGE_JSON_PATH.exists()
    with open(LEAKAGE_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["dataset_summary"]["total_samples"] == summary["total_samples"]
