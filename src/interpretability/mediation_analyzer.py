"""
Interfacial Chemistry vs Barrier Height Mediation Analysis Engine (Sprint 5.b.3).
Conducts causal mediation path analysis to determine whether metal sulfide formation enthalpy (Delta_Hf)
reduces contact resistance primarily indirectly via barrier height modulation (doping/pinning shift)
or directly through covalent orbital overlap and tunnel gap reduction.
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
from sklearn.linear_model import LinearRegression

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

MEDIATION_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "interfacial_chemistry_mediation_analysis.json"
MEDIATION_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "mediation_path_analysis.png"


def run_mediation_analysis(df: Optional[pd.DataFrame] = None, n_bootstraps: int = 1000, random_state: int = 42) -> Dict[str, Any]:
    """
    Executes Baron-Kenny and Preacher-Hayes causal mediation analysis:
    - Independent Variable (X): Normalized Sulfide Formation Enthalpy (-Delta_Hf / 500 kJ/mol)
    - Mediator (M): Schottky Barrier Height Phi_B (eV)
    - Outcome (Y): log10(Rc) (dex)
    - Covariate (Z): Gate Carrier Density n_2D (10^13 cm^-2)
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    X = -df["sulfide_formation_enthalpy_kj_mol"].values / 500.0
    M = df["physics_predicted_sbh_ev"].values
    Y = df["log10_rc"].values
    Z = df["gate_carrier_density_cm2"].values / 1e13
    n = len(df)

    # 1. Total Effect (Path C): Y ~ X + Z
    XZ = np.column_stack([X, Z])
    reg_c = LinearRegression().fit(XZ, Y)
    c_path = float(reg_c.coef_[0])

    # 2. Mediator Model (Path A): M ~ X + Z
    reg_a = LinearRegression().fit(XZ, M)
    a_path = float(reg_a.coef_[0])

    # 3. Outcome Model (Path B & Path C'): Y ~ M + X + Z
    MXZ = np.column_stack([M, X, Z])
    reg_outcome = LinearRegression().fit(MXZ, Y)
    b_path = float(reg_outcome.coef_[0])
    c_prime_path = float(reg_outcome.coef_[1])

    # Compute indirect effect: ab
    indirect_effect = a_path * b_path
    total_effect = c_prime_path + indirect_effect

    # Proportion mediated
    pct_indirect = float((indirect_effect / total_effect) * 100.0) if abs(total_effect) > 1e-6 else 0.0
    pct_direct = float((c_prime_path / total_effect) * 100.0) if abs(total_effect) > 1e-6 else 0.0

    # 4. Bootstrap Confidence Intervals for Indirect Effect
    rng = np.random.RandomState(random_state)
    boot_indirects = []
    for _ in range(n_bootstraps):
        boot_idx = rng.choice(n, size=n, replace=True)
        X_b, M_b, Y_b, Z_b = X[boot_idx], M[boot_idx], Y[boot_idx], Z[boot_idx]

        try:
            reg_a_b = LinearRegression().fit(np.column_stack([X_b, Z_b]), M_b)
            a_b = reg_a_b.coef_[0]

            reg_out_b = LinearRegression().fit(np.column_stack([M_b, X_b, Z_b]), Y_b)
            b_b = reg_out_b.coef_[0]
            boot_indirects.append(a_b * b_b)
        except Exception:
            continue

    boot_indirects = np.array(boot_indirects)
    ci_lower = float(np.percentile(boot_indirects, 2.5))
    ci_upper = float(np.percentile(boot_indirects, 97.5))

    # Sobel test
    # Compute standard errors from residuals
    res_a = M - reg_a.predict(XZ)
    s2_a = np.sum(res_a**2) / (n - 3)
    var_a = s2_a * np.linalg.pinv(np.dot(XZ.T, XZ))[0, 0]
    se_a = float(np.sqrt(max(1e-12, var_a)))

    res_out = Y - reg_outcome.predict(MXZ)
    s2_out = np.sum(res_out**2) / (n - 4)
    var_b = s2_out * np.linalg.pinv(np.dot(MXZ.T, MXZ))[0, 0]
    se_b = float(np.sqrt(max(1e-12, var_b)))

    sobel_se = float(np.sqrt(b_path**2 * se_a**2 + a_path**2 * se_b**2))
    sobel_z = float(indirect_effect / (sobel_se + 1e-12))
    sobel_p = float(2.0 * (1.0 - stats.norm.cdf(abs(sobel_z))))

    # Physical interpretation
    if pct_direct > 60.0:
        conclusion = "Direct orbital bonding dominates: Enthalpy reduces contact resistance primarily through intimate covalent coupling / tunnel gap reduction rather than barrier shift."
    elif pct_indirect > 60.0:
        conclusion = "Indirect barrier modulation dominates: Reactive metal formation enthalpy acts primarily through de-pinning and Schottky barrier height reduction."
    else:
        conclusion = "Dual mechanism: Both direct covalent overlap and indirect Schottky barrier modulation contribute meaningfully to resistance reduction."

    # Generate Figure
    MEDIATION_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _plot_mediation_path_diagram(a_path, b_path, c_prime_path, c_path, pct_direct, pct_indirect, sobel_p)

    summary = {
        "title": "Interfacial Chemistry (Delta_Hf) vs Schottky Barrier Height (Phi_B) Mediation Analysis",
        "n_samples": n,
        "n_bootstraps": n_bootstraps,
        "path_coefficients": {
            "path_a_enthalpy_to_sbh": round(a_path, 4),
            "path_b_sbh_to_log10_rc": round(b_path, 4),
            "path_c_prime_direct_enthalpy_to_log10_rc": round(c_prime_path, 4),
            "total_effect_c": round(total_effect, 4)
        },
        "indirect_effect": {
            "value": round(indirect_effect, 4),
            "bootstrap_95_ci": [round(ci_lower, 4), round(ci_upper, 4)],
            "sobel_z_score": round(sobel_z, 4),
            "sobel_p_value": round(sobel_p, 4)
        },
        "variance_share": {
            "pct_direct_orbital_bonding": round(pct_direct, 1),
            "pct_indirect_barrier_doping": round(pct_indirect, 1)
        },
        "physical_conclusion": conclusion
    }

    with open(MEDIATION_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def _plot_mediation_path_diagram(a, b, c_prime, c_total, pct_dir, pct_ind, p_val):
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.axis("off")

    # Define Node Positions
    pos_x = (0.15, 0.5)   # Independent: Sulfide Enthalpy
    pos_m = (0.50, 0.85)  # Mediator: Schottky Barrier
    pos_y = (0.85, 0.5)   # Outcome: log10(Rc)

    # Box styles
    bbox_props = dict(boxstyle="round,pad=0.6", fc="#e8f4f8", ec="#1f77b4", lw=2)
    bbox_mediator = dict(boxstyle="round,pad=0.6", fc="#fff2e6", ec="#ff7f0e", lw=2)
    bbox_outcome = dict(boxstyle="round,pad=0.6", fc="#e6f5ea", ec="#2ca02c", lw=2)

    # Draw Nodes
    ax.text(pos_x[0], pos_x[1], "Interfacial Reactivity\n" + r"$\Delta H_f$ (Enthalpy)",
            ha="center", va="center", bbox=bbox_props, fontsize=10, fontweight="bold")
    ax.text(pos_m[0], pos_m[1], "Mediator Variable\n" + r"Schottky Barrier $\Phi_B$",
            ha="center", va="center", bbox=bbox_mediator, fontsize=10, fontweight="bold")
    ax.text(pos_y[0], pos_y[1], "Device Outcome\n" + r"$\log_{10}(R_c)$",
            ha="center", va="center", bbox=bbox_outcome, fontsize=10, fontweight="bold")

    # Draw Arrows
    # Path A: X -> M
    ax.annotate("", xy=(0.42, 0.80), xytext=(0.24, 0.58),
                arrowprops=dict(arrowstyle="->", lw=2, color="#ff7f0e"))
    ax.text(0.30, 0.72, f"Path a = {a:.2f}\n(Barrier Shift)", ha="center", fontsize=9, fontweight="bold", color="#d95f02")

    # Path B: M -> Y
    ax.annotate("", xy=(0.78, 0.58), xytext=(0.58, 0.80),
                arrowprops=dict(arrowstyle="->", lw=2, color="#ff7f0e"))
    ax.text(0.70, 0.72, f"Path b = {b:.2f}\n(Thermionic Rate)", ha="center", fontsize=9, fontweight="bold", color="#d95f02")

    # Path C' (Direct): X -> Y
    ax.annotate("", xy=(0.73, 0.50), xytext=(0.27, 0.50),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1f77b4", linestyle="-"))
    ax.text(0.50, 0.44, f"Direct Path c' = {c_prime:.2f}\n(Orbital Overlap / Tunnel Gap)",
            ha="center", fontsize=9, fontweight="bold", color="#1f77b4")

    # Path C (Total): dashed bottom arc
    ax.text(0.50, 0.28, f"Total Effect c = {c_total:.2f}\n" +
                        f"Indirect Effect ab = {a*b:.3f} ({pct_ind:.1f}%)\n" +
                        f"Direct Effect c' = {c_prime:.3f} ({pct_dir:.1f}%)",
            ha="center", fontsize=9, fontweight="bold",
            bbox=dict(boxstyle="square,pad=0.5", fc="#f9f9f9", ec="gray", lw=1))

    ax.set_title(r"Causal Mediation Analysis: Interfacial Chemistry vs Barrier Height in MoS$_2$",
                 fontsize=12, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(MEDIATION_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = run_mediation_analysis()
    print("Mediation analysis complete.")
    print("Direct orbital bonding share:", res["variance_share"]["pct_direct_orbital_bonding"], "%")
    print("Indirect barrier modulation share:", res["variance_share"]["pct_indirect_barrier_doping"], "%")
    print("Conclusion:", res["physical_conclusion"])
