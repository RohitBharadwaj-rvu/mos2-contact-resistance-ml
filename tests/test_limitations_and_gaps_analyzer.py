"""
Unit tests for model limitations and dataset gaps analyzer (Sprint 6.a.3).
"""

import json
from pathlib import Path
import pytest

from src.physics.limitations_and_gaps_analyzer import (
    analyze_dataset_distributions_and_biases,
    define_physical_validity_envelopes,
    define_future_experimental_priorities,
    run_limitations_and_gaps_pipeline,
    LIMITATIONS_JSON_PATH,
    LIMITATIONS_MD_PATH,
    GAPS_FIGURE_PATH
)


def test_analyze_dataset_distributions_and_biases():
    biases = analyze_dataset_distributions_and_biases()
    assert biases["n_samples"] == 20
    assert "vdw_count" in biases["contact_type_split"]
    assert len(biases["major_literature_biases"]) >= 3
    assert biases["carrier_density_coverage_cm2"]["min"] > 0


def test_define_physical_validity_envelopes():
    env = define_physical_validity_envelopes()
    assert "gate_carrier_density" in env
    assert "schottky_barrier_height" in env
    assert "thermal_budget_limits" in env
    assert env["gate_carrier_density"]["valid_range_cm2"][0] == 1.0e11
    assert env["schottky_barrier_height"]["valid_range_ev"][1] == 1.20


def test_define_future_experimental_priorities():
    priorities = define_future_experimental_priorities()
    assert len(priorities) == 5
    for p in priorities:
        assert "priority_rank" in p
        assert "title" in p
        assert "rationale" in p
        assert "target_measurement" in p


def test_run_limitations_and_gaps_pipeline():
    output = run_limitations_and_gaps_pipeline()
    assert LIMITATIONS_JSON_PATH.exists()
    assert LIMITATIONS_MD_PATH.exists()
    assert GAPS_FIGURE_PATH.exists()

    with open(LIMITATIONS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "dataset_biases" in data
    assert "validity_envelopes" in data
    assert "future_experimental_priorities" in data
