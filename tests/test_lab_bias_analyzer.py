"""
Tests for Inter-Paper Variance and Lab Bias Analyzer (Sprint 1.f.4).
"""

from pathlib import Path
import json
import pytest
from src.visualization.lab_bias_analyzer import (
    analyze_inter_paper_variance,
    generate_variance_plots,
    VARIANCE_JSON_PATH,
    VARIANCE_PNG_PATH
)


def test_analyze_inter_paper_variance():
    """Verify statistical decomposition of variance across literature sources."""
    summary = analyze_inter_paper_variance()
    
    assert summary["total_source_papers"] >= 5
    assert "anova_f_statistic" in summary
    assert "anova_p_value" in summary
    assert "group_statistics" in summary
    assert "ti_cross_paper_benchmark" in summary
    
    # Check that Ti benchmarks exist across multiple papers
    ti_benchmarks = summary["ti_cross_paper_benchmark"]
    assert len(ti_benchmarks) >= 2
    uids = {item["source_uid"] for item in ti_benchmarks}
    assert len(uids) >= 2, "Ti contacts should be represented in at least 2 distinct papers"
    
    # Check output json file
    assert VARIANCE_JSON_PATH.exists()
    with open(VARIANCE_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["total_source_papers"] == summary["total_source_papers"]


def test_generate_variance_plots():
    """Verify generation of publication grouped boxplots and Ti cross-lab bar chart."""
    output_path = generate_variance_plots()
    assert output_path.exists()
    assert output_path.stat().st_size > 1000
    assert output_path == VARIANCE_PNG_PATH
