"""
Tests for Master Section 3 Audit Pipeline.
"""

import pytest
from src.validation.master_validation_audit import run_master_section_3_audit


def test_run_master_section_3_audit():
    """Verify that all Section 3 validation specifications, zero-leakage splits, and CV runners pass audit."""
    res = run_master_section_3_audit()
    assert res["status"] == "PASS"
    assert res["checks_failed"] == 0
    assert res["checks_passed"] >= 4
    
    cv_check = res["details"]["cv_execution_check"]
    assert cv_check["status"] == "PASS"
    assert cv_check["composite_score"] > 0.70
