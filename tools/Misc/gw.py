import math

# =========================
# INPUT PARAMETERS
# =========================

# Fracture toughness (MPa*sqrt(m))
K_IC_MPa_sqrt_m = 5.0
K_IC = K_IC_MPa_sqrt_m * 1e6

# Elastic properties
E_GPa = 450.0
nu = 0.17
E = E_GPa * 1e9
E_prime = E / (1 - nu**2)

# Atomic geometry
a = 1.89e-10                     # Si–C bond length
atoms_per_cell = 2              # SiC
cell_volume = a**3              # crude cubic estimate

# =========================
# BOND ENERGIES
# =========================

# Reported Si–C bond energy
bond_energy_kJ_per_mol = 318
bond_energy = bond_energy_kJ_per_mol * 1e3 / 6.022e23

# Coulomb estimate
e = 1.602e-19
epsilon_0 = 8.854e-12
epsilon_r = 9.7
Z_eff = 3.0

bond_energy_coulomb = (
    (Z_eff * e)**2 /
    (4 * math.pi * epsilon_0 * epsilon_r * a)
)

# =========================
# FRACTURE ENERGY
# =========================

G_c = K_IC**2 / E_prime           # J/m^2
gamma = G_c / 2                  # surface energy per surface

# =========================
# SURFACE ATOMIC DENSITY
# =========================

# approximate surface atom density
surface_atom_density = 1 / a**2
area_per_atom = 1 / surface_atom_density

fracture_energy_per_atom = G_c * area_per_atom

# =========================
# EFFECTIVE BOND COUNT
# =========================

N_bonds_reported = fracture_energy_per_atom / bond_energy
N_bonds_coulomb = fracture_energy_per_atom / bond_energy_coulomb

# =========================
# COHESIVE STRESS ESTIMATE
# =========================

sigma_cohesive = math.sqrt(E * gamma / a)
ideal_strength = E / 10

# =========================
# OUTPUT
# =========================

print("\n=== FRACTURE → ATOMISTICS CONSISTENCY CHECK ===")

print("\n--- Continuum ---")
print(f"K_IC: {K_IC_MPa_sqrt_m:.2f} MPa·√m")
print(f"G_c: {G_c:.2f} J/m²")
print(f"Surface energy γ: {gamma:.2f} J/m²")

print("\n--- Atomic scale ---")
print(f"Area per surface atom: {area_per_atom:.2e} m²")
print(f"Fracture energy per atom: {fracture_energy_per_atom:.2e} J")

print("\n--- Bond energies ---")
print(f"Reported bond energy: {bond_energy:.2e} J")
print(f"Coulomb bond energy: {bond_energy_coulomb:.2e} J")

print("\n--- Effective broken bonds per atom ---")
print(f"Using reported bond: {N_bonds_reported:.2f}")
print(f"Using Coulomb bond: {N_bonds_coulomb:.2f}")

print("\n--- Stress scale comparison ---")
print(f"Cohesive stress estimate: {sigma_cohesive/1e9:.1f} GPa")
print(f"Ideal strength ~ E/10: {ideal_strength/1e9:.1f} GPa")