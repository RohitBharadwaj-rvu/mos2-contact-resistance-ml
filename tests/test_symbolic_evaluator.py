"""
Unit tests for Sprint 4.d.3: Symbolic Regression Accuracy-Complexity & Physical Validity Evaluator.
"""

import pytest
import json
from pathlib import Path
from src.models.symbolic_evaluator import (
    evaluate_equation_physics,
    audit_all_discovered_symbolic_equations,
    AUDITED_EQUATIONS_JSON
)


def test_evaluate_equation_physics_valid():
    # Physically sound equation: Rc increases with sbh, decreases with n2d
    expr = "x_sbh - x_n2d + 3.66"
    res = evaluate_equation_physics(expr)
    assert res["phi_monotonic"] is True
    assert res["n2d_monotonic"] is True
    assert res["quantum_limit_satisfied"] is True
    assert res["passes_all_physics"] is True


def test_evaluate_equation_physics_invalid():
    # Unphysical equation: Rc decreases with sbh
    expr = "-2.0 * x_sbh + x_n2d"
    res = evaluate_equation_physics(expr)
    assert res["phi_monotonic"] is False
    assert res["passes_all_physics"] is False


def test_audit_all_discovered_symbolic_equations():
    res = audit_all_discovered_symbolic_equations()
    assert "recommended_symbolic_model" in res
    assert "audited_equations" in res
    assert len(res["audited_equations"]) >= 1

    rec = res["recommended_symbolic_model"]
    assert rec["oof_rmse"] < 0.50
    assert rec["composite_score"] > 0.70

    assert AUDITED_EQUATIONS_JSON.exists()
    with open(AUDITED_EQUATIONS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "recommended_symbolic_model" in data
