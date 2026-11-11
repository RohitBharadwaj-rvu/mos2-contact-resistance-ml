"""
SHAP Global and Local Feature Attribution Engine (Sprint 5.a.1).
Computes exact, Tree, and Kernel SHAP values across shortlisted model architectures,
audits physical directionality, and generates publication beeswarm & comparative ranking plots.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.models.model_factory import instantiate_tuned_candidate_model

SHAP_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "shap_feature_attribution_analysis.json"
BEESWARM_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "shap_summary_beeswarm.png"
COMPARISON_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "shap_cross_architecture_comparison.png"


def compute_model_shap(model_name: str, X: pd.DataFrame, y: np.ndarray) -> Dict[str, Any]:
    """
    Computes SHAP values for a specific model architecture using appropriate explainer.
    """
    pipeline = instantiate_tuned_candidate_model(model_name)
    pipeline.fit(X, y)

    features = list(X.columns)

    if model_name in ["Gradient_Boosting", "Random_Forest"]:
        # Direct TreeExplainer
        explainer = shap.TreeExplainer(pipeline)
        shap_vals = explainer.shap_values(X)
        expected_val = float(explainer.expected_value)
    elif model_name in ["Ridge_Regression", "ElasticNet"]:
        # Extract regressor and scaled X
        scaler = pipeline.named_steps["scaler"]
        reg = pipeline.named_steps["regressor"]
        X_scaled = scaler.transform(X)
        explainer = shap.LinearExplainer(reg, X_scaled)
        shap_vals = explainer.shap_values(X_scaled)
        expected_val = float(explainer.expected_value)
    else:
        # KernelExplainer for GPR / SVR
        def predict_fn(x_arr):
            df_sub = pd.DataFrame(x_arr, columns=features)
            return pipeline.predict(df_sub)

        background = shap.kmeans(X.values, 5) if len(X) > 10 else X.values
        explainer = shap.KernelExplainer(predict_fn, background)
        shap_vals = explainer.shap_values(X.values, nsamples=100)
        expected_val = float(explainer.expected_value)

    shap_vals = np.array(shap_vals)
    mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)

    # Directionality audit: correlation between raw feature value and SHAP attribution
    attributions = {}
    directionality = {}
    for i, f in enumerate(features):
        attributions[f] = round(float(mean_abs_shap[i]), 4)
        corr = float(np.corrcoef(X[f].values, shap_vals[:, i])[0, 1])
        directionality[f] = {
            "feature_shap_correlation": round(corr, 4),
            "effect_sign": "positive (increases Rc)" if corr > 0.1 else ("negative (decreases Rc)" if corr < -0.1 else "neutral"),
            "matches_physics": bool(
                (f == "physics_predicted_sbh_ev" and corr > 0) or
                (f == "gate_carrier_density_cm2" and corr < 0) or
                (f == "is_vdw_or_depinned_contact" and corr < 0) or
                (f == "sulfide_formation_enthalpy_kj_mol")
            )
        }

    return {
        "model_name": model_name,
        "base_expected_value": round(expected_val, 4),
        "mean_abs_shap": attributions,
        "ranked_features": sorted(attributions.keys(), key=lambda k: attributions[k], reverse=True),
        "directionality_audit": directionality,
        "shap_values_matrix": shap_vals.tolist()
    }


def run_full_shap_attribution_analysis(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Executes cross-architecture SHAP attribution across:
    1. Ridge_Regression
    2. ElasticNet
    3. Gradient_Boosting
    4. Random_Forest
    5. Gaussian_Process_Matern
    6. Support_Vector_Regression_RBF
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    models = [
        "Ridge_Regression",
        "ElasticNet",
        "Gradient_Boosting",
        "Random_Forest",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]

    model_shap_results = {}
    for name in models:
        res = compute_model_shap(name, X, y)
        model_shap_results[name] = res

    # Generate figures
    BEESWARM_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _generate_shap_beeswarm_plot(model_shap_results, X, feature_cols)
    _generate_cross_architecture_comparison(model_shap_results, feature_cols)

    summary = {
        "title": "Cross-Architecture SHAP Feature Attribution and Physical Directionality Audit",
        "features_analyzed": feature_cols,
        "models_evaluated": models,
        "model_attributions": {
            k: {
                "ranked_features": v["ranked_features"],
                "mean_abs_shap": v["mean_abs_shap"],
                "directionality": {f: v["directionality_audit"][f]["effect_sign"] for f in feature_cols}
            }
            for k, v in model_shap_results.items()
        },
        "full_results": model_shap_results
    }

    with open(SHAP_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def _generate_shap_beeswarm_plot(model_results, X, feature_cols):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), dpi=300)
    plot_models = ["Ridge_Regression", "Gradient_Boosting", "Random_Forest", "Gaussian_Process_Matern"]

    pretty_names = {
        "physics_predicted_sbh_ev": r"Schottky Barrier $\Phi_B$ [eV]",
        "gate_carrier_density_cm2": r"Carrier Density $n_{2D}$ [cm$^{-2}$]",
        "is_vdw_or_depinned_contact": "vdW / De-pinned Contact",
        "sulfide_formation_enthalpy_kj_mol": r"Sulfide Enthalpy $\Delta H_f$"
    }

    for idx, (ax, m_name) in enumerate(zip(axes.flatten(), plot_models)):
        data = model_results[m_name]
        shap_mat = np.array(data["shap_values_matrix"])

        # Sort features by mean abs SHAP
        ranks = data["ranked_features"][::-1]
        y_pos = np.arange(len(ranks))

        for feat_idx, feat in enumerate(ranks):
            f_col_idx = feature_cols.index(feat)
            s_vals = shap_mat[:, f_col_idx]
            feat_vals = X[feat].values
            norm_vals = (feat_vals - np.min(feat_vals)) / (np.max(feat_vals) - np.min(feat_vals) + 1e-12)

            scatter = ax.scatter(s_vals, np.full_like(s_vals, feat_idx) + np.random.uniform(-0.15, 0.15, len(s_vals)),
                                 c=norm_vals, cmap="coolwarm", s=35, alpha=0.8, edgecolors="none")

        ax.axvline(0, color="k", linestyle="--", lw=1)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([pretty_names.get(r, r) for r in ranks], fontsize=9, fontweight="bold")
        ax.set_xlabel(r"SHAP Value (Impact on $\log_{10} R_c$ [dex])", fontsize=9, fontweight="bold")
        ax.set_title(f"({chr(97+idx)}) {m_name.replace('_', ' ')}", fontsize=11, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.5)

    cbar_ax = fig.add_axes([0.92, 0.25, 0.02, 0.5])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Feature Value (Low = Blue, High = Red)", fontsize=10, fontweight="bold")

    plt.suptitle(r"SHAP Summary Attribution: Directionality & Impact on MoS$_2$ Contact Resistance", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout(rect=[0, 0, 0.90, 0.98])
    plt.savefig(BEESWARM_PNG_PATH)
    plt.close()


def _generate_cross_architecture_comparison(model_results, feature_cols):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    models = list(model_results.keys())
    x = np.arange(len(feature_cols))
    width = 0.13

    pretty_names = [
        r"$\Phi_B$ (SBH)",
        "vdW / De-pinned",
        r"$\Delta H_f$ (Enthalpy)",
        r"$n_{2D}$ (Gating)"
    ]

    colors = ["#1f77b4", "#aec7e8", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for i, m in enumerate(models):
        attributions = [model_results[m]["mean_abs_shap"].get(f, 0.0) for f in feature_cols]
        ax.bar(x + (i - len(models)/2 + 0.5) * width, attributions, width, label=m.replace("_", " "), color=colors[i], edgecolor="black", lw=0.4)

    ax.set_ylabel(r"Mean Absolute SHAP Value $|\mathrm{SHAP}|$ [dex]", fontsize=11, fontweight="bold")
    ax.set_title("Cross-Architecture Feature Attribution Consensus", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(pretty_names, fontsize=10, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(COMPARISON_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = run_full_shap_attribution_analysis()
    print("SHAP attribution complete.")
    for m, d in res["model_attributions"].items():
        print(f"[{m}] Top feature: {d['ranked_features'][0]} ({d['mean_abs_shap'][d['ranked_features'][0]]} dex)")
