# Sprint 1.e.5: Evaluate Target Variable Transformations

## Objective
Analyze the statistical distributions, ranges, skewness, and physical scaling of the primary target variables ($R_c$ and $\Phi_B$), and establish invertible mathematical transformations for regression modeling.

## Target Distribution Findings
1. **Contact Resistance ($R_c$ in $\Omega\cdot\mu\text{m}$):**
   - Empirical range: $123\,\Omega\cdot\mu\text{m}$ to $65,000\,\Omega\cdot\mu\text{m}$ (spanning nearly 3 orders of magnitude).
   - Skewness analysis: Raw $R_c$ exhibits high positive skewness ($> 2.5$), typical of thermally activated barrier transport $R_c \sim \exp(q\Phi_B / k_B T)$.
   - Log transformation: Applying $y = \log_{10}(R_c)$ drastically normalizes the distribution, collapsing skewness to $\approx 0.44$, eliminating outlier distortion, and aligning regression MSE with relative fractional error.
2. **Schottky Barrier Height ($\Phi_B$ in $\text{eV}$):**
   - Empirical range: $0.0\,\text{eV}$ to $1.45\,\text{eV}$.
   - Well-behaved bounded distribution within the $\text{MoS}_2$ bandgap ($1.8\,\text{eV}$), appropriate for linear regression without logarithmic distortion.

## Deliverables
- `src/features/target_transformer.py`: Target distribution analyzer and exact bidirectional transformation utilities (`log10` and `ln`).
- `tests/test_target_transformer.py`: Test suite validating skewness reduction and mathematical invertibility.
