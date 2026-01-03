import math

# ----------------------------
# Parameters (dimensionless)
# ----------------------------
k1 = 0.02   # chlorate pathway rate constant
k2 = 0.50   # oxygen-loss pathway (dominant)

m = 2       # reaction order (chlorate)
n = 1       # reaction order (oxygen)

OCl = 1.0   # initial hypochlorite (normalized)
ClO3 = 0.0  # chlorate formed

dt = 0.001  # time step
t_max = 50  # total integration time

# ----------------------------
# Time integration (Euler)
# ----------------------------
t = 0.0
while t < t_max and OCl > 1e-6:
    r1 = k1 * OCl**m
    r2 = k2 * OCl**n

    dOCl = -(r1 + r2) * dt
    dClO3 = (r1 / 3) * dt  # stoichiometry

    OCl += dOCl
    ClO3 += dClO3
    t += dt

# ----------------------------
# Yield math
# ----------------------------
theoretical_max = 1.0 / 3.0
yield_fraction = ClO3 / theoretical_max

# ----------------------------
# Output
# ----------------------------
print("=== Chlorate Yield (Heating Model) ===")
print(f"Time elapsed:           {t:.2f}")
print(f"Hypochlorite remaining: {OCl:.6f}")
print(f"Chlorate formed:        {ClO3:.6f}")
print(f"Theoretical max:        {theoretical_max:.6f}")
print(f"Fractional yield:       {yield_fraction:.2%}") 