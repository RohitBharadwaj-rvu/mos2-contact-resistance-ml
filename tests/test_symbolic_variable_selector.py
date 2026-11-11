"""
Unit tests for Sprint 4.d.1: Symbolic Input Variable Selector.
"""

import pytest
import json
import numpy as np
import pandas as pd
from pathlib import Path

from src.models.symbolic_variable_selector import (
    select_symbolic_input_variables,
    get_scaled_symbolic_dataset,
    SYMBOLIC_VARS_JSON
)


def test_select_symbolic_input_variables():
    spec = select_symbolic_input_variables()
    assert isinstance(spec, dict)
    assert "variables" in spec
    assert len(spec["variables"]) == 4

    symbols = [v["symbol"] for v in spec["variables"]]
    assert "x_sbh" in symbols
    assert "x_n2d" in symbols
    assert "x_vdw" in symbols
    assert "x_hf" in symbols

    assert "correlations_with_target" in spec
    for s in symbols:
        assert s in spec["correlations_with_target"]

    assert SYMBOLIC_VARS_JSON.exists()
    with open(SYMBOLIC_VARS_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["target_variable"] == "log10_rc"


def test_get_scaled_symbolic_dataset():
    X, y = get_scaled_symbolic_dataset()
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, np.ndarray)
    assert len(X) == 20
    assert len(y) == 20
    assert list(X.columns) == ["x_sbh", "x_n2d", "x_vdw", "x_hf"]
    # Check scaling bounds: should be well conditioned, O(1)
    assert X["x_n2d"].max() <= 5.0
    assert X["x_n2d"].min() >= 0.05
    assert not X.isna().any().any()
    assert not np.isnan(y).any()
