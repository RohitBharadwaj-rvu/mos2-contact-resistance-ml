"""
Unit tests for Sprint 5.c.2: 2D Regime Phase Diagram Visualizer.
"""

import pytest
import json
from pathlib import Path
from src.visualization.regime_map_visualizer import (
    generate_regime_phase_diagram_data,
    REGIME_MAP_JSON_PATH,
    REGIME_MAP_PNG_PATH,
    WORKFUNCTION_MAP_PNG_PATH
)


def test_generate_regime_phase_diagram_data():
    res = generate_regime_phase_diagram_data(grid_res=20)
    assert "regime_thresholds_dex" in res
    assert "white_space_regions" in res
    assert len(res["white_space_regions"]) >= 2
    assert res["literature_device_count"] == 20

    assert REGIME_MAP_JSON_PATH.exists()
    assert REGIME_MAP_PNG_PATH.exists()
    assert WORKFUNCTION_MAP_PNG_PATH.exists()
    assert REGIME_MAP_PNG_PATH.stat().st_size > 50000
    assert WORKFUNCTION_MAP_PNG_PATH.stat().st_size > 50000
