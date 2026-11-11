"""
Tests for Regression Error Metrics (Sprint 3.b.1).
"""

from pathlib import Path
import json
import pytest
import numpy as np
from src.validation.regression_metrics import (
    compute_log_rmse,
    compute_log_mae,
    compute_geometric_factor_error,
    compute_linear_medape,
    evaluate_regression_metrics,
    define_regression_error_metrics_spec,
    METRICS_JSON_PATH
)


def test_log_error_metrics():
    """Verify calculation of RMSE, MAE, geometric factor error, and MedAPE."""
    y_true = np.array([2.0, 3.0, 4.0])
    y_pred = np.array([2.0, 3.0, 4.0])
    
    # Perfect predictions
    assert compute_log_rmse(y_true, y_pred) == 0.0
    assert compute_log_mae(y_true, y_pred) == 0.0
    assert compute_geometric_factor_error(y_true, y_pred) == 1.0
    assert compute_linear_medape(10.0**y_true, 10.0**y_pred) == 0.0
    
    # Imperfect predictions (0.3 dex difference = factor of 2.0x)
    y_pred_shift = np.array([2.3, 3.3, 4.3])
    mae = compute_log_mae(y_true, y_pred_shift)
    assert abs(mae - 0.3) < 1e-5
    geom = compute_geometric_factor_error(y_true, y_pred_shift)
    assert abs(geom - 1.995) < 0.01


def test_evaluate_regression_metrics():
    """Verify comprehensive metric dictionary outputs."""
    y_true = np.array([2.0, 3.0, 3.5, 4.0])
    y_pred = np.array([2.1, 2.9, 3.6, 4.2])
    
    res = evaluate_regression_metrics(y_true, y_pred)
    assert "rmse_log10_dex" in res
    assert "mae_log10_dex" in res
    assert "geometric_factor_error" in res
    assert "medape_linear_pct" in res
    assert "r2_log10" in res
    
    assert res["rmse_log10_dex"] > 0.0
    assert res["r2_log10"] > 0.8


def test_define_regression_error_metrics_spec():
    """Verify specification JSON output."""
    spec = define_regression_error_metrics_spec()
    assert "metrics" in spec
    assert len(spec["metrics"]) == 4
    
    assert METRICS_JSON_PATH.exists()
    with open(METRICS_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["metrics"]) == len(spec["metrics"])
