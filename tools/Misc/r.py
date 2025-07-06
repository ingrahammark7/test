from sympy import symbols, log, sqrt, exp, simplify, pprint, N

# Declare symbols
en, ev, hvla, hvlamec, depth, ml_min = symbols('en ev hvla hvlamec depth ml_min', positive=True)

# Constants
log2 = log(2)
log2_sq = log2**2

# ml_eff as function of depth
ml_eff = (depth**2) / (hvla**2 * hvlamec * log2**2)

# Main expression
numerator = en * ev
denominator = log(ml_eff / ml_min)
attenuation = exp(-log2_sq * sqrt(hvlamec))

delivered_energy = numerator / denominator * attenuation

# Print the symbolic form
print("Symbolic closed-form expression for delivered energy:")
pprint(simplify(delivered_energy))

# Optional: plug in concrete values to evaluate
subs_vals = {
    en: 10**50,
    ev: 1e-19,
    hvla: 1.0,
    hvlamec: 0.5e6,
    depth: 1e308,
    ml_min: 1e6,
}

# Evaluate numerically in log10 scale to avoid overflow
log10_delivered = log(delivered_energy, 10).subs(subs_vals)
print("\nApproximate delivered energy in log10 scale:")
pprint(N(log10_delivered, 20))  # Increase precision for extreme values