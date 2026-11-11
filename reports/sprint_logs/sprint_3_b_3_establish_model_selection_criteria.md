# Sprint 3.b.3: Establish Model Selection Criteria

## Sprint Metadata
- **Sprint ID:** Sprint-3.b.3
- **Objective:** Establish the multi-objective selection criteria and composite scoring formula combining out-of-fold RMSE, Spearman rank correlation, pairwise concordance index, and parsimony penalty to declare champion models.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Multi-Objective Composite Selection Formula

To prevent selecting models that over-index on squared residuals at the expense of ordering fidelity, we established the official **Composite Selection Score ($\mathcal{S}_{\text{selection}}$)**:

$$\mathcal{S}_{\text{selection}} = 0.40 \cdot \max\left(0, 1 - \text{RMSE}_{\text{dex}}\right) + 0.35 \cdot \max\left(0, \rho_{\text{spearman}}\right) + 0.25 \cdot C_{\text{index}} - 0.05 \cdot \max\left(0, P - 4\right)$$

Where:
- **Accuracy Term ($40\%$ Weight):** Evaluates decade precision ($1.0$ at zero error, $0.0$ if $\text{RMSE} \ge 1.0\,\text{dex}$).
- **Ranking Term ($35\%$ Weight):** Enforces monotonic preservation of contact quality across publications.
- **Concordance Term ($25\%$ Weight):** Pairwise ordering accuracy ($C$-index).
- **Parsimony Penalty ($-0.05$ per excess feature):** Penalizes models utilizing more than 4 features, directly aligning with Harrell's $N/P \ge 5:1$ heuristic.

---

## 2. Hard Qualification Thresholds for Deployment

A model will only be considered qualified for production deployment and cleanroom recommendations if it simultaneously satisfies:
1. **Grouped 5-Fold $\text{RMSE}_{\text{dex}} \le 0.45$** (typical prediction error under factor of $2.8\times$).
2. **Spearman $\rho \ge 0.75$** (strong positive rank correlation).
3. **Concordance Index $C \ge 0.80$** (at least $80\%$ of pairwise contact comparisons correctly ordered).
4. **Physical Constraint Violations $= 0$** (zero negative barrier derivatives or sub-quantum predictions).

---

## 3. Deliverables Produced
- `src/validation/selection_criteria.py`: Implementation of composite selection scoring and qualification auditing.
- `tests/test_selection_criteria.py`: Verification tests for scoring weights, parsimony penalties, and threshold checks.
- `data/reference/model_selection_criteria.json`: Machine-readable specification governing Section 4 model tuning and final selection.
