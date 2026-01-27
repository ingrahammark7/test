import numpy as np, math

# Constants
c = 3e8
h = 6.626e-34
wavelength = 1e-6  # 1 micron
sigma = 1e-68      # photon-photon cross section (m^2)

# Inputs
P_in = 1e11        # 100 GW input
R = 0.999          # reflectivity
L = 1e4            # 10 km radius

# Photon energy
E_ph = h * c / wavelength

# Photon lifetime in cavity (approx)
# mean free path in sphere = 4R/3
mfp = 4*L/3
bounce_time = mfp / c
tau = bounce_time / (1 - R)

# Stored energy
E_stored = P_in * tau

# Number of photons stored
N_photons = E_stored / E_ph

# cavity volume
V = (4/3) * math.pi * L**3

# photon density
n = N_photons / V

# collision rate
collision_rate = n**2 * sigma * c * V

print("Photon lifetime (s):", tau)
print("Stored energy (J):", E_stored)
print("Photon density (1/m^3):", n)
print("Collision rate (events/s):", collision_rate)