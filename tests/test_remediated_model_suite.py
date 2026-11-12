"""
Unit tests for Remediated ML Model Suite & Leaderboard (Sprint 7.5).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd

from src.models.remediated_model_suite import (
    build_full_model_suite_registry,
    run_inner_tuning_loop,
    evaluate_task_nested_and_logo,
    LEADERBOARD_JSON_PATH,
    FIGURE_PATH
)


def test_registry_contains_full_model_families():
    registry = build_full_model_suite_registry()
    expected_models = [
        "Ridge_Regression",
        "ElasticNet",
        "Support_Vector_Regression",
        "Gaussian_Process_Matern",
        "Random_Forest",
        "Extra_Trees",
        "Gradient_Boosting",
        "Hist_Gradient_Boosting"
    ]
    for m in expected_models:
        assert m in registry
        assert "estimator_class" in registry[m]
        assert "param_grid" in registry[m]
        assert "family" in registry[m]
        assert len(registry[m]["param_grid"]) >= 1


def test_inner_tuning_loop_selects_valid_params():
    X_tr = pd.DataFrame({
        "w_m": np.linspace(3.5, 5.5, 20),
        "enthalpy": np.linspace(-300, -50, 20)
    })
    y_tr = 1.2 * X_tr["w_m"].values + 0.01 * X_tr["enthalpy"].values
    groups_tr = np.array([f"lab_{i % 4}" for i in range(20)])

    registry = build_full_model_suite_registry()
    best_p = run_inner_tuning_loop(X_tr, y_tr, groups_tr, registry["Support_Vector_Regression"], n_inner_splits=3)
    assert isinstance(best_p, dict)
    assert "C" in best_p
    assert "epsilon" in best_p


def test_evaluate_task_nested_and_logo_toy():
    X = pd.DataFrame({
        "f1": np.random.normal(0, 1, 24),
        "f2": np.random.normal(0, 1, 24)
    })
    y = np.random.normal(2.5, 0.4, 24)
    groups = np.array([f"paper_{i // 4}" for i in range(24)])

    res = evaluate_task_nested_and_logo(X, y, groups, task_name="Toy Task", target_unit="a.u.")
    assert "models" in res
    assert "Random_Forest" in res["models"]
    rf_data = res["models"]["Random_Forest"]
    assert "nested_group_kfold" in rf_data
    assert "leave_one_group_out" in rf_data
    assert rf_data["nested_group_kfold"]["rmse"] > 0
    assert rf_data["leave_one_group_out"]["rmse"] > 0


def test_leaderboard_file_integrity():
    assert LEADERBOARD_JSON_PATH.exists()
    assert FIGURE_PATH.exists()

    with open(LEADERBOARD_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "task_1_contact_resistance" in data
    assert "task_2_schottky_barrier_height" in data
    t1_models = data["task_1_contact_resistance"]["models"]
    assert "Random_Forest" in t1_models
    assert "LightGBM" in t1_models
    assert t1_models["Random_Forest"]["nested_group_kfold"]["rmse"] < 0.45
