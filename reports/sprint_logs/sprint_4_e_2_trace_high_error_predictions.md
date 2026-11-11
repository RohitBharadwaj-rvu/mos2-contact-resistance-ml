# Sprint 4.e.2 Log: Trace High-Error Predictions Back to Literature

## 1. Objectives & Methodological Approach
- Conduct forensic examination of the 3 highest residual outliers ($|e_i| \ge 0.35\,\text{dex}$) identified in Sprint 4.e.1.
- Trace each outlier back to primary literature sources (`SRC-EXP-2014-KAPPERA`, `SRC-EXP-2018-LIU`, `SRC-EXP-2014-MCDONNELL`).
- Dissect the fabrication physics, contact geometry, measurement methods, characterization environments, and interfacial defect chemistry.
- Classify discrepancies as uncaptured physical variables vs model architectural limits.

## 2. Summary of Forensics & Case Studies

| Device / Metal | Source Paper | Obs $R_c$ | Pred $R_c$ | Error Factor | Discrepancy Classification | Physical Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`dev_7` (1T-MoS2)** | Kappera et al. (2014) | $240\,\Omega\cdot\mu\text{m}$ | $616\,\Omega\cdot\mu\text{m}$ | $2.57\times$ (Overpredicted) | Covalent 2D Homojunction Physics | Chemically induced 1T phase creates an atomically seamless 2D-2H/1T homojunction with near-unity carrier transmission, eliminating van der Waals tunneling gaps. |
| **`dev_4` (Pt)** | Liu et al. (2018) | $65.0\,\text{k}\Omega\cdot\mu\text{m}$ | $26.0\,\text{k}\Omega\cdot\mu\text{m}$ | $2.50\times$ (Underpredicted) | Non-Linear Barrier Freeze-Out | Pt possesses an extreme work function ($\Phi_m \approx 5.65\,\text{eV}$), creating a massive Schottky barrier ($\Phi_B \approx 1.38\,\text{eV}$) that triggers exponential thermionic suppression and hole transport mismatch. |
| **`dev_14` (Pd)** | McDonnell et al. (2014) | $12.0\,\text{k}\Omega\cdot\mu\text{m}$ | $5.0\,\text{k}\Omega\cdot\mu\text{m}$ | $2.40\times$ (Underpredicted) | Deposition Damage & Defect Pinning | Direct high-energy thermal evaporation of Pd onto bare MoS2 induces high-density sulfur vacancy clusters ($V_S$), pinning the Fermi level and introducing localized defect scattering centers. |

## 3. Key Scientific Conclusions
1. **Model Resilience:** The maximum error across the entire literature corpus of 13 independent groups is only $2.57\times$ ($0.41\,\text{dex}$), which is remarkably tight given inter-laboratory differences in fabrication, annealing, and ambient humidity.
2. **Actionable Enrichment Opportunities:**
   - Incorporating a binary flag `is_phase_engineered_homojunction` accounts for 1T-phase atomic continuity.
   - Including `deposition_method` (transferred vs evaporated) accounts for beam damage and vacancy generation.

## 4. Implemented Deliverables
- `src/data/literature_outlier_tracer.py`: Literature tracing engine and case study generator.
- `tests/test_literature_outlier_tracer.py`: Unit test suite testing case study construction and file persistence.
- `data/processed/literature_outlier_case_studies.json`: Structured database of outlier forensics.
- `reports/literature_outlier_investigation.md`: Formal forensic report documenting the 3 case studies.

## 5. Verification
- `python -m pytest tests/test_literature_outlier_tracer.py` passed (2/2 green).
