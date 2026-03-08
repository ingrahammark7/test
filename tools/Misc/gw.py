# Full-featured EM force calculation for two one-atom-thick sheets

import math

# -----------------------
# Constants
# -----------------------
k = 8.988e9        # Coulomb constant (N·m²/C²)
e = 1.602e-19      # Elementary charge (C)

# -----------------------
# User-defined parameters
# -----------------------
Z = 26                    # Iron atomic number (nuclear charge)
atomic_radius = 1.26e-10  # Atomic radius (m)
lattice_spacing = 2.5e-10 # Approximate distance between atoms in lattice (m)
sheet_area = 1e-4         # Sheet area in m² (1 cm²)

# -----------------------
# Calculations
# -----------------------

# Charge of a single nucleus
q = Z * e

# Number of atoms in one sheet
num_atoms = int(sheet_area / lattice_spacing**2)

# Force between two single nuclei at atomic radius
F_single_atom = k * q**2 / atomic_radius**2

# Total force assuming every atom interacts with its opposite counterpart
F_total = F_single_atom * num_atoms

# -----------------------
# Output
# -----------------------
print(f"Single atom Coulomb force: {F_single_atom:.3e} N")
print(f"Number of atoms in sheet: {num_atoms:.3e}")
print(f"Total force between sheets: {F_total:.3e} N")