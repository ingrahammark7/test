import math

# -----------------------------
# Constants
# -----------------------------
c = 3e8                     # speed of light (m/s)
h = 6.626e-34               # Planck constant (J*s)

# Planck units
l_p = 1.616e-35             # Planck length (m)
E_p = 1.96e9                # Planck energy (J)

# -----------------------------
# Inputs
# -----------------------------
P_in = 1e11                 # 100 GW input power (W)
L = 1e4                     # cavity length (m) = 10 km
w = 0.01                    # beam waist (m) = 1 cm
reflectivity = 0.999        # 99.9% reflective
wavelength = 1e-6           # 1 micron laser

# Material limit (stored energy cap)
E_max = 1e6                 # 1 MJ cap (changeable)

# Duration of the run (seconds)
t_run = 0.001               # 1 millisecond (changeable)

# -----------------------------
# Derived quantities
# -----------------------------
E_photon = h * c / wavelength

# Gravitational cross-section estimate
sigma_grav = l_p**2 * (E_photon / E_p)**4

# Mode volume of cavity
V_mode = math.pi * w**2 * L

# mean free path in cavity (approx)
mfp = 4 * L / 3
bounce_time = mfp / c
tau = bounce_time / (1 - reflectivity)

# stored energy without cap
E_stored_raw = P_in * tau

# Apply hard cap
E_stored = min(E_stored_raw, E_max)

# photon count
N_photons = E_stored / E_photon

# photon density
n = N_photons / V_mode

# collision rate (events per second)
collision_rate = n**2 * sigma_grav * c * V_mode

# expected collisions during the run
expected_collisions = collision_rate * t_run

# time between collisions (if continuous)
time_between_collisions = 1 / collision_rate if collision_rate > 0 else float('inf')

print("Photon energy (J):", E_photon)
print("Gravitational cross-section (m^2):", sigma_grav)
print("Mode volume (m^3):", V_mode)
print("Capped stored energy (J):", E_stored)
print("Photon density (1/m^3):", n)
print("Collision rate (events/s):", collision_rate)
print("Expected collisions in run (t_run):", expected_collisions)
print("Time between collisions (s):", time_between_collisions)
print("Time between collisions (years):", time_between_collisions / (3600*24*365))