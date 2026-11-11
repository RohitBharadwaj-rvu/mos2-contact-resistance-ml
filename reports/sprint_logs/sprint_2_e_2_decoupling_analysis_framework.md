# Sprint 2.e.2: Design the Decoupling Analysis Framework

## Sprint Metadata
- **Sprint ID:** Sprint-2.e.2
- **Objective:** Formulate a methodological and mathematical framework for using model explanations (SHAP and permutation values) to decouple intrinsic metal properties from extrinsic processing, defect, and electrostatic gate conditions.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Domain Taxonomy Partitioning

Features are partitioned into three mutually exclusive physical domains:
1. **Intrinsic Metal Domain ($\mathcal{D}_{\text{intrinsic}}$):**
   - Metal work function ($\Phi_M$), Pauling electronegativity ($\chi_P$), $d$-band center ($E_d$), bulk metal resistivity ($\rho_M$), metal sulfide formation enthalpy ($\Delta H_f^\circ$).
2. **Extrinsic Processing & Interfacial Architecture ($\mathcal{D}_{\text{extrinsic}}$):**
   - Deposition technique (e-beam vs thermal vs transfer), contact architecture (top vs edge vs transferred vdW), vacuum base pressure ($P_{vac}$), post-annealing temperature ($T_{anneal}$), gas ambient, pinning suppression flag.
3. **Electrostatic & Operational State ($\mathcal{D}_{\text{electrostatic}}$):**
   - Gate carrier density ($n_{2D}$), dielectric permittivity ($\kappa$), measurement temperature ($T_{meas}$).

---

## 2. Mathematical Decoupling Formulation

Using local Shapley attributions, the log-contact resistance deviation for any device $x$ decomposes as:
$$\Delta \log_{10}(R_c)(x) = \Phi_{\text{intrinsic}}(x) + \Phi_{\text{extrinsic}}(x) + \Phi_{\text{electrostatic}}(x)$$
Where each domain attribution is the direct sum of its constituent feature Shapley values:
$$\Phi_{\text{domain}}(x) = \sum_{j \in \mathcal{D}_{\text{domain}}} \phi_j(x)$$
The normalized global attribution share is calculated as:
$$W_{\text{domain}} = \frac{\sum_{i=1}^N \sum_{j \in \mathcal{D}_{\text{domain}}} |\phi_{i,j}|}{\sum_{i=1}^N \sum_{j=1}^M |\phi_{i,j}|} \times 100\%$$

---

## 3. Actionable Experimental Answers Enabled
1. **Metal Selection vs Fab Optimization:** Directly quantifies what percentage of contact resistance variance is determined when buying the target metal versus how much can be engineered in the cleanroom.
2. **Maximum Achievable Fab Improvement:** For a given metal (e.g., standard Ti), computes the bounding interval $[\min(\Phi_{\text{extrinsic}}), \max(\Phi_{\text{extrinsic}})]$ to reveal the ceiling of annealing and ultra-high vacuum optimization.
3. **Electrostatic Gate Saturation:** Maps the 2D inflection point where electrostatic gating yields diminishing returns compared to lowering the interfacial barrier height.

---

## 4. Deliverables Produced
- `src/models/decoupling_framework.py`: Implementation of domain partitioning, mathematical specification, and attribution share aggregator.
- `tests/test_decoupling_framework.py`: Verification tests for partition exclusivity, schema serialization, and share normalization.
- `data/reference/decoupling_framework_spec.json`: Machine-readable specification governing Section 5 execution.
