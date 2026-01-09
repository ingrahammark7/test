# -----------------------------
# Atomic fracture simulation (console only)
# -----------------------------

# Material parameters for steel
cohesive_energy = 4.3  # eV per atom
bond_energy = cohesive_energy / 2  # eV per bond

# Elastic energy density proxy (arbitrary units)
elastic_energy_density = 0.25  # eV per bond-length

# Maximum crack length to simulate
max_crack_length = 200

# Critical energy criterion
critical_energy = 2 * bond_energy

# Simulate crack growth
print(f"{'Crack Len':>10} | {'Energy/Bond (eV)':>18} | {'Status':>10}")
print("-"*45)

critical_length = None

for L in range(1, max_crack_length + 1):
    # Energy released ~ L^2
    released_energy = elastic_energy_density * L**2
    # Bonds broken ~ L
    bonds_broken = L
    energy_per_bond = released_energy / bonds_broken
    
    status = "Stable"
    if energy_per_bond >= critical_energy:
        status = "Unstable"
        if critical_length is None:
            critical_length = L
    
    print(f"{L:10d} | {energy_per_bond:18.3f} | {status:>10}")

print("\nCritical crack length (where instability occurs):", critical_length)