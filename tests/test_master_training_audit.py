"""
Unit tests for Heading 4 Master Milestone Audit.
"""

import pytest
import json
from pathlib import Path
from src.models.master_training_audit import (
    run_heading_4_master_audit,
    MASTER_TRAINING_AUDIT_JSON
)


def test_run_heading_4_master_audit():
    res = run_heading_4_master_audit()
    assert res["status"] == "APPROVED"
    assert len(res["subheadings_verified"]) == 5
    assert MASTER_TRAINING_AUDIT_JSON.exists()

    with open(MASTER_TRAINING_AUDIT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["status"] == "APPROVED"
    assert "top_symbolic_formula" in data["key_milestone_achievements"]
    assert "top_regularized_model" in data["key_milestone_achievements"]
