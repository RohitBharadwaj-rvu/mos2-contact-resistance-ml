"""
Domain-Specific Monotonicity Constrained Models (Sprint 4.c.3).
Enforces physical monotonicity constraints on gradient boosted trees to guarantee physically plausible
predictions (e.g., d(Rc)/d(SBH) >= 0, d(Rc)/d(n_2D) <= 0, d(Rc)/d(vdW) <= 0).
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.validation.selection_criteria import evaluate_model_cv

CONSTRAINTS_COMPARISON_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "monotonic_constraints_comparison.json"


PHYSICAL_MONOTONICITY_RULES = {
    "physics_predicted_sbh_ev": 1,          # Higher Schottky barrier height physically MUST increase contact resistance (dRc/dPhi >= 0)
    "is_vdw_or_depinned_contact": -1,       # vdW/depinned contacts eliminate Fermi-level pinning, reducing Rc (dRc/d(vdW) <= 0)
    "sulfide_formation_enthalpy_kj_mol": 0, # Enthalpy has non-monotonic interactions (moderate reactivity can form good ohmic bonds vs high defect pinning)
    "gate_carrier_density_cm2": -1          # Higher gate carrier density thins depletion barrier and increases tunneling (dRc/d(n_2D) <= 0)
}


class MonotonicLGBMWrapper(BaseEstimator, RegressorMixin):
    """
    LightGBM Regressor enforcing monotonic physical constraints.
    """
    def __init__(
        self,
        monotone_constraints: Optional[List[int]] = None,
        n_estimators: int = 50,
        learning_rate: float = 0.05,
        max_depth: int = 3,
        num_leaves: int = 7,
        subsample: float = 0.8,
        min_child_samples: int = 2,
        random_state: int = 42
    ):
        self.monotone_constraints = monotone_constraints
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.num_leaves = num_leaves
        self.subsample = subsample
        self.min_child_samples = min_child_samples
        self.random_state = random_state
        self.model_ = None

    def fit(self, X, y):
        X_arr = np.asarray(X)
        y_arr = np.asarray(y)
        params = {
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate,
            "max_depth": self.max_depth,
            "num_leaves": self.num_leaves,
            "subsample": self.subsample,
            "subsample_freq": 1,
            "min_child_samples": self.min_child_samples,
            "random_state": self.random_state,
            "verbose": -1
        }
        if self.monotone_constraints is not None:
            params["monotone_constraints"] = self.monotone_constraints

        self.model_ = lgb.LGBMRegressor(**params)
        self.model_.fit(X_arr, y_arr)
        return self

    def predict(self, X):
        X_arr = np.asarray(X)
        return self.model_.predict(X_arr)


def get_monotonicity_vector(feature_names: List[str]) -> List[int]:
    """
    Maps feature names to their theoretical physical monotonicity direction (+1, -1, 0).
    """
    return [PHYSICAL_MONOTONICITY_RULES.get(f, 0) for f in feature_names]


def run_monotonicity_constraint_experiment(
    df: Optional[pd.DataFrame] = None,
    scheme: str = "grouped_5fold"
) -> Dict[str, Any]:
    """
    Compares unconstrained vs physically monotonic gradient boosted models
    across paper-grouped 5-fold cross validation.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    splits = get_cv_splits(df, scheme=scheme)
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    monotone_vector = get_monotonicity_vector(feature_cols)

    # 1. Unconstrained LightGBM
    unconstrained_lgbm = MonotonicLGBMWrapper(
        monotone_constraints=None,
        n_estimators=50,
        learning_rate=0.05,
        max_depth=3,
        num_leaves=7,
        random_state=42
    )
    unconstrained_metrics = evaluate_model_cv(unconstrained_lgbm, X, y, splits=splits)

    # 2. Monotonically Constrained LightGBM
    constrained_lgbm = MonotonicLGBMWrapper(
        monotone_constraints=monotone_vector,
        n_estimators=50,
        learning_rate=0.05,
        max_depth=3,
        num_leaves=7,
        random_state=42
    )
    constrained_metrics = evaluate_model_cv(constrained_lgbm, X, y, splits=splits)

    # 3. Unconstrained HistGB
    unconstrained_hist = HistGradientBoostingRegressor(
        monotonic_cst=None,
        max_iter=50,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )
    unconstrained_hist_metrics = evaluate_model_cv(unconstrained_hist, X, y, splits=splits)

    # 4. Monotonically Constrained HistGB
    constrained_hist = HistGradientBoostingRegressor(
        monotonic_cst=monotone_vector,
        max_iter=50,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )
    constrained_hist_metrics = evaluate_model_cv(constrained_hist, X, y, splits=splits)

    comparison = {
        "features": feature_cols,
        "monotone_constraints_applied": {
            feat: rule for feat, rule in zip(feature_cols, monotone_vector)
        },
        "lightgbm_unconstrained": unconstrained_metrics,
        "lightgbm_constrained": constrained_metrics,
        "histgb_unconstrained": unconstrained_hist_metrics,
        "histgb_constrained": constrained_hist_metrics,
        "summary_deltas": {
            "lgbm_score_gain": round(
                constrained_metrics["composite_selection_score"] - unconstrained_metrics["composite_selection_score"],
                4
            ),
            "lgbm_rmse_reduction_dex": round(
                unconstrained_metrics["underlying_metrics"]["rmse_log10_dex"] - constrained_metrics["underlying_metrics"]["rmse_log10_dex"],
                4
            ),
            "histgb_score_gain": round(
                constrained_hist_metrics["composite_selection_score"] - unconstrained_hist_metrics["composite_selection_score"],
                4
            ),
            "histgb_rmse_reduction_dex": round(
                unconstrained_hist_metrics["underlying_metrics"]["rmse_log10_dex"] - constrained_hist_metrics["underlying_metrics"]["rmse_log10_dex"],
                4
            )
        }
    }

    CONSTRAINTS_COMPARISON_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(CONSTRAINTS_COMPARISON_JSON, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2)

    return comparison


if __name__ == "__main__":
    res = run_monotonicity_constraint_experiment()
    print("Monotonicity constraint experiment complete.")
    print("LightGBM Score:", res["lightgbm_unconstrained"]["composite_selection_score"], "->", res["lightgbm_constrained"]["composite_selection_score"])
    print("HistGB Score:", res["histgb_unconstrained"]["composite_selection_score"], "->", res["histgb_constrained"]["composite_selection_score"])
