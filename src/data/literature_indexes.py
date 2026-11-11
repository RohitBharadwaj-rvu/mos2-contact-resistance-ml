"""
Scientific Literature Index Registry & Access Tools for Semiconductor Characterization.
Provides metadata, indexing policies, and query capabilities for MoS2 contact literature.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

INDEX_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "literature_indexes.json"


def load_literature_indexes() -> List[Dict[str, Any]]:
    """Loads the catalog of scientific literature indexes and publisher portals."""
    if not INDEX_REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Literature index registry not found at {INDEX_REGISTRY_PATH}")
    with open(INDEX_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_indexes_by_priority(min_priority: str = "High") -> List[Dict[str, Any]]:
    """Filters indexes based on priority tier ('Critical', 'High', etc.)."""
    indexes = load_literature_indexes()
    valid_priorities = ["Critical", "High"] if min_priority == "High" else ["Critical"]
    return [idx for idx in indexes if idx.get("priority_rating") in valid_priorities]


def get_api_capable_indexes() -> List[Dict[str, Any]]:
    """Returns only indexes that support automated programmatic API retrieval."""
    indexes = load_literature_indexes()
    return [idx for idx in indexes if idx.get("api_available", False)]


def summarize_index_registry() -> Dict[str, Any]:
    """Generates summary statistics of surveyed indexes."""
    indexes = load_literature_indexes()
    total = len(indexes)
    api_enabled = sum(1 for idx in indexes if idx.get("api_available"))
    critical = sum(1 for idx in indexes if idx.get("priority_rating") == "Critical")
    all_venues = []
    for idx in indexes:
        all_venues.extend(idx.get("key_venues", []))
    
    return {
        "total_indexes_surveyed": total,
        "api_enabled_count": api_enabled,
        "critical_priority_count": critical,
        "total_key_venues": len(all_venues),
        "venue_list": all_venues
    }


if __name__ == "__main__":
    summary = summarize_index_registry()
    print("Literature Index Survey Summary:")
    print(json.dumps(summary, indent=2))
