# Constants
import math
molar_mass_fe = 55.85  # grams/mole
mass_kg = 1.0  # kilograms of iron
mass_g = mass_kg * 1000  # convert to grams

avogadro = 6.022e23  # atoms/mole
cohesive_energy_ev = 4.28# eV per atom
ev_to_joule = 1.602e-19  # conversion factor
ar=126*math.pow(10,-12)
q=9*math.pow(10,9)
el=1.6*math.pow(10,-19)
ch=el*el*q
ch=ch/(ar*ar)
an=26
ch=an*ch
ac=avogadro*ch
mo=1000/molar_mass_fe
re=mo*ac
print("J high estimate",re)
re=re**(.5)
print("2gj kg consistent with steel",re)
# Step 1: Moles of iron
moles_fe = mass_g / molar_mass_fe

# Step 2: Number of atoms
atoms = moles_fe * avogadro

# Step 3: Bond energy per atom in joules
bond_energy_per_atom_j = cohesive_energy_ev * ev_to_joule

# Step 4: Total bond energy
total_bond_energy_joules = atoms * bond_energy_per_atom_j
total_bond_energy_mj = total_bond_energy_joules / 1e6

# Output
print(f"Total atoms in {mass_kg} kg iron: {atoms:.2e}")
print(f"Bond energy per atom: {bond_energy_per_atom_j:.2e} J")
print(f"Total bond energy: {total_bond_energy_joules:.2e} J ({total_bond_energy_mj:.2f} MJ)")