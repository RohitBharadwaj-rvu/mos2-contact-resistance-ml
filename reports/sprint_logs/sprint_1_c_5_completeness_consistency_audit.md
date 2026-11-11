# Sprint 1.c.5: Audit Data Completeness and Consistency

## Objective
Audit the entire literature corpus for reporting completeness across required device parameters, test physical consistency against the $\text{MoS}_2$ bandgap and sensible transport limits, and isolate uncalibrated or error-prone studies into a quarantine pool.

## Audit Rules & Protocol
1. **Mandatory Fields Verified:**
   - Electrode metal identity, contact architecture class, majority carrier injection polarity (n vs p), characterization method, measurement temperature, and at least one primary target ($R_c$ or $\Phi_B$).
2. **Physical Boundaries:**
   - Width-normalized contact resistance $R_c$: $[10, 10^7]\,\Omega\cdot\mu\text{m}$.
   - Schottky barrier height $\Phi_B$: $[0.0, 1.85]\,\text{eV}$ (constrained by monolayer $\text{MoS}_2$ fundamental bandgap $\sim 1.80\,\text{eV}$).
3. **Curation Decisions:**
   - **`ACCEPTED_PRIMARY_MODELING` (14 Sources):** Clean, high-fidelity datasets characterized via TLM, four-probe Hall bar, or multi-temperature Richardson activation.
   - **`QUARANTINED_AUXILIARY` (1 Source):** Radisavljevic 2011 (`ref_008_radisavljevic_2011`), quarantined due to uncalibrated two-probe extraction that overestimates contact resistance, preventing regression distortion.
   - **`REJECTED` (0 Sources):** No sources in current corpus had unrecoverable data entry or unphysical contradictions.

## Deliverables
- `data/processed/data_completeness_audit.json`: Complete audit registry.
- `src/data/completeness_auditor.py`: Pipeline module for data verification and cohort extraction.
- `tests/test_completeness_auditor.py`: Unit test suite.
