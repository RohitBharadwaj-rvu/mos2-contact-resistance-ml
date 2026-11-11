"""
Unified Preprocessor Factory for Heterogeneous Model Families (Sprint 4.a.2).
Constructs fold-isolated feature scaling, missing value imputation, and categorical encoding pipelines tailored to each specific ML algorithm family.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.impute import SimpleImputer

from src.features.categorical_encoders import build_categorical_preprocessor

PREPROCESSOR_SPEC_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "preprocessor_pipeline_spec.json"


def build_family_preprocessor(model_family: str,
                              numeric_cols: Optional[List[str]] = None,
                              categorical_cols: Optional[List[str]] = None) -> Pipeline:
    """
    Constructs an integrated imputer + scaler + encoder pipeline tailored to model family mathematical needs:
    - 'linear' / 'kernel' / 'bayesian': Impute median + StandardScaler
    - 'tree_ensemble': Impute median + Passthrough (or RobustScaler)
    - 'symbolic': Impute median + RobustScaler
    """
    if numeric_cols is None:
        numeric_cols = [
            "physics_predicted_sbh_ev",
            "is_vdw_or_depinned_contact",
            "sulfide_formation_enthalpy_kj_mol",
            "gate_carrier_density_cm2"
        ]
        
    fam_norm = model_family.lower().strip()
    if any(k in fam_norm for k in ["linear", "ridge", "lasso", "elasticnet"]):
        canonical_family = "linear"
    elif any(k in fam_norm for k in ["kernel", "bayesian", "gpr", "gaussian", "svr"]):
        canonical_family = "kernel"
    elif any(k in fam_norm for k in ["tree", "forest", "boost", "gradient"]):
        canonical_family = "tree_ensemble"
    elif any(k in fam_norm for k in ["symbolic", "gp", "formula"]):
        canonical_family = "symbolic"
    else:
        canonical_family = fam_norm

    if canonical_family in ["linear", "kernel"]:
        num_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
    elif canonical_family == "tree_ensemble":
        num_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
    elif canonical_family == "symbolic":
        num_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", MinMaxScaler(feature_range=(0.1, 1.0)))
        ])
    else:
        raise ValueError(f"Unknown model family: {model_family}")
        
    if categorical_cols:
        cat_preprocessor = build_categorical_preprocessor(strategy="one_hot", categorical_cols=categorical_cols)
        full_transformer = ColumnTransformer(
            transformers=[
                ("num", num_transformer, numeric_cols),
                ("cat", cat_preprocessor, categorical_cols)
            ]
        )
        return Pipeline([("preprocessor", full_transformer)])
    else:
        full_transformer = ColumnTransformer(
            transformers=[
                ("num", num_transformer, numeric_cols)
            ]
        )
        return Pipeline([("preprocessor", full_transformer)])


def define_preprocessor_spec() -> Dict[str, Any]:
    """Catalog of preprocessing rules per model family."""
    spec = {
        "title": "Preprocessor Pipeline Rules for Candidate Model Families",
        "families": {
            "linear_regularized": {
                "imputer": "SimpleImputer(strategy='median')",
                "scaler": "StandardScaler(mean=0, std=1)",
                "rationale": "Equalizes gradient descent penalties for L1/L2 penalties across diverse physical units."
            },
            "bayesian_kernel": {
                "imputer": "SimpleImputer(strategy='median')",
                "scaler": "StandardScaler(mean=0, std=1)",
                "rationale": "Prevents dimensions with huge raw values (e.g., carrier density 10^12) from dominating kernel distances."
            },
            "tree_ensembles": {
                "imputer": "SimpleImputer(strategy='median')",
                "scaler": "StandardScaler(mean=0, std=1)",
                "rationale": "Guarantees zero NaN entries across fold splits."
            },
            "symbolic_regression": {
                "imputer": "SimpleImputer(strategy='median')",
                "scaler": "MinMaxScaler(feature_range=(0.1, 1.0))",
                "rationale": "Avoids negative numbers and division by zero during transcendent operator evaluation."
            }
        }
    }
    
    PREPROCESSOR_SPEC_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(PREPROCESSOR_SPEC_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    s = define_preprocessor_spec()
    print("Preprocessor specifications serialized.")
