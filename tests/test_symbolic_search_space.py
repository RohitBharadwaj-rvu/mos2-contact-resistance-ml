"""
Tests for Symbolic Search Space and Protected Operators (Sprint 2.d.2).
"""

from pathlib import Path
import json
import pytest
import numpy as np
from src.models.symbolic_search_space import (
    protected_div,
    protected_exp,
    protected_log,
    protected_inv,
    define_symbolic_search_space,
    SEARCH_SPACE_JSON
)


def test_protected_operators():
    """Verify numerical stability of protected mathematical operators under extreme inputs."""
    # Test division by zero
    x1 = np.array([5.0, 10.0])
    x2 = np.array([0.0, 2.0])
    div_res = protected_div(x1, x2)
    assert div_res[0] == 1.0
    assert div_res[1] == 5.0
    assert np.isfinite(div_res).all()
    
    # Test exp overflow
    huge_x = np.array([1000.0, -100.0, 0.0])
    exp_res = protected_exp(huge_x)
    assert np.isfinite(exp_res).all()
    assert exp_res[0] <= np.exp(15.0)
    
    # Test log zero and negative
    bad_x = np.array([0.0, -5.0, 10.0])
    log_res = protected_log(bad_x)
    assert np.isfinite(log_res).all()
    
    # Test inv zero
    inv_res = protected_inv(np.array([0.0, 4.0]))
    assert inv_res[0] == 0.0
    assert inv_res[1] == 0.25


def test_define_symbolic_search_space():
    """Verify search space configuration parameters and physical constraints."""
    cfg = define_symbolic_search_space()
    
    assert "primitive_operators" in cfg
    assert len(cfg["primitive_operators"]) >= 5
    
    assert cfg["complexity_constraints"]["max_nodes"] <= 15
    assert cfg["complexity_constraints"]["max_tree_depth"] <= 5
    
    constraints = cfg["physical_inductive_constraints"]
    assert len(constraints) >= 2
    c_names = [c["constraint"] for c in constraints]
    assert "positive_schottky_monotonicity" in c_names
    assert "negative_gate_monotonicity" in c_names
    
    assert SEARCH_SPACE_JSON.exists()
    with open(SEARCH_SPACE_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["primitive_operators"]) == len(cfg["primitive_operators"])
