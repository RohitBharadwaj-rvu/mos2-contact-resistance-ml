"""
Title and Abstract Screening Engine for Semiconductor Contact Literature.
Performs high-throughput text screening against domain keywords and exclusion filters.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

from src.data.literature_harvester import load_raw_corpus
from src.data.quality_filter import audit_candidate_record

SCREENING_RESULTS_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "title_abstract_screening_results.json"


def screen_paper_title_and_abstract(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates paper title and abstract against relevance criteria.
    Returns audit dictionary with pass/fail decision and tags.
    """
    accepted, passed, rejections = audit_candidate_record(paper)
    
    # Classify decision
    if accepted:
        decision = "PASSED_TITLE_ABSTRACT"
    elif any("EXC-03" in r for r in rejections):
        decision = "REJECTED_OFF_TOPIC"
    elif any("EXC-02" in r for r in rejections):
        decision = "FLAGGED_ERROR_PRONE_METROLOGY"
    else:
        decision = "REJECTED_INCOMPLETE"
        
    return {
        "id": paper.get("id"),
        "source_uid": paper.get("source_uid"),
        "title": paper.get("title"),
        "decision": decision,
        "is_accepted": accepted,
        "passed_rules": passed,
        "rejection_reasons": rejections
    }


def execute_corpus_screening() -> List[Dict[str, Any]]:
    """Screens the entire raw literature corpus and persists results."""
    corpus = load_raw_corpus()
    results = [screen_paper_title_and_abstract(p) for p in corpus]
    
    SCREENING_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SCREENING_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    return results


def get_screening_summary() -> Dict[str, Any]:
    """Summarizes counts of accepted, rejected, and flagged publications."""
    if not SCREENING_RESULTS_PATH.exists():
        execute_corpus_screening()
    with open(SCREENING_RESULTS_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)
        
    summary = {}
    for r in results:
        dec = r["decision"]
        summary[dec] = summary.get(dec, 0) + 1
        
    return {
        "total_screened": len(results),
        "decision_counts": summary,
        "passed_count": sum(1 for r in results if r["is_accepted"]),
        "rejection_count": sum(1 for r in results if not r["is_accepted"])
    }
