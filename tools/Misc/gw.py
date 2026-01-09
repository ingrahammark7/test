import numpy as np

# -----------------------------
# Material parameters (steel)
# -----------------------------
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 0.25 # eV per bond-length
a = 0.25e-9                  # atomic spacing, meters
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # heat capacity per atom
Tmelt = 1800                 # K
Tion = 1.5e5                 # K, approximate plasma threshold
alpha = 1e-5                 # m^2/s, thermal diffusivity
max_crack_length = 200_000_000       # atoms

# -----------------------------
# Initialize lattice and crack
# -----------------------------
temperatures = np.full(max_crack_length, 300.0)  # K ambient
melted = np.zeros(max_crack_length, dtype=bool)
plasma = np.zeros(max_crack_length, dtype=bool)

# -----------------------------
# Function to compute crack tip speed
# -----------------------------
def crack_tip_speed(elastic_energy_per_atom, bond_energy, atomic_spacing):
    # Deterministic atomic timescale
    tau_bond = bond_energy / elastic_energy_per_atom  # eV / (eV/s) → s
    # In our simplified model, assume energy release per atom occurs per atomic vibration (~1e-13 s)
    tau_bond = max(tau_bond, 1e-13)  
    v_tip = atomic_spacing / tau_bond
    return v_tip, tau_bond

# -----------------------------
# Simulate crack growth
# -----------------------------
print(f"{'Atom':>4} | {'T_tip (K)':>12} | {'Melting':>7} | {'Plasma':>7} | {'t_cool (s)':>12} | {'t_growth (s)':>12} | {'Crossover':>9}")
print("-"*90)

crossover_length = None

for L in range(1, max_crack_length+1):
    # Energy released at crack tip
    released_energy = elastic_energy_density * L**2
    elastic_energy_per_atom = released_energy / 1  # 1 atom tip increment
    
    # Compute crack tip speed
    v_tip, tau_bond = crack_tip_speed(elastic_energy_per_atom, bond_energy, a)
    
    # Time to grow one atom
    t_growth = a / v_tip
    
    # Assign energy to tip atom
    tip_index = L-1
    delta_T = released_energy / cv
    temperatures[tip_index] += delta_T
    
    # Heat diffusion to neighboring atoms (1D)
    new_temps = temperatures.copy()
    for i in range(1, L-1):
        new_temps[i] += alpha * (temperatures[i-1] + temperatures[i+1] - 2*temperatures[i])
    temperatures[:L] = new_temps[:L]
    
    # Cooling time for the heated region
    L_heated = L * a  # total heated length in meters
    t_cool = L_heated**2 / alpha
    
    # Check melting and plasma
    melted[tip_index] = temperatures[tip_index] >= Tmelt
    plasma[tip_index] = temperatures[tip_index] >= Tion
    
    # Determine crossover
    crossover = False
    if t_cool >= t_growth and crossover_length is None:
        crossover = True
        crossover_length = L
    
    print(f"{L:4d} | {temperatures[tip_index]:12.1f} | {melted[tip_index]:7} | {plasma[tip_index]:7} | {t_cool:12.3e} | {t_growth:12.3e} | {str(crossover):>9}")

# -----------------------------
# Summary
# -----------------------------
print("\nCrossover length where cooling time exceeds growth time:", crossover_length, "atoms")
print("Final tip temperature:", temperatures[L-1], "K")
print("Total melted atoms:", melted.sum())
print("Total plasma atoms:", plasma.sum())