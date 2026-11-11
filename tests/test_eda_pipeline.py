"""
Tests for Consolidated EDA Pipeline.
"""

from pathlib import Path
import pytest
from src.visualization.eda_pipeline import run_full_eda_suite


def test_run_full_eda_suite():
    """Verify that complete EDA suite executes end-to-end and creates all artifacts."""
    res = run_full_eda_suite()
    
    assert res["status"] == "success"
    assert res["n_samples"] >= 20
    
    figures = res["figures"]
    for name, path_str in figures.items():
        p = Path(path_str)
        assert p.exists(), f"Figure {name} was not generated at {path_str}"
        assert p.stat().st_size > 1000, f"Figure {name} file is too small"
        
    recs = res["recommendations_summary"]
    assert "dataset_scale" in recs
    assert "target_formulation" in recs
