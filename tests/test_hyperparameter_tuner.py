"""
Unit tests for Sprint 4.c.2: Systematic Hyperparameter Tuning.
"""

import pytest
import json
from pathlib import Path
from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.hyperparameter_tuner import (
    get_tuning_grid,
    tune_single_architecture,
    run_systematic_hyperparameter_tuning,
    TUNED_HYPERPARAMS_JSON
)
from src.validation.splitting_protocol import get_cv_splits
from src.models.sample_complexity_analyzer import select_parsimonious_features


def test_get_tuning_grid():
    models = [
        "Ridge_Regression",
        "ElasticNet",
        "Gradient_Boosting",
        "Random_Forest",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]
    for m in models:
        grid = get_tuning_grid(m)
        assert isinstance(grid, list)
        assert len(grid) > 0
        assert isinstance(grid[0], dict)


def test_tune_single_architecture():
    df = get_cleaned_and_engineered_dataset()
    splits = get_cv_splits(df, scheme="grouped_5fold")
    features = select_parsimonious_features(df, max_features=4)
    X = df[features].copy()
    y = df["log10_rc"].values

    res = tune_single_architecture("Ridge_Regression", X, y, splits)
    assert res["model_name"] == "Ridge_Regression"
    assert "best_params" in res
    assert "best_composite_score" in res
    assert res["best_composite_score"] > 0.70
    assert "sensitivity_analysis" in res
    assert res["sensitivity_analysis"]["total_combinations_tested"] >= 5


def test_run_systematic_hyperparameter_tuning():
    res = run_systematic_hyperparameter_tuning()
    assert "models_tuned" in res
    assert len(res["models_tuned"]) == 6
    assert TUNED_HYPERPARAMS_JSON.exists()

    with open(TUNED_HYPERPARAMS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "models_tuned" in data
    assert "Gradient_Boosting" in data["models_tuned"]
    gb = data["models_tuned"]["Gradient_Boosting"]
    assert gb["best_composite_score"] > 0.70
