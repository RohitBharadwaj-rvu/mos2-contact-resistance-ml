"""
Tests for Sample Complexity and Capacity Constraints (Sprint 2.a.2).
"""

from pathlib import Path
import json
import pytest
from src.models.sample_complexity_analyzer import (
    compute_sample_complexity_constraints,
    select_parsimonious_features,
    COMPLEXITY_JSON_PATH
)


def test_compute_sample_complexity_constraints():
    """Verify calculated capacity limits and feature budgets."""
    constraints = compute_sample_complexity_constraints()
    
    assert constraints["dataset_dimensions"]["n_samples"] >= 20
    assert constraints["feature_budgets"]["recommended_active_features"] <= 5
    assert constraints["model_architecture_constraints"]["decision_tree_ensembles"]["max_depth"] <= 3
    assert constraints["model_architecture_constraints"]["symbolic_regression"]["max_equation_length_nodes"] <= 15
    
    assert COMPLEXITY_JSON_PATH.exists()
    with open(COMPLEXITY_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["dataset_dimensions"]["n_samples"] == constraints["dataset_dimensions"]["n_samples"]


def test_select_parsimonious_features():
    """Verify parsimonious feature selector returns non-collinear physical descriptors."""
    selected = select_parsimonious_features(max_features=4)
    assert len(selected) == 4
    assert "physics_predicted_sbh_ev" in selected
    assert "is_vdw_or_depinned_contact" in selected

