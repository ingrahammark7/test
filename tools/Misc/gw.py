import numpy as np

c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

N = 1e40
wavelength_m = 500e-9
R0 = 1e-12
dt = 1e-20
steps = 2000000

E0 = N * h * c / wavelength_m

g = 1e-9  # ppb anisotropy

R = R0
v = 0.0
E = E0

def schwarzschild_radius(M):
    return 2 * G * M / c**2

for i in range(steps):
    M = E / c**2
    Rs = schwarzschild_radius(M)

    a_grav = -G * M / R**2
    a_rad = (c**2 * g) / (3 * R)

    a = a_grav + a_rad

    v += a * dt
    R += v * dt

    if R <= Rs:
        print("Schwarzschild collapse at step", i)
        break

    if R <= 0:
        print("Collapse at step", i)
        break

    if i % 100000 == 0:
        print(f"Step {i}: R={R:.3e}, a={a:.3e}, Rs={Rs:.3e}")