import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e30
wavelength_m = 500e-9
R0 = 1e-12

# Derived quantities
E0 = N * h * c / wavelength_m

# Anisotropy parameter (inward)
f = 0.45        # <0.5 = inward momentum

# Integration settings
dt = 1e-20
steps = 200

R = R0
v = 0.0
E = E0

for i in range(steps):
    # Energy stays constant
    M = E / c**2

    # Energy density
    u = E / ((4/3) * np.pi * R**3)
    rho = u / c**2

    # Gravity
    a_grav = -G * M / R**2

    # Net pressure acceleration from inward anisotropy
    P_net = (2*f - 1) * (u/3)
    a_press = P_net / (rho * R)

    # Net acceleration
    a = a_grav + a_press

    # Integrate
    v += a * dt
    R += v * dt

    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}")