"""
Nested Paper-Wise Cross-Validation and Headline LOGO Benchmark (Sprint 7.4).
Eliminates selection optimism and guarantees true out-of-paper generalizability:
1. Outer GroupKFold (5 splits): Estimates performance on completely unseen literature publications.
2. Inner GroupKFold (3 splits): Selects hyperparameters strictly within the training fold.
3. Leave-One-Group-Out (LOGO / LPOCV): Benchmarks external generalization across all 23 primary sources.
"""

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
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel

from src.features.experimental_feature_engineer import (
    engineer_experimental_features,
    get_task1_rc_feature_names
)
from src.features.scientific_imputation_engine import ScientificMissingnessHandler
from src.validation.regression_metrics import evaluate_regression_metrics
from src.validation.selection_criteria import compute_composite_selection_score

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
FIGURES_DIR = ROOT_DIR / "reports" / "figures"
BENCHMARK_JSON_PATH = DATA_PROCESSED_DIR / "nested_and_logo_validation_benchmarks.json"
FIGURE_PATH = FIGURES_DIR / "nested_vs_logo_validation_comparison.png"


def get_candidate_model_registry() -> Dict[str, Dict[str, Any]]:
    """Defines candidate models and their hyperparameter tuning grids."""
    registry = {
        "Ridge_Regression": {
            "estimator_class": Ridge,
            "param_grid": [{"alpha": a} for a in [0.01, 0.1, 1.0, 5.0, 10.0, 50.0, 100.0]],
            "needs_scaling": True
        },
        "ElasticNet": {
            "estimator_class": ElasticNet,
            "param_grid": [{"alpha": a, "l1_ratio": l} for a in [0.05, 0.1, 0.5, 1.0] for l in [0.2, 0.5, 0.8]],
            "needs_scaling": True
        },
        "Random_Forest": {
            "estimator_class": RandomForestRegressor,
            "param_grid": [{"n_estimators": n, "max_depth": d, "random_state": 42} for n in [25, 50] for d in [2, 3, 4]],
            "needs_scaling": False
        },
        "Hist_Gradient_Boosting": {
            "estimator_class": HistGradientBoostingRegressor,
            "param_grid": [{"learning_rate": lr, "max_iter": m, "min_samples_leaf": s, "random_state": 42}
                           for lr in [0.02, 0.05, 0.1] for m in [20, 40] for s in [2, 4]],
            "needs_scaling": False
        },
        "Gaussian_Process_Matern": {
            "estimator_class": GaussianProcessRegressor,
            "param_grid": [{"kernel": Matern(length_scale=l, nu=2.5) + WhiteKernel(noise_level=n), "random_state": 42}
                           for l in [0.5, 1.0, 2.0] for n in [0.01, 0.1]],
            "needs_scaling": True
        }
    }

    # Attempt to add XGBoost if installed
    try:
        import xgboost as xgb
        registry["XGBoost_Regressor"] = {
            "estimator_class": xgb.XGBRegressor,
            "param_grid": [{"n_estimators": n, "max_depth": d, "learning_rate": lr, "random_state": 42}
                           for n in [20, 40] for d in [2, 3] for lr in [0.05, 0.1]],
            "needs_scaling": False
        }
    except ImportError:
        pass

    return registry


def run_inner_tuning_loop(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    groups_train: np.ndarray,
    model_config: Dict[str, Any],
    n_inner_splits: int = 3
) -> Dict[str, Any]:
    """
    Executes an inner GroupKFold search strictly within outer training folds to select optimal hyperparameters.
    """
    est_cls = model_config["estimator_class"]
    param_grid = model_config["param_grid"]
    needs_scaling = model_config["needs_scaling"]

    unique_groups = np.unique(groups_train)
    k_splits = min(n_inner_splits, len(unique_groups))
    if k_splits < 2:
        return param_grid[0]

    gkf_inner = GroupKFold(n_splits=k_splits)

    best_score = float("inf")
    best_params = param_grid[0]

    for params in param_grid:
        fold_rmses = []
        for in_tr_idx, in_val_idx in gkf_inner.split(X_train, y_train, groups=groups_train):
            X_in_tr, y_in_tr = X_train.iloc[in_tr_idx].copy(), y_train[in_tr_idx]
            X_in_val, y_in_val = X_train.iloc[in_val_idx].copy(), y_train[in_val_idx]

            # Fold-safe imputation and scaling
            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_in_tr = imputer.fit_transform(X_in_tr)
            X_in_val = imputer.transform(X_in_val)

            if needs_scaling:
                scaler = StandardScaler()
                X_in_tr = scaler.fit_transform(X_in_tr)
                X_in_val = scaler.transform(X_in_val)

            model = est_cls(**params)
            model.fit(X_in_tr, y_in_tr)
            preds = model.predict(X_in_val)
            rmse = float(np.sqrt(np.mean((y_in_val - preds) ** 2)))
            fold_rmses.append(rmse)

        mean_rmse = float(np.mean(fold_rmses))
        if mean_rmse < best_score:
            best_score = mean_rmse
            best_params = params

    return best_params


