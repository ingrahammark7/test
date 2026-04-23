import numpy as np

# physical parameters
Phi = 2e18      # atoms / m^2 / s
ns  = 1e19      # atoms / m^2
v_etch = 4e-6   # m / s

# reaction rate per site
r = Phi / ns  # 1/s

# Damköhler length scale (correct form)
ell_star = v_etch / r

print("Damköhler length scale (m):", ell_star)
print("Damköhler length scale (nm):", ell_star * 1e9)

# Damköhler number for reference length (1 nm)
l_ref = 1e-9
Da = (r * l_ref) / v_etch

print("Damköhler number at 1 nm:", Da)