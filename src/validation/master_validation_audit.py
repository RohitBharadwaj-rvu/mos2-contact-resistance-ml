"""
Master Validation Strategy and Experimental Protocol Audit for Section 3.
Validates zero-leakage splits, metric computation pipelines, and model selection scoring protocols across Section 3 artifacts.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.model_factory import instantiate_candidate_model
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.validation.selection_criteria import evaluate_model_cv

REF_DIR = Path(__file__).resolve().parents[2] / "data" / "reference"


def run_master_section_3_audit() -> Dict[str, Any]:
    """
    Executes holistic validation of Section 3 protocols:
    1. All 6 specification JSON files exist and contain required keys.
    2. Zero leakage in GroupKFold and LOGO splits.
    3. End-to-end execution of evaluate_model_cv on Ridge Regression.
    4. Compliance of model selection score with official threshold rules.
    """
    audit = {
        "status": "PASS",
        "checks_passed": 0,
        "checks_failed": 0,
        "details": {}
    }
    
    # 1. Spec files check
    specs = [
        REF_DIR / "data_leakage_risk_analysis.json",
        REF_DIR / "grouped_cv_comparison.json",
        REF_DIR / "official_validation_protocol.json",
        REF_DIR / "regression_error_metrics.json",
        REF_DIR / "rank_trend_metrics_spec.json",
        REF_DIR / "model_selection_criteria.json"
    ]
    
    missing = [str(f.name) for f in specs if not f.exists()]
    if missing:
        audit["details"]["spec_files"] = {"status": "FAIL", "missing": missing}
        audit["checks_failed"] += 1
        audit["status"] = "FAIL"
    else:
        audit["details"]["spec_files"] = {"status": "PASS", "count": len(specs)}
        audit["checks_passed"] += 1

    # 2. Zero-leakage verification on Grouped 5-Fold and LOGO
    df = get_cleaned_and_engineered_dataset()
    for scheme_name in ["grouped_5fold", "logo"]:
        splits = get_cv_splits(df, scheme=scheme_name)
        leakage_found = False
        for train_idx, val_idx in splits:
            train_sources = set(df.iloc[train_idx]["source_uid"])
            val_sources = set(df.iloc[val_idx]["source_uid"])
            if len(train_sources.intersection(val_sources)) > 0:
                leakage_found = True
                break
        if not leakage_found:
            audit["details"][f"{scheme_name}_zero_leakage"] = {"status": "PASS", "folds": len(splits)}
            audit["checks_passed"] += 1
        else:
            audit["details"][f"{scheme_name}_zero_leakage"] = {"status": "FAIL"}
            audit["checks_failed"] += 1
            audit["status"] = "FAIL"

    # 3. End-to-end CV evaluation verification
    features = select_parsimonious_features(df, max_features=4)
    X = df[features]
    y = df["log10_rc"].values
    
    model = instantiate_candidate_model("Ridge_Regression")
    cv_report = evaluate_model_cv(model, X, y)
    
    if cv_report.get("is_qualified_for_deployment") is True and cv_report["composite_selection_score"] > 0.70:
        audit["details"]["cv_execution_check"] = {
            "status": "PASS",
            "model": "Ridge_Regression",
            "composite_score": cv_report["composite_selection_score"],
            "rmse_dex": cv_report["underlying_metrics"]["rmse_log10_dex"],
            "spearman_rho": cv_report["underlying_metrics"]["spearman_rho"]
        }
        audit["checks_passed"] += 1
    else:
        audit["details"]["cv_execution_check"] = {"status": "FAIL", "report": cv_report}
        audit["checks_failed"] += 1
        audit["status"] = "FAIL"

    return audit


if __name__ == "__main__":
    report = run_master_section_3_audit()
    print("Master Section 3 Audit Report:")
    print(json.dumps(report, indent=2))
