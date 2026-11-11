"""
Tests for Learning Task Formulation (Sprint 2.a.1).
"""

from pathlib import Path
import json
import pytest
from src.models.task_formulation import (
    evaluate_target_correlations,
    define_learning_task_specifications,
    TASK_SPEC_JSON
)


def test_evaluate_target_correlations():
    """Verify statistical coupling between targets log10(Rc) and SBH."""
    res = evaluate_target_correlations()
    assert res["n_samples"] >= 15
    assert res["pearson_r"] > 0.70, "Rc and SBH must exhibit strong positive correlation"


def test_define_learning_task_specifications():
    """Verify task formulation schema and recommendations."""
    spec = define_learning_task_specifications()
    
    assert spec["primary_task"]["target_variable"] == "log10_rc"
    assert spec["auxiliary_task"]["target_variable"] == "schottky_barrier_height_ev"
    assert spec["formulations"]["independent_single_task"]["recommended"] is True
    assert spec["formulations"]["physics_chained_hybrid"]["recommended"] is True
    
    assert TASK_SPEC_JSON.exists()
    with open(TASK_SPEC_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["primary_task"]["name"] == spec["primary_task"]["name"]
