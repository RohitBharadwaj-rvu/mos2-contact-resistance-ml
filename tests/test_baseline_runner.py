"""
Tests for Baseline Cross-Validation Runner (Sprint 4.b.1).
"""

from pathlib import Path
import json
import pytest
from src.models.baseline_runner import (
    run_all_baseline_models_cv,
    BASELINE_RUNS_JSON
)


def test_run_all_baseline_models_cv():
    """Verify execution of baseline cross-validation runs under GroupKFold."""
    res = run_all_baseline_models_cv(scheme="grouped_5fold")
    
    assert res["validation_scheme"] == "grouped_5fold"
    assert res["n_samples"] >= 20
    
    models = res["baseline_models"]
    expected_baselines = [
        "mean_baseline",
        "median_baseline",
        "pure_physics_schottky",
        "ordinary_least_squares",
        "ridge_regression",
        "lasso_regression",
        "elastic_net"
    ]
    for b in expected_baselines:
        assert b in models
        m_rep = models[b]
        assert "composite_selection_score" in m_rep
        assert "oof_predictions" in m_rep
        assert len(m_rep["oof_predictions"]) == res["n_samples"]
        
    # Ridge should be qualified and outscore mean baseline
    assert models["ridge_regression"]["composite_selection_score"] > models["mean_baseline"]["composite_selection_score"]
    assert models["ridge_regression"]["is_qualified_for_deployment"] is True
    
    assert BASELINE_RUNS_JSON.exists()
