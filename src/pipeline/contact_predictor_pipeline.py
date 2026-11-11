"""
End-to-End Reproducible Inference and Prediction Pipeline (Sprint 6.b.2).
Provides high-level Python API and Command-Line Interface (CLI) for predicting MoS2 contact resistance,
classifying physical transport regimes, comparing with Landauer ballistic limits, and extracting design guidance.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.model_factory import instantiate_tuned_candidate_model
from src.models.symbolic_evaluator import DiscoveredSymbolicContactModel
from src.physics.theoretical_models_comparator import compute_landauer_quantum_limit
from src.interpretability.regime_definitions import classify_device_regime

ROOT_DIR = Path(__file__).resolve().parents[2]

# Standard reference metal physical parameters
METAL_DATABASE = {
    "Bi": {"work_function_ev": 4.22, "enthalpy_kj_mol": -70.0, "default_vdw": True},
    "Sb": {"work_function_ev": 4.55, "enthalpy_kj_mol": -80.0, "default_vdw": True},
    "Ti": {"work_function_ev": 4.33, "enthalpy_kj_mol": -135.0, "default_vdw": False},
    "Sc": {"work_function_ev": 3.50, "enthalpy_kj_mol": -150.0, "default_vdw": False},
    "Ag": {"work_function_ev": 4.26, "enthalpy_kj_mol": -30.0, "default_vdw": False},
    "Au": {"work_function_ev": 5.10, "enthalpy_kj_mol": -10.0, "default_vdw": False},
    "Pt": {"work_function_ev": 5.65, "enthalpy_kj_mol": -40.0, "default_vdw": False},
    "Pd": {"work_function_ev": 5.22, "enthalpy_kj_mol": -50.0, "default_vdw": False},
    "Ni": {"work_function_ev": 5.15, "enthalpy_kj_mol": -85.0, "default_vdw": False},
    "1T-MoS2": {"work_function_ev": 4.20, "enthalpy_kj_mol": 0.0, "default_vdw": True}
}


class MoS2ContactPredictor:
    """
    Production-ready inference pipeline for 2D MoS2 contact characterization.
    """
    def __init__(self):
        self._train_models()

    def _train_models(self):
        df = get_cleaned_and_engineered_dataset()
        # Features used for the best linear/ridge model
        self.feature_cols = [
            "physics_predicted_sbh_ev",
            "gate_carrier_density_cm2",
            "is_vdw_or_depinned_contact",
            "sulfide_formation_enthalpy_kj_mol"
        ]
        X = df[self.feature_cols].copy()
        # Normalize n2d for stability
        X["gate_carrier_density_cm2"] = X["gate_carrier_density_cm2"] / 1.0e13
        y = df["log10_rc"].values

        self.ml_model = instantiate_tuned_candidate_model("Ridge_Regression")
        self.ml_model.fit(X, y)
        self.symbolic_model = DiscoveredSymbolicContactModel(refit=False)

    def predict(
        self,
        metal: Optional[str] = "Bi",
        gate_carrier_density_cm2: float = 1.8e13,
        is_vdw_transferred: Optional[bool] = None,
        work_function_ev: Optional[float] = None,
        schottky_barrier_height_ev: Optional[float] = None,
        formation_enthalpy_kj_mol: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end prediction, physical limit check, and regime diagnosis.
        """
        warnings = []

        # 1. Resolve metal parameters
        if metal in METAL_DATABASE:
            m_props = METAL_DATABASE[metal]
            wf = work_function_ev if work_function_ev is not None else m_props["work_function_ev"]
            enth = formation_enthalpy_kj_mol if formation_enthalpy_kj_mol is not None else m_props["enthalpy_kj_mol"]
            vdw = is_vdw_transferred if is_vdw_transferred is not None else m_props["default_vdw"]
        else:
            wf = work_function_ev if work_function_ev is not None else 4.50
            enth = formation_enthalpy_kj_mol if formation_enthalpy_kj_mol is not None else -50.0
            vdw = is_vdw_transferred if is_vdw_transferred is not None else False

        # 2. Resolve Schottky barrier height
        if schottky_barrier_height_ev is not None:
            sbh = float(schottky_barrier_height_ev)
        else:
            # Estimate SBH based on work function and pinning
            chi_mos2 = 4.20
            if vdw:
                # Unpinned Schottky-Mott limit
                sbh = max(0.02, wf - chi_mos2)
            else:
                # Pinned Bardeen limit (S ~ 0.20, CNL ~ 4.5 eV)
                cnl = 4.50
                sbh = max(0.15, 0.35 + 0.20 * (wf - cnl))

        # 3. Check Physical Validity Envelopes
        if gate_carrier_density_cm2 > 3.0e13:
            warnings.append("High gate carrier density (> 3e13 cm^-2) risks dielectric rupture / Fowler-Nordheim oxide breakdown.")
        elif gate_carrier_density_cm2 < 1.0e12:
            warnings.append("Low gate carrier density (< 1e12 cm^-2) enters subthreshold regime where channel resistance dominates.")

        if sbh > 0.80:
            warnings.append("Large Schottky barrier height (> 0.8 eV) leads to severe cryogenic freeze-out and high thermionic resistance.")

        # 4. Model Predictions
        n2d_norm = gate_carrier_density_cm2 / 1.0e13
        X_eval = pd.DataFrame([{
            "physics_predicted_sbh_ev": sbh,
            "gate_carrier_density_cm2": n2d_norm,
            "is_vdw_or_depinned_contact": 1 if vdw else 0,
            "sulfide_formation_enthalpy_kj_mol": enth
        }])
        ml_log10_rc = float(self.ml_model.predict(X_eval)[0])
        ml_rc_ohm_um = float(10.0 ** ml_log10_rc)

        # Discovered Closed-form equation: log10(Rc) = Phi_B - (n2d / 1e13) + 3.660
        analytical_log10_rc = float(sbh - n2d_norm + 3.660)
        analytical_rc_ohm_um = float(10.0 ** analytical_log10_rc)

        # 5. Landauer Ballistic Quantum Limit
        rc_quantum_limit = compute_landauer_quantum_limit(gate_carrier_density_cm2)

        # Clip predictions to respect physical quantum limit
        ml_rc_final = max(ml_rc_ohm_um, rc_quantum_limit)
        analytical_rc_final = max(analytical_rc_ohm_um, rc_quantum_limit)

        # 6. Physical Regime Classification
        from src.interpretability.regime_definitions import define_contact_transport_regimes
        regimes_dict = define_contact_transport_regimes()
        regime_id = classify_device_regime(
            log10_rc=float(np.log10(ml_rc_final)),
            sbh_ev=sbh,
            n2d_cm2=gate_carrier_density_cm2,
            is_vdw=bool(vdw)
        )
        regime_meta = regimes_dict.get(regime_id, {})

        # 7. Actionable Optimization Guidance
        guidance = []
        if ml_rc_final < 100.0:
            guidance.append("Target achieved: Ultra-low contact resistance (< 100 Ohm*um) successfully satisfied for sub-1nm CMOS!")
        else:
            required_sbh_for_100 = round(2.0 + n2d_norm - 3.660, 3)
            if required_sbh_for_100 > 0:
                guidance.append(f"To reach < 100 Ohm*um at current gating, reduce Schottky barrier height below {required_sbh_for_100:.2f} eV.")
            else:
                required_n2d_for_100 = round((3.660 + sbh - 2.0) * 1e13, 1)
                guidance.append(f"To reach < 100 Ohm*um, gate carrier density must be boosted to >= {required_n2d_for_100:.1e} cm^-2 using thin high-k dielectric.")

        return {
            "inputs": {
                "metal": metal,
                "gate_carrier_density_cm2": gate_carrier_density_cm2,
                "effective_sbh_ev": round(sbh, 3),
                "metal_work_function_ev": round(wf, 2),
                "is_vdw_transferred": bool(vdw)
            },
            "predicted_contact_resistance": {
                "ml_model_ridge": {
                    "log10_rc_dex": round(float(np.log10(ml_rc_final)), 4),
                    "rc_ohm_um": round(ml_rc_final, 1)
                },
                "discovered_closed_form_law": {
                    "formula": "Rc = 4570 * 10^(Phi_B - n_2D/1e13) Ohm*um",
                    "log10_rc_dex": round(float(np.log10(analytical_rc_final)), 4),
                    "rc_ohm_um": round(analytical_rc_final, 1)
                }
            },
            "physical_limits": {
                "landauer_quantum_floor_ohm_um": round(rc_quantum_limit, 1),
                "is_ballistic_limited": bool(ml_rc_final <= rc_quantum_limit * 1.5)
            },
            "transport_regime": {
                "regime_id": regime_id,
                "regime_name": regime_meta.get("name", regime_id),
                "description": regime_meta.get("governing_physics", "")
            },
            "engineering_guidance": guidance,
            "validity_warnings": warnings
        }