def evaluate_nested_group_kfold(
    X: pd.DataFrame,
    y: np.ndarray,
    groups: np.ndarray,
    n_outer_splits: int = 5
) -> Dict[str, Any]:
    """
    Runs full Nested GroupKFold cross-validation across all candidate models.
    """
    registry = get_candidate_model_registry()
    unique_groups = np.unique(groups)
    k_outer = min(n_outer_splits, len(unique_groups))
    gkf_outer = GroupKFold(n_splits=k_outer)

    nested_results = {}

    for model_name, config in registry.items():
        oof_predictions = np.zeros_like(y, dtype=float)
        outer_fold_metrics = []

        for fold_idx, (tr_idx, te_idx) in enumerate(gkf_outer.split(X, y, groups=groups)):
            X_tr, y_tr, g_tr = X.iloc[tr_idx].copy(), y[tr_idx], groups[tr_idx]
            X_te, y_te = X.iloc[te_idx].copy(), y[te_idx]

            # 1. Inner loop for hyperparameter tuning
            best_params = run_inner_tuning_loop(X_tr, y_tr, g_tr, config, n_inner_splits=3)

            # 2. Refit on full outer training split
            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_tr_proc = imputer.fit_transform(X_tr)
            X_te_proc = imputer.transform(X_te)

            if config["needs_scaling"]:
                scaler = StandardScaler()
                X_tr_proc = scaler.fit_transform(X_tr_proc)
                X_te_proc = scaler.transform(X_te_proc)

            est = config["estimator_class"](**best_params)
            est.fit(X_tr_proc, y_tr)

            te_preds = est.predict(X_te_proc)
            oof_predictions[te_idx] = te_preds

            fold_rmse = float(np.sqrt(np.mean((y_te - te_preds) ** 2)))
            outer_fold_metrics.append({"fold": fold_idx, "best_params": str(best_params), "rmse": round(fold_rmse, 4)})

        # Aggregate overall out-of-fold metrics
        rmse_total = float(np.sqrt(np.mean((y - oof_predictions) ** 2)))
        mae_total = float(np.mean(np.abs(y - oof_predictions)))
        rho, _ = spearmanr(y, oof_predictions)
        tau, _ = kendalltau(y, oof_predictions)

        # Multi-objective composite score
        score = compute_composite_selection_score(y, oof_predictions, feature_count=X.shape[1])

        nested_results[model_name] = {
            "validation_scheme": "Nested_GroupKFold_5",
            "rmse_dex": round(rmse_total, 4),
            "mae_dex": round(mae_total, 4),
            "spearman_rho": round(float(rho), 4),
            "kendall_tau": round(float(tau), 4),
            "composite_score": round(float(score["composite_selection_score"]), 4),
            "outer_folds": outer_fold_metrics,
            "oof_predictions": [round(float(p), 4) for p in oof_predictions]
        }

    return nested_results


def evaluate_leave_one_group_out(
    X: pd.DataFrame,
    y: np.ndarray,
    groups: np.ndarray
) -> Dict[str, Any]:
    """
    Executes Leave-One-Group-Out (LOGO / LPOCV) across all independent primary publications.
    """
    registry = get_candidate_model_registry()
    logo = LeaveOneGroupOut()
    logo_results = {}

    for model_name, config in registry.items():
        oof_predictions = np.zeros_like(y, dtype=float)
        paper_breakdown = {}

        for tr_idx, te_idx in logo.split(X, y, groups=groups):
            held_out_paper = str(groups[te_idx][0])
            X_tr, y_tr = X.iloc[tr_idx].copy(), y[tr_idx]
            X_te, y_te = X.iloc[te_idx].copy(), y[te_idx]

            # Fast fold-safe default configuration
            default_params = config["param_grid"][0]
            imputer = ScientificMissingnessHandler(mode="fold_imputed")
            X_tr_proc = imputer.fit_transform(X_tr)
            X_te_proc = imputer.transform(X_te)

            if config["needs_scaling"]:
                scaler = StandardScaler()
                X_tr_proc = scaler.fit_transform(X_tr_proc)
                X_te_proc = scaler.transform(X_te_proc)

            est = config["estimator_class"](**default_params)
            est.fit(X_tr_proc, y_tr)

            te_preds = est.predict(X_te_proc)
            oof_predictions[te_idx] = te_preds

            paper_rmse = float(np.sqrt(np.mean((y_te - te_preds) ** 2)))
            paper_breakdown[held_out_paper] = {
                "n_samples": int(len(te_idx)),
                "actual_log10_rc": [round(float(val), 3) for val in y_te],
                "pred_log10_rc": [round(float(val), 3) for val in te_preds],
                "rmse_dex": round(paper_rmse, 4)
            }

        rmse_total = float(np.sqrt(np.mean((y - oof_predictions) ** 2)))
        mae_total = float(np.mean(np.abs(y - oof_predictions)))
        rho, _ = spearmanr(y, oof_predictions)
        tau, _ = kendalltau(y, oof_predictions)
        score = compute_composite_selection_score(y, oof_predictions, feature_count=X.shape[1])

        logo_results[model_name] = {
            "validation_scheme": f"Leave_One_Group_Out ({len(paper_breakdown)} sources)",
            "rmse_dex": round(rmse_total, 4),
            "mae_dex": round(mae_total, 4),
            "spearman_rho": round(float(rho), 4),
            "kendall_tau": round(float(tau), 4),
            "composite_score": round(float(score["composite_selection_score"]), 4),
            "paper_breakdown": paper_breakdown,
            "oof_predictions": [round(float(p), 4) for p in oof_predictions]
        }

    return logo_results


