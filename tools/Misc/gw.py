import numpy as np

# -----------------------------
# Material parameters
# -----------------------------
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 0.25 # eV per bond-length
a = 0.25e-9                  # atomic spacing (m)
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # heat capacity per atom
Tmelt = 1800                 # K
Tion = 1.5e5                 # plasma threshold
alpha = 1e-5                 # m^2/s, thermal diffusivity

# -----------------------------
# Simulation parameters
# -----------------------------
max_crack_length = 100000  # atoms

# -----------------------------
# Precompute elastic energy per crack length
# -----------------------------
L_array = np.arange(1, max_crack_length + 1)
elastic_energy = elastic_energy_density * L_array**2  # total energy released per crack tip

# -----------------------------
# Crack tip speed and growth time
# -----------------------------
tau_bond = np.maximum(bond_energy / elastic_energy, 1e-13)  # s
v_tip = a / tau_bond
t_growth = a / v_tip

# -----------------------------
# Cooling time for heated region
# -----------------------------
L_heated_m = L_array * a
t_cool = L_heated_m**2 / alpha

# -----------------------------
# Tip temperature estimate
# -----------------------------
T_tip = 300 + elastic_energy / cv  # simple deterministic tip temperature
melted = T_tip >= Tmelt
plasma = T_tip >= Tion

# -----------------------------
# Determine crossover
# -----------------------------
crossover_indices = np.where(t_cool >= t_growth)[0]
crossover_length = L_array[crossover_indices[0]] if crossover_indices.size > 0 else None

# -----------------------------
# Console output (summary)
# -----------------------------
print(f"Simulation for {max_crack_length} atoms (fast deterministic)")
print(f"Crossover length where cooling time exceeds growth time: {crossover_length} atoms")
print(f"Tip temperature at max crack length: {T_tip[-1]:.1f} K")
print(f"Melting at tip: {melted[-1]}")
print(f"Plasma at tip: {plasma[-1]}")