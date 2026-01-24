import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e20
wavelength_m = 500e-9
R0 = 1e-10

# Derived quantities
E = N * h * c / wavelength_m
M = E / c**2

# Anisotropy parameter (negative means inward pressure)
alpha = -0.9

# Integration settings
dt = 1e-20
steps = 200

R = R0
v = 0.0

for i in range(steps):
    # Energy density and mass density
    V = (4/3) * np.pi * R**3
    u = E / V
    rho = u / c**2

    # Gravity acceleration
    a_grav = -G * M / R**2

    # Effective pressure acceleration (anisotropic)
    a_press = alpha * (u / 3) / (rho * R)

    a = a_grav + a_press

    v += a * dt
    R += v * dt

    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}")