def run_full_validation_benchmark_suite() -> Dict[str, Any]:
    """
    Executes Nested GroupKFold and LOGO across the primary experimental dataset,
    compares them, generates the benchmark JSON and publication graphic.
    """
    df = engineer_experimental_features()
    feature_cols = get_task1_rc_feature_names()

    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    groups = df["source_uid"].values

    print(f"Evaluating Nested GroupKFold across {len(X)} primary devices and {len(np.unique(groups))} source groups...")
    nested_res = evaluate_nested_group_kfold(X, y, groups, n_outer_splits=5)

    print(f"Evaluating Leave-One-Group-Out (LOGO) across {len(np.unique(groups))} source groups...")
    logo_res = evaluate_leave_one_group_out(X, y, groups)

    benchmark_output = {
        "title": "Nested GroupKFold and Leave-One-Group-Out (LOGO) Benchmark Suite",
        "dataset_statistics": {
            "n_observations": int(len(X)),
            "n_source_groups": int(len(np.unique(groups))),
            "features_evaluated": feature_cols
        },
        "nested_group_kfold_results": nested_res,
        "leave_one_group_out_results": logo_res
    }

    BENCHMARK_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BENCHMARK_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(benchmark_output, f, indent=2)

    _plot_validation_comparison(nested_res, logo_res)
    return benchmark_output


def _plot_validation_comparison(nested_res: Dict[str, Any], logo_res: Dict[str, Any]):
    models = sorted(list(nested_res.keys()))
    nested_rmse = [nested_res[m]["rmse_dex"] for m in models]
    logo_rmse = [logo_res[m]["rmse_dex"] for m in models]

    nested_rho = [nested_res[m]["spearman_rho"] for m in models]
    logo_rho = [logo_res[m]["spearman_rho"] for m in models]

    x = np.arange(len(models))
    width = 0.35

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Subplot 1: RMSE Comparison
    axes[0].bar(x - width/2, nested_rmse, width, label="Nested GroupKFold (Unbiased)", color="#1f77b4", edgecolor="black")
    axes[0].bar(x + width/2, logo_rmse, width, label="Leave-One-Group-Out (LOGO)", color="#ff7f0e", edgecolor="black")
    axes[0].set_ylabel("Out-of-Fold RMSE (dex)", fontsize=11, fontweight="bold")
    axes[0].set_title("Cross-Paper Generalization: RMSE by Validation Protocol", fontsize=12, fontweight="bold")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([m.replace('_', '\n') for m in models], fontsize=9)
    axes[0].legend(fontsize=10)
    axes[0].grid(axis="y", alpha=0.3, linestyle="--")

    # Subplot 2: Spearman Rank Correlation Comparison
    axes[1].bar(x - width/2, nested_rho, width, label="Nested GroupKFold (Unbiased)", color="#2ca02c", edgecolor="black")
    axes[1].bar(x + width/2, logo_rho, width, label="Leave-One-Group-Out (LOGO)", color="#9467bd", edgecolor="black")
    axes[1].set_ylabel("Spearman Rank Correlation (rho)", fontsize=11, fontweight="bold")
    axes[1].set_title("Rank Preservation: Spearman rho by Validation Protocol", fontsize=12, fontweight="bold")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([m.replace('_', '\n') for m in models], fontsize=9)
    axes[1].legend(fontsize=10)
    axes[1].set_ylim(0, 1.0)
    axes[1].grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURE_PATH, dpi=300)
    plt.close()


if __name__ == "__main__":
    out = run_full_validation_benchmark_suite()
    print("Nested and LOGO validation suite completed successfully.")
    print("Saved benchmark JSON to:", BENCHMARK_JSON_PATH)
    print("Saved figure to:", FIGURE_PATH)
