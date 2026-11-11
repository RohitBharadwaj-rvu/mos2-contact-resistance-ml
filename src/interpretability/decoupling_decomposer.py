"""
Intrinsic vs Extrinsic Resistance Decomposition Engine (Sprint 5.b.2).
Decomposes total observed contact resistance into fundamental intrinsic transport (SBH, gating, quantum limit)
and extrinsic processing-induced modifiers (vdW transfer, defect creation, interfacial chemical bonding).
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features

DECOUPLING_RESULTS_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "intrinsic_extrinsic_decoupling_results.json"
DECOUPLING_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "intrinsic_vs_extrinsic_decomposition.png"


def run_intrinsic_extrinsic_decomposition(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Decomposes log10(Rc) = f_intrinsic(Phi_B, n_2D) + g_extrinsic(vdW, Delta_Hf) + epsilon.
    Quantifies the exact percentage of total variance explained by intrinsic vs extrinsic factors.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    y = df["log10_rc"].values
    n = len(y)
    total_var = float(np.var(y, ddof=1))

    # Intrinsic features: barrier height and gate carrier density
    phi = df["physics_predicted_sbh_ev"].values
    n2d_norm = df["gate_carrier_density_cm2"].values / 1e13
    X_intrinsic = np.column_stack([phi, n2d_norm])

    # Extrinsic features: vdW/depinning flag and interfacial formation enthalpy
    vdw = df["is_vdw_or_depinned_contact"].values
    hf_norm = -df["sulfide_formation_enthalpy_kj_mol"].values / 500.0
    X_extrinsic = np.column_stack([vdw, hf_norm])

    # 1. Fit intrinsic component model: f_intrinsic(Phi_B, n_2D) via ANOVA LinearRegression
    lr_int = LinearRegression()
    lr_int.fit(X_intrinsic, y)
    y_intrinsic_pred = lr_int.predict(X_intrinsic)

    # 2. Fit extrinsic modifier on intrinsic residuals: e_int = y - y_intrinsic
    residual_int = y - y_intrinsic_pred
    lr_ext = LinearRegression()
    lr_ext.fit(X_extrinsic, residual_int)
    y_extrinsic_mod = lr_ext.predict(X_extrinsic)

    # 3. Overall model & unexplained noise
    y_combined = y_intrinsic_pred + y_extrinsic_mod
    epsilon = y - y_combined

    # Variance decomposition
    var_intrinsic = float(np.var(y_intrinsic_pred, ddof=1))
    var_extrinsic = float(np.var(y_extrinsic_mod, ddof=1))
    var_epsilon = float(np.var(epsilon, ddof=1))

    # Calculate percentage explained
    pct_intrinsic = round((var_intrinsic / total_var) * 100.0, 1)
    pct_extrinsic = round((var_extrinsic / total_var) * 100.0, 1)
    pct_unexplained = round(max(0.0, 100.0 - (pct_intrinsic + pct_extrinsic)), 1)

    # Device-by-device decomposition
    device_records = []
    for idx in range(n):
        row = df.iloc[idx]
        device_records.append({
            "device_id": str(row.get("device_id", f"dev_{idx}")),
            "contact_metal": str(row.get("contact_metal", "Unknown")),
            "source_uid": str(row.get("source_uid", "Unknown")),
            "observed_log10_rc": round(float(y[idx]), 4),
            "intrinsic_log10_rc": round(float(y_intrinsic_pred[idx]), 4),
            "extrinsic_modifier_dex": round(float(y_extrinsic_mod[idx]), 4),
            "residual_noise_dex": round(float(epsilon[idx]), 4),
            "observed_rc_linear_ohm_um": round(float(10.0 ** y[idx]), 1),
            "intrinsic_rc_linear_ohm_um": round(float(10.0 ** y_intrinsic_pred[idx]), 1),
            "extrinsic_factor_multiplier": round(float(10.0 ** y_extrinsic_mod[idx]), 2)
        })

    # Generate Figure
    DECOUPLING_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _plot_decomposition(device_records, pct_intrinsic, pct_extrinsic, pct_unexplained, y, y_intrinsic_pred, y_extrinsic_mod)

    summary = {
        "title": "Intrinsic vs Extrinsic Contact Resistance Decomposition",
        "n_samples": n,
        "total_variance_dex2": round(total_var, 4),
        "variance_decomposition": {
            "intrinsic_variance_dex2": round(var_intrinsic, 4),
            "extrinsic_variance_dex2": round(var_extrinsic, 4),
            "unexplained_noise_variance_dex2": round(var_epsilon, 4),
            "pct_variance_explained_intrinsic": pct_intrinsic,
            "pct_variance_explained_extrinsic": pct_extrinsic,
            "pct_variance_unexplained_noise": pct_unexplained
        },
        "intrinsic_model_coefficients": {
            "intercept": round(float(lr_int.intercept_), 4),
            "coef_sbh_ev": round(float(lr_int.coef_[0]), 4),
            "coef_n2d_norm": round(float(lr_int.coef_[1]), 4)
        },
        "extrinsic_modifier_coefficients": {
            "intercept": round(float(lr_ext.intercept_), 4),
            "coef_vdw_depinning": round(float(lr_ext.coef_[0]), 4),
            "coef_sulfide_enthalpy_norm": round(float(lr_ext.coef_[1]), 4)
        },
        "device_decompositions": device_records
    }

    with open(DECOUPLING_RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def _plot_decomposition(device_records, pct_int, pct_ext, pct_noise, y, y_int, y_ext):
    fig = plt.figure(figsize=(14, 5.5), dpi=300)
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1.4, 1.2])

    # 1. Donut Chart of Variance Explained
    ax1 = fig.add_subplot(gs[0])
    labels = [
        f"Intrinsic Physics\n({pct_int}%)",
        f"Extrinsic Processing\n({pct_ext}%)",
        f"Unexplained Noise\n({pct_noise}%)"
    ]
    sizes = [pct_int, pct_ext, pct_noise]
    colors = ["#1f77b4", "#ff7f0e", "#7f7f7f"]
    wedges, texts = ax1.pie(sizes, labels=labels, colors=colors, startangle=140,
                            wedgeprops=dict(width=0.45, edgecolor="white", lw=2),
                            textprops=dict(fontsize=9, fontweight="bold"))
    ax1.set_title("(a) Variance Decomposition", fontsize=11, fontweight="bold")

    # 2. Waterfall Stacked Decomposition for Representative Devices
    ax2 = fig.add_subplot(gs[1])
    # Pick 5 diverse benchmark contacts: Bi (vdW), Ti (reactive), Au (pinned), 1T-MoS2 (homojunction), Pt (high SBH)
    rep_metals = ["Bi", "Ti", "Au", "1T-MoS2", "Pt"]
    selected = []
    for m in rep_metals:
        match = next((d for d in device_records if d["contact_metal"] == m), None)
        if match:
            selected.append(match)

    m_names = [d["contact_metal"] for d in selected]
    y_ints = [d["intrinsic_log10_rc"] for d in selected]
    y_exts = [d["extrinsic_modifier_dex"] for d in selected]
    y_obs = [d["observed_log10_rc"] for d in selected]

    y_pos = np.arange(len(selected))
    ax2.barh(y_pos, y_ints, label="Intrinsic Component $f(\\Phi_B, n_{2D})$", color="#1f77b4", alpha=0.85, edgecolor="black")
    ax2.barh(y_pos, y_exts, left=y_ints, label="Extrinsic Modifier $g(\\mathrm{vdW}, \\Delta H_f)$", color="#ff7f0e", alpha=0.85, edgecolor="black")
    ax2.scatter(y_obs, y_pos, color="red", s=50, marker="D", edgecolors="black", label="Observed Total", zorder=5)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(m_names, fontsize=10, fontweight="bold")
    ax2.set_xlabel(r"$\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$ [dex]", fontsize=10, fontweight="bold")
    ax2.set_title("(b) Additive Mechanism Decomposition", fontsize=11, fontweight="bold")
    ax2.legend(loc="lower right", fontsize=8)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # 3. Scatter: Intrinsic Component vs Observed Total
    ax3 = fig.add_subplot(gs[2])
    ax3.scatter(y_int, y, c="navy", s=55, edgecolors="k", lw=0.6, alpha=0.85)
    lims = [1.8, 5.0]
    ax3.plot(lims, lims, "k--", lw=1.2, label="1:1 (Pure Intrinsic)")
    ax3.set_xlabel(r"Intrinsic Prediction $f_{\mathrm{intrinsic}}(\Phi_B, n_{2D})$ [dex]", fontsize=10, fontweight="bold")
    ax3.set_ylabel(r"Observed $\log_{10} R_c$ [dex]", fontsize=10, fontweight="bold")
    ax3.set_title("(c) Intrinsic Component vs Ground Truth", fontsize=11, fontweight="bold")
    ax3.legend(loc="upper left", fontsize=8)
    ax3.grid(True, linestyle=":", alpha=0.5)

    plt.suptitle(r"Intrinsic vs Extrinsic Contact Resistance Decoupling in MoS$_2$", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(DECOUPLING_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = run_intrinsic_extrinsic_decomposition()
    print("Intrinsic vs extrinsic decomposition complete.")
    v = res["variance_decomposition"]
    print(f"Variance Explained: Intrinsic = {v['pct_variance_explained_intrinsic']}%, Extrinsic = {v['pct_variance_explained_extrinsic']}%, Noise = {v['pct_variance_unexplained_noise']}%")
