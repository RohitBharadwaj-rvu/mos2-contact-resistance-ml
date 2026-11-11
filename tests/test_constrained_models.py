"""
Unit tests for Sprint 4.c.3: Domain-Specific Monotonicity Constraints.
"""

import pytest
import json
import numpy as np
from pathlib import Path
from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.constrained_models import (
    PHYSICAL_MONOTONICITY_RULES,
    get_monotonicity_vector,
    MonotonicLGBMWrapper,
    run_monotonicity_constraint_experiment,
    CONSTRAINTS_COMPARISON_JSON
)


def test_monotonicity_rules_definition():
    assert "physics_predicted_sbh_ev" in PHYSICAL_MONOTONICITY_RULES
    assert PHYSICAL_MONOTONICITY_RULES["physics_predicted_sbh_ev"] == 1
    assert PHYSICAL_MONOTONICITY_RULES["is_vdw_or_depinned_contact"] == -1
    assert PHYSICAL_MONOTONICITY_RULES["gate_carrier_density_cm2"] == -1

    vec = get_monotonicity_vector(["physics_predicted_sbh_ev", "gate_carrier_density_cm2"])
    assert vec == [1, -1]


def test_monotonic_lgbm_fit_predict():
    X = np.array([[0.1, 1e12], [0.3, 5e12], [0.5, 1e13], [0.8, 2e13]])
    y = np.array([2.5, 2.8, 3.2, 3.8])
    model = MonotonicLGBMWrapper(monotone_constraints=[1, -1], n_estimators=10)
    model.fit(X, y)
    preds = model.predict(X)
    assert len(preds) == len(y)
    assert not np.isnan(preds).any()


def test_run_monotonicity_constraint_experiment():
    res = run_monotonicity_constraint_experiment()
    assert "summary_deltas" in res
    assert "lightgbm_unconstrained" in res
    assert "lightgbm_constrained" in res
    assert CONSTRAINTS_COMPARISON_JSON.exists()

    with open(CONSTRAINTS_COMPARISON_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "summary_deltas" in data
