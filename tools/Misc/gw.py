# Constants
c = 299792458.0          # speed of light (m/s)
G = 6.67430e-11          # gravitational constant (m^3 kg^-1 s^-2)

# Inputs
n = 1e60                # number of photons
E_gamma = 1e-19         # energy per photon (J)
r = 1e-12               # radius of confinement (m)

# Total energy and mass
E_total = n * E_gamma
M = E_total / c**2

# Schwarzschild radius
r_s = 2 * G * M / c**2

# Energy density
volume = (4/3) * 3.141592653589793 * r**3
rho_E = E_total / volume

# Light-crossing time
t_light = r / c

# Output
print("Total energy (J):", E_total)
print("Equivalent mass (kg):", M)
print("Schwarzschild radius (m):", r_s)
print("System radius (m):", r)
print("Energy density (J/m^3):", rho_E)
print("Light-crossing time (s):", t_light)

if r <= r_s:
    print(">>> Collapse inevitable: trapped surface forms")
else:
    print(">>> No horizon yet (but increasing density strengthens gravity)")