"""
Unit tests for Sprint 4.c.1: Hyperparameter Search Space Catalog.
"""

import pytest
import json
from pathlib import Path
from src.models.hyperparameter_spaces import (
    define_hyperparameter_search_spaces,
    HYPERPARAMS_JSON_PATH
)


def test_define_hyperparameter_search_spaces():
    spec = define_hyperparameter_search_spaces()
    assert isinstance(spec, dict)
    assert "search_spaces" in spec
    spaces = spec["search_spaces"]
    
    # Must cover key shortlisted architectures
    expected_models = [
        "Ridge_Regression",
        "ElasticNet",
        "Gradient_Boosting",
        "Random_Forest",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]
    for m in expected_models:
        assert m in spaces
        assert "search_grid" in spaces[m]
        assert "regularization_mechanism" in spaces[m]
        assert len(spaces[m]["regularization_mechanism"]) > 10

    # Ensure JSON file is created and readable
    assert HYPERPARAMS_JSON_PATH.exists()
    with open(HYPERPARAMS_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["title"] == spec["title"]
    assert "Ridge_Regression" in loaded["search_spaces"]
