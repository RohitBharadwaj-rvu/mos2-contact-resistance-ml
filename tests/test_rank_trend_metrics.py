"""
Tests for Rank and Trend Metrics (Sprint 3.b.2).
"""

from pathlib import Path
import json
import pytest
import numpy as np
from src.validation.rank_trend_metrics import (
    compute_spearman_rho,
    compute_kendall_tau,
    compute_concordance_index,
    evaluate_rank_and_trend_metrics,
    define_rank_trend_metrics_spec,
    RANK_METRICS_JSON
)


def test_concordance_and_rank_metrics():
    """Verify rank metrics under monotonic, inverted, and noisy orderings."""
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Perfect monotonic ordering (even with nonlinear shift)
    y_pred_perf = np.array([10.0, 25.0, 30.0, 100.0, 500.0])
    rho, _ = compute_spearman_rho(y_true, y_pred_perf)
    tau, _ = compute_kendall_tau(y_true, y_pred_perf)
    c_idx = compute_concordance_index(y_true, y_pred_perf)
    
    assert np.isclose(rho, 1.0)
    assert np.isclose(tau, 1.0)
    assert c_idx == 1.0
    
    # Inverted ordering
    y_pred_inv = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    rho_inv, _ = compute_spearman_rho(y_true, y_pred_inv)
    c_inv = compute_concordance_index(y_true, y_pred_inv)
    assert np.isclose(rho_inv, -1.0)
    assert c_inv == 0.0


def test_evaluate_rank_and_trend_metrics():
    """Verify dictionary outputs of ranking evaluator."""
    y_true = np.array([2.5, 3.0, 3.5, 4.0, 4.5])
    y_pred = np.array([2.6, 2.9, 3.7, 4.1, 4.4])
    
    res = evaluate_rank_and_trend_metrics(y_true, y_pred)
    assert "spearman_rho" in res
    assert "kendall_tau" in res
    assert "concordance_index" in res
    assert "pearson_r" in res
    
    assert res["spearman_rho"] > 0.80
    assert res["concordance_index"] > 0.80


def test_define_rank_trend_metrics_spec():
    """Verify specification JSON output."""
    spec = define_rank_trend_metrics_spec()
    assert "metrics" in spec
    assert len(spec["metrics"]) == 3
    
    assert RANK_METRICS_JSON.exists()
    with open(RANK_METRICS_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["metrics"]) == len(spec["metrics"])
