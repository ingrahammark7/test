import numpy as np
import math

# Constants
c = 3e8                     # speed of light (m/s)
h = 6.626e-34               # Planck constant (J*s)
eV = 1.602e-19              # J per eV

# Input parameters
P = 1e11                    # 100 GW
L = 1e4                     # 10 km radius
wavelength = 1e-6           # 1 micron laser (typical)
sigma = 1e-68               # photon-photon scattering cross-section (m^2)

# Photon energy
E_photon = h * c / wavelength

# photons per second
photon_rate = P / E_photon

# cavity volume (sphere)
V = (4/3) * math.pi * L**3

# photon density (photons per m^3)
# We assume steady-state energy density: photons occupy the cavity volume
photon_density = (photon_rate / c) / V

# photon-photon collision rate per volume
collision_rate_density = photon_density**2 * sigma * c

# total collision rate in the cavity
collision_rate_total = collision_rate_density * V

# time between collisions
if collision_rate_total > 0:
    time_between_collisions = 1 / collision_rate_total
else:
    time_between_collisions = float('inf')

print("Photon energy (J):", E_photon)
print("Photon rate (1/s):", photon_rate)
print("Cavity volume (m^3):", V)
print("Photon density (1/m^3):", photon_density)
print("Collision rate (events/s):", collision_rate_total)
print("Time between collisions (s):", time_between_collisions)
print("Time between collisions (years):", time_between_collisions / (3600*24*365))