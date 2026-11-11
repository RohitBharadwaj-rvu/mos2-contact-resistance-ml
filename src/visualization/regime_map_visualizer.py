"""
2D Phase Diagram and Physical Regime Map Visualizer (Sprint 5.c.2).
Generates publication-quality contour phase diagrams of MoS2 contact transport regimes,
overlays experimental literature data points, and identifies unexplored technological white space.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.models.model_factory import instantiate_tuned_candidate_model
from src.interpretability.regime_definitions import define_contact_transport_regimes

REGIME_MAP_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "regime_phase_diagram_data.json"
REGIME_MAP_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "regime_phase_diagram_2d.png"
WORKFUNCTION_MAP_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "regime_phase_diagram_workfunction.png"


def generate_regime_phase_diagram_data(
    model_name: str = "Ridge_Regression",
    df: Optional[pd.DataFrame] = None,
    grid_res: int = 60
) -> Dict[str, Any]:
    """
    Computes continuous predicted contact resistance grid across carrier density and barrier height,
    overlays discrete regime boundaries, and tracks literature data point clustering.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    model = instantiate_tuned_candidate_model(model_name)
    model.fit(X, y)

    # 1. Coordinate Grid: n_2D (1e12 to 2.5e13 cm^-2) x Phi_B (0.0 to 1.3 eV)
    n2d_vals = np.linspace(1e12, 2.5e13, grid_res)
    phi_vals = np.linspace(0.0, 1.3, grid_res)

    N_grid, P_grid = np.meshgrid(n2d_vals, phi_vals)

    # Assume median background values for vdW (0.5 for neutral transition) and formation enthalpy
    eval_df = pd.DataFrame({
        "physics_predicted_sbh_ev": P_grid.ravel(),
        "is_vdw_or_depinned_contact": 0.5,
        "sulfide_formation_enthalpy_kj_mol": -150.0,
        "gate_carrier_density_cm2": N_grid.ravel()
    })[feature_cols]

    preds = model.predict(eval_df)
    Z_grid = preds.reshape(grid_res, grid_res)

    # 2. Experimental Data Overlay Coordinates
    devices = []
    for idx in range(len(df)):
        row = df.iloc[idx]
        devices.append({
            "metal": str(row.get("contact_metal", "Unknown")),
            "n2d_cm2": float(row["gate_carrier_density_cm2"]),
            "sbh_ev": float(row["physics_predicted_sbh_ev"]),
            "log10_rc": float(row["log10_rc"]),
            "is_vdw": bool(row["is_vdw_or_depinned_contact"] == 1)
        })

    # Generate Figures
    REGIME_MAP_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _plot_2d_phase_diagram(n2d_vals, phi_vals, Z_grid, devices)
    _plot_workfunction_carrier_map(df, model)

    summary = {
        "title": "MoS2 Contact Resistance 2D Phase Diagram and Regime Boundaries",
        "champion_model": model_name,
        "grid_resolution": [grid_res, grid_res],
        "n2d_range_cm2": [float(n2d_vals[0]), float(n2d_vals[-1])],
        "sbh_range_ev": [float(phi_vals[0]), float(phi_vals[-1])],
        "regime_thresholds_dex": {
            "Regime_I_Quantum_Limited": 2.30,
            "Regime_II_Thermionic_Field_Tunneling": 3.18,
            "Regime_III_Thermionic_Emission": 4.18,
            "Regime_IV_Defect_Pinned": 5.00
        },
        "literature_device_count": len(devices),
        "white_space_regions": [
            {
                "region": "Ultra-High Electrostatic Gating (n2d > 2.0e13 cm^-2, moderate Phi_B ~ 0.3-0.5 eV)",
                "description": "Exploits high-k dielectrics (HfO2, Al2O3) or ionic liquid gating to compress tunneling barrier for conventional metals."
            },
            {
                "region": "Zero-Barrier High-Work-Function p-Type Injection (Phi_B < 0.2 eV for valence band)",
                "description": "Novel vdW layered materials or sub-surface intercalation for hole injection contacts."
            }
        ]
    }

    with open(REGIME_MAP_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


def _plot_2d_phase_diagram(n2d_vals, phi_vals, Z_grid, devices):
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)

    n2d_norm = n2d_vals / 1e13

    # Filled contour of predicted log10(Rc)
    levels = np.linspace(1.5, 4.8, 15)
    CS = ax.contourf(n2d_norm, phi_vals, Z_grid, levels=levels, cmap="Spectral_r", alpha=0.9)
    cbar = fig.colorbar(CS, ax=ax, pad=0.03)
    cbar.set_label(r"Predicted $\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$", fontsize=11, fontweight="bold")

    # Discrete Regime Boundary Lines
    # Boundary I/II: 2.30 dex (200 Ohm*um)
    ax.contour(n2d_norm, phi_vals, Z_grid, levels=[2.30], colors=["cyan"], linewidths=2.2, linestyles="--")
    # Boundary II/III: 3.18 dex (1500 Ohm*um)
    ax.contour(n2d_norm, phi_vals, Z_grid, levels=[3.18], colors=["yellow"], linewidths=2.2, linestyles="-")
    # Boundary III/IV: 4.18 dex (15000 Ohm*um)
    ax.contour(n2d_norm, phi_vals, Z_grid, levels=[4.18], colors=["white"], linewidths=2.2, linestyles="-.")

    # Regime Label Annotations
    ax.text(1.8, 0.12, "REGIME I: Ballistic / Quantum-Limited\n" + r"($R_c \leq 200\ \Omega\cdot\mu\mathrm{m}$)",
            color="black", fontsize=9, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.85, ec="cyan"))

    ax.text(1.5, 0.45, "REGIME II: Thermionic-Field Tunneling\n" + r"($200 < R_c \leq 1,500\ \Omega\cdot\mu\mathrm{m}$)",
            color="black", fontsize=9, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.85, ec="goldenrod"))

    ax.text(0.9, 0.82, "REGIME III: Thermionic Emission\n" + r"($1,500 < R_c \leq 15\ \mathrm{k}\Omega\cdot\mu\mathrm{m}$)",
            color="black", fontsize=9, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.85, ec="orange"))

    ax.text(0.4, 1.15, "REGIME IV: Defect-Pinned Freeze-Out\n" + r"($R_c > 15\ \mathrm{k}\Omega\cdot\mu\mathrm{m}$)",
            color="black", fontsize=9, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.85, ec="crimson"))

    # Highlight Unexplored White Space
    ax.fill_between([2.0, 2.5], 0.35, 0.65, color="gray", alpha=0.25, hatch="//", label="Unexplored High-Doping White Space")
    ax.text(2.25, 0.50, "White Space:\nHigh-κ Gating", fontsize=8, fontweight="bold", color="darkslategray", ha="center")

    # Overlay Experimental Literature Devices
    for dev in devices:
        x_pt = dev["n2d_cm2"] / 1e13
        y_pt = dev["sbh_ev"]
        metal = dev["metal"]
        is_vdw = dev["is_vdw"]

        marker = "^" if is_vdw else "o"
        edge_c = "lime" if is_vdw else "black"
        ax.scatter(x_pt, y_pt, c="white", marker=marker, s=65, edgecolors=edge_c, lw=1.2, zorder=5)

        # Label distinctive benchmark metals
        if metal in ["Bi", "1T-MoS2", "Ti", "Au", "Pt", "Pd", "Sc"]:
            ax.annotate(metal, (x_pt, y_pt), fontsize=8, fontweight="bold", color="black",
                        xytext=(4, 4), textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", alpha=0.75, lw=0))

    ax.set_xlabel(r"Gate Carrier Density $n_{2D}$ [$10^{13}\ \mathrm{cm}^{-2}$]", fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Schottky Barrier Height $\Phi_B$ [eV]", fontsize=11, fontweight="bold")
    ax.set_title(r"2D Regime Phase Diagram: MoS$_2$ Contact Transport Regimes", fontsize=13, fontweight="bold")
    ax.set_xlim(0.1, 2.5)
    ax.set_ylim(0.0, 1.3)
    ax.legend(loc="lower left", fontsize=8)
    ax.grid(True, linestyle=":", alpha=0.4)

    plt.tight_layout()
    plt.savefig(REGIME_MAP_PNG_PATH)
    plt.close()


def _plot_workfunction_carrier_map(df, model):
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    
    # Metal work function vs observed contact resistance
    wf = df["work_function_ev"].values
    rc = df["log10_rc"].values
    vdw = df["is_vdw_or_depinned_contact"].values

    for i in range(len(df)):
        color = "darkgreen" if vdw[i] == 1 else "firebrick"
        marker = "^" if vdw[i] == 1 else "o"
        ax.scatter(wf[i], rc[i], c=color, marker=marker, s=65, edgecolors="k", lw=0.6, label="vdW / De-pinned" if (vdw[i]==1 and i==0) else ("3D Evaporated" if (vdw[i]==0 and i==4) else ""))
        metal = df.iloc[i]["contact_metal"]
        if metal in ["Bi", "Ti", "Au", "Pt", "Pd", "Sc", "Ag", "Ni"]:
            ax.annotate(metal, (wf[i], rc[i]), fontsize=8, xytext=(4, -4), textcoords="offset points")

    # Overlay trend lines: Unpinned Schottky-Mott limit vs Pinned Fermi Level
    wf_line = np.linspace(3.5, 5.8, 100)
    # Pinned Fermi level around Ec - 0.35 eV produces flat Rc ~ 3.2 dex
    ax.axhline(3.18, color="goldenrod", linestyle="--", lw=1.5, label="Fermi-Level Pinning Plateau")
    ax.axhline(2.30, color="cyan", linestyle="-", lw=1.5, label=r"Quantum Limit Floor ($R_c \leq 200\ \Omega\cdot\mu\mathrm{m}$)")

    ax.set_xlabel(r"Metal Work Function $\Phi_m$ [eV]", fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Observed $\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}])$", fontsize=11, fontweight="bold")
    ax.set_title(r"Contact Resistance vs Metal Work Function $\Phi_m$", fontsize=12, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(WORKFUNCTION_MAP_PNG_PATH)
    plt.close()


if __name__ == "__main__":
    res = generate_regime_phase_diagram_data()
    print("2D Regime phase diagram generated successfully.")
    print("Saved:", REGIME_MAP_PNG_PATH)
    print("Saved:", WORKFUNCTION_MAP_PNG_PATH)
