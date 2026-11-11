# Sprint 4.c.1 Log: Identify Key Hyperparameters for Each Architecture

## 1. Objectives & Theoretical Scope
- Catalog the core capacity controls, regularization parameters, and search intervals for all shortlisted regression architectures.
- Prevent over-parameterization given the small sample regime ($N=20$ devices across 13 literature sources) by bounding search spaces to structurally compact configurations.
- Document the specific regularizing mechanism of each parameter (e.g., L2 shrinkage, tree depth pruning, kernel bandwidth bounds, epsilon margin).

## 2. Key Hyperparameters and Capacity Controls

1. **Ridge Regression & ElasticNet:**
   - `alpha` ($\alpha \in [0.01, 50.0]$): Controls L2 penalization to prevent ill-conditioned matrix inversion in collinear solid-state descriptor spaces.
   - `l1_ratio` ($r \in [0.1, 0.9]$): Governs the trade-off between exact feature zeroing (L1) and smooth cooperative shrinkage (L2).

2. **Gradient Boosting Regressor:**
   - `n_estimators` ($\in [20, 75]$) & `learning_rate` ($\eta \in [0.01, 0.1]$): Restricts gradient descent step accumulation.
   - `max_depth` ($\in \{2, 3\}$): Enforces shallow decision boundaries, preventing individual literature sample memorization.
   - `subsample` ($\in [0.7, 1.0]$): Adds stochastic subsampling to inject bagging diversity.
   - `min_samples_leaf` ($\ge 2$): Prohibits single-device leaf leaves.

3. **Random Forest Regressor:**
   - `n_estimators` ($\in [30, 80]$): Provides adequate variance reduction without excess complexity.
   - `max_depth` ($\in \{2, 3\}$) & `min_samples_split` ($\in [3, 6]$): Bounds tree depth and node partitioning.

4. **Gaussian Process Regressor (Matérn 3/2 & 5/2):**
   - `length_scale_init` ($\ell \in [0.5, 5.0]$): Prevents kernel bandwidth collapse into narrow delta spikes around training clusters.
   - `noise_level_init` ($\sigma_n^2 \in [0.01, 0.2]$): Absorbs non-intrinsic experimental scatter without forcing overfitting to measurement noise.

5. **Support Vector Regression (RBF):**
   - `C` ($\in [0.5, 20.0]$): Regulates penalty slack on out-of-tube points.
   - `epsilon` ($\epsilon \in [0.02, 0.20]$): Defines the margin of indifference for TLM characterization uncertainty.
   - `gamma` ($\gamma \in [0.05, 0.5]$): Controls the influence radius of support vectors.

## 3. Implemented Deliverables
- `src/models/hyperparameter_spaces.py`: Implemented parameter definitions and export routines.
- `tests/test_hyperparameter_spaces.py`: Test suite validating architecture coverage and dictionary integrity.
- `data/reference/hyperparameter_search_spaces.json`: Serialized catalog.

## 4. Verification & Validation
- Ran `python -m pytest tests/test_hyperparameter_spaces.py` — Passed (100% green).
