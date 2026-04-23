import numpy as np

# -----------------------------
# Domain (z direction only)
# -----------------------------
Lz = 5e-7          # 500 nm domain
Nz = 200
dz = Lz / Nz
z = np.linspace(0, Lz, Nz)

dt = 1e-10
steps = 2000

# -----------------------------
# Physical parameters
# -----------------------------
ng = 1e25          # gas density (1/m^3)

# cross-sections (heavy > light)
sigma_L = 1e-19
sigma_H = 5e-19

m_L = 1.0
m_H = 10.0

vL = 1e3
vH = 3e2

# diffusion coefficients (kinetic approximation)
lambda_L = 1 / (ng * sigma_L)
lambda_H = 1 / (ng * sigma_H)

D_L = (1/3) * lambda_L * vL
D_H = (1/3) * lambda_H * vH

# lifetimes
tau_L = 1 / (ng * sigma_L * vL)
tau_H = 1 / (ng * sigma_H * vH)

# surface reaction strengths
kL = 1e-2
kH = 5e-2

E0 = 1.0
alpha = 2.0

# -----------------------------
# Initial conditions
# -----------------------------
nL = np.ones(Nz) * 1e20
nH = np.ones(Nz) * 1e20

h = 0.0  # etched depth (m)

def reaction_prob(n):
    return (n**alpha) / (n**alpha + E0**alpha)

# -----------------------------
# PDE solver loop
# -----------------------------
for step in range(steps):

    # diffusion (finite difference, deterministic)
    nL_new = nL.copy()
    nH_new = nH.copy()

    for i in range(1, Nz - 1):
        nL_new[i] = nL[i] + dt * (
            D_L * (nL[i+1] - 2*nL[i] + nL[i-1]) / dz**2
            - nL[i] / tau_L
        )

        nH_new[i] = nH[i] + dt * (
            D_H * (nH[i+1] - 2*nH[i] + nH[i-1]) / dz**2
            - nH[i] / tau_H
        )

    nL, nH = nL_new, nH_new

    # boundary at surface (z = 0)
    RL = kL * nL[0] * reaction_prob(nL[0])
    RH = kH * nH[0] * reaction_prob(nH[0])

    R = RL + RH

    # deterministic etch front motion
    h += R * dt

    # depletion at surface
    nL[0] *= 0.99
    nH[0] *= 0.98

# -----------------------------
# Output
# -----------------------------
print("Final etched depth (nm):", h * 1e9)

# emergent diffusion lengths
print("Light diffusion length (nm):", np.sqrt(D_L * tau_L) * 1e9)
print("Heavy diffusion length (nm):", np.sqrt(D_H * tau_H) * 1e9)