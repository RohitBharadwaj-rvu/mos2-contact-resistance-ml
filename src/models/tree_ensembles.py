"""
Tree-Based Ensemble Architecture Evaluator (Sprint 2.c.1).
Investigates Random Forest, Gradient Boosting, and Extra Trees regressors for non-linear contact resistance modeling under small-N capacity constraints.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features

TREE_EVAL_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "tree_ensemble_evaluation.json"


def build_tree_model(model_name: str, max_depth: int = 3, n_estimators: int = 50, random_state: int = 42):
    """Instantiates a capacity-constrained tree ensemble regressor."""
    if model_name == "random_forest":
        return RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=random_state
        )
    elif model_name == "gradient_boosting":
        return GradientBoostingRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=0.05,
            subsample=0.8,
            random_state=random_state
        )
    elif model_name == "extra_trees":
        return ExtraTreesRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=random_state
        )
    else:
        raise ValueError(f"Unknown tree model: {model_name}")


def evaluate_tree_ensembles(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Evaluates tree ensemble models on the curated MoS2 dataset."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    models = {
        "random_forest": build_tree_model("random_forest"),
        "gradient_boosting": build_tree_model("gradient_boosting"),
        "extra_trees": build_tree_model("extra_trees")
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X, y)
        preds = model.predict(X)
        
        rmse = float(np.sqrt(mean_squared_error(y, preds)))
        mae = float(mean_absolute_error(y, preds))
        r2 = float(r2_score(y, preds))
        corr = float(np.corrcoef(y, preds)[0, 1]) if np.std(preds) > 1e-6 else 0.0
        
        importances = {col: round(float(imp), 3) for col, imp in zip(feature_cols, model.feature_importances_)}
        
        results[name] = {
            "rmse_log10_rc": round(rmse, 3),
            "mae_log10_rc": round(mae, 3),
            "r2_score": round(r2, 3),
            "pearson_r": round(corr, 3),
            "feature_importances": importances
        }
        
    output_data = {
        "features_used": feature_cols,
        "n_samples": len(df),
        "hyperparameters": {
            "max_depth": 3,
            "n_estimators": 50,
            "min_samples_leaf": 2
        },
        "models": results
    }
    
    TREE_EVAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TREE_EVAL_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    return output_data


if __name__ == "__main__":
    res = evaluate_tree_ensembles()
    print("Tree ensemble evaluation results:")
    print(json.dumps(res, indent=2))
