# Sprint 3.b.2: Research Rank and Trend Correlation Metrics

## Sprint Metadata
- **Sprint ID:** Sprint-3.b.2
- **Objective:** Investigate correlation and ranking metrics to assess whether a model correctly orders contact performance across research groups, even when baseline resistance values suffer systematic inter-laboratory shifts.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Rationale for Monotonic Ranking Metrics

In multi-laboratory experimental compilations, cross-laboratory variations (differences in base vacuum, probe station contact resistance, and annealing furnace contamination) frequently introduce systematic additive offsets ($\pm 0.3\,\text{dex}$) in $R_c$.
However, for experimental design and material screening, the most critical question is:
> **"Does the model correctly rank Candidate A as superior to Candidate B?"**

A model that preserves exact rank order despite a constant lab offset is far more physically insightful and useful in the cleanroom than one that minimizes absolute squared residuals by memorizing lab identifiers.

---

## 2. Selected Rank Metrics & Mathematical Formulation

1. **Spearman's Rank Correlation ($\rho$):**
   $$\rho = 1 - \frac{6 \sum d_i^2}{N(N^2 - 1)}$$
   - Target threshold: $\rho \ge 0.80$.
   - Measures general monotonic fidelity across all devices; invariant to arbitrary monotonic transformations.
2. **Kendall's Tau ($\tau_b$):**
   $$\tau_b = \frac{C - D}{\sqrt{(C + D + T_x)(C + D + T_y)}}$$
   - Target threshold: $\tau \ge 0.65$.
   - Directly measures the net proportion of concordant ($C$) versus discordant ($D$) pairwise metal rankings.
3. **Pairwise Concordance Index ($C$-index):**
   $$C\text{-index} = \frac{\sum_{i < j} \mathbf{1}\left[(\hat{y}_i - \hat{y}_j)(y_i - y_j) > 0\right]}{\sum_{i < j} \mathbf{1}\left[y_i \ne y_j\right]}$$
   - Target threshold: $C \ge 0.85$.
   - Represents the exact probability that for two randomly chosen experimental contact configurations, the model correctly predicts which device exhibits lower contact resistance.

---

## 3. Deliverables Produced
- `src/validation/rank_trend_metrics.py`: Calculation engine for Spearman $\rho$, Kendall $\tau$, and pairwise $C$-index.
- `tests/test_rank_trend_metrics.py`: Verification tests covering monotonic scaling, inverted orderings, and metric dictionaries.
- `data/reference/rank_trend_metrics_spec.json`: Machine-readable specification.
