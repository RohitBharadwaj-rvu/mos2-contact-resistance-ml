# Sprint 3.a.3: Configure the Splitting Protocol & Fold Balance

## Sprint Metadata
- **Sprint ID:** Sprint-3.a.3
- **Objective:** Configure, audit, and serialize the official machine learning splitting protocol for the project; audit fold-wise sample sizes, target coverage, and architectural balance under `GroupKFold(n_splits=5)`.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Fold Balance & Distribution Audit

Under the official `GroupKFold(n_splits=5, groups=source_uid)` partitioning:
- **Total Samples:** $N = 20$.
- **Total Publication Clusters:** $G = 13$.
- **Validation Sample Sizes:** Every fold contains either 3, 4, or 5 samples ($N_{val} \in [3, 5]$, $N_{train} \in [15, 17]$), satisfying balance criteria.
- **Target Span:** Across all 5 folds, the minimum target span $\max(\log_{10} R_c) - \min(\log_{10} R_c) \ge 0.73\,\text{dex}$, guaranteeing that no validation fold is degenerate or concentrated at a single delta spike.
- **Architectural Representation:** Transferred vdW / semimetal contacts are distributed across folds, ensuring both de-pinned and pinned regimes are evaluated out-of-fold.

---

## 2. Official Project Validation Protocol Specification

The protocol mandates a two-tier evaluation hierarchy:
1. **Tier 1: Grouped 5-Fold Cross-Validation (`GroupKFold`):**
   - Strictly grouped by `source_uid`.
   - Used for inner-loop hyperparameter optimization, feature selection, and algorithm shortlisting.
2. **Tier 2: Leave-One-Group-Out Benchmark (`LOGO`):**
   - 13 folds; precisely models deploying a model into a brand-new literature lab.
   - Used for final model certification and performance claims.
3. **Prohibited Practices:**
   - Shuffled random splitting on grouped tabular nanomaterials data.
   - Pre-fitting scalers or feature encoders globally prior to cross-validation fold splitting.

---

## 3. Deliverables Produced
- `src/validation/splitting_protocol.py`: Fold balance audit and protocol generator.
- `tests/test_splitting_protocol.py`: Verification tests for fold size balance and schema requirements.
- `data/reference/official_validation_protocol.json`: Machine-readable protocol specification governing Section 4.
