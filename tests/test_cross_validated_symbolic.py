"""
Unit tests for Cross-Validated Symbolic Regression & Held-Out Law Evaluation (Sprint 7.6).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd

from src.models.cross_validated_symbolic_engine import (
    SymbolicEquationModel,
    build_candidate_symbolic_equations,
    evaluate_symbolic_equations_out_of_fold,
    SYMBOLIC_BENCHMARK_JSON,
    SYMBOLIC_FIGURE_PATH
)


def test_symbolic_equation_model_fit_predict():
    def toy_func(X, a, b):
        return a * X[:, 0] + b * X[:, 1]

    m = SymbolicEquationModel(
        name="toy",
        latex_formula="y = a x0 + b x1",
        func=toy_func,
        p0=[1.0, 1.0]
    )
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    y = np.array([5.0, 11.0, 17.0, 23.0])  # y = 1*x0 + 2*x1

    m.fit(X, y)
    assert m.params_ is not None
    preds = m.predict(X)
    assert np.allclose(preds, y, atol=0.1)


def test_build_candidate_symbolic_equations():
    candidates = build_candidate_symbolic_equations()
    assert "Linear_Scaling_Baseline" in candidates
    assert "Thermionic_Field_Emission_Law" in candidates
    assert "Reactivity_Depinning_Closed_Form" in candidates
    assert "Discovered_Compact_GP_Law" in candidates

    for name, c in candidates.items():
        assert "latex" in c
        assert "complexity" in c
        assert callable(c["model_factory"])


def test_symbolic_benchmark_file_and_figure_exist():
    assert SYMBOLIC_BENCHMARK_JSON.exists()
    assert SYMBOLIC_FIGURE_PATH.exists()

    with open(SYMBOLIC_BENCHMARK_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "scientific_qualification" in data
    assert "Discovered_Compact_GP_Law" in data["equations"]
    gp_law = data["equations"]["Discovered_Compact_GP_Law"]
    assert gp_law["leave_one_group_out"]["rmse_dex"] < 0.45
    assert gp_law["leave_one_group_out"]["spearman_rho"] > 0.85
