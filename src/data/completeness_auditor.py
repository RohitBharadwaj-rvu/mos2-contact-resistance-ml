"""
Data Completeness and Physical Consistency Audit Engine.
Evaluates reporting completeness, inspects physical contradictions, and quarantines noisy or incomplete sources.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

from src.data.literature_harvester import load_raw_corpus
from src.data.methodology_auditor import load_methodology_audit

COMPLETENESS_AUDIT_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "data_completeness_audit.json"

REQUIRED_FIELDS = [
    "contact_metal",
    "contact_type",
    "carrier_type",
    "characterization_method",
    "temperature_k"
]


def audit_source_completeness(paper: Dict[str, Any], method_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits single source for data completeness and physical consistency.
    Assigns: 'ACCEPTED_PRIMARY_MODELING', 'QUARANTINED_AUXILIARY', or 'REJECTED'.
    """
    missing_fields = [f for f in REQUIRED_FIELDS if f not in paper or paper[f] is None]
    
    rc = paper.get("reported_rc_ohm_um")
    sbh = paper.get("reported_sbh_ev")
    
    # Must have at least one target metric
    if rc is None and sbh is None:
        missing_fields.append("target_metrics_rc_and_sbh")
        
    inconsistencies = []
    
    # Physical consistency checks
    if rc is not None and (rc < 10.0 or rc > 1e7):
        inconsistencies.append(f"Rc value {rc} Ohm*um outside expected physical range [10, 10^7]")
        
    if sbh is not None and (sbh < 0.0 or sbh > 1.85):
        inconsistencies.append(f"SBH value {sbh} eV outside MoS2 bandgap limit [0.0, 1.85]")
        
    # Check methodology quality score
    quality_score = method_record.get("composite_quality_score", 0)
    method_name = paper.get("characterization_method", "")
    
    # Decision assignment
    if missing_fields or (rc is None and sbh is None):
        curation_decision = "REJECTED"
        quarantine_reason = f"Missing required fields: {missing_fields}"
    elif "two-probe" in method_name.lower() or quality_score < 70:
        curation_decision = "QUARANTINED_AUXILIARY"
        quarantine_reason = f"Suboptimal metrology: {method_name} (Quality Score: {quality_score})"
    elif inconsistencies:
        curation_decision = "QUARANTINED_AUXILIARY"
        quarantine_reason = f"Physical inconsistencies: {inconsistencies}"
    else:
        curation_decision = "ACCEPTED_PRIMARY_MODELING"
        quarantine_reason = None

    carrier_density = paper.get("carrier_density_cm2")
    is_high_carrier_density = carrier_density is not None and carrier_density >= 1e13
        
    return {
        "id": paper.get("id"),
        "source_uid": paper.get("source_uid"),
        "title": paper.get("title"),
        "curation_decision": curation_decision,
        "quality_score": quality_score,
        "missing_fields": missing_fields,
        "inconsistencies": inconsistencies,
        "quarantine_reason": quarantine_reason,
        "is_high_carrier_density": is_high_carrier_density
    }


def execute_completeness_audit() -> List[Dict[str, Any]]:
    """Runs completeness and consistency audit across all literature records."""
    corpus = load_raw_corpus()
    methods = {m["id"]: m for m in load_methodology_audit()}
    
    audit_results = [
        audit_source_completeness(p, methods.get(p["id"], {}))
        for p in corpus
    ]
    
    COMPLETENESS_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLETENESS_AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)
        
    return audit_results


def get_curated_modeling_dataset_sources() -> List[str]:
    """Returns list of paper IDs accepted for primary machine learning modeling."""
    if not COMPLETENESS_AUDIT_PATH.exists():
        execute_completeness_audit()
    with open(COMPLETENESS_AUDIT_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)
    return [r["id"] for r in results if r["curation_decision"] == "ACCEPTED_PRIMARY_MODELING"]
