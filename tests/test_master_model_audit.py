"""
Tests for Master Section 2 Audit Pipeline.
"""

import pytest
from src.models.master_model_audit import run_master_section_2_audit


def test_run_master_section_2_audit():
    """Verify that all Section 2 specifications, shortlisted models, and decoupling partitions pass audit."""
    res = run_master_section_2_audit()
    assert res["status"] == "PASS"
    assert res["checks_failed"] == 0
    assert res["checks_passed"] >= 3
    
    # Check that all shortlisted models achieved R2 >= 0.85
    models = res["details"]["shortlisted_models_execution"]["models"]
    for m_name, m_info in models.items():
        assert m_info["fit_success"] is True
        assert m_info["passed_threshold"] is True
