import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e29
wavelength_m = 500e-9
R0 = 1e-12

# Derived quantities
E0 = N * h * c / wavelength_m
M0 = E0 / c**2

# Anisotropy parameter
f = 0.55        # fraction of photons moving inward (0.5 = isotropic)
f1=f

# Reflectivity / leakage
leak_rate = 0.0  # 0 = perfect reflection, 0.01 = 1% energy lost per step

# Integration settings
dt = 1e-20
steps = 200

R = R0
v = 0.0
E = E0

for i in range(steps):
    # Update energy (leakage)
    E *= (1 - leak_rate)

    # Update mass
    M = E / c**2

    # Energy density
    u = E / ((4/3) * np.pi * R**3)
    rho = u / c**2

    # Gravity
    a_grav = -G * M / R**2
    f=f1+(a_grav/c)

    # Net pressure acceleration from anisotropy
    P_net = (2*f - 1) * (u/3)
    a_press = P_net / (rho * R)

    # Net acceleration
    a = a_grav + a_press

    # Integrate
    v += a * dt
    R += v * dt

    # Stop if collapse
    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}")