"""
Leakage-Free Categorical Encoding Pipeline (Sprint 4.a.1).
Implements fold-isolated One-Hot and Physics-Ranked categorical encoding for MoS2 contact architecture, deposition method, and gate dielectrics.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer

ENCODING_SPEC_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "categorical_encoding_spec.json"

# Physics-ranked domain orders
ARCHITECTURE_RANKING = ["top_contact", "edge_contact", "transferred_vdw"]
DEPOSITION_RANKING = ["thermal_evaporation", "e_beam_evaporation", "mechanical_transfer"]


def build_categorical_preprocessor(strategy: str = "one_hot", categorical_cols: Optional[List[str]] = None) -> ColumnTransformer:
    """
    Constructs a scikit-learn ColumnTransformer that fits strictly within training folds,
    preventing any out-of-fold information leakage.
    """
    if categorical_cols is None:
        categorical_cols = ["contact_architecture", "deposition_method"]
        
    if strategy == "one_hot":
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    elif strategy == "physics_ordinal":
        encoder = OrdinalEncoder(
            categories=[ARCHITECTURE_RANKING, DEPOSITION_RANKING],
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )
    else:
        raise ValueError(f"Unknown categorical encoding strategy: {strategy}")
        
    return ColumnTransformer(
        transformers=[
            ("cat", encoder, categorical_cols)
        ],
        remainder="passthrough"
    )


def define_categorical_encoding_spec() -> Dict[str, Any]:
    """Catalog of categorical encoding rules and physics-informed hierarchies."""
    spec = {
        "title": "Categorical Variable Encoding Specification for MoS2 Contact ML",
        "categorical_variables": {
            "contact_architecture": {
                "categories": ARCHITECTURE_RANKING,
                "physics_rank": {"top_contact": 0, "edge_contact": 1, "transferred_vdw": 2},
                "rationale": "Transferred vdW contacts suppress Fermi-level pinning; edge contacts provide 1D covalent orbital overlap."
            },
            "deposition_method": {
                "categories": DEPOSITION_RANKING,
                "physics_rank": {"thermal_evaporation": 0, "e_beam_evaporation": 1, "mechanical_transfer": 2},
                "rationale": "Mechanical transfer eliminates high-energy kinetic bombardment and defect creation."
            }
        },
        "recommended_strategy": "OneHotEncoder with handle_unknown='ignore' inside Pipeline to guarantee zero data leakage",
        "leakage_safeguards": [
            "Encoders must only be fitted on training fold indices",
            "Unseen test categories must encode to zero-vectors rather than throwing errors"
        ]
    }
    
    ENCODING_SPEC_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(ENCODING_SPEC_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    spec = define_categorical_encoding_spec()
    print("Categorical encoding specification serialized successfully.")
