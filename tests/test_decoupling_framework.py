"""
Tests for Intrinsic vs Extrinsic Decoupling Framework (Sprint 2.e.2).
"""

from pathlib import Path
import json
import pytest
from src.models.decoupling_framework import (
    get_feature_domain_partition,
    define_decoupling_analysis_spec,
    calculate_domain_attribution_shares,
    decouple_model_predictions,
    DECOUPLING_SPEC_JSON
)


def test_get_feature_domain_partition():
    """Verify mutual exclusivity and coverage of domain partitions."""
    partition = get_feature_domain_partition()
    
    assert "intrinsic_metal_domain" in partition
    assert "extrinsic_processing_domain" in partition
    assert "electrostatic_operational_domain" in partition
    
    # Check key features are classified properly
    assert "work_function_ev" in partition["intrinsic_metal_domain"]
    assert "deposition_method" in partition["extrinsic_processing_domain"]
    assert "gate_carrier_density_cm2" in partition["electrostatic_operational_domain"]
    
    # Check mutual exclusivity
    s1 = set(partition["intrinsic_metal_domain"])
    s2 = set(partition["extrinsic_processing_domain"])
    s3 = set(partition["electrostatic_operational_domain"])
    assert len(s1.intersection(s2)) == 0
    assert len(s1.intersection(s3)) == 0
    assert len(s2.intersection(s3)) == 0


def test_define_decoupling_analysis_spec():
    """Verify schema of decoupling specification."""
    spec = define_decoupling_analysis_spec()
    assert "mathematical_decomposition" in spec
    assert "target_experimental_questions" in spec
    assert len(spec["target_experimental_questions"]) == 3
    
    assert DECOUPLING_SPEC_JSON.exists()
    with open(DECOUPLING_SPEC_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["title"] == spec["title"]


def test_calculate_domain_attribution_shares():
    """Verify aggregation of feature attributions into domain percentages."""
    attribs = {
        "work_function_ev": 0.50,
        "is_vdw_or_depinned_contact": 0.30,
        "gate_carrier_density_cm2": 0.20
    }
    shares = calculate_domain_attribution_shares(attribs)
    
    assert shares["intrinsic_share_pct"] == 50.0
    assert shares["extrinsic_share_pct"] == 30.0
    assert shares["electrostatic_share_pct"] == 20.0
    assert round(sum(shares.values()), 1) == 100.0


def test_decouple_model_predictions():
    """Verify end-to-end model prediction decoupling into physical domain shares."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    import pandas as pd
    import numpy as np
    
    X = pd.DataFrame({
        "work_function_ev": [4.0, 4.5, 5.0, 5.5],
        "is_vdw_or_depinned_contact": [1.0, 0.0, 0.0, 0.0],
        "gate_carrier_density_cm2": [1e12, 5e12, 1e13, 2e13]
    })
    y = np.array([2.5, 3.2, 3.8, 4.2])
    
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=1.0))
    ]).fit(X, y)
    res = decouple_model_predictions(model, X, y)
    
    assert "feature_attributions" in res
    assert "domain_shares" in res
    shares = res["domain_shares"]
    assert "intrinsic_share_pct" in shares
    assert "extrinsic_share_pct" in shares
    assert "electrostatic_share_pct" in shares

