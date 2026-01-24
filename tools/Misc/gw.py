import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e40
wavelength_m = 500e-9
R0 = 1e-15

# Derived quantities
E0 = N * h * c / wavelength_m

# Anisotropy parameter
f0 = 0.55        # base inward fraction
k = 1e-20        # dimensionless coupling

# Reference acceleration (choose something physical)
a0 = 1e25       # m/s^2

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

    # Dimensionless anisotropy adjustment
    f = f0 + k * (a_grav / a0)

    # Clamp f between 0 and 1
    f = max(0.0, min(1.0, f))

    # Net pressure acceleration from anisotropy
    P_net = (2*f0 - 1) * (u/3)
    a_press = P_net / (rho * R)
    a_press/=300e3

    # Net acceleration
    a = a_grav + a_press

    # Integrate
    v += a * dt
    R += v * dt

    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}, f={f:.3f}")