import numpy as np

# -----------------------------
# Material parameters (steel)
# -----------------------------
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 0.25 # eV per bond-length
max_crack_length = 200

# Thermal parameters
kB = 8.617e-5  # eV/K
T_list = [300, 500, 800]  # K: room, hot, extreme

# Steel properties
Tmelt = 1800  # K
cv = 3 * kB   # Heat capacity per atom (Dulong-Petit)
yield_stress_fraction = 0.5  # fraction of bonds failing before plasticity blunts

# -----------------------------
# Function to compute critical length
# -----------------------------
def compute_critical_lengths(T):
    # Thermal activation reduces effective bond energy
    effective_bond_energy = bond_energy - kB*T
    critical_energy = 2 * effective_bond_energy

    critical_lengths = {
        "cold_instability": None,
        "thermal_instability": None,
        "plastic_limit": None,
        "melting_limit": None
    }

    for L in range(1, max_crack_length+1):
        released_energy = elastic_energy_density * L**2
        bonds_broken = L
        energy_per_bond = released_energy / bonds_broken

        # 1) Cold instability (deterministic)
        if critical_lengths["cold_instability"] is None:
            if energy_per_bond >= 2 * bond_energy:
                critical_lengths["cold_instability"] = L

        # 2) Thermal instability
        if critical_lengths["thermal_instability"] is None:
            if energy_per_bond >= critical_energy:
                critical_lengths["thermal_instability"] = L

        # 3) Plasticity: assume fraction of bonds can fail before blunting
        if critical_lengths["plastic_limit"] is None:
            if energy_per_bond >= critical_energy * yield_stress_fraction:
                critical_lengths["plastic_limit"] = L

        # 4) Melting: local tip temperature = released_energy per atom / cv
        local_temp = released_energy / cv
        if critical_lengths["melting_limit"] is None:
            if local_temp + T >= Tmelt:
                critical_lengths["melting_limit"] = L

    return critical_lengths

# -----------------------------
# Run simulation
# -----------------------------
for T in T_list:
    print(f"\n--- Simulation at T = {T} K ---")
    crit_lengths = compute_critical_lengths(T)
    print(f"{'Crossover':>20} | {'Critical crack length (atoms)':>30}")
    print("-"*55)
    for key, val in crit_lengths.items():
        print(f"{key:>20} | {str(val):>30}")