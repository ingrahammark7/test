import numpy as np
import math

# -----------------------------
# Constants
# -----------------------------
c = 3e8                     # speed of light (m/s)
h = 6.626e-34               # Planck constant (J*s)

# -----------------------------
# Inputs
# -----------------------------
P_in = 1e11                 # 100 GW input power (W)
R = 1e4                     # radius of cavity (m) = 10 km
wavelength = 1e-6           # 1 micron laser
reflectivity = 0.999        # 99.9% reflective walls

# QED photon-photon cross section at optical energies
sigma = 1e-68               # m^2

# -----------------------------
# Derived quantities
# -----------------------------
E_photon = h * c / wavelength

# Mean free path in sphere ~ 4R/3
mfp = 4 * R / 3

# time between bounces
bounce_time = mfp / c

# photon lifetime (tau)
tau = bounce_time / (1 - reflectivity)

# stored energy
E_stored = P_in * tau

# number of photons stored
N_photons = E_stored / E_photon

# volume of sphere
V = (4/3) * math.pi * R**3

# photon density
n = N_photons / V

# collision rate
collision_rate = n**2 * sigma * c * V

# time between collisions
time_between_collisions = 1 / collision_rate if collision_rate > 0 else float('inf')

print("Photon energy (J):", E_photon)
print("Stored energy (J):", E_stored)
print("Photon count:", N_photons)
print("Photon density (1/m^3):", n)
print("Collision rate (events/s):", collision_rate)
print("Time between collisions (s):", time_between_collisions)
print("Time between collisions (years):", time_between_collisions / (3600*24*365))