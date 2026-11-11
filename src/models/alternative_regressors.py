"""
Alternative Non-Linear Regression Architectures (Sprint 2.c.2).
Investigates Gaussian Process Regression (GPR), Support Vector Regression (SVR), and Kernel Ridge Regression (KRR) under small-N Bayesian and kernel paradigms.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel, Matern
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features

ALT_EVAL_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "alternative_regressors_evaluation.json"


def build_alternative_model(model_name: str) -> Any:
    """Builds pre-configured alternative regression models with standard scaling."""
    if model_name == "gaussian_process_rbf":
        kernel = C(1.0, (1e-2, 1e2)) * RBF(length_scale=2.0, length_scale_bounds=(1e-1, 50.0)) + WhiteKernel(noise_level=0.1, noise_level_bounds=(1e-3, 1.0))
        reg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5, random_state=42)
    elif model_name == "gaussian_process_matern":
        kernel = C(1.0, (1e-2, 1e2)) * Matern(length_scale=2.0, nu=2.5, length_scale_bounds=(1e-1, 50.0)) + WhiteKernel(noise_level=0.1, noise_level_bounds=(1e-3, 1.0))
        reg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5, random_state=42)
    elif model_name == "svr_rbf":
        reg = SVR(kernel="rbf", C=5.0, epsilon=0.1)
    elif model_name == "kernel_ridge":
        reg = KernelRidge(kernel="rbf", alpha=0.05, gamma=0.2)
    else:
        raise ValueError(f"Unknown alternative model: {model_name}")
        
    return Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", reg)
    ])


def evaluate_alternative_regressors(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Evaluates alternative regressors on the curated MoS2 contact dataset."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    models = {
        "gaussian_process_rbf": build_alternative_model("gaussian_process_rbf"),
        "gaussian_process_matern": build_alternative_model("gaussian_process_matern"),
        "svr_rbf": build_alternative_model("svr_rbf"),
        "kernel_ridge": build_alternative_model("kernel_ridge")
    }
    
    results = {}
    for name, pipe in models.items():
        pipe.fit(X, y)
        preds = pipe.predict(X)
        
        rmse = float(np.sqrt(mean_squared_error(y, preds)))
        mae = float(mean_absolute_error(y, preds))
        r2 = float(r2_score(y, preds))
        corr = float(np.corrcoef(y, preds)[0, 1]) if np.std(preds) > 1e-6 else 0.0
        
        model_info = {
            "rmse_log10_rc": round(rmse, 3),
            "mae_log10_rc": round(mae, 3),
            "r2_score": round(r2, 3),
            "pearson_r": round(corr, 3)
        }
        
        # Extract GPR posterior uncertainty if applicable
        reg = pipe.named_steps["regressor"]
        if isinstance(reg, GaussianProcessRegressor):
            X_scaled = pipe.named_steps["scaler"].transform(X)
            _, std = reg.predict(X_scaled, return_std=True)
            model_info["mean_uncertainty_sigma"] = round(float(np.mean(std)), 3)
            model_info["optimized_kernel"] = str(reg.kernel_)
            
        results[name] = model_info
        
    output_data = {
        "features_used": feature_cols,
        "n_samples": len(df),
        "models": results
    }
    
    ALT_EVAL_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(ALT_EVAL_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    return output_data


if __name__ == "__main__":
    res = evaluate_alternative_regressors()
    print("Alternative Regressors Evaluation Results:")
    print(json.dumps(res, indent=2))
