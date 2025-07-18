import numpy as np

# Constants
volume_air = 5.1e18        # m³, troposphere volume
water_density = 10         # g/m³ average vapor
water_mass = volume_air * water_density  # grams
molar_mass_water = 18      # g/mol
mol_water = water_mass / molar_mass_water

# Water molecules globally
NA = 6.022e23
water_molecules = mol_water * NA

# Salt parameters
mol_salt = 1e6             # Try 1 million mol as an example
ions_per_mol = 2
total_ions = mol_salt * ions_per_mol * NA

# Contact rate (ion touches 1 molecule/sec)
contact_time = 6.05e5  # seconds (1 week)
total_contacts_per_ion = contact_time
total_contacts_possible = total_ions * total_contacts_per_ion

# Efficiency: what percent of water gets touched?
efficacy = total_contacts_possible / water_molecules

print(f"Water molecules in air: {water_molecules:.2e}")
print(f"Total salt ions released: {total_ions:.2e}")
print(f"Total ion-molecule contacts: {total_contacts_possible:.2e}")
print(f"Coverage efficacy: {efficacy:.4f} ({efficacy*100:.2f}%)")
print(f"Salt mass: {mol_salt * 58.5:.2f} g ({(mol_salt * 58.5)/1e6:.2f} tonnes)")