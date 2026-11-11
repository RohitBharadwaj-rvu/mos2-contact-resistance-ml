"""
Baseline Regression Models (Sprint 2.b.1 & 2.b.2).
Implements naive statistical baselines (Mean, Median, Stratified) and physics-based reference models to establish the performance floor.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import mean_squared_error, mean_absolute_error

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

BASELINE_DEF_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "baseline_model_definitions.json"


class MeanBaselineRegressor(BaseEstimator, RegressorMixin):
    """Predicts the global mean of the training target variable."""
    def __init__(self):
        self.mean_ = None
        
    def fit(self, X, y):
        self.mean_ = float(np.mean(y))
        return self
        
    def predict(self, X):
        return np.full(shape=(len(X),), fill_value=self.mean_)


class MedianBaselineRegressor(BaseEstimator, RegressorMixin):
    """Predicts the global median of the training target variable (minimizes MAE)."""
    def __init__(self):
        self.median_ = None
        
    def fit(self, X, y):
        self.median_ = float(np.median(y))
        return self
        
    def predict(self, X):
        return np.full(shape=(len(X),), fill_value=self.median_)


class PurePhysicsSchottkyBaseline(BaseEstimator, RegressorMixin):
    """
    Zero-parameter physical reference model.
    Predicts log10(Rc) directly from the unpinned Schottky-Mott barrier via thermionic emission:
    Rc = R0 * exp(q * (Phi_M - chi) / kT)
    """
    def __init__(self, electron_affinity: float = 4.2, r0_log10: float = 2.0, kbt_ev: float = 0.0259):
        self.chi = electron_affinity
        self.r0 = r0_log10
        self.kbt = kbt_ev
        
    def fit(self, X, y=None):
        if y is not None:
            if isinstance(X, pd.DataFrame):
                wf = X["work_function_ev"].values
            else:
                wf = np.asarray(X)[:, 0]
            sbh_sm = np.clip(wf - self.chi, 0.0, 2.0)
            ideal_shift = (0.43429 / self.kbt) * np.clip(sbh_sm, 0.0, 0.3)
            self.r0 = float(np.median(y - ideal_shift))
        return self
        
    def predict(self, X):
        # Expects X to have work_function_ev or an array where column 0 is work_function_ev
        if isinstance(X, pd.DataFrame):
            wf = X["work_function_ev"].values
        else:
            wf = np.asarray(X)[:, 0]
        sbh_sm = np.clip(wf - self.chi, 0.0, 2.0)
        # Thermionic slope: log10(e) / (kT) = 0.43429 / 0.0259 = 16.76 / eV (saturated at high barriers)
        log_rc_pred = self.r0 + (0.43429 / self.kbt) * np.clip(sbh_sm, 0.0, 0.3)
        return log_rc_pred


def define_naive_statistical_baselines() -> Dict[str, Any]:
    """Catalog of statistical and physical benchmark baselines."""
    baselines = {
        "mean_regressor": {
            "type": "naive_statistical",
            "description": "Predicts constant training target mean. Minimizes squared loss among constant predictors.",
            "loss_optimized": "MSE"
        },
        "median_regressor": {
            "type": "naive_statistical",
            "description": "Predicts constant training target median. Minimizes L1 absolute loss among constant predictors.",
            "loss_optimized": "MAE"
        },
        "pure_physics_schottky_baseline": {
            "type": "physical_reference",
            "description": "Calculates log10(Rc) directly from ideal Schottky-Mott barrier (Phi_M - 4.2 eV) assuming classic thermionic transport without Fermi pinning.",
            "parameters": {"electron_affinity_ev": 4.2, "assumed_kbt_ev": 0.0259}
        }
    }
    
    BASELINE_DEF_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(BASELINE_DEF_JSON, "w", encoding="utf-8") as f:
        json.dump(baselines, f, indent=2)
        
    return baselines


def evaluate_baselines_on_curated_data(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Evaluates the reference baselines on the master curated MoS2 dataset."""
    define_naive_statistical_baselines()
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    y = df["log10_rc"].values
    X_wf = df[["work_function_ev"]]
    
    models = {
        "mean_baseline": MeanBaselineRegressor(),
        "median_baseline": MedianBaselineRegressor(),
        "pure_physics_schottky": PurePhysicsSchottkyBaseline()
    }
    
    results = {}
    for name, model in models.items():
        if name == "pure_physics_schottky":
            model.fit(X_wf, y)
            preds = model.predict(X_wf)
        else:
            model.fit(y, y)
            preds = model.predict(y)
            
        rmse = float(np.sqrt(mean_squared_error(y, preds)))
        mae = float(mean_absolute_error(y, preds))
        corr = float(np.corrcoef(y, preds)[0, 1]) if np.std(preds) > 1e-6 else 0.0
        
        results[name] = {
            "rmse_log10_rc": round(rmse, 3),
            "mae_log10_rc": round(mae, 3),
            "pearson_r": round(corr, 3)
        }
        
    return results


if __name__ == "__main__":
    b_defs = define_naive_statistical_baselines()
    scores = evaluate_baselines_on_curated_data()
    print("Baseline Model Definitions & Scores:")
    print(json.dumps(scores, indent=2))
