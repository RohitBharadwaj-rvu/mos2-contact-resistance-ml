"""
Unit tests for Sprint 4.e.2: Literature Outlier Investigation.
"""

import pytest
import json
from pathlib import Path
from src.data.literature_outlier_tracer import (
    trace_literature_outliers,
    CASE_STUDIES_JSON,
    CASE_STUDIES_MD,
    OUTLIER_LITERATURE_METADATA
)


def test_outlier_literature_metadata():
    assert "SRC-EXP-2014-KAPPERA" in OUTLIER_LITERATURE_METADATA
    assert "SRC-EXP-2018-LIU" in OUTLIER_LITERATURE_METADATA
    assert "SRC-EXP-2014-MCDONNELL" in OUTLIER_LITERATURE_METADATA


def test_trace_literature_outliers():
    res = trace_literature_outliers()
    assert "total_outliers_analyzed" in res
    assert res["total_outliers_analyzed"] >= 1
    assert "case_studies" in res
    assert len(res["case_studies"]) == res["total_outliers_analyzed"]

    for cs in res["case_studies"]:
        assert "citation" in cs
        assert "physical_root_cause" in cs
        assert "discrepancy_classification" in cs
        assert len(cs["physical_root_cause"]) > 20

    assert CASE_STUDIES_JSON.exists()
    assert CASE_STUDIES_MD.exists()
    assert CASE_STUDIES_MD.stat().st_size > 500
