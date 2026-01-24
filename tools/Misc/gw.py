import numpy as np
import math

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Parameters
N = 1e30
wavelength_m = 500e-9
R0 = 1e-12

E0 = N * h * c / wavelength_m

# Initial anisotropy (inward)
f = 0.49        # <0.5 inward

# Anisotropy decay time (seconds)
tau = 1e-18     # try different values

# Energy leakage per step
leak_rate = 1e-4

# Integration settings
dt = 1e-20
steps = 200

R = R0
v = 0.0
E = E0

for i in range(steps):
    # Energy leakage
    E *= (1 - leak_rate)

    # Mass equivalent
    M = E / c**2

    # Energy density
    u = E / ((4/3) * math.pi * R**3)
    rho = u / c**2

    # Gravity
    a_grav = -G * M / R**2

    # Update anisotropy with decay
    f = 0.5 + (f - 0.5) * math.exp(-dt/tau)

    # Pressure
    P_net = (2*f - 1) * (u/3)
    P_net = max(-u/3, min(u/3, P_net))
    a_press = P_net / (rho * R)

    # Net acceleration
    a = a_grav + a_press

    # Integrate
    v += a * dt
    R += v * dt

    if R <= 0:
        print(f"Collapse at step {i}, time {i*dt:.3e} s, f={f:.6f}")
        break

    if i % 20 == 0:
        print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}, f={f:.6f}")