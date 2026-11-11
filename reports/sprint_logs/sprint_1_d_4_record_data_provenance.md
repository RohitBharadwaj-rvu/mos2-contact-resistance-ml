# Sprint 1.d.4: Record Data Provenance and Context

## Objective
Establish an immutable audit trail and cryptographic provenance tracking ledger for every extracted data point, documenting primary publication source UIDs, exact figure/table citations, experimental caveats, and verification status.

## Provenance Ledger Architecture
1. **Cryptographic Integrity:**
   - Every data point (`DP-001` through `DP-020`) generates a deterministic SHA-256 verification hash spanning row identifiers, metal type, targets ($R_c, \Phi_B$), and provenance citations.
2. **Recorded Attributes:**
   - Source UID (`SRC-EXP-2021-SHEN`, `SRC-EXP-2018-LIU`, etc.)
   - Canonical Article Title, Journal Venue, Year, DOI
   - Exact Provenance Location within primary publication (e.g. `Figure 2c and Table 1`, `Figure 3b`, `Figure 4 and Table II`)
   - Complete fabrication recipe context: deposition vacuum pressure, annealing ambient gas, dielectric stack, and carrier density.
   - Audit Status: `Verified_Against_Primary_Source`.

## Deliverables
- `data/processed/data_provenance_ledger.json` & `.csv`: Auditable master provenance ledger.
- `src/data/provenance_tracker.py`: Ledger generation, hashing, and lookup module.
- `tests/test_provenance_tracker.py`: Test suite validating hash determinism and lookup accuracy.
