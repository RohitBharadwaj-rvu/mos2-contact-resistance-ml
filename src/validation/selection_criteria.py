"""
Official Model Selection Criteria and Composite Scoring Engine (Sprint 3.b.3).
Defines multi-objective selection criteria combining out-of-fold RMSE, Spearman rank correlation, and pairwise concordance index.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.base import clone

from src.validation.regression_metrics import evaluate_regression_metrics
from src.validation.rank_trend_metrics import evaluate_rank_and_trend_metrics

SELECTION_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "model_selection_criteria.json"


def compute_composite_selection_score(y_true_log: np.ndarray, y_pred_log: np.ndarray, feature_count: int = 4) -> Dict[str, Any]:
    """
    Computes composite model selection score:
    Score = 0.40 * (1 - min(1, RMSE)) + 0.35 * max(0, Spearman_rho) + 0.25 * Concordance_index
    Penalizes models exceeding parsimonious feature budgets.
    """
    reg_metrics = evaluate_regression_metrics(y_true_log, y_pred_log)
    rank_metrics = evaluate_rank_and_trend_metrics(y_true_log, y_pred_log)
    
    rmse = reg_metrics["rmse_log10_dex"]
    rho = rank_metrics["spearman_rho"]
    c_index = rank_metrics["concordance_index"]
    
    # Accuracy component: 1.0 at RMSE=0, 0.0 at RMSE >= 1.0 dex
    accuracy_term = max(0.0, 1.0 - min(1.0, rmse))
    rank_term = max(0.0, rho)
    concordance_term = c_index
    
    raw_score = 0.40 * accuracy_term + 0.35 * rank_term + 0.25 * concordance_term
    
    # Parsimony penalty: -0.05 per feature over 4
    excess_features = max(0, feature_count - 4)
    parsimony_penalty = excess_features * 0.05
    final_score = max(0.0, raw_score - parsimony_penalty)
    
    # Qualification check
    qualifies = bool(
        rmse <= 0.45 and
        rho >= 0.75 and
        c_index >= 0.80 and
        feature_count <= 6
    )
    
    return {
        "composite_selection_score": round(float(final_score), 4),
        "raw_score": round(float(raw_score), 4),
        "parsimony_penalty": round(float(parsimony_penalty), 3),
        "is_qualified_for_deployment": qualifies,
        "sub_scores": {
            "accuracy_score_weighted": round(float(0.40 * accuracy_term), 4),
            "rank_score_weighted": round(float(0.35 * rank_term), 4),
            "concordance_score_weighted": round(float(0.25 * concordance_term), 4)
        },
        "underlying_metrics": {
            "rmse_log10_dex": rmse,
            "spearman_rho": rho,
            "concordance_index": c_index
        }
    }


def define_model_selection_criteria_spec() -> Dict[str, Any]:
    """Official formalization of model selection thresholds."""
    spec = {
        "title": "MoS2 Contact Resistance Official Model Selection Criteria",
        "composite_formula": "Score = 0.40 * (1 - min(1, RMSE)) + 0.35 * max(0, rho) + 0.25 * C_index - 0.05 * max(0, P - 4)",
        "hard_qualification_thresholds": {
            "max_grouped_rmse_dex": 0.45,
            "min_spearman_rho": 0.75,
            "min_concordance_index": 0.80,
            "max_active_features": 6,
            "max_physical_violations": 0
        },
        "role_in_pipeline": "Determines the winning champion architecture and hyperparameter configuration across Grouped 5-Fold and LOGO cross-validation."
    }
    
    SELECTION_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SELECTION_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


def evaluate_model_cv(model: Any, X: Any, y: np.ndarray, splits: Optional[List[Tuple[np.ndarray, np.ndarray]]] = None) -> Dict[str, Any]:
    """
    Executes cross-validation across provided splits, aggregates out-of-fold predictions,
    and returns full composite selection report.
    """
    if splits is None:
        from src.validation.splitting_protocol import get_cv_splits
        splits = get_cv_splits(scheme="grouped_5fold")
        
    oof_preds = np.zeros_like(y, dtype=float)
    fold_metrics = []
    
    for fold_idx, (train_idx, val_idx) in enumerate(splits):
        m = clone(model)
        X_train = X.iloc[train_idx] if isinstance(X, pd.DataFrame) else X[train_idx]
        y_train = y[train_idx]
        X_val = X.iloc[val_idx] if isinstance(X, pd.DataFrame) else X[val_idx]
        y_val = y[val_idx]
        
        m.fit(X_train, y_train)
        pred_val = m.predict(X_val)
        oof_preds[val_idx] = pred_val
        
        fold_metrics.append({
            "fold": fold_idx,
            "rmse_dex": round(float(np.sqrt(np.mean((y_val - pred_val) ** 2))), 4),
            "mae_dex": round(float(np.mean(np.abs(y_val - pred_val))), 4)
        })
        
    feature_count = X.shape[1] if hasattr(X, "shape") else 4
    score_report = compute_composite_selection_score(y, oof_preds, feature_count=feature_count)
    score_report["fold_metrics"] = fold_metrics
    score_report["oof_predictions"] = [round(float(p), 4) for p in oof_preds]
    
    return score_report


if __name__ == "__main__":
    spec = define_model_selection_criteria_spec()
    print("Model selection criteria specification serialized.")
