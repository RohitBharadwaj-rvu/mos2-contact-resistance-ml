"""
Unit test for Master Heading 5 Milestone Interpretability Audit.
"""

from src.interpretability.master_interpretability_audit import run_master_interpretability_audit, AUDIT_JSON_PATH


def test_master_heading_5_interpretability_audit():
    res = run_master_interpretability_audit()
    assert res["all_passed"] is True
    assert AUDIT_JSON_PATH.exists()
    assert len(res["subheadings_audited"]) == 3
    assert res["summary_metrics"]["variance_intrinsic_pct"] > 80.0
    assert res["summary_metrics"]["mediation_indirect_pct"] > 80.0
