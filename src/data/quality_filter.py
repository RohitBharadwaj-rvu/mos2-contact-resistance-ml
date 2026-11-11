"""
Quality Filtering and Source Screening Engine.
Applies formal inclusion/exclusion criteria to curate high-reliability MoS2 contact papers.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

CRITERIA_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "inclusion_exclusion_criteria.json"


def load_inclusion_exclusion_criteria() -> Dict[str, Any]:
    """Loads formal inclusion and exclusion criteria checklist."""
    if not CRITERIA_PATH.exists():
        raise FileNotFoundError(f"Criteria file not found at {CRITERIA_PATH}")
    with open(CRITERIA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def audit_candidate_record(record: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """
    Evaluates a candidate publication or extracted data record against criteria.
    Returns: (is_accepted: bool, passed_rules: List[str], rejection_reasons: List[str])
    """
    criteria = load_inclusion_exclusion_criteria()
    passed = []
    rejections = []
    
    # Check Exclusions first
    title_and_abstract = (record.get("title", "") + " " + record.get("abstract", "")).lower()
    off_topic_keywords = ["photocatalysis", "hydrogen evolution", "battery anode", "lubricant"]
    if any(kw in title_and_abstract for kw in off_topic_keywords):
        rejections.append("EXC-03: Off-topic application domain")
        
    rc = record.get("reported_rc_ohm_um")
    sbh = record.get("reported_sbh_ev")
    if rc is not None and rc <= 0:
        rejections.append("EXC-04: Unphysical non-positive contact resistance")
    if sbh is not None and (sbh < 0.0 or sbh > 2.0):
        rejections.append("EXC-04: Unphysical Schottky barrier height outside 0-2.0 eV")
        
    method = record.get("characterization_method", "")
    if "two-probe" in method.lower() and "tlm" not in method.lower() and "four-probe" not in method.lower():
        rejections.append("EXC-02: Uncalibrated two-probe measurement without decoupling")

    # Check Inclusions
    mat_terms = [
        "mos2", "molybdenum disulf", "molybdenum disulph",
        "two-dimensional semiconductor", "2d semiconductor",
        "transition metal dichalcogenide", "tmdc"
    ]
    if any(mt in title_and_abstract for mt in mat_terms) or record.get("contact_system"):
        passed.append("INC-01: Target Material System")
    else:
        rejections.append("INC-01: Failed material confirmation (MoS2)")
        
    if record.get("contact_metal") or record.get("contact_system"):
        passed.append("INC-02: Identified Contact Metal/Architecture")
    else:
        rejections.append("INC-02: Missing contact electrode specification")
        
    if rc is not None or sbh is not None:
        passed.append("INC-03: Quantitative Metric Reporting")
    else:
        rejections.append("INC-03: No numerical Rc or SBH reported")
        
    valid_methods = ["tlm", "richardson", "arrhenius", "four-probe", "hall", "activation", "xps"]
    if any(vm in method.lower() for vm in valid_methods):
        passed.append("INC-04: Valid Characterization Metrology")
    elif "two-probe" not in method.lower():
        passed.append("INC-04: Accepted Device Metrology")

    is_accepted = len(rejections) == 0
    return is_accepted, passed, rejections
