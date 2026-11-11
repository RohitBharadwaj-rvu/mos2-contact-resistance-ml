# Sprint 1.e.4: Research Domain-Specific Feature Engineering

## Objective
Engineer domain-specific physical descriptors combining elemental material constants, semiconductor interface physics, and electrostatic gating models to represent the non-linear physics of metal-$\text{MoS}_2$ junctions.

## Engineered Physical Descriptors
1. **Schottky-Mott Barrier Mismatch ($\Phi_M - \chi_s$):**
   - Quantifies the unpinned band alignment relative to the $\text{MoS}_2$ electron affinity ($\chi_s = 4.20\,\text{eV}$).
2. **Charge Neutrality Level Distance ($\Delta E_{CNL} = \Phi_M - 4.42\,\text{eV}$):**
   - Quantifies the dipole charging driving force for metal-induced gap states (MIGS).
3. **Chemical Interfacial Reactivity ($|\chi_M - \chi_S|$ & $\Delta H_f^\circ$):**
   - Difference in Pauling electronegativity and metal-sulfide formation enthalpy, predicting sulfur vacancy creation and chemical bonding vs pristine van der Waals separation.
4. **Interface Depinning Index & Pinning Factor ($S$):**
   - Discrete index separating pristine vdW transferred and semimetallic contacts ($S \approx 0.95$) from high-energy evaporated 3D metal interfaces ($S \approx 0.15$).
5. **Gate-Modulated Degenerate Fermi Shift ($\Delta E_F$):**
   - 2D density-of-states band filling shift: $\Delta E_F = \frac{\pi \hbar^2}{2 m^*} n_{2D}$.
6. **Physics-Predicted Hybrid Barrier ($\Phi_{B,theory}$):**
   - Synthesizes pinning, Schottky-Mott, and gate modulation: $\Phi_{B} = S(\Phi_M - \chi_s) + (1-S)(E_C - E_{CNL}) - \Delta E_F$.
7. **Thermal Activation & Vacuum Scale ($k_B T$, $\log_{10} P_{vac}$):**
   - Scales thermionic emission and chamber vacuum quality.

## Deliverables
- `src/features/feature_engineer.py`: Automated enrichment pipeline calculating all 9 physical descriptors.
- `tests/test_feature_engineer.py`: Unit tests validating physical sanity and non-null guarantees.
