"""
Master Interpretability and Decoupling Milestone Audit (Heading 5).
Validates cross-module consistency across SHAP attributions, PDP/ICE curves,
confounding analyses, ANOVA variance decomposition, causal mediation, and regime maps.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parents[2]
FIGURES_DIR = ROOT_DIR / "reports" / "figures"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DATA_REFERENCE_DIR = ROOT_DIR / "data" / "reference"
AUDIT_JSON_PATH = DATA_PROCESSED_DIR / "master_heading_5_interpretability_audit.json"


def run_master_interpretability_audit() -> Dict[str, Any]:
    """
    Executes comprehensive verification across all Section 5 deliverables.
    """
    audit_results = {
        "heading": "Heading 5: Interpretability, Decoupling Analysis, and Interpretable Regime Mapping",
        "subheadings_audited": ["5.a", "5.b", "5.c"],
        "checks": {},
        "summary_metrics": {},
        "all_passed": True
    }

    # 1. Verify JSON Data Deliverables
    required_json_files = {
        "shap_attributions": DATA_PROCESSED_DIR / "shap_feature_attribution_analysis.json",
        "pdp_ice_curves": DATA_PROCESSED_DIR / "pdp_and_permutation_importance.json",
        "confounding_analysis": DATA_PROCESSED_DIR / "inter_feature_confounding_analysis.json",
        "variance_decomposition": DATA_PROCESSED_DIR / "intrinsic_extrinsic_decoupling_results.json",
        "mediation_analysis": DATA_PROCESSED_DIR / "interfacial_chemistry_mediation_analysis.json",
        "regime_definitions": DATA_REFERENCE_DIR / "contact_transport_regimes.json",
        "regime_phase_diagram": DATA_PROCESSED_DIR / "regime_phase_diagram_data.json",
        "design_rules": DATA_REFERENCE_DIR / "design_rules_ultra_low_contact_resistance.json"
    }

    for name, path in required_json_files.items():
        exists = path.exists() and path.stat().st_size > 0
        audit_results["checks"][f"file_{name}"] = {"path": str(path.relative_to(ROOT_DIR)), "exists": exists}
        if not exists:
            audit_results["all_passed"] = False

    # 2. Verify Generated Figure Deliverables
    required_figures = [
        "shap_summary_beeswarm.png",
        "shap_cross_architecture_comparison.png",
        "permutation_importance_oof.png",
        "pdp_ice_curves.png",
        "pdp_2d_interaction_surface.png",
        "confounding_partial_correlation_matrix.png",
        "intrinsic_vs_extrinsic_decomposition.png",
        "mediation_path_analysis.png",
        "regime_phase_diagram_2d.png",
        "regime_phase_diagram_workfunction.png"
    ]

    for fig_name in required_figures:
        fig_path = FIGURES_DIR / fig_name
        exists = fig_path.exists() and fig_path.stat().st_size > 0
        audit_results["checks"][f"figure_{fig_name}"] = {"path": f"reports/figures/{fig_name}", "exists": exists}
        if not exists:
            audit_results["all_passed"] = False

    # 3. Verify Scientific Findings and Consistency
    # A. Variance Decomposition Consistency
    with open(required_json_files["variance_decomposition"], "r", encoding="utf-8") as f:
        decomp_data = json.load(f)
    v_info = decomp_data["variance_decomposition"]
    var_intrinsic = v_info["pct_variance_explained_intrinsic"]
    var_extrinsic = v_info["pct_variance_explained_extrinsic"]
    var_unexplained = v_info["pct_variance_unexplained_noise"]

    audit_results["summary_metrics"]["variance_intrinsic_pct"] = var_intrinsic
    audit_results["summary_metrics"]["variance_extrinsic_pct"] = var_extrinsic
    audit_results["summary_metrics"]["variance_unexplained_pct"] = var_unexplained
    assert var_intrinsic > var_extrinsic, "Intrinsic physics must dominate extrinsic factors"
    assert abs(var_intrinsic + var_extrinsic + var_unexplained - 100.0) < 1.0, "Sum of variance fractions must be ~100%"

    # B. Causal Mediation Consistency
    with open(required_json_files["mediation_analysis"], "r", encoding="utf-8") as f:
        med_data = json.load(f)
    m_info = med_data["variance_share"]
    indirect_frac = m_info["pct_indirect_barrier_doping"]
    direct_frac = m_info["pct_direct_orbital_bonding"]
    audit_results["summary_metrics"]["mediation_indirect_pct"] = indirect_frac
    audit_results["summary_metrics"]["mediation_direct_pct"] = direct_frac
    assert abs(indirect_frac + direct_frac - 100.0) < 1.0, "Mediation fractions must sum to 100%"
    assert indirect_frac > 80.0, "Indirect mediation via barrier reduction must be primary mechanism"

    # C. Regime Definitions Consistency
    with open(required_json_files["regime_definitions"], "r", encoding="utf-8") as f:
        regime_data = json.load(f)
    assert len(regime_data["regime_definitions"]) == 4
    assert len(regime_data["classified_devices"]) == 20

    # D. Design Rules Consistency
    with open(required_json_files["design_rules"], "r", encoding="utf-8") as f:
        rules_data = json.load(f)
    assert "target_100_ohm_um" in rules_data["threshold_tables"]
    t100_scenarios = rules_data["threshold_tables"]["target_100_ohm_um"]["scenario_thresholds"]
    assert any(s["is_target_achievable"] for s in t100_scenarios), "At least one high-gating scenario must reach <100 Ohm*um"

    AUDIT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)

    return audit_results


if __name__ == "__main__":
    res = run_master_interpretability_audit()
    print("Master Heading 5 Interpretability Audit complete.")
    print("All checks passed:", res["all_passed"])
