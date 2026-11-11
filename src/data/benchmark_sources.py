"""
Benchmark Compilations and Review Literature Access Module.
Manages metadata and data point extraction registries from landmark review papers.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

BENCHMARK_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "benchmark_compilations.json"


def load_benchmark_compilations() -> List[Dict[str, Any]]:
    """Loads metadata for pre-existing literature benchmarks and reviews."""
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(f"Benchmark compilations not found at {BENCHMARK_PATH}")
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_total_reported_data_points() -> int:
    """Calculates total experimental data points tabulated across surveyed benchmark reviews."""
    benchmarks = load_benchmark_compilations()
    return sum(b.get("data_points_reported", 0) for b in benchmarks)


def get_all_covered_metals() -> List[str]:
    """Returns a sorted deduplicated list of all contact metals covered across benchmarks."""
    benchmarks = load_benchmark_compilations()
    metals = set()
    for b in benchmarks:
        metals.update(b.get("metals_covered", []))
    return sorted(list(metals))


def get_benchmark_by_id(benchmark_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific benchmark compilation by ID."""
    benchmarks = load_benchmark_compilations()
    for b in benchmarks:
        if b["id"] == benchmark_id:
            return b
    return None
