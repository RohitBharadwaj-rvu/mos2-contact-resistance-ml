"""
Unit tests for Sprint 5.b.2: Intrinsic vs Extrinsic Decomposition.
"""

import pytest
import json
from pathlib import Path
from src.interpretability.decoupling_decomposer import (
    run_intrinsic_extrinsic_decomposition,
    DECOUPLING_RESULTS_JSON,
    DECOUPLING_PNG_PATH
)


def test_run_intrinsic_extrinsic_decomposition():
    res = run_intrinsic_extrinsic_decomposition()
    assert "variance_decomposition" in res
    assert "device_decompositions" in res
    assert len(res["device_decompositions"]) == 20

    v = res["variance_decomposition"]
    assert "pct_variance_explained_intrinsic" in v
    assert "pct_variance_explained_extrinsic" in v
    assert "pct_variance_unexplained_noise" in v
    assert v["pct_variance_explained_intrinsic"] > 60.0
    assert v["pct_variance_explained_extrinsic"] > 0.0

    # Sum of percentages should approximately equal 100
    total_pct = v["pct_variance_explained_intrinsic"] + v["pct_variance_explained_extrinsic"] + v["pct_variance_unexplained_noise"]
    assert 99.0 <= total_pct <= 101.0

    assert DECOUPLING_RESULTS_JSON.exists()
    assert DECOUPLING_PNG_PATH.exists()
    assert DECOUPLING_PNG_PATH.stat().st_size > 50000
