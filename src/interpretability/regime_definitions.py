"""
Physical Transport Regime Catalog and Classifier (Sprint 5.c.1).
Defines governing solid-state transport regimes (Quantum-Limited, Thermionic-Field Tunneling,
Thermionic Emission, Defect-Dominated Pinning) and classifies experimental 2D contact devices.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

REGIMES_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "contact_transport_regimes.json"


def define_contact_transport_regimes() -> Dict[str, Any]:
    """
    Returns formal catalog of physical transport regimes in MoS2 contacts.
    """
    regimes = {
        "Regime_I_Quantum_Limited": {
            "name": "Ballistic / Quantum-Limited Regime",
            "rc_range_ohm_um": [10.0, 200.0],
            "rc_range_dex": [1.0, 2.30],
            "criteria": {
                "max_sbh_ev": 0.15,
                "min_n2d_cm2": 1.0e13,
                "requires_vdw_or_homojunction": True
            },
            "governing_physics": (
                "Landauer-Sharvin ballistic quantum injection limit. Van der Waals de-pinning or "
                "phase-engineered 1T metallic homojunction eliminates the interfacial vacuum barrier, "
                "allowing near-unity quantum transmission."
            ),
            "typical_technologies": ["Bi(0001) transferred vdW", "1T-MoS2 chemical homojunction", "Sb(0001)"]
        },
        "Regime_II_Thermionic_Field_Tunneling": {
            "name": "Thermionic-Field / Tunneling-Dominated Regime",
            "rc_range_ohm_um": [200.0, 1500.0],
            "rc_range_dex": [2.30, 3.18],
            "criteria": {
                "max_sbh_ev": 0.45,
                "min_n2d_cm2": 8.0e12,
                "requires_vdw_or_homojunction": False
            },
            "governing_physics": (
                "Field emission (Fowler-Nordheim or direct tunneling) through an electrostatically compressed "
                "depletion width (W_dep ~ sqrt(eps / n_2D)). Highly responsive to gate bias."
            ),
            "typical_technologies": ["Ti/Au evaporated and annealed", "Ag", "In", "Sc"]
        },
        "Regime_III_Thermionic_Emission": {
            "name": "Thermionic Emission-Dominated Regime",
            "rc_range_ohm_um": [1500.0, 15000.0],
            "rc_range_dex": [3.18, 4.18],
            "criteria": {
                "max_sbh_ev": 0.70,
                "min_n2d_cm2": 3.0e12,
                "requires_vdw_or_homojunction": False
            },
            "governing_physics": (
                "Classical Richardson-Dushman thermionic emission over the Schottky barrier. "
                "Strong exponential temperature dependence J ~ A* T^2 exp(-q*Phi_B / k_B*T)."
            ),
            "typical_technologies": ["Au evaporated", "Ni", "Cr", "Mo"]
        },
        "Regime_IV_Defect_Dominated_Pinned": {
            "name": "Defect-Dominated / Fermi-Level Pinned Regime",
            "rc_range_ohm_um": [15000.0, 100000.0],
            "rc_range_dex": [4.18, 5.0],
            "criteria": {
                "min_sbh_ev": 0.70,
                "requires_vdw_or_homojunction": False
            },
            "governing_physics": (
                "MIGS (Metal-Induced Gap States) and high-density sulfur vacancy clusters (V_S) pin the Fermi level "
                "deep near mid-gap. High work function metals suffer severe thermionic freeze-out and localized defect hopping."
            ),
            "typical_technologies": ["Pt transferred/evaporated", "Pd unpassivated evaporated"]
        }
    }
    return regimes


def classify_device_regime(
    log10_rc: float,
    sbh_ev: float,
    n2d_cm2: float,
    is_vdw: bool
) -> str:
    """
    Classifies a device into its primary physical transport regime based on resistance and descriptor thresholds.
    """
    if log10_rc <= 2.30 or (sbh_ev <= 0.15 and n2d_cm2 >= 1.0e13 and is_vdw):
        return "Regime_I_Quantum_Limited"
    elif log10_rc <= 3.18 or (sbh_ev <= 0.45 and n2d_cm2 >= 8.0e12):
        return "Regime_II_Thermionic_Field_Tunneling"
    elif log10_rc <= 4.18 or (sbh_ev <= 0.70):
        return "Regime_III_Thermionic_Emission"
    else:
        return "Regime_IV_Defect_Dominated_Pinned"


def classify_dataset_regimes(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Classifies all devices in the curated master dataset into their physical transport regimes.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    regimes_def = define_contact_transport_regimes()
    classified_records = []
    regime_counts = {k: 0 for k in regimes_def.keys()}

    for idx in range(len(df)):
        row = df.iloc[idx]
        rc_log = float(row["log10_rc"])
        sbh = float(row["physics_predicted_sbh_ev"])
        n2d = float(row["gate_carrier_density_cm2"])
        vdw = bool(row["is_vdw_or_depinned_contact"] == 1)

        reg_key = classify_device_regime(rc_log, sbh, n2d, vdw)
        regime_counts[reg_key] += 1

        classified_records.append({
            "device_id": str(row.get("device_id", f"dev_{idx}")),
            "contact_metal": str(row.get("contact_metal", "Unknown")),
            "source_uid": str(row.get("source_uid", "Unknown")),
            "observed_log10_rc": round(rc_log, 4),
            "observed_rc_linear_ohm_um": round(float(10.0 ** rc_log), 1),
            "schottky_barrier_height_ev": round(sbh, 4),
            "gate_carrier_density_cm2": n2d,
            "is_vdw": vdw,
            "classified_regime": reg_key,
            "regime_name": regimes_def[reg_key]["name"]
        })

    summary = {
        "title": "MoS2 Contact Physical Transport Regimes and Dataset Classifications",
        "n_samples": len(df),
        "regime_definitions": regimes_def,
        "regime_distribution": regime_counts,
        "classified_devices": classified_records
    }

    REGIMES_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REGIMES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    res = classify_dataset_regimes()
    print("Physical regimes classified successfully.")
    for k, v in res["regime_distribution"].items():
        print(f"  - {k}: {v} devices")
