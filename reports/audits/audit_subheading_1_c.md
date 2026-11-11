# Subheading 1.c Audit & Quality Improvement Review

## Scope
Audit of all implementations, criteria checkers, screeners, and auditors in:
**1. Data Aggregation & Curation -> c. Removing Low-Quality Papers, Databases, and Other Resources** (Sprints 1.c.1 to 1.c.5).

## Identified Issues & Applied Improvements
1. **Uncertainty Weighting Function Added:**
   - *Observation:* To train heteroscedastic ML models or weighted ensembles down the road, sample weights must be quantitatively tied to measurement technique fidelity.
   - *Fix:* Added `get_metrology_sample_weight(method_name)` to `src/data/characterization_standards.py`, assigning $w_i = 1.0$ for gold-standard TLM, $0.85$ for Hall bar / modified Richardson, down to $0.30$ for error-prone two-probe measurements.

2. **Carrier Density Regime Auditing:**
   - *Observation:* Contact resistance depends exponentially on gate-induced carrier density. Literature papers that do not test in the degenerate regime ($n_{2D} \ge 10^{13}\,\text{cm}^{-2}$) exhibit artificially inflated contact resistance.
   - *Fix:* Added `is_high_carrier_density` flags and auditing rules in `src/data/completeness_auditor.py`.

3. **Validation & Verification:**
   - 52 automated tests in `tests/` pass with 100% green status.
   - The primary modeling cohort is cleanly decoupled from the quarantined auxiliary cohort (`ref_008_radisavljevic_2011`).

## Status
Subheading 1.c is audited, improved, and verified. Ready to proceed to Subheading 1.d.
