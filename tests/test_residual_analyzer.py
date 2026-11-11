"""
Unit tests for Sprint 4.e.1: Out-of-Fold Residual Diagnostics.
"""

import pytest
import json
from pathlib import Path
from src.visualization.residual_analyzer import (
    run_residual_diagnostics,
    RESIDUALS_JSON_PATH,
    PARITY_PNG_PATH,
    DIAGNOSTICS_PNG_PATH
)


def test_run_residual_diagnostics():
    res = run_residual_diagnostics()
    assert "residual_statistics" in res
    assert "all_device_residuals" in res
    assert len(res["all_device_residuals"]) == 20
    assert "outlier_count" in res

    stats = res["residual_statistics"]
    assert "mean_residual_dex" in stats
    assert "shapiro_wilk_pvalue" in stats
    assert "heteroskedasticity_pearson_r" in stats

    # Files must exist
    assert RESIDUALS_JSON_PATH.exists()
    assert PARITY_PNG_PATH.exists()
    assert DIAGNOSTICS_PNG_PATH.exists()
    assert PARITY_PNG_PATH.stat().st_size > 50000
    assert DIAGNOSTICS_PNG_PATH.stat().st_size > 50000
