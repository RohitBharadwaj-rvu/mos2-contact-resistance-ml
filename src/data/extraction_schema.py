"""
Extraction Schema Validator and Template Generator.
Validates extracted tabular data rows against the master JSON schema.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "extraction_schema.json"


def load_extraction_schema() -> Dict[str, Any]:
    """Loads the formal extraction JSON schema."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema not found at {SCHEMA_PATH}")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_extraction_row(row: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates a single extracted row dictionary against required fields and physical ranges.
    Returns: (is_valid: bool, error_messages: List[str])
    """
    schema = load_extraction_schema()
    required = schema.get("required", [])
    errors = []
    
    # Check required presence
    for req in required:
        if req not in row or row[req] is None or row[req] == "":
            errors.append(f"Missing mandatory field '{req}'")
            
    # Check physical ranges
    rc = row.get("contact_resistance_rc_ohm_um")
    if rc is not None and rc < 0:
        errors.append(f"Negative contact resistance: {rc}")
        
    sbh = row.get("schottky_barrier_height_ev")
    if sbh is not None and (sbh < 0.0 or sbh > 2.0):
        errors.append(f"Schottky barrier height {sbh} eV out of range [0.0, 2.0]")
        
    temp = row.get("measurement_temperature_k")
    if temp is not None and (temp < 1.0 or temp > 500.0):
        errors.append(f"Measurement temperature {temp} K out of range [1.0, 500.0]")
        
    return (len(errors) == 0, errors)


def create_empty_row_template() -> Dict[str, Any]:
    """Generates an empty extraction row dictionary with all schema keys."""
    schema = load_extraction_schema()
    props = schema.get("properties", {})
    return {k: None for k in props.keys()}
