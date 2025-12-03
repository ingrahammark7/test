# Example: triboelectric onset calculator
import numpy as np

# Constants
eV_to_J = 1.602e-19

# Inputs
mass_atom = 4.65e-26        # N2 molecule, kg
bond_energy_eV = 5.15 /2#oxtgen        # N2 triple bond
velocity = 340               # m/s, Mach 1
aggregation_factor = 138+16   # feedback multiplier

# Calculations
bond_energy_J = bond_energy_eV * eV_to_J
kinetic_energy = 0.5 * mass_atom * velocity**2
effective_energy = kinetic_energy * aggregation_factor

print(f"Kinetic energy per molecule: {kinetic_energy:.3e} J")
print(f"Effective energy with aggregation: {effective_energy:.3e} J")
print(f"Bond energy: {bond_energy_J:.3e} J")

if effective_energy >= bond_energy_J:
    print("Triboelectric/plasma onset likely")
else:
    print("No significant plasma formation")