"""
Tests for Master Section 1 Audit Pipeline.
"""

import pytest
from src.data.master_data_audit import run_master_section_1_audit


def test_run_master_section_1_audit():
    """Verify that all Section 1 artifacts, physical sanity bounds, and files pass audit."""
    res = run_master_section_1_audit()
    assert res["status"] == "PASS"
    assert res["checks_failed"] == 0
    assert res["checks_passed"] >= 5
