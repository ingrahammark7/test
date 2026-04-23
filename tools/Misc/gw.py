import numpy as np

# -----------------------------
# Grid
# -----------------------------
Nx = 100
Nz = 200

Lx = 1e-6   # 1 micron feature width
Lz = 5e-7   # 500 nm depth

dx = Lx / Nx
dz = Lz / Nz

x = np.linspace(0, Lx, Nx)
z = np.linspace(0, Lz, Nz)

dt = 1e-11
steps = 2000

# -----------------------------
# Physics parameters
# -----------------------------
lambda_eff = 1e-7   # transport attenuation length (~100 nm scale emerges here)

Phi0 = 1.0

Y_L = 1.0
Y_H = 2.0

# surface height (initial flat)
h = np.zeros(Nx)

# -----------------------------
# helper: slope (shadowing)
# -----------------------------
def slope(h):
    dhdx = np.zeros_like(h)
    dhdx[1:-1] = (h[2:] - h[:-2]) / (2*dx)
    return dhdx

# -----------------------------
# simulation loop
# -----------------------------
for step in range(steps):

    dhdx = slope(h)

    R = np.zeros(Nx)

    for i in range(Nx):

        # angular collapse (depth attenuation)
        depth = h[i]
        A = np.exp(-depth / lambda_eff)

        # shadowing (steep walls reduce flux)
        S = 1.0 / (1.0 + dhdx[i]**2)

        # two-species effective yield (kept simple but coupled)
        R_L = Phi0 * A * S * Y_L
        R_H = Phi0 * A * S * Y_H

        R[i] = R_L + R_H

    # update surface
    h += R * dt

# -----------------------------
# output
# -----------------------------
print("Max etched depth (nm):", np.max(h) * 1e9)
print("Min etched depth (nm):", np.min(h) * 1e9)
print("AR (aspect ratio):", np.max(h) / Lx)