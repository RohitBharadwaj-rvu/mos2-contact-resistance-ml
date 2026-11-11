"""
Tests for Default Non-Linear Architecture Cross-Validation Runner (Sprint 4.b.2).
"""

from pathlib import Path
import json
import pytest
from src.models.nonlinear_runner import (
    run_all_default_nonlinear_models_cv,
    NONLINEAR_RUNS_JSON
)


def test_run_all_default_nonlinear_models_cv():
    """Verify execution of default non-linear models cross-validation under GroupKFold."""
    res = run_all_default_nonlinear_models_cv(scheme="grouped_5fold")
    
    assert res["validation_scheme"] == "grouped_5fold"
    assert res["n_samples"] >= 20
    
    models = res["default_nonlinear_models"]
    expected_models = [
        "Random_Forest",
        "Gradient_Boosting",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]
    for m in expected_models:
        assert m in models
        m_rep = models[m]
        assert "composite_selection_score" in m_rep
        assert "oof_predictions" in m_rep
        assert len(m_rep["oof_predictions"]) == res["n_samples"]
        assert m_rep["underlying_metrics"]["rmse_log10_dex"] < 0.60
        
    assert NONLINEAR_RUNS_JSON.exists()
