"""
Source Accessibility and Export Tool Evaluator.
Ranks discovery sources by API accessibility, export formats, and automated citation tracking capabilities.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

MATRIX_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "source_accessibility_matrix.json"


def load_accessibility_matrix() -> Dict[str, Any]:
    """Loads source accessibility evaluation matrix."""
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"Matrix file not found at {MATRIX_PATH}")
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def rank_sources_by_accessibility(category: str = "literature_indexes") -> List[Tuple[str, float, str]]:
    """
    Ranks sources in descending order of accessibility score.
    Returns list of tuples: (source_id, accessibility_score, recommended_role).
    """
    matrix = load_accessibility_matrix()
    items = matrix.get(category, {})
    ranked = sorted(
        [(k, v["accessibility_score"], v["recommended_role"]) for k, v in items.items()],
        key=lambda x: x[1],
        reverse=True
    )
    return ranked


def get_export_formats_summary() -> Dict[str, List[str]]:
    """Maps each literature source to its supported export formats."""
    matrix = load_accessibility_matrix()
    summary = {}
    for src_id, data in matrix.get("literature_indexes", {}).items():
        summary[src_id] = data.get("export_formats", [])
    return summary


def get_primary_extraction_pipeline_recommendation() -> Dict[str, str]:
    """Returns the operational recommendation for literature mining and physical property gathering."""
    return {
        "literature_discovery": "OpenAlex REST API (CC0) + Crossref API for programmatic retrieval and DOI normalization",
        "citation_expansion": "OpenAlex forward/backward citation graph traversal",
        "high_impact_reviews": "Targeted full-text parsing of Nature, IEEE, ACS, and Chem Soc Rev landmark papers",
        "2d_materials_properties": "C2DB (DTU Computational 2D Materials Database)",
        "bulk_metal_properties": "NIST Standard Reference Data + CRC Handbook + Materials Project"
    }
