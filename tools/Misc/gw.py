import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34
m_e = 9.10938356e-31

# Parameters
N = 1e45               # initial photon count
wavelength = 500e-9     # photon wavelength (m)
R0 = 1e-12              # initial radius (m)

# Anisotropy parameter
g = 1e-9                # <1/3 means inward bias

# Pair production threshold
pair_threshold = 2 * m_e * c**2   # energy needed for e+e-

# Integration
dt = 1e-22
steps = 200000

# Thermal noise (0 to remove)
thermal_noise = 0.0

# Initial conditions
R = R0
v = 0.0

def photon_energy(lam):
    return h * c / lam

def schwarzschild_radius(M):
    return 2 * G * M / c**2

def gr_factor(R, M):
    # approximate GR correction factor
    # stronger gravity as you approach Rs
    Rs = schwarzschild_radius(M)
    return 1.0 / (1.0 - Rs / R + 1e-30)

for i in range(steps):
    # Photon energy
    E_ph = photon_energy(wavelength)

    # Total energy
    E_total = N * E_ph

    # Convert to mass
    M = E_total / c**2

    # GR correction factor
    gr = gr_factor(R, M)

    # Gravity acceleration (with GR boost)
    a_grav = -G * M / (R**2) * gr

    # Radiation pressure acceleration (anisotropy)
    a_rad = (c**2 * g) / (3 * R)

    # Thermal noise (outward)
    a_noise = thermal_noise / R

    # Net acceleration
    a = a_grav + a_rad + a_noise

    # Integrate
    v += a * dt
    R += v * dt

    # Pair production (simple model)
    # If photon energy exceeds threshold, convert fraction to mass
    if E_ph >= pair_threshold:
        # convert 1% per step
        N *= 0.99

    # Collapse checks
    Rs = schwarzschild_radius(M)
    if R <= Rs:
        print("BLACK HOLE COLLAPSE at step", i, "time", i*dt, "s")
        print("R =", R, "Rs =", Rs)
        break

    if R <= 0:
        print("RADIUS COLLAPSE at step", i, "time", i*dt, "s")
        break

    if i % 20000 == 0:
        print("Step", i, "R=", R, "v=", v, "a=", a, "Rs=", Rs)

print("Simulation finished.")