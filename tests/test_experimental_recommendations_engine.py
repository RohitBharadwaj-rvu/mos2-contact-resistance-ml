"""
Unit tests for experimental recommendations engine (Sprint 6.a.2).
"""

import json
from pathlib import Path
import pytest

from src.physics.experimental_recommendations_engine import (
    compute_parameter_roi_ranking,
    generate_laboratory_decision_flowchart,
    run_experimental_recommendations_pipeline,
    ROI_JSON_PATH,
    ROI_FIGURE_PATH
)


def test_compute_parameter_roi_ranking():
    params = compute_parameter_roi_ranking()
    assert len(params) >= 7

    # Verify Tier 1 features have higher impact than Tier 4
    tier_1 = [p for p in params if "Tier 1" in p["tier"]]
    tier_4 = [p for p in params if "Tier 4" in p["tier"]]
    assert len(tier_1) >= 2
    assert len(tier_4) >= 2

    for t1 in tier_1:
        assert t1["max_impact_dex"] > 0.5
        for t4 in tier_4:
            assert t1["max_impact_dex"] > t4["max_impact_dex"]


def test_generate_laboratory_decision_flowchart():
    steps = generate_laboratory_decision_flowchart()
    assert len(steps) == 4
    for s in steps:
        assert "step" in s
        assert "action" in s
        assert "guideline" in s


def test_run_experimental_recommendations_pipeline():
    output = run_experimental_recommendations_pipeline()
    assert "parameter_ranking" in output
    assert "decision_hierarchy" in output
    assert ROI_JSON_PATH.exists()
    assert ROI_FIGURE_PATH.exists()

    with open(ROI_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["parameter_ranking"]) >= 7
