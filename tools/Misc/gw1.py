import numpy as np

# --- Constants ---
e = 1.602e-19       # Elementary charge (C)
delta_V = 0.1       # Action potential amplitude (V)
lambda_const = 1e-3 # Length constant (1 mm)
N_ions = 1e9        # Approx ions per AP
vesicle_energy = 5e-14  # J, synaptic vesicle release
num_neurons = 1e11  # Number of neurons in human brain

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
firing_rate = 1  # Hz
P_neuron = E_AP * firing_rate
print(f"Average power per neuron at {firing_rate} Hz: {P_neuron:.2e} W")

# --- 4. Total brain power ---
P_brain = P_neuron * num_neurons
print(f"Total brain power for {num_neurons:.0e} neurons firing at {firing_rate} Hz: {P_brain:.2f} W")

# --- Optional: power vs firing rate ---
frequencies = np.array([0.1, 1, 5, 10, 20, 50, 100])  # Hz
P_brain_array = E_AP * frequencies * num_neurons

print("\nBrain power vs firing rate (W):")
for f, P in zip(frequencies, P_brain_array):
    print(f"{f} Hz: {P:.2f} W")