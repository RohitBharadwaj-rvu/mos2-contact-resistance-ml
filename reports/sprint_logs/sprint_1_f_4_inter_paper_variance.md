# Sprint 1.f.4: Inter-Paper Variance and Systematic Lab Bias

## Sprint Metadata
- **Sprint ID:** Sprint-1.f.4
- **Objective:** Evaluate inter-paper variance and systematic lab bias across literature sources (quantify cross-lab spread for identical contacts like $\text{Ti}/\text{MoS}_2$, assess publication-grouped clustering, and evaluate within-study vs between-study variance).
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Motivation & Context
In meta-analysis of nanomaterials experimental data, cross-laboratory discrepancies often arise from variations in base vacuum pressure during e-beam evaporation, chemical purity of sources, surface contamination (resist residue), transfer methods, and differing post-annealing protocols.
Quantifying the magnitude of this "lab bias" relative to the physical signal (Schottky barrier height, work function mismatch, semimetal pinning suppression) is crucial for:
1. Validating whether physical features have sufficient explanatory signal over noise.
2. Determining appropriate cross-validation split strategies (e.g. GroupKFold by `source_uid`).

---

## 2. Statistical Findings

### ANOVA Decomposition
- **Total Source Papers Represented:** 13 peer-reviewed studies.
- **ANOVA $F$-statistic:** $1.711$ ($p = 0.251$).
  - The between-study variance does not overwhelm the intrinsic physics; the $p$-value $> 0.05$ indicates that group labels alone do not account for the variance compared to the spread introduced by testing different contact metals within studies.

### Cross-Lab Benchmarking: Identical Metal ($\text{Ti}/\text{MoS}_2$)
Titanium is the most widely tested standard n-type contact metal across multiple institutions.
We benchmarked experimental $R_c$ values reported across independent groups:
1. **English et al. (2016, Stanford):** $R_c = 740\,\Omega\cdot\mu\text{m}$ (as-deposited, e-beam, $P < 10^{-7}\,\text{Torr}$).
2. **Liu et al. (2020, Nanjing/Peking):** $R_c = 550\,\Omega\cdot\mu\text{m}$ (post-annealed at $300^\circ\text{C}$).
3. **Allain et al. (2015, Review / Standard Fab Compilation):** $R_c \approx 2000\,\Omega\cdot\mu\text{m}$ (unoptimized ambient fab).

**Key Takeaway:**
- Inter-lab variation for the identical contact metal ($\text{Ti}$) is approximately **$3.6\times$** ($550$ to $2000\,\Omega\cdot\mu\text{m}$).
- In contrast, intentional material and contact engineering choices—such as semimetal hybridization ($\text{Bi}$, $R_c = 123\,\Omega\cdot\mu\text{m}$) versus high work function metals ($\text{Au}/\text{Pt}$, $R_c = 12,000$ to $65,000\,\Omega\cdot\mu\text{m}$)—yield a spread exceeding **$500\times$**.
- Therefore, physical contact parameters dominate over systematic experimental noise by more than two orders of magnitude.

---

## 3. Deliverables Produced
1. `src/visualization/lab_bias_analyzer.py`:
   - `analyze_inter_paper_variance()`: Computes group-level summary statistics and ANOVA test.
   - `generate_variance_plots()`: Produces grouped boxplot and cross-lab $\text{Ti}$ bar chart.
2. `tests/test_lab_bias_analyzer.py`: Automated verification suite.
3. `data/processed/inter_paper_variance_summary.json`: Serialized ANOVA and cross-lab benchmark metrics.
4. `reports/figures/inter_paper_variance_analysis.png`: High-resolution dual-panel visualization.
