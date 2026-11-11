"""
Tests for Master Benchmark Leaderboard Aggregator (Subheading 4.b Audit).
"""

from pathlib import Path
import json
import pytest
from src.models.model_benchmark_aggregator import (
    compile_master_benchmark_leaderboard,
    LEADERBOARD_JSON_PATH
)


def test_compile_master_benchmark_leaderboard():
    """Verify aggregation, sorting, and qualification reporting of master leaderboard."""
    board = compile_master_benchmark_leaderboard()
    
    assert board["n_models_evaluated"] == 11
    assert "leaderboard" in board
    assert len(board["leaderboard"]) == 11
    
    # Leaderboard must be strictly descending in composite score
    scores = [m["composite_score"] for m in board["leaderboard"]]
    assert scores == sorted(scores, reverse=True)
    
    # Top model pre-tuning should be a qualified parametric or ensemble model
    top_model = board["leaderboard"][0]
    assert top_model["is_qualified"] is True
    assert top_model["composite_score"] > 0.80
    
    assert LEADERBOARD_JSON_PATH.exists()
