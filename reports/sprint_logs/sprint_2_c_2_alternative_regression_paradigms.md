# Sprint 2.c.2: Investigate Alternative Regression Paradigms

## Sprint Metadata
- **Sprint ID:** Sprint-2.c.2
- **Objective:** Explore alternative regression paradigms (Gaussian Process Regression with RBF and Matérn kernels, Support Vector Regression, Kernel Ridge Regression) for small-$N$ non-linear modeling with uncertainty quantification.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Architectural Motivation for Kernel and Bayesian Methods

While tree-based methods offer discrete step-function partitioning, semiconductor physics is inherently smooth and governed by continuous exponential barrier transport.
Alternative kernel-based and Bayesian methods offer critical advantages in small-$N$ regimes ($N = 20$):
1. **Gaussian Process Regression (GPR):**
   - Exact Bayesian non-parametric inference.
   - Provides analytic predictive uncertainty $\sigma_*(x_*)$ alongside mean predictions $\mu_*(x_*)$, preventing overconfident extrapolations when evaluating unmeasured contact metals or novel 2D heterostructures.
   - Tested Kernels:
     - Constant $\times$ RBF + WhiteKernel (infinite smoothness).
     - Constant $\times$ Matérn ($\nu = 2.5$) + WhiteKernel (allows finite differentiability, capturing sharp contact de-pinning transitions).
2. **Support Vector Regression (SVR):**
   - Employs $\epsilon$-insensitive loss function: errors smaller than $\epsilon = 0.10\,\text{dex}$ incur zero penalty.
   - Naturally discards minor experimental characterization noise and establishes sparsity in dual support vectors.
3. **Kernel Ridge Regression (KRR):**
   - Closed-form regularized dual representation $(K + \alpha I)^{-1} y$.

---

## 2. Quantitative Comparison on Curated Dataset

| Architecture | Kernel / Hyperparameters | $\text{RMSE} (\log_{10} R_c)$ | $\text{MAE} (\log_{10} R_c)$ | $R^2$ Score | Pearson $r$ | Predictive Uncertainty ($\bar{\sigma}$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPR (RBF)** | $C \times \text{RBF}(l=13) + \text{White}(0.031)$ | $0.147\,\text{dex}$ | $0.115\,\text{dex}$ | $0.952$ | $0.976$ | $0.199\,\text{dex}$ |
| **GPR (Matérn 5/2)**| $C \times \text{Matérn}(l=14.8) + \text{White}(0.026)$| $0.127\,\text{dex}$ | $0.091\,\text{dex}$ | $0.964$ | $0.982$ | $0.186\,\text{dex}$ |
| **SVR (RBF)** | $C = 5.0, \epsilon = 0.10$ | $0.090\,\text{dex}$ | $0.085\,\text{dex}$ | $0.982$ | $0.993$ | N/A (deterministic) |
| **Kernel Ridge** | $\text{RBF}, \alpha = 0.05, \gamma = 0.20$ | $0.123\,\text{dex}$ | $0.099\,\text{dex}$ | $0.967$ | $0.985$ | N/A (deterministic) |

---

## 3. Physical Insights
- **Noise Estimation:** GPR automatically learned an optimal noise variance $\sigma_{noise}^2 \approx 0.026 - 0.031\,\text{dex}^2$, corresponding to an inherent experimental noise standard deviation of $\approx 0.16\,\text{dex}$ ($\approx 45\%$ experimental variability). This matches almost exactly our empirical cross-lab $\text{Ti}$ spread ($0.2\,\text{dex}$) identified in Sprint 1.f.4.
- **Matérn Superiority:** Matérn $\nu=2.5$ outperforms RBF ($R^2 = 0.964$ vs $0.952$), confirming that physical contact resistance contains localized interface transitions better modeled with relaxed smoothness.

---

## 4. Deliverables Produced
- `src/models/alternative_regressors.py`: Implementation of GPR, SVR, and Kernel Ridge pipelines.
- `tests/test_alternative_regressors.py`: Unit tests verifying pipeline execution, metrics, and Bayesian uncertainty.
- `data/reference/alternative_regressors_evaluation.json`: Machine-readable results and optimized kernel hyperparameter values.
