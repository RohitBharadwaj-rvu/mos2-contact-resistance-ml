"""
Scientific Imputation and Missingness Provenance Engine (Sprint 7.2).
Replaces naive hardcoded default imputations with scientifically rigorous missingness handling:
1. Distinguishes 'as_fabricated_unannealed' (physical zero-treatment) from 'unreported' (missing data).
2. Distinguishes 'measured' vs 'calculated_from_gating' vs 'unreported' carrier density.
3. Preserves NaNs natively for tree-based models (XGBoost, HistGradientBoosting, LightGBM).
4. Generates fold-safe missingness indicator masks and median imputations strictly within CV training folds for linear models.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "primary_experimental_literature_dataset.csv"
AUDIT_JSON_PATH = ROOT_DIR / "data" / "processed" / "missingness_provenance_audit.json"


class ScientificMissingnessHandler(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer that applies scientifically justified missingness handling.
    Fitted strictly on training folds to prevent data leakage.
    """
    def __init__(self, mode: str = "native_nan"):
        """
        mode:
          - 'native_nan': Keeps NaNs intact and adds binary missingness indicator flags (for XGBoost / Tree models).
          - 'fold_imputed': Imputes training median and adds binary indicator flags (for Ridge / Linear models).
        """
        self.mode = mode
        self.train_medians_ = {}
        self.indicator_cols_ = []

    def fit(self, X: pd.DataFrame, y=None):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        self.train_medians_ = {}
        for col in X.columns:
            if np.issubdtype(X[col].dtype, np.number):
                valid_vals = X[col].dropna()
                self.train_medians_[col] = float(valid_vals.median()) if len(valid_vals) > 0 else 0.0
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        X_out = X.copy()

        # Add missingness indicators for columns with missing values
        for col in X.columns:
            if X[col].isna().any():
                indicator_name = f"{col}_is_missing"
                X_out[indicator_name] = X[col].isna().astype(float)
                if indicator_name not in self.indicator_cols_:
                    self.indicator_cols_.append(indicator_name)

                if self.mode == "fold_imputed":
                    fill_val = self.train_medians_.get(col, 0.0)
                    X_out[col] = X_out[col].fillna(fill_val)

        return X_out


def audit_dataset_missingness_provenance(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Audits the primary experimental dataset for reporting completeness, distinguishing
    between deliberately unannealed devices and truly unreported parameters.
    """
    if df is None:
        df = pd.read_csv(RAW_DATA_PATH)

    total_devices = len(df)

    # 1. Annealing status breakdown
    annealing_counts = df["post_annealing_status"].value_counts().to_dict()

    # 2. Carrier density provenance breakdown
    carrier_provenance = df["carrier_density_provenance"].value_counts().to_dict()

    # 3. Vacuum base pressure provenance
    vacuum_provenance = df["vacuum_provenance"].value_counts().to_dict()

    # 4. Schottky barrier height measurement status
    sbh_measured_count = int(df["measured_sbh_ev"].notna().sum())
    sbh_unmeasured_count = total_devices - sbh_measured_count

    # 5. Missingness summary
    missing_by_col = {}
    for col in df.columns:
        n_missing = int(df[col].isna().sum())
        if n_missing > 0:
            missing_by_col[col] = {
                "missing_count": n_missing,
                "missing_pct": round(n_missing / total_devices * 100, 1)
            }

    audit_summary = {
        "total_primary_observations": total_devices,
        "annealing_provenance": {
            "categories": annealing_counts,
            "scientific_rationale": (
                "Unannealed devices (as_fabricated_unannealed) represent a deliberate physical state (T=20C, duration=0min). "
                "They are modeled with an explicit binary flag 'is_annealed = 0', rather than treated as missing data."
            )
        },
        "carrier_density_provenance": {
            "categories": carrier_provenance,
            "scientific_rationale": (
                "Distinguishes directly measured Hall carrier density from electrostatic gating capacitance calculation "
                "(n_2D = Cox*(Vgs-Vth)/q). Prevents conflating electrostatic gating with Hall transport measurements."
            )
        },
        "vacuum_pressure_provenance": {
            "categories": vacuum_provenance,
            "scientific_rationale": (
                "Differentiates explicit UHV chamber readings (< 1e-8 Torr) from standard high-vacuum base pressure."
            )
        },
        "schottky_barrier_measurements": {
            "measured_count": sbh_measured_count,
            "unmeasured_count": sbh_unmeasured_count,
            "measured_fraction_pct": round(sbh_measured_count / total_devices * 100, 1),
            "scientific_rationale": (
                "Measured SBH is strictly separated from physics-estimated SBH to prevent data leakage "
                "and circular reasoning in contact resistance prediction."
            )
        },
        "columns_with_missing_values": missing_by_col
    }

    AUDIT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2)

    return audit_summary


if __name__ == "__main__":
    res = audit_dataset_missingness_provenance()
    print("Scientific missingness provenance audit complete.")
    print(f"Total Devices: {res['total_primary_observations']}")
    print(f"Annealing Status: {res['annealing_provenance']['categories']}")
    print(f"Carrier Density Provenance: {res['carrier_density_provenance']['categories']}")
    print(f"Measured SBH Devices: {res['schottky_barrier_measurements']['measured_count']}/{res['total_primary_observations']}")
