import numpy as np
import matplotlib.pyplot as plt

# Constants
sigma_steel = 1e7
sigma_graphite = 1e4
A = 1e-4  # m^2
F = 96485
z_H2 = 2
V_mol = 22.4
V_applied = 1.0  # volts

currents = [1, 5]  # amperes
lengths = np.linspace(0.01, 0.5, 50)  # meters

def resistance(L, sigma):
    return L / (sigma * A)

def hydrogen_per_meter(I, V_drop, L):
    # Effective fraction of voltage reaching tip
    fraction = np.maximum(0, 1 - V_drop / V_applied)
    I_effective = I * fraction
    # Total H2 for 1 hour
    n_H2 = (I_effective * 3600) / (z_H2 * F)
    V_H2_total = n_H2 * V_mol
    # Index per meter
    return V_H2_total / L

plt.figure(figsize=(10,6))
for I in currents:
    V_drop_steel = I * resistance(lengths, sigma_steel)
    V_drop_graphite = I * resistance(lengths, sigma_graphite)
    H2_steel = hydrogen_per_meter(I, V_drop_steel, lengths)
    H2_graphite = hydrogen_per_meter(I, V_drop_graphite, lengths)
    
    plt.plot(lengths*100, H2_steel, '--', label=f'Steel {I}A')
    plt.plot(lengths*100, H2_graphite, '-', label=f'Graphite {I}A')

plt.xlabel("Electrode length (cm)")
plt.ylabel("Hydrogen production per meter (L/m) in 1 hour")
plt.title("Indexed hydrogen production vs electrode length for Steel and Graphite")
plt.legend()
plt.grid(True)
plt.show()