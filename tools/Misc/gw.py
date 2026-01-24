import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e30               # photon count
wavelength_m = 500e-9  # photon wavelength
R0 = 1e-12             # initial radius (m)
f = 0.45               # anisotropy (0.5 isotropic)

dt = 1e-20
steps = 200

# Derived quantities
E0 = N * h * c / wavelength_m

# Initial conditions
R = R0
v = 0.0
E = E0

def schwarzschild_radius(M):
    return 2 * G * M / c**2

for i in range(steps):
    # Total mass-energy
    M = E / c**2

    # Schwarzschild radius
    Rs = schwarzschild_radius(M)

    # Energy density
    u = E / ((4/3) * np.pi * R**3)
    rho = u / c**2

    # Gravity acceleration
    a_grav = -G * M / R**2

    # Radiation pressure (anisotropic)
    P_rad = (2 * f - 1) * (u / 3)

    # Pressure acceleration
    a_press = 3 * P_rad / (rho * R)

    # Net acceleration
    a = a_grav + a_press

    # Integrate motion
    v += a * dt
    R += v * dt

    # Collapse checks
    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s")
        break

    if R <= Rs:
        print(f"Schwarzschild collapse at step {i}, time {i*dt:.3e} s, R={R:.3e}, Rs={Rs:.3e}")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}, Rs={Rs:.3e}")