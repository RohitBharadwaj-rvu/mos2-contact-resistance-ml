"""
Tests for Symbolic Regression Survey (Sprint 2.d.1).
"""

from pathlib import Path
import json
import pytest
from src.models.symbolic_survey import (
    survey_symbolic_regression_frameworks,
    SYMBOLIC_SURVEY_JSON
)


def test_survey_symbolic_regression_frameworks():
    """Verify that survey covers core symbolic frameworks and identifies primary implementation."""
    survey = survey_symbolic_regression_frameworks()
    
    assert "frameworks" in survey
    names = [f["name"] for f in survey["frameworks"]]
    assert "gplearn" in names
    assert "PySR" in names
    assert "PySINDy" in names
    
    # Primary recommended framework should be gplearn
    primary = [f for f in survey["frameworks"] if f["status"] == "PRIMARY_RECOMMENDED"][0]
    assert primary["name"] == "gplearn"
    assert primary["suitability_score"] >= 9.0
    
    assert SYMBOLIC_SURVEY_JSON.exists()
    with open(SYMBOLIC_SURVEY_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["frameworks"]) == len(survey["frameworks"])
