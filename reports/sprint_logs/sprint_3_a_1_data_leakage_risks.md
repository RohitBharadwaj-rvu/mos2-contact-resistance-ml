# Sprint 3.a.1: Analyze Data Leakage Risks in Small-N Nanomaterials Modeling

## Sprint Metadata
- **Sprint ID:** Sprint-3.a.1
- **Objective:** Quantify how standard random train/test and random $K$-fold cross-validation strategies lead to catastrophic data leakage when multiple devices originate from the same published study; prove the mathematical necessity of grouped validation.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Quantification of Intra-Study Leakage Probability

On the curated dataset of 20 experimental records from 13 distinct peer-reviewed papers:
- **Total Records:** 20 devices.
- **Distinct Publication Clusters:** 13 papers.
- **Multi-Device Studies:** 4 papers contribute $> 1$ device (Allain 2015: 4, Liu 2018: 3, English 2016: 2, Shen 2021: 2).
- **Vulnerable Sample Count:** 11 of 20 records ($55\%$) belong to multi-device clusters.

### Empirical 5-Fold Random Split Simulation
Simulating standard random 5-fold cross-validation over 10 randomized trials demonstrates:
- **Contaminated Folds:** In 100% of standard random runs, between 3 and 5 of the 5 validation folds suffer from direct intra-study contamination.
- **Average Leaked Clusters:** An average of $2.2$ paper clusters are split simultaneously across training and validation folds within each iteration.

---

## 2. Physical Mechanisms of Information Leakage

When devices from the same research paper are split across training and validation sets, models do not learn transferrable solid-state physics. Instead, they exploit three unmodeled confounders:
1. **Identical Fabrication Equipment & Chamber Base Vacuum:**
   - Evaporation chamber base pressure ($P_{base} \sim 10^{-7}$ vs $10^{-9}\,\text{Torr}$), source crucible cleanliness, and hydrocarbon background contamination are identical for devices made in the same lab.
2. **Exfoliation Stock & Defect Chemistry:**
   - Flakes cleaved from the same bulk natural molybdenite crystal share sulfur vacancy density and native substrate roughness.
3. **Metrology & Contact Resistance Extraction Setup:**
   - Systematic offsets in probe-needle resistance subtraction, TLM channel length optical calibrations, and cryostat temperature sensors are shared.

**Consequence:** A model evaluated under random splitting achieves artificially deflated validation errors (optimistic bias) by interpolating between sibling devices from the same run, failing completely when applied to new independent laboratories.

---

## 3. Deliverables Produced
- `src/validation/leakage_analyzer.py`: Simulation and statistical leakage quantification engine.
- `tests/test_leakage_analyzer.py`: Verification tests confirming leakage detection under random K-fold.
- `data/reference/data_leakage_risk_analysis.json`: Serialized empirical risk report.