def main():
    parser = argparse.ArgumentParser(description="MoS2 Contact Resistance ML & Physics Inference Pipeline")
    parser.add_argument("--metal", type=str, default="Bi", help="Contact metal (e.g., Bi, Sb, Ti, Sc, Au, Pt)")
    parser.add_argument("--n2d", type=float, default=1.8e13, help="Gate carrier density in cm^-2 (e.g., 1.8e13)")
    parser.add_argument("--vdw", action="store_true", help="Set flag if contact is van der Waals transferred")
    parser.add_argument("--sbh", type=float, default=None, help="Explicit Schottky barrier height in eV")
    parser.add_argument("--json", action="store_true", help="Output result as pure JSON")

    args = parser.parse_args()
    predictor = MoS2ContactPredictor()
    res = predictor.predict(
        metal=args.metal,
        gate_carrier_density_cm2=args.n2d,
        is_vdw_transferred=args.vdw if args.vdw else None,
        schottky_barrier_height_ev=args.sbh
    )

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("\n=======================================================")
        print("  MoS2 Contact Resistance & Physics Inference Pipeline")
        print("=======================================================")
        print(f"Device Input: Metal = {res['inputs']['metal']} | n_2D = {res['inputs']['gate_carrier_density_cm2']:.2e} cm^-2 | vdW = {res['inputs']['is_vdw_transferred']}")
        print(f"Effective Schottky Barrier: {res['inputs']['effective_sbh_ev']:.3f} eV")
        print("-------------------------------------------------------")
        print(f"Predicted Contact Resistance (ML):    {res['predicted_contact_resistance']['ml_model_ridge']['rc_ohm_um']} Ohm*um")
        print(f"Predicted Contact Resistance (Formula): {res['predicted_contact_resistance']['discovered_closed_form_law']['rc_ohm_um']} Ohm*um")
        print(f"Landauer Quantum Ballistic Limit:     {res['physical_limits']['landauer_quantum_floor_ohm_um']} Ohm*um")
        print(f"Transport Regime:                     {res['transport_regime']['regime_name']}")
        print("-------------------------------------------------------")
        for g in res["engineering_guidance"]:
            print(f"Design Guidance: {g}")
        for w in res["validity_warnings"]:
            print(f"Warning: {w}")
        print("=======================================================\n")


if __name__ == "__main__":
    main()
