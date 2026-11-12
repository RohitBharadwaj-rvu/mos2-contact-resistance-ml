"""
Unit tests for Nested GroupKFold and LOGO Validation Benchmark Suite (Sprint 7.4).
"""

from pathlib import Path
import pytest
import numpy as np
import pandas as pd

from src.validation.nested_grouped_cv import (
    get_candidate_model_registry,
    run_inner_tuning_loop,
    evaluate_nested_group_kfold,
    evaluate_leave_one_group_out,
    BENCHMARK_JSON_PATH,
    FIGURE_PATH
)


def test_get_candidate_model_registry():
    reg = get_candidate_model_registry()
    assert "Ridge_Regression" in reg
    assert "ElasticNet" in reg
    assert "Random_Forest" in reg
    assert "Hist_Gradient_Boosting" in reg
    assert "Gaussian_Process_Matern" in reg

    for name, config in reg.items():
        assert "estimator_class" in config
        assert "param_grid" in config
        assert len(config["param_grid"]) >= 1


def test_run_inner_tuning_loop():
    X_tr = pd.DataFrame({
        "feat1": np.linspace(1, 20, 20),
        "feat2": np.linspace(5, 50, 20)
    })
    y_tr = 2.0 * X_tr["feat1"].values + np.random.normal(0, 0.1, 20)
    groups_tr = np.array([f"paper_{i % 5}" for i in range(20)])

    reg = get_candidate_model_registry()
    best_params = run_inner_tuning_loop(X_tr, y_tr, groups_tr, reg["Ridge_Regression"], n_inner_splits=3)
    assert isinstance(best_params, dict)
    assert "alpha" in best_params


def test_evaluate_nested_group_kfold_toy():
    X = pd.DataFrame({
        "f1": np.random.normal(0, 1, 24),
        "f2": np.random.normal(0, 1, 24)
    })
    y = np.random.normal(3, 0.5, 24)
    groups = np.array([f"paper_{i // 4}" for i in range(24)])

    res = evaluate_nested_group_kfold(X, y, groups, n_outer_splits=3)
    assert "Ridge_Regression" in res
    ridge_res = res["Ridge_Regression"]
    assert "rmse_dex" in ridge_res
    assert "spearman_rho" in ridge_res
    assert len(ridge_res["outer_folds"]) == 3
    assert len(ridge_res["oof_predictions"]) == 24


def test_evaluate_leave_one_group_out_toy():
    X = pd.DataFrame({
        "f1": np.random.normal(0, 1, 15),
        "f2": np.random.normal(0, 1, 15)
    })
    y = np.random.normal(3, 0.5, 15)
    groups = np.array([f"src_{i // 3}" for i in range(15)])

    res = evaluate_leave_one_group_out(X, y, groups)
    assert "Ridge_Regression" in res
    ridge_res = res["Ridge_Regression"]
    assert len(ridge_res["paper_breakdown"]) == 5
    assert len(ridge_res["oof_predictions"]) == 15
