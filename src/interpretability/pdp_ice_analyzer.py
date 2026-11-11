"""
Permutation Importance, Partial Dependence (PDP), and ICE Engine (Sprint 5.a.2).
Computes out-of-fold permutation importance, 1D PDP with ICE curves, and 2D interaction surfaces
to reveal non-linear transport responses and heterogeneous sub-populations.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.models.model_factory import instantiate_tuned_candidate_model
from src.validation.regression_metrics import compute_log_rmse

PDP_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "pdp_and_permutation_importance.json"
PDP_ICE_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "pdp_ice_curves.png"
PDP_2D_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "pdp_2d_interaction_surface.png"
PERM_IMP_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "permutation_importance_oof.png"


def compute_oof_permutation_importance(
    model_name: str = "Ridge_Regression",
    df: Optional[pd.DataFrame] = None,
    n_repeats: int = 10,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Computes model-agnostic out-of-fold permutation importance across paper-grouped folds.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    splits = get_cv_splits(df, scheme="grouped_5fold")
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    # Baseline out-of-fold predictions
    oof_baseline = np.zeros(len(y))
    fold_models = []

    for train_idx, val_idx in splits:
        model = instantiate_tuned_candidate_model(model_name)
        model.fit(X.iloc[train_idx], y[train_idx])
        oof_baseline[val_idx] = model.predict(X.iloc[val_idx])
        fold_models.append((model, val_idx))

    base_rmse = compute_log_rmse(y, oof_baseline)

    rng = np.random.RandomState(random_state)
    importances = {f: [] for f in feature_cols}

    for repeat in range(n_repeats):
        for f in feature_cols:
            oof_permuted = np.zeros(len(y))
            for model, val_idx in fold_models:
                X_val_perm = X.iloc[val_idx].copy()
                # Scramble feature f within the validation fold
                X_val_perm[f] = rng.permutation(X_val_perm[f].values)
                oof_permuted[val_idx] = model.predict(X_val_perm)

            perm_rmse = compute_log_rmse(y, oof_permuted)
            delta_rmse = perm_rmse - base_rmse
            importances[f].append(float(delta_rmse))

    summary = {}
    for f in feature_cols:
        arr = np.array(importances[f])
        summary[f] = {
            "mean_delta_rmse_dex": round(float(np.mean(arr)), 4),
            "std_delta_rmse_dex": round(float(np.std(arr)), 4),
            "relative_importance_pct": 0.0  # calculated below
        }

    total_gain = sum(v["mean_delta_rmse_dex"] for v in summary.values())
    for f in feature_cols:
        summary[f]["relative_importance_pct"] = round(
            float(summary[f]["mean_delta_rmse_dex"] / total_gain * 100.0) if total_gain > 0 else 0.0, 1
        )

    return {
        "model_name": model_name,
        "base_oof_rmse_dex": round(float(base_rmse), 4),
        "permutation_importance": summary
    }


def compute_pdp_and_ice(
    model_name: str = "Ridge_Regression",
    df: Optional[pd.DataFrame] = None,
    grid_points: int = 50
) -> Dict[str, Any]:
    """
    Computes 1D Partial Dependence and ICE curves for continuous physical descriptors.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    model = instantiate_tuned_candidate_model(model_name)
    model.fit(X, y)

    continuous_features = [
        ("gate_carrier_density_cm2", 1e12, 2e13, r"Gate Carrier Density $n_{2D}$ [cm$^{-2}$]"),
        ("physics_predicted_sbh_ev", 0.0, 1.3, r"Schottky Barrier Height $\Phi_B$ [eV]"),
        ("sulfide_formation_enthalpy_kj_mol", -350.0, 0.0, r"Sulfide Enthalpy $\Delta H_f$ [kJ/mol]")
    ]

    pdp_results = {}

    for feat, f_min, f_max, label in continuous_features:
        grid = np.linspace(f_min, f_max, grid_points)
        ice_curves = []

        for idx in range(len(X)):
            X_temp = pd.DataFrame([X.iloc[idx].values] * grid_points, columns=feature_cols)
            X_temp[feat] = grid
            preds = model.predict(X_temp)
            ice_curves.append(preds.tolist())

        ice_arr = np.array(ice_curves)
        pdp_mean = np.mean(ice_arr, axis=0)

        pdp_results[feat] = {
            "label": label,
            "grid": [round(float(g), 4) for g in grid],
            "pdp_mean_curve": [round(float(p), 4) for p in pdp_mean],
            "ice_curves": ice_arr.tolist()
        }

    return pdp_results


