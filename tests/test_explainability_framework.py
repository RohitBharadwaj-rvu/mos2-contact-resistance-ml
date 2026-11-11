"""
Tests for Post-Hoc Explainability Framework (Sprint 2.e.1).
"""

from pathlib import Path
import json
import pytest
from src.models.explainability_framework import (
    evaluate_post_hoc_explanation_frameworks,
    compute_prototype_permutation_importance,
    EXPLAINABILITY_JSON
)


def test_evaluate_post_hoc_explanation_frameworks():
    """Verify methods catalog covers TreeSHAP, KernelSHAP, Permutation, and PDP."""
    spec = evaluate_post_hoc_explanation_frameworks()
    
    assert "methods" in spec
    names = [m["name"] for m in spec["methods"]]
    assert "TreeSHAP" in names
    assert "KernelSHAP" in names
    assert "Permutation_Feature_Importance" in names
    assert "Partial_Dependence_PDP" in names
    
    assert EXPLAINABILITY_JSON.exists()
    with open(EXPLAINABILITY_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["methods"]) == len(spec["methods"])


def test_compute_prototype_permutation_importance():
    """Verify permutation feature importance computes non-negative mean degradation on real data."""
    importances = compute_prototype_permutation_importance("Gradient_Boosting")
    assert len(importances) >= 3
    # Gate density and predicted barrier should have highest permutation degradation
    top_feature = max(importances, key=importances.get)
    assert top_feature in ["gate_carrier_density_cm2", "physics_predicted_sbh_ev"]
    assert importances[top_feature] > 0.05
