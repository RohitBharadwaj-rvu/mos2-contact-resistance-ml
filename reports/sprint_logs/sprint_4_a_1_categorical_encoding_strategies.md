# Sprint 4.a.1: Implement Leakage-Free Categorical Encoding Strategies

## Sprint Metadata
- **Sprint ID:** Sprint-4.a.1
- **Objective:** Design, test, and implement methods for encoding categorical variables strictly within training folds, ensuring that unseen categories in validation folds never cause data leakage or runtime crashes.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Categorical Encoders Evaluated

In the curated $\text{MoS}_2$ contact dataset, key categorical attributes encode critical processing and structural Seams:
1. `contact_architecture` (`top_contact`, `edge_contact`, `transferred_vdw`).
2. `deposition_method` (`thermal_evaporation`, `e_beam_evaporation`, `mechanical_transfer`).

### Selected Encoding Paradigms

1. **One-Hot Encoding with Out-of-Distribution Zeroing (`OneHotEncoder(handle_unknown='ignore')`):**
   - Fits exclusively on training indices.
   - If a held-out test paper introduces a category not present in the training split, it safely assigns a zero-vector, preventing runtime exceptions and avoiding data leakage.
2. **Physics-Ranked Ordinal Encoding:**
   - Maps categories according to their theoretical interface defect density and Fermi-level pinning suppression:
     - **Architecture:** $\text{top\_contact} (0) < \text{edge\_contact} (1) < \text{transferred\_vdw} (2)$.
     - **Deposition:** $\text{thermal} (0) < \text{e\_beam} (1) < \text{mechanical\_transfer} (2)$.
   - Retains a single dense column without inflating feature dimensionality in small-$N$ regimes.

---

## 2. Deliverables Produced
- `src/features/categorical_encoders.py`: Implementation of `build_categorical_preprocessor()` with OneHot and Physics-Ordinal modes.
- `tests/test_categorical_encoders.py`: Automated verification suite for fold isolation and unseen category handling.
- `data/reference/categorical_encoding_spec.json`: Serialized encoding specification.
