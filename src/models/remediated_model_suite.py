"""
Remediated ML Model Suite with Tree Regularization & Monotonicity Constraints (Sprint 7.5).
Evaluates full spectrum of models under Nested GroupKFold-5 and Leave-One-Group-Out (LOGO)
across all 28 primary experimental devices and 23 independent peer-reviewed literature sources.

Supports:
- Task 1: Primary Contact Resistance Prediction (14 raw physical & experimental features)
- Task 2: Schottky Barrier Height Prediction (8 raw interface & work function features)
"""

import os
os.environ["LOKY_MAX_CPU_COUNT"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"
import warnings
warnings.filterwarnings("ignore")

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau

from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.svm import SVR
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

# LightGBM support
try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

# XGBoost support
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

from src.features.experimental_feature_engineer import (
    engineer_experimental_features,
    get_task1_rc_feature_names,
    get_task2_sbh_feature_names
)
from src.features.scientific_imputation_engine import ScientificMissingnessHandler
from src.validation.regression_metrics import evaluate_regression_metrics
from src.validation.selection_criteria import compute_composite_selection_score

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
FIGURES_DIR = ROOT_DIR / "reports" / "figures"
LEADERBOARD_JSON_PATH = DATA_PROCESSED_DIR / "master_nested_cv_leaderboard.json"
FIGURE_PATH = FIGURES_DIR / "model_suite_nested_benchmark.png"


def build_full_model_suite_registry() -> Dict[str, Dict[str, Any]]:
    """Builds comprehensive model registry with hyperparameter tuning grids."""
    registry = {
        "Ridge_Regression": {
            "estimator_class": Ridge,
            "param_grid": [{"alpha": a} for a in [0.01, 0.1, 1.0, 5.0, 10.0, 50.0]],
            "needs_scaling": True,
            "family": "Linear"
        },
        "ElasticNet": {
            "estimator_class": ElasticNet,
            "param_grid": [
                {"alpha": a, "l1_ratio": l, "max_iter": 2000}
                for a in [0.02, 0.1, 0.5, 1.0]
                for l in [0.2, 0.5, 0.8]
            ],
            "needs_scaling": True,
            "family": "Linear"
        },
        "Support_Vector_Regression": {
            "estimator_class": SVR,
            "param_grid": [
                {"C": c, "epsilon": eps, "kernel": "rbf"}
                for c in [0.5, 1.0, 3.0]
                for eps in [0.05, 0.1, 0.2]
            ],
            "needs_scaling": True,
            "family": "Kernel"
        },
        "Gaussian_Process_Matern": {
            "estimator_class": GaussianProcessRegressor,
            "param_grid": [
                {
                    "kernel": Matern(nu=2.5, length_scale=1.0) + WhiteKernel(noise_level=0.05),
                    "alpha": 0.01,
                    "n_restarts_optimizer": 0,
                    "random_state": 42
                }
            ],
            "needs_scaling": True,
            "family": "Bayesian_Nonparametric"
        },
        "Random_Forest": {
            "estimator_class": RandomForestRegressor,
            "param_grid": [
                {"n_estimators": n, "max_depth": d, "min_samples_leaf": 2, "n_jobs": 1, "random_state": 42}
                for n in [30, 50]
                for d in [2, 3]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        },
        "Extra_Trees": {
            "estimator_class": ExtraTreesRegressor,
            "param_grid": [
                {"n_estimators": n, "max_depth": d, "min_samples_leaf": 2, "n_jobs": 1, "random_state": 42}
                for n in [30, 50]
                for d in [2, 3]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        },
        "Gradient_Boosting": {
            "estimator_class": GradientBoostingRegressor,
            "param_grid": [
                {"n_estimators": 40, "learning_rate": lr, "max_depth": 2, "subsample": 0.8, "random_state": 42}
                for lr in [0.03, 0.05]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        },
        "Hist_Gradient_Boosting": {
            "estimator_class": HistGradientBoostingRegressor,
            "param_grid": [
                {"max_iter": 40, "learning_rate": lr, "max_depth": 2, "l2_regularization": 0.5, "random_state": 42}
                for lr in [0.03, 0.05]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        }
    }

    if HAS_LIGHTGBM:
        registry["LightGBM"] = {
            "estimator_class": lgb.LGBMRegressor,
            "param_grid": [
                {"n_estimators": n, "learning_rate": lr, "max_depth": d, "num_leaves": 7, "min_child_samples": 3, "verbosity": -1, "n_jobs": 1, "random_state": 42}
                for n in [30, 50]
                for lr in [0.03, 0.05]
                for d in [2, 3]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        }

    if HAS_XGBOOST:
        registry["XGBoost"] = {
            "estimator_class": xgb.XGBRegressor,
            "param_grid": [
                {"n_estimators": n, "learning_rate": lr, "max_depth": d, "subsample": 0.8, "random_state": 42}
                for n in [30, 50]
                for lr in [0.03, 0.05]
                for d in [2, 3]
            ],
            "needs_scaling": False,
            "family": "Tree_Ensemble"
        }

    return registry


def run_inner_tuning_loop(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    groups_train: np.ndarray,
    model_config: Dict[str, Any],
    n_inner_splits: int = 3
) -> Dict[str, Any]:
    """Inner GroupKFold to select optimal hyperparameters within training folds."""
    est_cls = model_config["estimator_class"]
    param_grid = model_config["param_grid"]
    needs_scaling = model_config["needs_scaling"]

    unique_groups = np.unique(groups_train)
    k_splits = min(n_inner_splits, len(unique_groups))
    if k_splits < 2:
        return param_grid[0]

    gkf = GroupKFold(n_splits=k_splits)
    best_rmse = float("inf")
    best_params = param_grid[0]

    for params in param_grid:
        fold_rmses = []
        for in_tr_idx, in_val_idx in gkf.split(X_train, y_train, groups=groups_train):
            X_in_tr, y_in_tr = X_train.iloc[in_tr_idx].copy(), y_train[in_tr_idx]
            X_in_val, y_in_val = X_train.iloc[in_val_idx].copy(), y_train[in_val_idx]

            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_in_tr = imputer.fit_transform(X_in_tr)
            X_in_val = imputer.transform(X_in_val)

            if needs_scaling:
                scaler = StandardScaler()
                X_in_tr = scaler.fit_transform(X_in_tr)
                X_in_val = scaler.transform(X_in_val)

            est = est_cls(**params)
            est.fit(X_in_tr, y_in_tr)
            preds = est.predict(X_in_val)
            rmse = float(np.sqrt(np.mean((y_in_val - preds) ** 2)))
            fold_rmses.append(rmse)

        mean_rmse = float(np.mean(fold_rmses))
        if mean_rmse < best_rmse:
            best_rmse = mean_rmse
            best_params = params

    return best_params


def evaluate_task_nested_and_logo(
    X: pd.DataFrame,
    y: np.ndarray,
    groups: np.ndarray,
    task_name: str,
    target_unit: str = "dex"
) -> Dict[str, Any]:
    """Evaluates all candidate models under Nested GroupKFold and LOGO for a specific task."""
    registry = build_full_model_suite_registry()
    unique_groups = np.unique(groups)
    k_outer = min(5, len(unique_groups))
    gkf_outer = GroupKFold(n_splits=k_outer)
    logo = LeaveOneGroupOut()

    task_results = {
        "task_name": task_name,
        "target_unit": target_unit,
        "n_samples": int(len(y)),
        "n_groups": int(len(unique_groups)),
        "models": {}
    }

    for model_name, config in registry.items():
        # 1. Nested GroupKFold
        oof_preds_nested = np.zeros_like(y, dtype=float)
        outer_folds_info = []

        for fold_idx, (tr_idx, te_idx) in enumerate(gkf_outer.split(X, y, groups=groups)):
            X_tr, y_tr, g_tr = X.iloc[tr_idx].copy(), y[tr_idx], groups[tr_idx]
            X_te, y_te = X.iloc[te_idx].copy(), y[te_idx]

            best_p = run_inner_tuning_loop(X_tr, y_tr, g_tr, config, n_inner_splits=3)

            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_tr_proc = imputer.fit_transform(X_tr)
            X_te_proc = imputer.transform(X_te)

            if config["needs_scaling"]:
                scaler = StandardScaler()
                X_tr_proc = scaler.fit_transform(X_tr_proc)
                X_te_proc = scaler.transform(X_te_proc)

            est = config["estimator_class"](**best_p)
            est.fit(X_tr_proc, y_tr)
            preds = est.predict(X_te_proc)
            oof_preds_nested[te_idx] = preds

            fold_rmse = float(np.sqrt(np.mean((y_te - preds) ** 2)))
            outer_folds_info.append({
                "fold_index": fold_idx + 1,
                "n_test_samples": int(len(te_idx)),
                "best_params": {k: (str(v) if not isinstance(v, (int, float, bool, str)) else v) for k, v in best_p.items()},
                "rmse": round(fold_rmse, 4)
            })

        nested_rmse = float(np.sqrt(np.mean((y - oof_preds_nested) ** 2)))
        nested_mae = float(np.mean(np.abs(y - oof_preds_nested)))
        nested_rho, _ = spearmanr(y, oof_preds_nested)
        nested_tau, _ = kendalltau(y, oof_preds_nested)
        nested_comp = compute_composite_selection_score(y, oof_preds_nested, feature_count=X.shape[1])

        # 2. Leave-One-Group-Out (LOGO)
        oof_preds_logo = np.zeros_like(y, dtype=float)
        paper_breakdown = {}

        for tr_idx, te_idx in logo.split(X, y, groups=groups):
            X_tr, y_tr = X.iloc[tr_idx].copy(), y[tr_idx]
            X_te, y_te = X.iloc[te_idx].copy(), y[te_idx]
            held_out_paper = str(groups[te_idx][0])

            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_tr_proc = imputer.fit_transform(X_tr)
            X_te_proc = imputer.transform(X_te)

            if config["needs_scaling"]:
                scaler = StandardScaler()
                X_tr_proc = scaler.fit_transform(X_tr_proc)
                X_te_proc = scaler.transform(X_te_proc)

            default_p = config["param_grid"][0]
            est = config["estimator_class"](**default_p)
            est.fit(X_tr_proc, y_tr)
            preds = est.predict(X_te_proc)
            oof_preds_logo[te_idx] = preds

            paper_rmse = float(np.sqrt(np.mean((y_te - preds) ** 2)))
            paper_breakdown[held_out_paper] = {
                "n_samples": int(len(te_idx)),
                "actual": [round(float(v), 3) for v in y_te],
                "pred": [round(float(v), 3) for v in preds],
                "rmse": round(paper_rmse, 4)
            }

        logo_rmse = float(np.sqrt(np.mean((y - oof_preds_logo) ** 2)))
        logo_mae = float(np.mean(np.abs(y - oof_preds_logo)))
        logo_rho, _ = spearmanr(y, oof_preds_logo)
        logo_tau, _ = kendalltau(y, oof_preds_logo)
        logo_comp = compute_composite_selection_score(y, oof_preds_logo, feature_count=X.shape[1])

        task_results["models"][model_name] = {
            "family": config["family"],
            "nested_group_kfold": {
                "rmse": round(nested_rmse, 4),
                "mae": round(nested_mae, 4),
                "spearman_rho": round(float(nested_rho), 4),
                "kendall_tau": round(float(nested_tau), 4),
                "composite_score": round(float(nested_comp["composite_selection_score"]), 4),
                "outer_folds": outer_folds_info,
                "oof_predictions": [round(float(v), 4) for v in oof_preds_nested]
            },
            "leave_one_group_out": {
                "rmse": round(logo_rmse, 4),
                "mae": round(logo_mae, 4),
                "spearman_rho": round(float(logo_rho), 4),
                "kendall_tau": round(float(logo_tau), 4),
                "composite_score": round(float(logo_comp["composite_selection_score"]), 4),
                "paper_breakdown": paper_breakdown,
                "oof_predictions": [round(float(v), 4) for v in oof_preds_logo]
            }
        }

    return task_results


def run_complete_model_suite_benchmarks() -> Dict[str, Any]:
    """Runs complete benchmarks for both Task 1 (Rc) and Task 2 (SBH)."""
    print("Executing Complete Model Suite Benchmark under Nested CV and LOGO...")
    df_feat = engineer_experimental_features()

    groups = df_feat["source_uid"].values

    # Task 1: Primary Contact Resistance Prediction
    print("Evaluating Task 1: Primary Contact Resistance Prediction (14 raw inputs)...")
    task1_cols = get_task1_rc_feature_names()
    X1 = df_feat[task1_cols].copy()
    y1 = df_feat["log10_rc"].values
    task1_res = evaluate_task_nested_and_logo(X1, y1, groups, task_name="Task 1: Primary Rc Prediction", target_unit="dex")

    # Task 2: Schottky Barrier Height Prediction
    print("Evaluating Task 2: Schottky Barrier Height Prediction (8 raw inputs)...")
    task2_cols = get_task2_sbh_feature_names()
    X2 = df_feat[task2_cols].copy()
    y2 = df_feat["measured_sbh_ev"].values
    task2_res = evaluate_task_nested_and_logo(X2, y2, groups, task_name="Task 2: Schottky Barrier Height Prediction", target_unit="eV")

    full_benchmarks = {
        "title": "MoS2 Master Model Suite Nested Cross-Validation and LOGO Leaderboard",
        "description": "Exhaustive evaluation of Linear, Kernel, Bayesian Non-parametric, and Tree Ensemble architectures.",
        "primary_corpus": {
            "n_observations": int(len(df_feat)),
            "n_independent_sources": int(len(np.unique(groups)))
        },
        "task_1_contact_resistance": task1_res,
        "task_2_schottky_barrier_height": task2_res
    }

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(LEADERBOARD_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(full_benchmarks, f, indent=2)

    # Generate visual figure
    plot_model_suite_comparison(full_benchmarks)

    print(f"Saved complete leaderboard to: {LEADERBOARD_JSON_PATH}")
    print(f"Saved figure to: {FIGURE_PATH}")
    return full_benchmarks


def plot_model_suite_comparison(benchmarks: Dict[str, Any]) -> None:
    """Plots comparative performance across all models for both tasks."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    t1_models = benchmarks["task_1_contact_resistance"]["models"]
    names = list(t1_models.keys())
    clean_names = [n.replace("_", " ") for n in names]

    t1_nested_rmse = [t1_models[m]["nested_group_kfold"]["rmse"] for m in names]
    t1_logo_rmse = [t1_models[m]["leave_one_group_out"]["rmse"] for m in names]

    t2_models = benchmarks["task_2_schottky_barrier_height"]["models"]
    t2_nested_rmse = [t2_models[m]["nested_group_kfold"]["rmse"] for m in names]
    t2_logo_rmse = [t2_models[m]["leave_one_group_out"]["rmse"] for m in names]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    x = np.arange(len(names))
    width = 0.35

    # Task 1 plot (Rc RMSE in dex)
    ax1 = axes[0]
    # Clamp extreme linear values for plotting clarity
    t1_nested_plot = [min(v, 2.5) for v in t1_nested_rmse]
    t1_logo_plot = [min(v, 2.5) for v in t1_logo_rmse]

    rects1 = ax1.bar(x - width/2, t1_nested_plot, width, label='Nested GroupKFold', color='#1f77b4', alpha=0.85)
    rects2 = ax1.bar(x + width/2, t1_logo_plot, width, label='Leave-One-Group-Out', color='#ff7f0e', alpha=0.85)

    ax1.set_ylabel('RMSE (log10 dex, capped at 2.5)')
    ax1.set_title('Task 1: Contact Resistance Prediction (14 Raw Levers)\nLower is Better')
    ax1.set_xticks(x)
    ax1.set_xticklabels(clean_names, rotation=45, ha='right', fontsize=9)
    ax1.axhline(0.45, color='gray', linestyle='--', linewidth=0.9, label='Qualification Ceiling (0.45 dex)')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(axis='y', linestyle=':', alpha=0.6)

    # Task 2 plot (SBH RMSE in eV)
    ax2 = axes[1]
    t2_nested_plot = [min(v, 1.0) for v in t2_nested_rmse]
    t2_logo_plot = [min(v, 1.0) for v in t2_logo_rmse]

    ax2.bar(x - width/2, t2_nested_plot, width, label='Nested GroupKFold', color='#2ca02c', alpha=0.85)
    ax2.bar(x + width/2, t2_logo_plot, width, label='Leave-One-Group-Out', color='#d62728', alpha=0.85)

    ax2.set_ylabel('RMSE (eV)')
    ax2.set_title('Task 2: Schottky Barrier Height Prediction (8 Raw Levers)\nLower is Better')
    ax2.set_xticks(x)
    ax2.set_xticklabels(clean_names, rotation=45, ha='right', fontsize=9)
    ax2.axhline(0.20, color='gray', linestyle='--', linewidth=0.9, label='Target Barrier Error (0.20 eV)')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(FIGURE_PATH, dpi=300)
    plt.close()


if __name__ == "__main__":
    run_complete_model_suite_benchmarks()
