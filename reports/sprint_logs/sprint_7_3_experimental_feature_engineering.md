# Sprint 7.3 Log: Un-Biased Experimental Feature Space & Dual-Task Formulation

## 1. Sprint Objective
Address critical Audit Concern B:
- Rebuild the prediction task using the full suite of actual physical and experimental inputs: metal work function $W_M$, deposition method, annealing temperature/ambient/duration, $\text{MoS}_2$ layer count and physical thickness, gate dielectric material and equivalent oxide thickness (EOT), and measurement temperature.
- Completely eliminate the circular assumption in previous feature engineering where a fixed pinning factor ($S = 0.95$ for vdW, $S = 0.15$ for conventional) was baked into the input feature `physics_predicted_sbh_ev`.
- Establish two distinct, scientifically defensible prediction tasks:
  1. **Task 1 (Primary Contact Resistance Prediction):** Predict $R_c$ directly from raw experimental and materials levers without using pre-calculated or measured barrier heights as inputs.
  2. **Task 2 (Schottky Barrier Height Prediction):** Predict measured $\Phi_B$ from metal work function, formation enthalpy, and deposition architecture.

---

## 2. Technical Architecture & Input Feature Sets

### 2.1. Task 1: Primary Contact Resistance ($R_c$) Prediction Feature Set
Contains 14 un-biased physical and experimental parameters:
1. `work_function_ev`: Clean vacuum metal work function ($3.50\,\text{eV}$ for Sc to $5.65\,\text{eV}$ for Pt).
2. `pauling_electronegativity`: Pauling scale electronegativity of contact element.
3. `sulfide_formation_enthalpy_kj_mol`: Metal sulfide compound standard Gibbs formation enthalpy (chemical reactivity proxy).
4. `metal_resistivity_ohm_cm`: Bulk electrical resistivity of contact pad.
5. `is_vdw_or_depinned_contact`: Binary indicator ($1$ for vdW transferred or metallic phase homojunction, $0$ for evaporated/sputtered).
6. `log_vacuum_pressure`: Base chamber vacuum level during deposition ($\log_{10}(\text{Torr})$).
7. `is_annealed`: Binary indicator of post-deposition thermal treatment.
8. `post_annealing_temperature_c`: Post-deposition annealing temperature ($20^\circ\text{C}$ if unannealed, up to $300^\circ\text{C}$).
9. `thermal_budget_k_min`: Integrated thermal budget ($T_K \times t_{\text{min}}$).
10. `layer_count`: Atomic layer count ($1$ to $5$).
11. `thickness_nm`: Channel thickness ($0.65\,\text{nm}$ for monolayer to $3.3\,\text{nm}$).
12. `n2d_norm_1e13`: Gate-accumulated carrier density ($n_{2D} / 10^{13}\,\text{cm}^{-2}$).
13. `log10_eot_nm`: Base-10 logarithm of Equivalent Oxide Thickness ($\text{EOT} = t_{ox} \cdot \frac{3.9}{\kappa_{ox}}$).
14. `measurement_temperature_k`: Ambient temperature during electrical characterization ($4.2\,\text{K}$ to $300\,\text{K}$).

### 2.2. Task 2: Schottky Barrier Height ($\Phi_B$) Prediction Feature Set
Contains 8 interface and materials descriptors to predict measured $\Phi_B$:
1. `work_function_ev`: Metal work function.
2. `work_function_offset_cbm_ev`: Offset from ideal $\text{MoS}_2$ conduction band minimum ($W_M - 4.20\,\text{eV}$).
3. `pauling_electronegativity`: Pauling electronegativity.
4. `sulfide_formation_enthalpy_kj_mol`: Interfacial chemical reactivity.
5. `is_vdw_or_depinned_contact`: Deposition architecture (de-pinned vs pinned).
6. `log_vacuum_pressure`: Chamber vacuum.
7. `is_annealed`: Annealing flag.
8. `post_annealing_temperature_c`: Annealing temperature.

---

## 3. Key Deliverables
- `src/features/experimental_feature_engineer.py`: Feature engineering pipeline and task-specific selector.
- `tests/test_experimental_feature_engineer.py`: Unit test suite verifying feature integrity and absence of circular assumptions.
- `data/processed/master_experimental_features_dataset.csv`: Processed dataset (28 rows, 61 columns).

---

## 4. Verification & Status
- Unit tests: 100% passing.
- Circular assumptions removed.
- Completed Sprint 7.3.
