import numpy as np
import matplotlib.pyplot as plt

# parameters
steps = 2000
d = 10.0            # initial grain size
T = 1.0             # normalized temperature field

A0 = 1.0
Ea = 2.0

alpha = 5.0         # boundary scattering strength
C = 1.0

d_hist = []
T_hist = []

for t in range(steps):

    # thermal conductivity decreases with smaller grains
    k = 1.0 / (1.0 + alpha / d)

    # grain growth rate increases with temperature
    A = A0 * np.exp(-Ea / (T + 1e-6))

    # heat equation surrogate (simple relaxation)
    dTdt = -k * T
    T += dTdt * 0.01

    # grain evolution (curvature-driven)
    ddt = A / d
    d += ddt * 0.01

    d_hist.append(d)
    T_hist.append(T)

plt.plot(d_hist, label="grain size")
plt.plot(T_hist, label="temperature")
plt.legend()
plt.show()