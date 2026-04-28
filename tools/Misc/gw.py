import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# iron physical parameters
# ----------------------------
gamma = 0.7                 # J/m^2
kB = 1.38e-23
T = 300

Q = 0.8 * 1.6e-19          # activation energy (J ~ 0.8 eV)
M0 = 1e-4                  # prefactor (m^4/J·s typical order)

dt = 1e3                   # seconds (coarse-grained time step)
steps = 2000

# initial grain size (nanocrystalline start)
R = 50e-9  # 50 nm

history = []

for t in range(steps):

    # mobility (Arrhenius)
    M = M0 * np.exp(-Q / (kB * T))

    # curvature-driven growth law
    dR = M * gamma / R

    # update
    R += dt * dR

    history.append(R)

plt.plot(np.array(history)*1e6)
plt.xlabel("time step")
plt.ylabel("grain size (µm)")
plt.title("Curvature-driven grain growth in iron (minimal model)")
plt.show()