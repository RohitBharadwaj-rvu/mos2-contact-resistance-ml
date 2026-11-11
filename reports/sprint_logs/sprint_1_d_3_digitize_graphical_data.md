# Sprint 1.d.3: Identify and Digitize Graphical Data

## Objective
Implement a mathematical coordinate transformation and calibration engine to digitize graphical data curves from landmark literature plots where underlying numerical tabular data was omitted.

## Digitized Experimental Curves
1. **English et al. (IEDM 2016, Fig. 4):**
   - $R_c$ vs carrier concentration $n_{2D}$ ($2\times 10^{12}$ to $1.5\times 10^{13}\,\text{cm}^{-2}$) for UHV Ti/Au and Au-only contacts, tracking exponential reduction in contact resistance as Fermi level approaches degenerate band-filling.
2. **Allain et al. (Nature Materials 2015, Fig. 3):**
   - Schottky barrier height $\Phi_B$ vs metal work function $\Phi_M$ across Sc, Ti, Mo, Au, Ni, Pt, from which we quantitatively extract the Fermi-level pinning factor slope $S = d\Phi_B / d\Phi_M \approx 0.22$.

## Calibration Engine & Uncertainty Propagation
- Developed `transform_pixel_to_physical()` supporting both linear and logarithmic axes with pixel inversion.
- Attached extraction uncertainty ($\pm 3-5\%$) per digitized point.

## Deliverables
- `data/raw/digitized_graphical_points.json`: Digitized points with experimental metadata.
- `src/data/graphical_digitizer.py`: Calibration engine and pinning factor calculator.
- `tests/test_graphical_digitizer.py`: Unit tests validating coordinate mapping and pinning regressions.
