# Sprint 3.b.1: Research Regression Error Metrics

## Sprint Metadata
- **Sprint ID:** Sprint-3.b.1
- **Objective:** Evaluate standard regression error metrics across logarithmic and physical scales; establish mathematically sound, scale-invariant metrics for $\text{MoS}_2$ contact resistance predictions spanning orders of magnitude.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Metric Evaluation Across Multi-Decade Scales

Nanoscale contact resistance spans over four orders of magnitude ($10^2$ to $10^5\,\Omega\cdot\mu\text{m}$). Standard linear regression metrics suffer severe pathologies when applied directly:
- **Flaw of Linear $\text{RMSE}$:** A single prediction error on a high-resistance device ($60,000\,\Omega\cdot\mu\text{m}$) dominates the loss function, completely masking whether the model accurately predicts low-resistance ohmic contacts ($120\,\Omega\cdot\mu\text{m}$).
- **Flaw of Standard $\text{MAPE}$:** Dividing by raw resistance penalizes low-resistance devices asymmetrically.

### Selected Multi-Decade Error Metrics

1. **Root Mean Squared Log Error ($\text{RMSE}_{\log_{10}}$, units: dex):**
   $$\text{RMSE}_{\text{dex}} = \sqrt{\frac{1}{N} \sum_{i=1}^N \left(\log_{10} R_{c,i} - \log_{10} \hat{R}_{c,i}\right)^2}$$
   - Direct physical interpretation in decades ("dex").
   - $\text{RMSE} = 0.20\,\text{dex}$ indicates typical prediction scatter within a factor of $10^{0.20} \approx 1.58\times$.
2. **Mean Absolute Log Error ($\text{MAE}_{\log_{10}}$, units: dex):**
   $$\text{MAE}_{\text{dex}} = \frac{1}{N} \sum_{i=1}^N \left|\log_{10} R_{c,i} - \log_{10} \hat{R}_{c,i}\right|$$
   - Maximally robust to occasional outlier devices produced by noisy experimental characterization.
3. **Geometric Factor Error ($X$-Fold Accuracy):**
   $$\text{Geometric Factor} = 10^{\text{MAE}_{\text{dex}}}$$
   - Intuitive for experimentalists: e.g., $\text{Factor} = 1.35\times$ indicates predictions match experiment within $35\%$ on average.
4. **Median Absolute Percentage Error ($\text{MedAPE}$, units: %):**
   $$\text{MedAPE} = \text{median}\left(\frac{|R_c - \hat{R}_c|}{R_c}\right) \times 100\%$$
   - Scale-invariant median percentage error.

---

## 2. Deliverables Produced
- `src/validation/regression_metrics.py`: Calculation engine for decade, geometric factor, and linear percentage errors.
- `tests/test_regression_metrics.py`: Verification tests for metric boundaries and precision.
- `data/reference/regression_error_metrics.json`: Serialized metric specification.
