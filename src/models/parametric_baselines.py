"""
Simple Parametric Baseline Regressors (Sprint 2.b.2).
Implements and evaluates standard low-complexity linear models (OLS, Ridge, Lasso, ElasticNet) as parametric benchmarks.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features

PARAMETRIC_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "parametric_baseline_results.json"


def build_parametric_pipeline(model_name: str, alpha: float = 1.0, l1_ratio: float = 0.5) -> Pipeline:
    """Builds a scikit-learn standard scaling + linear regressor pipeline."""
    if model_name == "ols":
        reg = LinearRegression()
    elif model_name == "ridge":
        reg = Ridge(alpha=alpha, random_state=42)
    elif model_name == "lasso":
        reg = Lasso(alpha=alpha, random_state=42, max_iter=2000)
    elif model_name == "elastic_net":
        reg = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42, max_iter=2000)
    else:
        raise ValueError(f"Unknown model name: {model_name}")
        
    return Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", reg)
    ])


def evaluate_parametric_baselines(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Evaluates OLS, Ridge, Lasso, and ElasticNet models on the master curated dataset."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    models = {
        "ordinary_least_squares": build_parametric_pipeline("ols"),
        "ridge_regression": build_parametric_pipeline("ridge", alpha=1.0),
        "lasso_regression": build_parametric_pipeline("lasso", alpha=0.1),
        "elastic_net": build_parametric_pipeline("elastic_net", alpha=0.1, l1_ratio=0.5)
    }
    
    results = {}
    for name, pipe in models.items():
        pipe.fit(X, y)
        preds = pipe.predict(X)
        
        rmse = float(np.sqrt(mean_squared_error(y, preds)))
        mae = float(mean_absolute_error(y, preds))
        r2 = float(r2_score(y, preds))
        corr = float(np.corrcoef(y, preds)[0, 1]) if np.std(preds) > 1e-6 else 0.0
        
        # Extract standardized feature weights
        reg = pipe.named_steps["regressor"]
        coefs = {col: round(float(w), 3) for col, w in zip(feature_cols, reg.coef_)}
        
        results[name] = {
            "rmse_log10_rc": round(rmse, 3),
            "mae_log10_rc": round(mae, 3),
            "r2_score": round(r2, 3),
            "pearson_r": round(corr, 3),
            "coefficients": coefs,
            "intercept": round(float(reg.intercept_), 3)
        }
        
    output_data = {
        "features_used": feature_cols,
        "n_samples": len(df),
        "models": results
    }
    
    PARAMETRIC_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PARAMETRIC_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    return output_data


if __name__ == "__main__":
    res = evaluate_parametric_baselines()
    print("Evaluated parametric baselines:")
    print(json.dumps(res, indent=2))
