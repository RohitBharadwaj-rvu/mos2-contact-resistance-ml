"""
Tests for Baseline Models (Sprint 2.b.1).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd
from src.models.baseline_models import (
    MeanBaselineRegressor,
    MedianBaselineRegressor,
    PurePhysicsSchottkyBaseline,
    define_naive_statistical_baselines,
    evaluate_baselines_on_curated_data,
    BASELINE_DEF_JSON
)


def test_mean_and_median_regressors():
    """Verify statistical properties of naive estimators."""
    y = np.array([2.0, 3.0, 4.0, 10.0])
    X = np.zeros((4, 2))
    
    mean_reg = MeanBaselineRegressor().fit(X, y)
    preds_mean = mean_reg.predict(X)
    assert np.allclose(preds_mean, 4.75)
    
    median_reg = MedianBaselineRegressor().fit(X, y)
    preds_median = median_reg.predict(X)
    assert np.allclose(preds_median, 3.5)


def test_pure_physics_schottky_baseline():
    """Verify physical bounds and scaling of unpinned thermionic reference."""
    X_df = pd.DataFrame({"work_function_ev": [4.0, 4.5, 5.2]})
    phys_reg = PurePhysicsSchottkyBaseline()
    preds = phys_reg.predict(X_df)
    
    assert len(preds) == 3
    # Higher work function metal should yield higher contact resistance
    assert preds[2] >= preds[1] >= preds[0]


def test_evaluate_baselines_on_curated_data():
    """Verify baseline evaluation returns valid error metrics on real dataset."""
    scores = evaluate_baselines_on_curated_data()
    assert "mean_baseline" in scores
    assert "median_baseline" in scores
    assert "pure_physics_schottky" in scores
    
    # Root mean squared error must be positive
    assert scores["mean_baseline"]["rmse_log10_rc"] > 0.0
    assert scores["mean_baseline"]["mae_log10_rc"] > 0.0
    
    assert BASELINE_DEF_JSON.exists()
