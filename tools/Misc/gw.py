import numpy as np

# -----------------------------
# Material parameters (scaled realistically)
# -----------------------------
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 1e-4  # eV per bond-length (scaled down to get physical temps)
a = 0.25e-9                  # atomic spacing (m)
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # eV/K per atom
Tmelt = 1800                 # K
Tion = 1.5e5                 # K
alpha = 1e-5                 # m^2/s

# -----------------------------
# Simulation parameters
# -----------------------------
max_crack_length = 100000    # atoms
heated_layers = 10           # 10x10x10 cube = 1000 atoms in heated region
N_heated_atoms = heated_layers**3

# -----------------------------
# Precompute elastic energy per crack length
# -----------------------------
L_array = np.arange(1, max_crack_length + 1)
elastic_energy = elastic_energy_density * L_array**2  # eV per crack tip

# -----------------------------
# Crack tip speed and growth time
# -----------------------------
tau_bond = np.maximum(bond_energy / elastic_energy, 1e-13)
v_tip = a / tau_bond
t_growth = a / v_tip  # same as tau_bond

# -----------------------------
# Cooling time for heated region
# -----------------------------
L_heated_m = L_array * a
t_cool = L_heated_m**2 / alpha

# -----------------------------
# Tip temperature using fixed heated region
# -----------------------------
T_tip = 300 + elastic_energy / (cv * N_heated_atoms)

# -----------------------------
# Melting and plasma checks
# -----------------------------
melted = T_tip >= Tmelt
plasma_original = T_tip >= Tion

# -----------------------------
# Cooling crossover
# -----------------------------
crossover_indices = np.where(t_cool >= t_growth)[0]
crossover_length = L_array[crossover_indices[0]] if crossover_indices.size > 0 else None

# -----------------------------
# Physically consistent melting crossover
# -----------------------------
melting_mask = (T_tip >= Tmelt) & (t_cool >= t_growth)
melting_index = np.argmax(melting_mask) if np.any(melting_mask) else None
melting_length = L_array[melting_index] if melting_index is not None else None

# -----------------------------
# Physically consistent plasma crossover
# -----------------------------
plasma_mask = (T_tip >= Tion) & (t_cool >= t_growth)
plasma_index = np.argmax(plasma_mask) if np.any(plasma_mask) else None
plasma_length = L_array[plasma_index] if plasma_index is not None else None

# -----------------------------
# Console output
# -----------------------------
print(f"Simulation for {max_crack_length} atoms (realistic energy scaling)")
print(f"Crossover length where cooling time exceeds growth time: {crossover_length} atoms")
print(f"Tip temperature at max crack length: {T_tip[-1]:.1f} K")
print(f"Melting at tip (simple model): {melted[-1]}")
print(f"Plasma at tip (simple model): {plasma_original[-1]}")
print(f"Crossover length where melting occurs (physical, considering cooling): {melting_length} atoms")
if melting_length is not None:
    print(f"Tip temperature at melting length: {T_tip[melting_index]:.1f} K")
print(f"Crossover length where plasma occurs (physical, considering cooling): {plasma_length} atoms")
if plasma_length is not None:
    print(f"Tip temperature at plasma length: {T_tip[plasma_index]:.1f} K")