def compute_2d_pdp_surface(
    model_name: str = "Ridge_Regression",
    df: Optional[pd.DataFrame] = None,
    grid_res: int = 40
) -> Dict[str, Any]:
    """
    Computes 2D partial dependence grid across n_2D x Phi_B interaction space.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    model = instantiate_tuned_candidate_model(model_name)
    model.fit(X, y)

    n2d_grid = np.linspace(2e12, 1.8e13, grid_res)
    phi_grid = np.linspace(0.0, 1.2, grid_res)

    N_mesh, P_mesh = np.meshgrid(n2d_grid, phi_grid)
    Z_mesh = np.zeros_like(N_mesh)

    # Average over background distribution of remaining features
    median_vdw = float(X["is_vdw_or_depinned_contact"].median())
    median_hf = float(X["sulfide_formation_enthalpy_kj_mol"].median())

    eval_df = pd.DataFrame({
        "physics_predicted_sbh_ev": P_mesh.ravel(),
        "is_vdw_or_depinned_contact": median_vdw,
        "sulfide_formation_enthalpy_kj_mol": median_hf,
        "gate_carrier_density_cm2": N_mesh.ravel()
    })[feature_cols]

    preds = model.predict(eval_df)
    Z_mesh = preds.reshape(grid_res, grid_res)

    return {
        "n2d_grid": n2d_grid.tolist(),
        "phi_grid": phi_grid.tolist(),
        "Z_mesh": Z_mesh.tolist()
    }


def run_full_pdp_and_permutation_analysis(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Runs full suite of out-of-fold permutation importance, 1D PDP+ICE, and 2D interaction surfaces.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    perm_res = compute_oof_permutation_importance("Ridge_Regression", df)
    pdp_res = compute_pdp_and_ice("Ridge_Regression", df)
    pdp_2d = compute_2d_pdp_surface("Ridge_Regression", df)

    # Generate Figures
    PDP_ICE_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _plot_pdp_ice(pdp_res, df)
    _plot_2d_interaction_surface(pdp_2d, df)
    _plot_permutation_importance(perm_res)

    output = {
        "title": "Model-Agnostic Permutation Importance and Partial Dependence Analysis",
        "permutation_importance": perm_res,
        "pdp_1d_curves": {
            k: {
                "label": v["label"],
                "grid_sample": v["grid"][:5],
                "pdp_mean_sample": v["pdp_mean_curve"][:5]
            }
            for k, v in pdp_res.items()
        }
    }

    with open(PDP_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output


def _plot_pdp_ice(pdp_res, df):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
    features = list(pdp_res.keys())

    for idx, (ax, feat) in enumerate(zip(axes, features)):
        data = pdp_res[feat]
        grid = np.array(data["grid"])
        ice = np.array(data["ice_curves"])
        pdp_mean = np.array(data["pdp_mean_curve"])

        # Plot individual ICE lines
        for i in range(len(ice)):
            ax.plot(grid, ice[i], color="gray", alpha=0.25, lw=0.8)

        # Plot population PDP mean
        ax.plot(grid, pdp_mean, color="crimson", lw=2.5, label="PDP Population Mean")

        # Formatting
        if "density" in feat:
            ax.set_xlabel(r"Gate Carrier Density $n_{2D}$ [$10^{13}\ \mathrm{cm}^{-2}$]", fontsize=10, fontweight="bold")
            ax.set_xticks(np.linspace(1e12, 2e13, 5))
            ax.set_xticklabels([f"{x/1e13:.1f}" for x in np.linspace(1e12, 2e13, 5)])
        else:
            ax.set_xlabel(data["label"], fontsize=10, fontweight="bold")

        ax.set_ylabel(r"Predicted $\log_{10} R_c$ [dex]", fontsize=10, fontweight="bold")
        ax.set_title(f"({chr(97+idx)}) {feat.replace('_', ' ').title()}", fontsize=11, fontweight="bold")
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, linestyle=":", alpha=0.5)

    plt.suptitle("1D Partial Dependence (PDP) & Individual Conditional Expectation (ICE) Curves", fontsize=12, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(PDP_ICE_PNG_PATH)
    plt.close()


def _plot_2d_interaction_surface(pdp_2d, df):
    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
    
    n2d_grid = np.array(pdp_2d["n2d_grid"]) / 1e13
    phi_grid = np.array(pdp_2d["phi_grid"])
    Z = np.array(pdp_2d["Z_mesh"])

    CS = ax.contourf(n2d_grid, phi_grid, Z, levels=14, cmap="viridis")
    cbar = fig.colorbar(CS, ax=ax)
    cbar.set_label(r"Predicted $\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$", fontsize=10, fontweight="bold")

    # Contour lines
    lines = ax.contour(n2d_grid, phi_grid, Z, levels=[2.0, 2.5, 3.0, 3.5, 4.0], colors="white", linewidths=0.8, linestyles="--")
    ax.clabel(lines, inline=True, fontsize=8, fmt="%.1f dex")

    # Overlay experimental data points
    exp_n2d = df["gate_carrier_density_cm2"].values / 1e13
    exp_phi = df["physics_predicted_sbh_ev"].values
    ax.scatter(exp_n2d, exp_phi, c="red", edgecolors="black", s=45, lw=0.6, label="Experimental Literature Devices", zorder=5)

    ax.set_xlabel(r"Normalized Gate Carrier Density $\tilde{n}_{2D}$ [$10^{13}\ \mathrm{cm}^{-2}$]", fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Schottky Barrier Height $\Phi_B$ [eV]", fontsize=11, fontweight="bold")
    ax.set_title(r"2D Partial Dependence Interaction Surface: $n_{2D} \times \Phi_B$", fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(PDP_2D_PNG_PATH)
    plt.close()


def _plot_permutation_importance(perm_res):
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    data = perm_res["permutation_importance"]
    
    features = list(data.keys())
    means = [data[f]["mean_delta_rmse_dex"] for f in features]
    stds = [data[f]["std_delta_rmse_dex"] for f in features]

    pretty_labels = [
        r"$\Phi_B$ (Schottky Barrier)",
        "vdW / De-pinned Contact",
        r"$\Delta H_f$ (Enthalpy)",
        r"$n_{2D}$ (Carrier Density)"
    ]

    y_pos = np.arange(len(features))
    ax.barh(y_pos, means, xerr=stds, align="center", color="teal", edgecolor="black", alpha=0.8, capsize=4)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pretty_labels, fontsize=10, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel(r"Mean Increase in Out-of-Fold RMSE $\Delta\mathrm{RMSE}$ [dex]", fontsize=10, fontweight="bold")
    ax.set_title("Out-of-Fold Model-Agnostic Permutation Feature Importance", fontsize=11, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(PERM_IMP_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = run_full_pdp_and_permutation_analysis()
    print("PDP & Permutation importance complete.")
    for f, d in res["permutation_importance"]["permutation_importance"].items():
        print(f"  - {f}: Delta RMSE = {d['mean_delta_rmse_dex']} dex ({d['relative_importance_pct']}%)")
