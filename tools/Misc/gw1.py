import numpy as np
import matplotlib.pyplot as plt

# Constants
ke = 8.987e9  # Coulomb constant, N·m²/C²
e = 1.602e-19  # Elementary charge, C
m_p = 1.673e-27  # Proton mass, kg
r0 = 1e-10  # Characteristic atomic spacing, m
Z = 1  # Assume single effective charge per atom

# Number of atoms
N = np.logspace(0, 6, 500)  # From 1 atom to 1 million atoms

# Escape velocity scaling
v_bulk = np.sqrt(2 * ke * Z * e**2 / (m_p * r0)) * N**(1/3)      # Bulk-like
v_surface = np.sqrt(2 * ke * Z * e**2 / (m_p * r0)) * N**(1/6)   # Surface-dominated

# Plot
plt.figure(figsize=(8,6))
plt.loglog(N, v_bulk/1e3, label='Bulk-like (v ~ N^(1/3))')
plt.loglog(N, v_surface/1e3, label='Surface-dominated (v ~ N^(1/6))')
plt.xlabel('Number of atoms (N)')
plt.ylabel('Escape velocity (km/s)')
plt.title('Escape velocity vs cluster size')
plt.grid(True, which='both', ls='--')
plt.legend()
plt.show()