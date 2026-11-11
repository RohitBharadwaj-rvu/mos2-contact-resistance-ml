"""
Unit tests for quantitative design rules extraction (Sprint 5.c.3).
"""

import json
from pathlib import Path
import pytest
from src.interpretability.design_rules_extractor import (
    compute_design_thresholds,
    generate_technology_recommendations,
    run_design_rules_extraction,
    DESIGN_RULES_JSON_PATH,
    DESIGN_RULES_MD_PATH
)


def test_compute_design_thresholds():
    res = compute_design_thresholds(rc_target_ohm_um=100.0)
    assert res["target_rc_ohm_um"] == 100.0
    assert pytest.approx(res["target_rc_dex"], rel=1e-3) == 2.0
    assert "Phi_B_max" in res["governing_design_formula"]
    assert len(res["scenario_thresholds"]) >= 4

    # High gating scenario should be achievable
    peak_gating = [s for s in res["scenario_thresholds"] if s["gate_carrier_density_cm2"] >= 2.0e13][0]
    assert peak_gating["is_target_achievable"] is True
    assert peak_gating["max_tolerable_sbh_ev"] > 0.0


def test_compute_design_thresholds_500():
    res = compute_design_thresholds(rc_target_ohm_um=500.0)
    assert res["target_rc_ohm_um"] == 500.0
    assert pytest.approx(res["target_rc_dex"], rel=1e-3) == 2.69897
    assert len(res["scenario_thresholds"]) >= 4


def test_generate_technology_recommendations():
    recs = generate_technology_recommendations()
    assert len(recs) == 4
    for r in recs:
        assert "scenario_id" in r
        assert "application" in r
        assert "target_rc" in r
        assert "recommended_contact_strategy" in r
        assert "interface_engineering" in r
        assert "gate_dielectric_spec" in r
        assert "thermal_budget_limit" in r


def test_run_design_rules_extraction_pipeline():
    output = run_design_rules_extraction()
    assert "threshold_tables" in output
    assert "technology_recommendations" in output
    assert DESIGN_RULES_JSON_PATH.exists()
    assert DESIGN_RULES_MD_PATH.exists()

    with open(DESIGN_RULES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "target_100_ohm_um" in data["threshold_tables"]

    with open(DESIGN_RULES_MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()
    assert "Executive Summary & Governing Physical Design Equation" in md_text
    assert "Sub-100" in md_text
