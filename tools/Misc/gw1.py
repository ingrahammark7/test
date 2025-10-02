import numpy as np

# Constants
e = 1.602e-19       # Elementary charge (C)
delta_V = 0.1       # Action potential amplitude (V)
lambda_const = 1e-3 # Length constant (1 mm)

# Distances (meters)
distances = np.array([1e-6, 1e-4, 1e-3, 1e-2])  # 1 μm, 0.1 mm, 1 mm, 1 cm

# Minimal energy for one electron
E_min = e * delta_V * np.exp(distances / lambda_const)

for d, E in zip(distances, E_min):
    print(f"Distance: {d*1e3:.3f} mm, Minimal Energy (1 electron): {E:.2e} J")