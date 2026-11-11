# Sprint 2.c.1: Investigate Tree-Based Ensemble Methods

## Sprint Metadata
- **Sprint ID:** Sprint-2.c.1
- **Objective:** Investigate decision-tree ensemble and boosting frameworks (Random Forest, Gradient Boosting, Extra Trees) under small-$N$ capacity constraints ($\text{max\_depth} \le 3$, $\text{min\_samples\_leaf} \ge 2$).
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Architectural Exploration & Heuristic Bounds

Tree ensembles offer natural handling of non-linear saturation effects (such as carrier freeze-out and high-density gate screening) without requiring explicit basis transformations. However, with $N = 20$, standard unconstrained trees with default infinite depth will split down to individual samples, producing severe overfitting.
We established strict regularization hyperparameters:
- `max_depth = 3`: Maximum of 8 terminal leaf regions.
- `min_samples_split = 4`, `min_samples_leaf = 2`: Precludes isolating single experimental records.
- `subsample = 0.8` (in Gradient Boosting) to introduce stochastic bagging variance reduction.

---

## 2. In-Sample Benchmark Comparison

| Model Architecture | $\text{RMSE} (\log_{10} R_c)$ | $\text{MAE} (\log_{10} R_c)$ | $R^2$ Score | Top Feature by Importance |
| :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | $0.223\,\text{dex}$ | $0.158\,\text{dex}$ | $0.890$ | `gate_carrier_density_cm2` ($66.1\%$) |
| **Gradient Boosting** | $0.083\,\text{dex}$ | $0.068\,\text{dex}$ | $0.985$ | `gate_carrier_density_cm2` ($67.8\%$) |
| **Extra Trees** | $0.241\,\text{dex}$ | $0.159\,\text{dex}$ | $0.871$ | `gate_carrier_density_cm2` ($58.2\%$) |

---

## 3. Physical Insights from Tree Splits
- Decision trees prioritize `gate_carrier_density_cm2` at the root split ($> 60\%$ split importance), reflecting the strong exponential gating modulation of 2D $\text{MoS}_2$ channels between depletion ($n_{2D} \sim 10^{11}\,\text{cm}^{-2}$) and strong accumulation ($n_{2D} \ge 10^{13}\,\text{cm}^{-2}$).
- Secondary splits branch on `physics_predicted_sbh_ev` and `is_vdw_or_depinned_contact`, capturing the barrier-height difference between semimetals (Bi, Sb) and evaporated metals.

---

## 4. Deliverables Produced
- `src/models/tree_ensembles.py`: Module for capacity-constrained tree ensemble construction and evaluation.
- `tests/test_tree_ensembles.py`: Verification tests for tree hyperparameters and metric ranges.
- `data/reference/tree_ensemble_evaluation.json`: Machine-readable results and feature importances.
