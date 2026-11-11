"""
Grouped Cross-Validation Scheme Evaluator (Sprint 3.a.2).
Implements and benchmarks GroupKFold and Leave-One-Group-Out (LOGO) cross-validation schemes grouped by source paper UID, quantifying the empirical optimism penalty of random splits.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, GroupKFold, LeaveOneGroupOut
from sklearn.metrics import mean_squared_error, mean_absolute_error

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.models.model_factory import instantiate_candidate_model

GROUPED_CV_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "grouped_cv_comparison.json"


def get_paper_grouped_splits(df: pd.DataFrame, n_splits: int = 5) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Generates GroupKFold train/val index splits grouped strictly by source_uid."""
    gkf = GroupKFold(n_splits=n_splits)
    groups = df["source_uid"].values
    return list(gkf.split(df, groups=groups))


def get_leave_one_group_out_splits(df: pd.DataFrame) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Generates LeaveOneGroupOut train/val index splits across all distinct literature papers."""
    logo = LeaveOneGroupOut()
    groups = df["source_uid"].values
    return list(logo.split(df, groups=groups))


def compare_random_vs_grouped_cv(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Evaluates Ridge Regression and Gradient Boosting under Random 5-Fold vs Grouped 5-Fold vs LOGO.
    Quantifies the exact 'Optimism Penalty' (empirical validation score degradation under zero-leakage splits).
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    groups = df["source_uid"].values
    
    models_to_test = ["Ridge_Regression", "Gradient_Boosting", "Gaussian_Process_Matern"]
    cv_schemes = {
        "random_5fold": KFold(n_splits=5, shuffle=True, random_state=42),
        "grouped_5fold": GroupKFold(n_splits=5),
        "leave_one_group_out": LeaveOneGroupOut()
    }
    
    results = {}
    for m_name in models_to_test:
        model_scores = {}
        for cv_name, cv_obj in cv_schemes.items():
            oof_preds = np.zeros_like(y)
            fold_counts = np.zeros_like(y)
            
            if cv_name == "random_5fold":
                splits = cv_obj.split(X)
            else:
                splits = cv_obj.split(X, y, groups=groups)
                
            for train_idx, val_idx in splits:
                model = instantiate_candidate_model(m_name)
                model.fit(X.iloc[train_idx], y[train_idx])
                oof_preds[val_idx] = model.predict(X.iloc[val_idx])
                fold_counts[val_idx] += 1
                
            rmse = float(np.sqrt(mean_squared_error(y, oof_preds)))
            mae = float(mean_absolute_error(y, oof_preds))
            corr = float(np.corrcoef(y, oof_preds)[0, 1]) if np.std(oof_preds) > 1e-6 else 0.0
            
            model_scores[cv_name] = {
                "rmse_log10_rc": round(rmse, 3),
                "mae_log10_rc": round(mae, 3),
                "pearson_r": round(corr, 3)
            }
            
        # Calculate optimism penalty (Grouped RMSE minus Random RMSE)
        opt_penalty = round(model_scores["grouped_5fold"]["rmse_log10_rc"] - model_scores["random_5fold"]["rmse_log10_rc"], 3)
        model_scores["optimism_penalty_rmse"] = opt_penalty
        results[m_name] = model_scores
        
    summary = {
        "dataset_n_samples": len(df),
        "dataset_n_clusters": len(np.unique(groups)),
        "models_evaluated": results,
        "recommendation": "Use Grouped 5-Fold as standard cross-validation and LOGO as the rigorous out-of-distribution benchmark."
    }
    
    GROUPED_CV_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(GROUPED_CV_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    return summary


if __name__ == "__main__":
    res = compare_random_vs_grouped_cv()
    print("Random vs Grouped CV Comparison:")
    print(json.dumps(res, indent=2))
