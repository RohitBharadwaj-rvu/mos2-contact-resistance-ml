"""
Unit tests for theoretical models comparison (Sprint 6.a.1).
"""

import json
from pathlib import Path
import pytest

from src.physics.theoretical_models_comparator import (
    compute_landauer_quantum_limit,
    evaluate_fermi_level_pinning_parameter,
    evaluate_thermionic_vs_tunneling_scaling,
    run_theoretical_comparison_pipeline,
    THEORY_COMPARISON_JSON_PATH,
    THEORY_FIGURE_PATH
)


def test_compute_landauer_quantum_limit():
    rc_1e13 = compute_landauer_quantum_limit(1.0e13)
    # Theoretical single-contact 2D ballistic quantum limit is in the range 15 - 45 Ohm*um
    assert 15.0 <= rc_1e13 <= 45.0

    rc_2e13 = compute_landauer_quantum_limit(2.0e13)
    # Inverse square-root scaling with carrier density
    assert rc_2e13 < rc_1e13
    assert pytest.approx(rc_1e13 / rc_2e13, rel=1e-2) == (2.0 ** 0.5)


def test_evaluate_fermi_level_pinning_parameter():
    res = evaluate_fermi_level_pinning_parameter()
    assert "all_contacts" in res
    assert "pinning_parameter_S" in res["all_contacts"]
    # Empirical slope should be positive
    assert res["all_contacts"]["pinning_parameter_S"] >= 0.0


def test_evaluate_thermionic_vs_tunneling_scaling():
    res = evaluate_thermionic_vs_tunneling_scaling()
    assert "ml_slope_dex_per_ev" in res
    assert "pure_thermionic_slope_300k_dex_per_ev" in res
    assert res["scaling_ratio_thermionic_to_ml"] > 5.0
    assert "Thermionic-Field" in res["physical_mechanism_deduction"]


def test_run_theoretical_comparison_pipeline():
    output = run_theoretical_comparison_pipeline()
    assert "quantum_limit_comparison" in output
    assert output["quantum_limit_comparison"]["quantum_bound_respected"] is True
    assert THEORY_COMPARISON_JSON_PATH.exists()
    assert THEORY_FIGURE_PATH.exists()

    with open(THEORY_COMPARISON_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "fermi_level_pinning_analysis" in data
