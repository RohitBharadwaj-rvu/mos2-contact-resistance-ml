"""Tests for Benchmark Compilations Registry."""

from src.data.benchmark_sources import (
    load_benchmark_compilations,
    get_total_reported_data_points,
    get_all_covered_metals,
    get_benchmark_by_id
)


def test_load_benchmark_compilations():
    benchmarks = load_benchmark_compilations()
    assert len(benchmarks) >= 5
    ids = [b["id"] for b in benchmarks]
    assert "allain_2015_natmat" in ids
    assert "shen_2021_nature" in ids
    assert "liu_2018_nature" in ids


def test_total_data_points():
    total_pts = get_total_reported_data_points()
    assert total_pts >= 150  # Over 150 compiled experimental points in literature reviews


def test_covered_metals():
    metals = get_all_covered_metals()
    for expected in ["Ti", "Au", "Pd", "Sc", "Ni", "Bi", "In"]:
        assert expected in metals


def test_get_benchmark_by_id():
    b = get_benchmark_by_id("shen_2021_nature")
    assert b is not None
    assert b["journal"] == "Nature"
    assert "Bi" in b["metals_covered"]
