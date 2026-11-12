"""
Unit tests for Sprint 4.d.2: Symbolic Regression Search Runner.
"""

import pytest
import json
from pathlib import Path
from src.models.symbolic_search_runner import (
    program_to_sympy_str,
    run_symbolic_search_across_complexity_levels,
    PARETO_FRONTIER_JSON
)


def test_program_to_sympy_str():
    prog = "add(X0, inv(X1))"
    res = program_to_sympy_str(prog)
    assert "x_sbh" in res
    assert "x_n2d" in res


def test_run_symbolic_search_across_complexity_levels():
    if PARETO_FRONTIER_JSON.exists():
        with open(PARETO_FRONTIER_JSON, "r", encoding="utf-8") as f:
            res = json.load(f)
    else:
        res = run_symbolic_search_across_complexity_levels()
    assert "discovered_equations" in res
    assert len(res["discovered_equations"]) == 4
    assert "pareto_frontier" in res
    assert len(res["pareto_frontier"]) >= 1

    for eq in res["discovered_equations"]:
        assert "clean_algebraic_expression" in eq
        assert "oof_rmse" in eq
        assert "complexity_length" in eq
        assert eq["complexity_length"] > 0
        assert eq["oof_rmse"] < 1.0

    assert PARETO_FRONTIER_JSON.exists()
    with open(PARETO_FRONTIER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["discovered_equations"]) == 4
