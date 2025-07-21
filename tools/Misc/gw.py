import numpy as np
import math

# Physical Constants
c = 3e8  # Speed of light, m/s
h = 6.626e-34  # Planck's constant, J*s
G = 6.67430e-11  # Gravitational constant, m^3/kg/s^2
proton_mass = 1.67e-27  # kg
planck_length = 1.616e-35  # m
atomic_radius = 1e-10  # m
seconds_per_year = 3.1536e7  # s

# Energy Unit (arbitrary scaling)
pc = 6e-34  # J (you defined this)

# Scaled particle count
par = 1e10
scaled_radius = atomic_radius * (par ** (1/3))  # Assuming 3D packing
volume = (4/3) * np.pi * atomic_radius**3

# Proton rest energy
E_proton = proton_mass * c**2  # ~1.5e-10 J

# Number of Planck photons extractable from one proton, scaled
N = (E_proton / pc) * par

# Total power for all these photons over a year
total_energy = N * pc
crossings_per_year = (c / scaled_radius) * seconds_per_year  # photon crossings in confined radius
freq_factor = crossings_per_year ** (1/3)

# Estimate of minimum approach (inverse square root scaling)
d_min = atomic_radius / math.sqrt(N * crossings_per_year)

# Outputs
print(f"Scaled equivalent mass: {proton_mass * par:.3e} kg")
print(f"Total photon energy: {total_energy:.3e} J")
print(f"Planck photon count (scaled): {N:.3e}")
print(f"Minimum distance from confinement: {d_min:.3e} m")