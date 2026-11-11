"""
Official Splitting Protocol and Fold Balance Auditor (Sprint 3.a.3).
Analyzes fold-wise representation, target balance, and architectural coverage under GroupKFold and LeaveOneGroupOut protocols.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

PROTOCOL_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "official_validation_protocol.json"


def audit_grouped_fold_distributions(df: Optional[pd.DataFrame] = None, n_splits: int = 5) -> Dict[str, Any]:
    """
    Audits GroupKFold(n_splits=5) fold distributions:
    - Number of validation samples per fold.
    - Distribution of targets (mean log10_rc, min, max).
    - Presence of de-pinned/vdW vs evaporated contacts.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    gkf = GroupKFold(n_splits=n_splits)
    groups = df["source_uid"].values
    
    fold_summaries = []
    for fold_idx, (train_idx, val_idx) in enumerate(gkf.split(df, groups=groups)):
        val_df = df.iloc[val_idx]
        val_targets = val_df["log10_rc"].values
        val_papers = val_df["source_uid"].unique().tolist()
        
        has_vdw = int(val_df["is_vdw_or_depinned_contact"].sum())
        n_evaporated = len(val_df) - has_vdw
        
        fold_summaries.append({
            "fold_index": fold_idx,
            "validation_sample_count": len(val_df),
            "training_sample_count": len(train_idx),
            "papers_in_validation": val_papers,
            "target_mean_log10_rc": round(float(np.mean(val_targets)), 3),
            "target_std_log10_rc": round(float(np.std(val_targets)), 3) if len(val_targets) > 1 else 0.0,
            "target_min_log10_rc": round(float(np.min(val_targets)), 3),
            "target_max_log10_rc": round(float(np.max(val_targets)), 3),
            "vdw_depinned_contacts_count": has_vdw,
            "evaporated_contacts_count": n_evaporated
        })
        
    audit_results = {
        "n_splits": n_splits,
        "total_samples": len(df),
        "total_groups": len(np.unique(groups)),
        "folds": fold_summaries,
        "balance_assessment": {
            "min_val_size": min(f["validation_sample_count"] for f in fold_summaries),
            "max_val_size": max(f["validation_sample_count"] for f in fold_summaries),
            "is_balanced": bool(max(f["validation_sample_count"] for f in fold_summaries) - min(f["validation_sample_count"] for f in fold_summaries) <= 3)
        }
    }
    
    return audit_results


def get_official_validation_protocol() -> Dict[str, Any]:
    """Generates and serializes the complete, authoritative validation protocol."""
    fold_audit = audit_grouped_fold_distributions()
    
    protocol = {
        "title": "MoS2 Contact Resistance Official Machine Learning Validation Protocol",
        "primary_cv_scheme": {
            "scheme": "GroupKFold",
            "n_splits": 5,
            "grouping_variable": "source_uid",
            "leakage_guarantee": "Zero source_uid overlap between training and validation sets",
            "role": "Hyperparameter optimization, feature pruning, and cross-validation model selection."
        },
        "secondary_benchmark_scheme": {
            "scheme": "LeaveOneGroupOut (LOGO)",
            "n_splits": 13,
            "grouping_variable": "source_uid",
            "role": "True out-of-distribution transfer benchmark assessing prediction on completely unseen literature cleanrooms."
        },
        "fold_distribution_audit": fold_audit,
        "prohibited_practices": [
            "Random train_test_split without source grouping",
            "Random KFold or StratifiedKFold on rows from the same paper",
            "StandardScaler fitting on the entire dataset prior to splitting"
        ]
    }
    
    PROTOCOL_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROTOCOL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(protocol, f, indent=2)
        
    return protocol


if __name__ == "__main__":
    p = get_official_validation_protocol()
    print("Official validation protocol serialized successfully.")
