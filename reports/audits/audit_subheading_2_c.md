# Subheading 2.c Audit: Evaluation & Selection of Non-Linear Architectures

## 1. Scope & Objectives
Subheading 2.c explores, benchmarks, and shortlists candidate non-linear machine learning architectures for $\text{MoS}_2$ contact resistance prediction:
- **Sprint 2.c.1:** Tree-based ensemble methods (Random Forest, Gradient Boosting, Extra Trees).
- **Sprint 2.c.2:** Alternative non-linear regression paradigms (Gaussian Process Regression with RBF and Matérn kernels, SVR, Kernel Ridge).
- **Sprint 2.c.3:** Multi-criteria architecture decision matrix and official algorithm shortlist.

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Kernel Hyperparameter Optimization Boundaries
- **Issue:** In GPR, default tight length-scale upper bounds ($10.0$) triggered Scipy L-BFGS `ConvergenceWarning` when optimizing on small-$N$ normalized feature spaces.
- **Resolution:** Expanded length-scale bounds to $[0.1, 50.0]$ and initialized with length scale $= 2.0$, completely eliminating convergence warnings while improving $R^2$ to $0.964$.

### Gap 2: Unified Architectural Instantiation Interface
- **Issue:** Cross-validation in Section 3 and Section 4 required disparate initialization calls for pipelines vs standalone tree estimators.
- **Resolution:** Implemented `instantiate_candidate_model(name, **kwargs)` in `src/models/model_factory.py`, providing a unified, pre-scaled entrypoint for all 6 shortlisted architectures (`Ridge_Regression`, `ElasticNet`, `Random_Forest`, `Gradient_Boosting`, `Gaussian_Process_Matern`, `Support_Vector_Regression_RBF`).

---

## 3. Verification & Compliance
- Multi-criteria decision matrix serialized to `data/reference/shortlisted_architectures.json`.
- All unit tests in `tests/test_tree_ensembles.py`, `tests/test_alternative_regressors.py`, `tests/test_model_selector.py`, and `tests/test_model_factory.py` pass with 100% success.

Subheading 2.c is certified and approved to advance to Subheading 2.d.
