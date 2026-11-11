"""
Intrinsic vs Extrinsic Decoupling Analysis Framework (Sprint 2.e.2).
Formulates the mathematical partition and attribution aggregation methodology for separating intrinsic metal properties from extrinsic processing and electrostatic gate conditions.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DECOUPLING_SPEC_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "decoupling_framework_spec.json"


def get_feature_domain_partition() -> Dict[str, List[str]]:
    """
    Partitions the feature space into three mutually exclusive physical domains:
    1. Intrinsic Metal Properties: Elemental/chemical attributes of the contact material.
    2. Extrinsic Processing & Defects: Fabrication environment, thermal history, and transfer architecture.
    3. Electrostatic & Operational: Gate doping density, dielectric constants, and thermal carrier excitation.
    """
    return {
        "intrinsic_metal_domain": [
            "work_function_ev",
            "pauling_electronegativity",
            "sulfide_formation_enthalpy_kj_mol",
            "d_band_center_ev",
            "metal_resistivity_ohm_cm",
            "schottky_mott_barrier_ev",
            "electronegativity_diff_sulfur"
        ],
        "extrinsic_processing_domain": [
            "contact_architecture",
            "is_vdw_or_depinned_contact",
            "deposition_method",
            "vacuum_base_pressure_torr",
            "log_vacuum_pressure",
            "post_annealing_temperature_c",
            "post_annealing_gas_ambient",
            "adhesion_layer",
            "effective_pinning_factor_s"
        ],
        "electrostatic_operational_domain": [
            "gate_carrier_density_cm2",
            "measurement_temperature_k",
            "thermal_energy_kbt_ev",
            "fermi_level_shift_ev"
        ]
    }


def define_decoupling_analysis_spec() -> Dict[str, Any]:
    """
    Formalizes the decoupling analysis protocol:
    1. Mathematical decomposition of SHAP vectors across physical domains.
    2. Interaction tensor separation (Intrinsic x Extrinsic coupling).
    3. Quantified metrics for experimentalists (Upper bound on processing optimization).
    """
    partition = get_feature_domain_partition()
    
    spec = {
        "title": "Intrinsic vs Extrinsic Contact Decoupling Framework",
        "feature_domains": partition,
        "mathematical_decomposition": {
            "shap_partition_formula": "Delta log10(Rc)(x) = Phi_intrinsic(x) + Phi_extrinsic(x) + Phi_electrostatic(x)",
            "domain_attribution_share": "W_domain = sum(|phi_{i, j in domain}|) / sum(|phi_{total}|)",
            "interaction_separation": "Separates additive main effects from cross-domain synergy Phi_{intrinsic, extrinsic}(x)"
        },
        "target_experimental_questions": [
            {
                "question": "What fraction of contact resistance variance is strictly governed by metal elemental choice versus fabrication recipe?",
                "metric": "Global Attribution Share (W_intrinsic vs W_extrinsic)"
            },
            {
                "question": "For a standard evaporated metal (e.g., Ti), what is the maximum achievable Rc reduction via vacuum optimization and thermal annealing alone?",
                "metric": "Local Partial Residual Optimization Range [min(Phi_extrinsic), max(Phi_extrinsic)]"
            },
            {
                "question": "At what gate doping density does electrostatic modulation saturate and become dominated by interfacial tunnel barrier height?",
                "metric": "2D Decoupling Response Surface Inflection Points"
            }
        ]
    }
    
    DECOUPLING_SPEC_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(DECOUPLING_SPEC_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


def calculate_domain_attribution_shares(feature_attributions: Dict[str, float]) -> Dict[str, float]:
    """
    Aggregates arbitrary feature attributions (SHAP or Permutation values)
    into normalized domain contribution percentages.
    """
    partition = get_feature_domain_partition()
    domain_totals = {
        "intrinsic_share_pct": 0.0,
        "extrinsic_share_pct": 0.0,
        "electrostatic_share_pct": 0.0
    }
    
    total_abs_imp = 0.0
    for feat, imp in feature_attributions.items():
        abs_imp = abs(imp)
        total_abs_imp += abs_imp
        
        if feat in partition["intrinsic_metal_domain"]:
            domain_totals["intrinsic_share_pct"] += abs_imp
        elif feat in partition["extrinsic_processing_domain"]:
            domain_totals["extrinsic_share_pct"] += abs_imp
        elif feat in partition["electrostatic_operational_domain"]:
            domain_totals["electrostatic_share_pct"] += abs_imp
        else:
            # Fallback based on naming heuristics
            if "sbh" in feat or "barrier" in feat or "pinning" in feat:
                domain_totals["extrinsic_share_pct"] += abs_imp
            else:
                domain_totals["intrinsic_share_pct"] += abs_imp
                
    if total_abs_imp > 0:
        for k in domain_totals:
            domain_totals[k] = round((domain_totals[k] / total_abs_imp) * 100.0, 2)
            
    return domain_totals


if __name__ == "__main__":
    spec = define_decoupling_analysis_spec()
    print("Decoupling framework specification serialized.")
    # Example attribution calculation
    test_attribs = {
        "work_function_ev": 0.35,
        "is_vdw_or_depinned_contact": 0.25,
        "gate_carrier_density_cm2": 0.40
    }
    shares = calculate_domain_attribution_shares(test_attribs)
    print("Example domain attribution shares:")
    print(json.dumps(shares, indent=2))
