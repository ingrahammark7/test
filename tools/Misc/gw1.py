import numpy as np

# --- Constants ---
e = 1.602e-19       # Elementary charge (C)
delta_V = 0.1       # Action potential amplitude (V)
lambda_const = 1e-3 # Axon length constant (1 mm)
N_ions = 1e9        # Number of ions moved per AP
vesicle_energy = 5e-14  # Energy per synaptic vesicle release (J)
num_neurons = 1e11  # Total neurons in human brain
kB = 1.38e-23       # Boltzmann constant (J/K)
T = 310             # Body temperature (K)
R = 8.314           # Gas constant (J/mol·K)
F = 96485           # Faraday constant (C/mol)

# --- Distances between neurons (meters) ---
distances = np.array([1e-6, 1e-4, 1e-3, 1e-2])  # 1 μm, 0.1 mm, 1 mm, 1 cm

# --- 1. Minimal energy for a single electron ---
E_min_electron = e * delta_V * np.exp(distances / lambda_const)

print("Minimal energy to move ONE electron:")
for d, E in zip(distances, E_min_electron):
    print(f"Distance: {d*1e3:.3f} mm, Energy: {E:.2e} J")

# --- 2. Realistic AP energy ---
E_AP = N_ions * e * delta_V + vesicle_energy
print(f"\nRealistic neuron AP energy: {E_AP:.2e} J")

# --- 3. Average power per neuron at given firing rate ---
firing_rate = 10  # Hz, close to human reaction speed
P_neuron = E_AP * firing_rate
print(f"Average power per neuron at {firing_rate} Hz: {P_neuron:.2e} W")

# --- 4. Total brain power ---
P_brain = P_neuron * num_neurons
print(f"Total brain power for {num_neurons:.0e} neurons at {firing_rate} Hz: {P_brain:.2f} W")

# --- 5. Energy per bit vs number of ions used ---
ions_per_bit = np.array([10, 100, 1e3, 1e4, 1e5, 1e6])
E_bit = ions_per_bit * e * delta_V
print("\nEnergy per bit vs number of ions used:")
for ions, E in zip(ions_per_bit, E_bit):
    print(f"{int(ions)} ions -> {E:.2e} J/bit")

# --- 6. Neuron thermal stability ---
V_thermal = kB * T / e  # ~26 mV
print(f"\nThermal voltage at body temp: {V_thermal:.2f} V (for comparison)")

# Critical K+ concentration for stability (E_K ~ V_thermal)
K_out = 5  # mM typical extracellular
E_crit = V_thermal  # Voltage where neuron destabilizes

# Solve for K_in such that E_K = V_thermal
K_in_crit = K_out / np.exp(E_crit / V_thermal)
print(f"Critical intracellular K+ for stability: {K_in_crit:.2f} mM")
print("Actual physiological K+ inside neuron: ~140 mM")

# Critical Na+ (approx) for AP viability
Na_in = 10   # mM
Na_out = 145 # mM
print(f"Actual physiological Na+ inside neuron: {Na_in} mM, outside: {Na_out} mM")

# --- Optional: total number of electrons and fraction free ions ---
neuron_mass = 1e-12  # kg
atom_mass = 2e-26    # kg/atom (average)
Z_avg = 6            # average number of electrons per atom

N_atoms = neuron_mass / atom_mass
N_electrons = N_atoms * Z_avg
free_ions = 1e7
fraction_free = free_ions / N_electrons

print(f"\nEstimated total electrons per neuron: {N_electrons:.2e}")
print(f"Number of free ions for signaling: {free_ions}")
print(f"Fraction of electrons used in signaling: {fraction_free:.2e}")