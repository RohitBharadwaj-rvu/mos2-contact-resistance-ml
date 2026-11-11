"""
Baseline Cross-Validation Execution Engine (Sprint 4.b.1).
Executes rigorous paper-grouped 5-fold cross-validation for naive statistical baselines and simple parametric linear models.
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
from src.models.baseline_models import MeanBaselineRegressor, MedianBaselineRegressor, PurePhysicsSchottkyBaseline
from src.models.parametric_baselines import build_parametric_pipeline

BASELINE_RUNS_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "baseline_cross_validation_results.json"


def run_all_baseline_models_cv(df: Optional[pd.DataFrame] = None, scheme: str = "grouped_5fold") -> Dict[str, Any]:
    """
    Trains and cross-validates all statistical and parametric baselines under strict paper-grouped splits:
    1. MeanBaseline
    2. MedianBaseline
    3. PurePhysicsSchottkyBaseline
    4. Ordinary Least Squares
    5. Ridge Regression
    6. Lasso Regression
    7. ElasticNet
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    splits = get_cv_splits(df, scheme=scheme)
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    baselines = {
        "mean_baseline": MeanBaselineRegressor(),
        "median_baseline": MedianBaselineRegressor(),
        "pure_physics_schottky": PurePhysicsSchottkyBaseline(),
        "ordinary_least_squares": build_parametric_pipeline("ols"),
        "ridge_regression": build_parametric_pipeline("ridge", alpha=1.0),
        "lasso_regression": build_parametric_pipeline("lasso", alpha=0.1),
        "elastic_net": build_parametric_pipeline("elastic_net", alpha=0.1, l1_ratio=0.5)
    }
    
    results = {}
    for name, model in baselines.items():
        if name in ["mean_baseline", "median_baseline"]:
            # Univariate y target fit
            oof_preds = np.zeros_like(y, dtype=float)
            for train_idx, val_idx in splits:
                m = MeanBaselineRegressor() if name == "mean_baseline" else MedianBaselineRegressor()
                m.fit(X.iloc[train_idx], y[train_idx])
                oof_preds[val_idx] = m.predict(X.iloc[val_idx])
            from src.validation.selection_criteria import compute_composite_selection_score
            score_rep = compute_composite_selection_score(y, oof_preds, feature_count=0)
            score_rep["oof_predictions"] = [round(float(p), 4) for p in oof_preds]
            results[name] = score_rep
        elif name == "pure_physics_schottky":
            oof_preds = np.zeros_like(y, dtype=float)
            X_wf = df[["work_function_ev"]].copy()
            for train_idx, val_idx in splits:
                m = PurePhysicsSchottkyBaseline()
                m.fit(X_wf.iloc[train_idx], y[train_idx])
                oof_preds[val_idx] = m.predict(X_wf.iloc[val_idx])
            from src.validation.selection_criteria import compute_composite_selection_score
            score_rep = compute_composite_selection_score(y, oof_preds, feature_count=1)
            score_rep["oof_predictions"] = [round(float(p), 4) for p in oof_preds]
            results[name] = score_rep
        else:
            score_rep = evaluate_model_cv(model, X, y, splits=splits)
            results[name] = score_rep
            
    summary = {
        "validation_scheme": scheme,
        "n_samples": len(df),
        "features_used": feature_cols,
        "baseline_models": results
    }
    
    BASELINE_RUNS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(BASELINE_RUNS_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    return summary


if __name__ == "__main__":
    res = run_all_baseline_models_cv()
    print("Baseline cross-validation completed.")
    for name, m in res["baseline_models"].items():
        print(f"  - {name}: Score = {m['composite_selection_score']}, RMSE = {m['underlying_metrics']['rmse_log10_dex']} dex, Qualified = {m['is_qualified_for_deployment']}")
