# constants
c = 299792458.0
G = 6.67430e-11

# inputs
n = 1e30
E_gamma = 1e-19     # J
R = 1e-12           # m

# total energy and mass
E = n * E_gamma
M = E / c**2

# dynamical (causal) collapse time
t_collapse = R / c

# optional: curvature timescale (same order)
t_gr = (R**3 / (G * M))**0.5

print("Total energy (J):", E)
print("Equivalent mass (kg):", M)
print("Light-crossing time (s):", t_collapse)
print("Gravitational timescale (s):", t_gr)