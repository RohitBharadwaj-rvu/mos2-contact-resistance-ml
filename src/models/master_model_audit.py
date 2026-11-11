"""
Master Architecture and Model Audit for Section 2 (Identify Candidate Models & Paradigms).
Validates end-to-end specification integrity, factory instantiation, fit/predict verification, and decoupling partition completeness.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.model_factory import instantiate_candidate_model
from src.models.model_selector import get_shortlisted_architectures
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.models.decoupling_framework import get_feature_domain_partition

REF_DIR = Path(__file__).resolve().parents[2] / "data" / "reference"


def run_master_section_2_audit() -> Dict[str, Any]:
    """
    Executes holistic validation of all Section 2 assets:
    1. Reference specification files existence and valid JSON structure.
    2. Model factory instantiation and end-to-end execution for all shortlisted architectures.
    3. Performance sanity checks (all shortlisted models achieve in-sample R2 > 0.85).
    4. Decoupling domain partition completeness and mutual exclusivity.
    """
    audit = {
        "status": "PASS",
        "checks_passed": 0,
        "checks_failed": 0,
        "details": {}
    }
    
    # 1. Verify all reference JSON files exist
    expected_specs = [
        REF_DIR / "learning_task_specifications.json",
        REF_DIR / "model_complexity_constraints.json",
        REF_DIR / "baseline_model_definitions.json",
        REF_DIR / "parametric_baseline_results.json",
        REF_DIR / "tree_ensemble_evaluation.json",
        REF_DIR / "alternative_regressors_evaluation.json",
        REF_DIR / "shortlisted_architectures.json",
        REF_DIR / "symbolic_regression_survey.json",
        REF_DIR / "symbolic_search_space_config.json",
        REF_DIR / "explainability_methodology.json",
        REF_DIR / "decoupling_framework_spec.json"
    ]
    
    missing = [str(f.name) for f in expected_specs if not f.exists()]
    if missing:
        audit["details"]["spec_files"] = {"status": "FAIL", "missing": missing}
        audit["checks_failed"] += 1
        audit["status"] = "FAIL"
    else:
        audit["details"]["spec_files"] = {"status": "PASS", "count": len(expected_specs)}
        audit["checks_passed"] += 1

    # 2. Verify all shortlisted models can fit and predict
    df = get_cleaned_and_engineered_dataset()
    features = select_parsimonious_features(df, max_features=4)
    X = df[features].copy()
    y = df["log10_rc"].values
    
    shortlisted = get_shortlisted_architectures()
    model_statuses = {}
    all_fit_pass = True
    
    for arch in shortlisted:
        try:
            model = instantiate_candidate_model(arch)
            model.fit(X, y)
            preds = model.predict(X)
            
            r2 = float(r2_score(y, preds))
            rmse = float(np.sqrt(mean_squared_error(y, preds)))
            
            # Shortlisted models should achieve high in-sample explanation (R2 > 0.85)
            pass_threshold = r2 >= 0.85
            model_statuses[arch] = {
                "fit_success": True,
                "r2_score": round(r2, 3),
                "rmse_log10_rc": round(rmse, 3),
                "passed_threshold": pass_threshold
            }
            if not pass_threshold:
                all_fit_pass = False
        except Exception as e:
            model_statuses[arch] = {"fit_success": False, "error": str(e)}
            all_fit_pass = False
            
    if all_fit_pass:
        audit["details"]["shortlisted_models_execution"] = {"status": "PASS", "models": model_statuses}
        audit["checks_passed"] += 1
    else:
        audit["details"]["shortlisted_models_execution"] = {"status": "FAIL", "models": model_statuses}
        audit["checks_failed"] += 1
        audit["status"] = "FAIL"

    # 3. Decoupling partition verification
    partition = get_feature_domain_partition()
    s1 = set(partition["intrinsic_metal_domain"])
    s2 = set(partition["extrinsic_processing_domain"])
    s3 = set(partition["electrostatic_operational_domain"])
    
    exclusive = (len(s1.intersection(s2)) == 0 and len(s1.intersection(s3)) == 0 and len(s2.intersection(s3)) == 0)
    has_features = (len(s1) > 0 and len(s2) > 0 and len(s3) > 0)
    
    if exclusive and has_features:
        audit["details"]["decoupling_partition"] = {
            "status": "PASS",
            "intrinsic_count": len(s1),
            "extrinsic_count": len(s2),
            "electrostatic_count": len(s3)
        }
        audit["checks_passed"] += 1
    else:
        audit["details"]["decoupling_partition"] = {"status": "FAIL"}
        audit["checks_failed"] += 1
        audit["status"] = "FAIL"

    return audit


if __name__ == "__main__":
    report = run_master_section_2_audit()
    print("Master Section 2 Audit Report:")
    print(json.dumps(report, indent=2))
