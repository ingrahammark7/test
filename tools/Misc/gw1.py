import math

# -----------------------------
# Constants
# -----------------------------
c = 3e8                     # speed of light (m/s)
h = 6.626e-34               # Planck constant (J*s)
sigma = 1e-68               # photon-photon cross-section (m^2)

# -----------------------------
# Inputs
# -----------------------------
P_in = 1e11                 # 100 GW input power (W)
R = 1e4                     # cavity length (m) = 10 km
w = 0.01                    # beam waist (m) = 1 cm
reflectivity = 0.999        # 99.9% reflective

wavelength = 1e-6           # 1 micron laser
I_max = 1e14                # max intensity before damage (W/m^2)

# -----------------------------
# Derived quantities
# -----------------------------
E_photon = h * c / wavelength

# Mode volume of cavity
V_mode = math.pi * w**2 * R

# intensity of beam
I_beam = P_in / (math.pi * w**2)

# If intensity exceeds damage threshold, cap stored energy
if I_beam > I_max:
    print("WARNING: Intensity exceeds damage threshold.")
    P_effective = I_max * math.pi * w**2
else:
    P_effective = P_in

# mean free path in cavity (approx)
mfp = 4 * R / 3
bounce_time = mfp / c
tau = bounce_time / (1 - reflectivity)

# stored energy (limited by intensity)
E_stored = P_effective * tau

# photon count
N_photons = E_stored / E_photon

# photon density
n = N_photons / V_mode

# collision rate
collision_rate = n**2 * sigma * c * V_mode

# time between collisions
time_between_collisions = 1 / collision_rate if collision_rate > 0 else float('inf')

print("Mode volume (m^3):", V_mode)
print("Beam intensity (W/m^2):", I_beam)
print("Effective power (W):", P_effective)
print("Stored energy (J):", E_stored)
print("Photon count:", N_photons)
print("Photon density (1/m^3):", n)
print("Collision rate (events/s):", collision_rate)
print("Time between collisions (s):", time_between_collisions)
print("Time between collisions (years):", time_between_collisions / (3600*24*365))