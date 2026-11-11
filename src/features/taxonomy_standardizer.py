"""
Categorical Taxonomy Standardizer.
Maps raw free-text experimental descriptions to canonical categories.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "categorical_taxonomies.json"


def load_categorical_taxonomies() -> Dict[str, Any]:
    """Loads canonical category mappings."""
    if not TAXONOMY_PATH.exists():
        raise FileNotFoundError(f"Taxonomy file not found at {TAXONOMY_PATH}")
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def standardize_deposition_method(raw_text: str) -> str:
    """Standardizes raw deposition description."""
    tax = load_categorical_taxonomies()
    mappings = tax.get("deposition_method_mappings", {})
    clean = raw_text.strip().lower()
    return mappings.get(clean, "Thermal_Evaporation")


def standardize_contact_architecture(raw_text: str) -> str:
    """Standardizes raw architecture description."""
    tax = load_categorical_taxonomies()
    mappings = tax.get("architecture_mappings", {})
    clean = raw_text.strip().lower()
    return mappings.get(clean, "Top_Contact")


def standardize_gate_dielectric(raw_text: str) -> str:
    """Standardizes gate dielectric text."""
    tax = load_categorical_taxonomies()
    mappings = tax.get("dielectric_mappings", {})
    clean = raw_text.strip().lower()
    return mappings.get(clean, "SiO2")


def standardize_annealing_ambient(raw_text: Optional[str]) -> str:
    """Standardizes post-annealing ambient gas."""
    if not raw_text:
        return "None"
    tax = load_categorical_taxonomies()
    mappings = tax.get("annealing_ambient_mappings", {})
    clean = raw_text.strip().lower()
    return mappings.get(clean, "None")
