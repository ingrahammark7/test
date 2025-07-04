import math

# Constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
ATOMIC_RADIUS_SI = 1.1e-10  # meters
ATOMIC_DIAMETER_SI = 2 * ATOMIC_RADIUS_SI  # m
SPEED_OF_ENERGY = 3e8  # m/s, assume upper bound of light speed

# Transistor definition
ATOMS_PER_SIDE = 50  # adjustable
TOTAL_ATOMS = ATOMS_PER_SIDE ** 3

# Step 1: Time to cross one atom
transit_time_per_atom = ATOMIC_DIAMETER_SI / SPEED_OF_ENERGY  # seconds

# Step 2: Crossings per second
crossings_per_second = 1 / transit_time_per_atom

# Step 3: Geometric crossings (3D cube root)
geometric_crossings = crossings_per_second ** (1/3)

# Step 4: Power per crossing
power_watts = crossings_per_second * PLANCK_CONSTANT  # W per atomic path

# Step 5: Extrapolated power per m²
# Area of a single atomic column: (atomic diameter)^2
single_atom_area = ATOMIC_DIAMETER_SI ** 2  # m²

# Number of such atomic paths in 1 m²
paths_per_m2 = 1 / single_atom_area

# Total power over 1 m²
power_per_m2 = power_watts * paths_per_m2

# Output
print("=== Single Silicon Transistor Quantum Model ===")
print(f"Atoms per side:                  {ATOMS_PER_SIDE}")
print(f"Total atoms:                     {TOTAL_ATOMS}")
print(f"Atomic diameter:                 {ATOMIC_DIAMETER_SI:.2e} m")
print(f"Transit time per atom:           {transit_time_per_atom:.2e} s")
print(f"Crossings per second:            {crossings_per_second:.2e}")
print(f"Geometric crossings (per axis):  {geometric_crossings:.2e}")
print(f"Power (crossings × h):           {power_watts:.2e} W")
print(f"Power density over 1 m²:         {power_per_m2:.2e} W/m²")