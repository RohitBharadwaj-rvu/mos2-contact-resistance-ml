# Sprint 1.a.3: Locate Pre-Existing Benchmark Compilations

## Objective
Identify, evaluate, and systematically catalog recent landmark review articles, meta-analyses, and high-impact experimental studies on 2D transistor contacts that contain aggregated benchmark tables of $R_c$ and $\Phi_B$.

## Key Landmark Sources Identified
1. **Allain et al. (Nature Materials 2015, DOI: 10.1038/nmat4452):**
   - Pioneer meta-analysis quantifying Fermi-level pinning ($S \approx 0.1$) on $\text{MoS}_2$ and $\text{WSe}_2$ across Ti, Mo, Ni, Au, Pt, and Sc.
2. **Shen et al. (Nature 2021, DOI: 10.1038/s41586-021-03472-9):**
   - Semimetal Bi (0001) contact breakthrough ($R_c \approx 123\,\Omega\cdot\mu\text{m}$, zero Schottky barrier), containing a comprehensive literature comparison table of state-of-the-art contact resistances.
3. **Liu et al. (Nature 2018, DOI: 10.1038/s41586-018-0129-8):**
   - Mechanically transferred van der Waals contacts demonstrating restoration of the Schottky-Mott limit ($S \approx 0.96$) across Ag, In, Cu, Au, Pt, and Ti.
4. **Schulman et al. (Chem. Soc. Rev. 2018, DOI: 10.1039/C7CS00828A):**
   - Comprehensive review analyzing phase-engineering (1T metallic phase), 1D edge contacts, chemical doping, and high-$k$ dielectric screening.
5. **Kappera et al. (Nature Materials 2014, DOI: 10.1038/nmat4080):**
   - Phase-engineered $1\text{T}\text{-}\text{MoS}_2$ contacts achieving $R_c \approx 200–300\,\Omega\cdot\mu\text{m}$.
6. **English et al. (IEDM 2016, DOI: 10.1109/IEDM.2016.7838355):**
   - Ultra-high vacuum TLM measurements across carrier densities and temperatures.

## Deliverables
- `data/reference/benchmark_compilations.json`: Master index of landmark reviews and experimental benchmark compilations comprising >190 aggregated literature measurements.
- `src/data/benchmark_sources.py`: Python module for benchmark querying, metal coverage analysis, and data extraction auditing.
- `tests/test_benchmark_sources.py`: Test suite validating benchmark sources registry integrity.
