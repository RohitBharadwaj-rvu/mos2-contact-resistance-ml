# Sprint 1.c.1: Research Valid Characterization Standards

## Objective
Establish a rigorous physical foundation for evaluating experimental metrology used to extract contact resistance ($R_c$) and Schottky barrier height ($\Phi_B$) on $\text{MoS}_2$ FETs, differentiating gold-standard methods from error-prone techniques.

## Metrological Analysis
1. **Contact Resistance Metrology:**
   - **Transmission Line Method (TLM) [Gold Standard, Score 10/10]:** Measures multiple channel lengths to cleanly decouple $R_{channel}$ from contact resistance $2 R_c$. Typical experimental uncertainty $\sim 10\%$.
   - **Four-Probe / Multi-Terminal Hall Bar [High, Score 8.5/10]:** Directly probes channel potential drop without contact current distortion.
   - **Two-Probe Extraction [Error-Prone, Score 3.0/10]:** Cannot separate channel sheet resistance from contact resistance. Conflates mobility variations with contact quality.
2. **Schottky Barrier Height Metrology:**
   - **Modified 2D Richardson Temperature Activation [Gold Standard, Score 10/10]:** Evaluates Arrhenius activation across temperature ($77\text{ K} - 350\text{ K}$) using 2D density-of-states thermionic scaling ($I_{2D} \propto T^{3/2}$) and flat-band voltage extrapolation. Uncertainty $\le 0.03\,\text{eV}$.
   - **Single Room-Temperature I-V Diode Fitting [Error-Prone, Score 3.5/10]:** Fails in 2D FETs due to large ideality factors ($n \gg 2$) caused by gate-induced tunneling.

## Deliverables
- `data/reference/characterization_standards.json`: Complete metrology classification and error bounds.
- `src/data/characterization_standards.py`: Python module for reliability scoring and 2D thermionic current calculations.
- `tests/test_characterization_standards.py`: Test suite validating metrology ratings and equations.
