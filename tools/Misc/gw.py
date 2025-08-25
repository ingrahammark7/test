import math

# Constants
c = 3e8          # speed of light
G = 6.7e-11      # gravitational constant
m1 = 2e-32       # photon mass
d = 8000         # iron density kg/m^3

# Photon effective speed per DOF
v_eff = c**(1/6)

# Start with an initial guess for r (meters)
r = 1e-10
delta = 1e-12   # step size for iteration
max_iter = 1000000

for i in range(max_iter):
    # mass of iron in sphere of radius r
    m2 = r**3 * d

    # gravitational energy (G m1 m2 / r)
    g_energy = G * m1 * m2 / r

    # photon kinetic energy along one axis
    en = 0.5 * m1 * v_eff**2

    # check if we are close enough
    if abs(en - g_energy) / en < 1e-6:
        break

    # adjust r depending on whether g_energy < or > en
    if g_energy < en:
        r += delta
    else:
        r -= delta

print(f"Minimal radius r: {r:.6e} m")
print(f"Photon energy en: {en:.6e} J")
print(f"Gravitational energy g: {g_energy:.6e} J")
print(f"Photon effective speed: {v_eff:.6f} m/s")