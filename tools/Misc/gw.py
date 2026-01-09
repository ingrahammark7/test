import numpy as np

# -----------------------------
# Material parameters (steel)
# -----------------------------
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 0.25 # eV per bond-length
max_crack_length = 50        # smaller for console
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # heat capacity per atom
Tmelt = 1800                  # K
Tion = 1.5e5                  # K, approximate plasma threshold
alpha = 0.1                  # arbitrary heat diffusion coefficient per step

# -----------------------------
# Initialize lattice and crack
# -----------------------------
temperatures = np.full(max_crack_length, 300.0)  # K ambient
melted = np.zeros(max_crack_length, dtype=bool)
plasma = np.zeros(max_crack_length, dtype=bool)

# -----------------------------
# Simulate crack growth atom by atom
# -----------------------------
print(f"{'Atom':>4} | {'Energy released (eV)':>20} | {'T_local (K)':>12} | {'Melting':>7} | {'Plasma':>7}")
print("-"*60)

for L in range(1, max_crack_length+1):
    # Elastic energy released at crack tip
    released_energy = elastic_energy_density * L**2
    delta_T = released_energy / cv
    
    # Assign heat to tip atom
    tip_index = L-1
    temperatures[tip_index] += delta_T
    
    # Simple 1D heat diffusion for one timestep
    new_temps = temperatures.copy()
    for i in range(1, L-1):
        new_temps[i] += alpha * (temperatures[i-1] + temperatures[i+1] - 2*temperatures[i])
    temperatures[:L] = new_temps[:L]
    
    # Check melting and plasma
    melted[:L] = temperatures[:L] >= Tmelt
    plasma[:L] = temperatures[:L] >= Tion
    
    print(f"{L:4d} | {released_energy:20.3f} | {temperatures[tip_index]:12.1f} | {melted[tip_index]} | {plasma[tip_index]}")

# -----------------------------
# Summary
# -----------------------------
print("\nFinal crack tip temperature:", temperatures[L-1])
print("Number of melted atoms:", melted.sum())
print("Number of plasma atoms:", plasma.sum())