"""
Default Non-Linear Architecture Cross-Validation Runner (Sprint 4.b.2).
Trains shortlisted non-linear models (Random Forest, Gradient Boosting, GPR, SVR) with default capacity settings on paper-grouped 5-fold cross-validation.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.validation.selection_criteria import evaluate_model_cv
from src.models.model_factory import instantiate_candidate_model
from src.models.model_selector import get_shortlisted_architectures

NONLINEAR_RUNS_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "default_nonlinear_cross_validation_results.json"


def run_all_default_nonlinear_models_cv(df: Optional[pd.DataFrame] = None, scheme: str = "grouped_5fold") -> Dict[str, Any]:
    """
    Evaluates default non-linear architectures on grouped cross-validation splits:
    1. Random_Forest
    2. Gradient_Boosting
    3. Gaussian_Process_Matern
    4. Support_Vector_Regression_RBF
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    splits = get_cv_splits(df, scheme=scheme)
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    nonlinear_models = [
        "Random_Forest",
        "Gradient_Boosting",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]
    
    results = {}
    for name in nonlinear_models:
        model = instantiate_candidate_model(name)
        score_rep = evaluate_model_cv(model, X, y, splits=splits)
        results[name] = score_rep
        
    summary = {
        "validation_scheme": scheme,
        "n_samples": len(df),
        "features_used": feature_cols,
        "default_nonlinear_models": results
    }
    
    NONLINEAR_RUNS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(NONLINEAR_RUNS_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    return summary


if __name__ == "__main__":
    res = run_all_default_nonlinear_models_cv()
    print("Default non-linear models cross-validation completed.")
    for name, m in res["default_nonlinear_models"].items():
        print(f"  - {name}: Score = {m['composite_selection_score']}, RMSE = {m['underlying_metrics']['rmse_log10_dex']} dex, Qualified = {m['is_qualified_for_deployment']}")
