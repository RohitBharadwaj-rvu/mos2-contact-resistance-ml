# Sprint 2.a.2: Assess Sample-to-Feature Ratios and Model Complexity Constraints

## Sprint Metadata
- **Sprint ID:** Sprint-2.a.2
- **Objective:** Evaluate how the number of usable rows and features in the curated dataset constrains the complexity of models that can realistically be trained without overfitting; establish mathematical feature budgets and hyperparameter bounds.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Mathematical Generalization Bounds for $N = 20$

In small-$N$ empirical nanomaterials modeling, the risk of data memorization and variance explosion is acute:
- **Sample Size:** $N = 20$ experimentally verified contact records across 13 distinct publication sources.
- **Degrees of Freedom:** With 13 publication clusters, the effective cluster-level degrees of freedom is $df = 12$.
- **Harrell's Sample-to-Feature Ratio Heuristic:**
  - Standard linear modeling demands $N / P \ge 10:1$ to maintain stable parameter variance. For $N = 20$, this permits only $P \le 2$ unregularized predictors.
  - In regularized linear regimes ($L_1 / L_2$), $N / P \ge 4:1$ to $5:1$ is viable, permitting a maximum budget of **$P = 4$ active features**.
  - Feeding all 12+ candidate physical descriptors into an unregularized regression would leave $df < 7$, leading to severe multicollinearity-induced variance inflation.

---

## 2. Model Architecture Capacity Constraints

To enforce generalization and prevent spurious correlations, we establish strict programmatic bounds across model families:

| Model Family | Maximum Capacity Constraint | Regularization Strategy | Rationale |
| :--- | :--- | :--- | :--- |
| **Linear / ElasticNet** | Max active features $P \le 4$ | $\alpha \in [10^{-3}, 10^2]$, $L_1$ ratio $\in [0.1, 0.9]$ | Shrinks irrelevant coefficients to zero and curbs weight variance. |
| **Decision Trees / Forests** | $\text{max\_depth} \le 3$, $\text{min\_samples\_leaf} \ge 2$ | $N_{\text{estimators}} \le 50$, $\text{max\_features} = \sqrt{P}$ | Prevents single-sample leaf splits; limits depth to 3 decision nodes. |
| **Gaussian Processes (GPR)** | Low-rank kernels (RBF + WhiteKernel) | Noise level $\alpha_{\text{noise}} \ge 0.05$ | Incorporates experimental noise directly into the covariance kernel. |
| **Symbolic Regression** | Max equation length $\le 12$ nodes | Parsimony coefficient $= 0.05$ | Prevents higher-order Runge polynomials and over-parameterized expressions. |

---

## 3. Deliverables Produced
- `src/models/sample_complexity_analyzer.py`: Module computing feature budgets and capacity boundaries.
- `tests/test_sample_complexity_analyzer.py`: Automated verification suite.
- `data/reference/model_complexity_constraints.json`: Serialized constraints governing Section 4 model training.
