"""
Out-of-Fold Residual Diagnostics and Parity Visualizer (Sprint 4.e.1).
Analyzes residual distributions, heteroskedasticity, normality, feature-residual correlations,
and generates parity diagnostic plots with publication styling.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.models.model_factory import instantiate_tuned_candidate_model
from src.validation.selection_criteria import evaluate_model_cv

RESIDUALS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "out_of_fold_residuals_analysis.json"
PARITY_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "residual_parity_plot.png"
DIAGNOSTICS_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "residual_diagnostics.png"


def run_residual_diagnostics(
    df: Optional[pd.DataFrame] = None,
    champion_model_name: str = "Ridge_Regression",
    scheme: str = "grouped_5fold"
) -> Dict[str, Any]:
    """
    Computes out-of-fold residuals for the champion model and generates diagnostic visualizations.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    splits = get_cv_splits(df, scheme=scheme)
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    # Evaluate champion model
    model = instantiate_tuned_candidate_model(champion_model_name)
    eval_res = evaluate_model_cv(model, X, y, splits=splits)
    
    oof_preds = np.array(eval_res["oof_predictions"])
    residuals = y - oof_preds
    abs_residuals = np.abs(residuals)
    factor_errors = 10.0 ** abs_residuals

    # Normality test
    shapiro_stat, shapiro_p = stats.shapiro(residuals)
    skewness = float(stats.skew(residuals))
    kurt = float(stats.kurtosis(residuals))

    # Heteroskedasticity check: correlation between pred and abs(residual)
    het_r, het_p = stats.pearsonr(oof_preds, abs_residuals)

    # Attach to dataframe for outlier tracking
    records = []
    for idx in range(len(df)):
        row = df.iloc[idx]
        rec = {
            "device_id": str(row.get("device_id", f"dev_{idx}")),
            "contact_metal": str(row.get("contact_metal", "Unknown")),
            "source_paper_title": str(row.get("source_paper_title", "Unknown")),
            "source_uid": str(row.get("source_uid", "Unknown")),
            "observed_log10_rc": round(float(y[idx]), 4),
            "predicted_log10_rc": round(float(oof_preds[idx]), 4),
            "residual_dex": round(float(residuals[idx]), 4),
            "abs_residual_dex": round(float(abs_residuals[idx]), 4),
            "multiplicative_factor_error": round(float(factor_errors[idx]), 2),
            "is_outlier": bool(abs_residuals[idx] >= 0.35)
        }
        records.append(rec)

    # Sort by absolute error
    records_sorted = sorted(records, key=lambda x: x["abs_residual_dex"], reverse=True)
    outliers = [r for r in records_sorted if r["is_outlier"]]

    # Generate Figures
    PARITY_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _generate_parity_plot(y, oof_preds, df, champion_model_name, eval_res)
    _generate_residual_diagnostics_plot(y, oof_preds, residuals, df, champion_model_name)

    summary = {
        "champion_model": champion_model_name,
        "n_samples": len(df),
        "validation_scheme": scheme,
        "residual_statistics": {
            "mean_residual_dex": round(float(np.mean(residuals)), 4),
            "median_residual_dex": round(float(np.median(residuals)), 4),
            "std_residual_dex": round(float(np.std(residuals)), 4),
            "max_abs_residual_dex": round(float(np.max(abs_residuals)), 4),
            "mean_factor_error": round(float(np.mean(factor_errors)), 2),
            "median_factor_error": round(float(np.median(factor_errors)), 2),
            "shapiro_wilk_stat": round(float(shapiro_stat), 4),
            "shapiro_wilk_pvalue": round(float(shapiro_p), 4),
            "skewness": round(skewness, 4),
            "kurtosis": round(kurt, 4),
            "heteroskedasticity_pearson_r": round(float(het_r), 4),
            "heteroskedasticity_pvalue": round(float(het_p), 4)
        },
        "outlier_count": len(outliers),
        "outliers": outliers,
        "all_device_residuals": records_sorted
    }

    with open(RESIDUALS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def _generate_parity_plot(y, oof_preds, df, model_name, eval_res):
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    
    # 1:1 perfect line
    min_val = min(np.min(y), np.min(oof_preds)) - 0.3
    max_val = max(np.max(y), np.max(oof_preds)) + 0.3
    line_x = np.linspace(min_val, max_val, 100)
    
    ax.plot(line_x, line_x, "k-", lw=1.5, label="Perfect Agreement (1:1)")
    ax.fill_between(line_x, line_x - 0.3, line_x + 0.3, color="blue", alpha=0.10, label=r"$\pm 0.3$ dex (2$\times$ factor)")
    ax.plot(line_x, line_x + 0.3, "b--", lw=0.8, alpha=0.6)
    ax.plot(line_x, line_x - 0.3, "b--", lw=0.8, alpha=0.6)
    ax.plot(line_x, line_x + 1.0, "r:", lw=0.8, alpha=0.5, label=r"$\pm 1.0$ dex (10$\times$ factor)")
    ax.plot(line_x, line_x - 1.0, "r:", lw=0.8, alpha=0.5)

    # Scatter points colored by contact metal or de-pinning
    vdw = df["is_vdw_or_depinned_contact"].values
    for idx in range(len(df)):
        color = "forestgreen" if vdw[idx] == 1 else "firebrick"
        marker = "^" if vdw[idx] == 1 else "o"
        metal = df.iloc[idx]["contact_metal"]
        ax.scatter(y[idx], oof_preds[idx], c=color, marker=marker, s=65, edgecolors="k", lw=0.6, zorder=4)
        # Label high outliers
        if abs(y[idx] - oof_preds[idx]) >= 0.35:
            ax.annotate(f"{metal}", (y[idx], oof_preds[idx]), fontsize=7, xytext=(4, -4), textcoords="offset points")

    rmse = eval_res["underlying_metrics"]["rmse_log10_dex"]
    rho = eval_res["underlying_metrics"]["spearman_rho"]
    score = eval_res["composite_selection_score"]
    
    stats_text = f"{model_name} (Grouped 5-Fold OOF)\nRMSE = {rmse:.3f} dex\nSpearman $\\rho$ = {rho:.3f}\nScore = {score:.3f}"
    ax.text(0.04, 0.94, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9))

    ax.set_xlabel(r"Observed $\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$", fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Predicted $\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$", fontsize=11, fontweight="bold")
    ax.set_title("Out-of-Fold Parity Plot: MoS$_2$ Contact Resistance", fontsize=12, fontweight="bold")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(PARITY_PNG_PATH)
    plt.close()


def _generate_residual_diagnostics_plot(y, oof_preds, residuals, df, model_name):
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), dpi=300)
    
    # 1. Histogram & Normal KDE
    ax1 = axes[0, 0]
    ax1.hist(residuals, bins=9, density=True, alpha=0.6, color="royalblue", edgecolor="black")
    mu, std = np.mean(residuals), np.std(residuals)
    x_norm = np.linspace(mu - 3.5*std, mu + 3.5*std, 100)
    ax1.plot(x_norm, stats.norm.pdf(x_norm, mu, std), "r-", lw=2, label="Gaussian Fit")
    ax1.axvline(0, color="k", linestyle="--", lw=1)
    ax1.set_xlabel("Residual [dex]", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Probability Density", fontsize=10, fontweight="bold")
    ax1.set_title("(a) Residual Distribution Normality", fontsize=11, fontweight="bold")
    ax1.legend(fontsize=8)
    ax1.grid(True, linestyle=":", alpha=0.5)

    # 2. Residuals vs Predicted (Homoskedasticity)
    ax2 = axes[0, 1]
    ax2.scatter(oof_preds, residuals, c="navy", s=50, edgecolors="k", lw=0.6)
    ax2.axhline(0, color="k", linestyle="--", lw=1)
    ax2.axhline(0.3, color="gray", linestyle=":", lw=0.8)
    ax2.axhline(-0.3, color="gray", linestyle=":", lw=0.8)
    ax2.set_xlabel(r"Predicted $\log_{10}(R_c)$ [dex]", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Residual [dex]", fontsize=10, fontweight="bold")
    ax2.set_title("(b) Residuals vs Predicted (Homoskedasticity)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)

    # 3. Residuals vs Carrier Density
    ax3 = axes[1, 0]
    n2d = df["gate_carrier_density_cm2"].values / 1e13
    ax3.scatter(n2d, residuals, c="darkgreen", s=50, edgecolors="k", lw=0.6)
    ax3.axhline(0, color="k", linestyle="--", lw=1)
    ax3.set_xlabel(r"Normalized Carrier Density $\tilde{n}_{2D}$ [$10^{13}\ \mathrm{cm}^{-2}$]", fontsize=10, fontweight="bold")
    ax3.set_ylabel("Residual [dex]", fontsize=10, fontweight="bold")
    ax3.set_title(r"(c) Residuals vs Carrier Density $n_{2D}$", fontsize=11, fontweight="bold")
    ax3.grid(True, linestyle=":", alpha=0.5)

    # 4. Residuals vs Schottky Barrier Height
    ax4 = axes[1, 1]
    sbh = df["physics_predicted_sbh_ev"].values
    ax4.scatter(sbh, residuals, c="darkorange", s=50, edgecolors="k", lw=0.6)
    ax4.axhline(0, color="k", linestyle="--", lw=1)
    ax4.set_xlabel(r"Schottky Barrier Height $\Phi_B$ [eV]", fontsize=10, fontweight="bold")
    ax4.set_ylabel("Residual [dex]", fontsize=10, fontweight="bold")
    ax4.set_title(r"(d) Residuals vs Schottky Barrier Height $\Phi_B$", fontsize=11, fontweight="bold")
    ax4.grid(True, linestyle=":", alpha=0.5)

    plt.suptitle(f"MoS$_2$ Contact Resistance Error Diagnostics: {model_name}", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(DIAGNOSTICS_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = run_residual_diagnostics()
    print("Residual diagnostics complete.")
    print("Shapiro p-value:", res["residual_statistics"]["shapiro_wilk_pvalue"])
    print("Heteroskedasticity r:", res["residual_statistics"]["heteroskedasticity_pearson_r"])
    print("Outliers count:", res["outlier_count"])
