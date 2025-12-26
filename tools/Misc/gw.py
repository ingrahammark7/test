import math

# =========================
# INPUT PARAMETERS
# =========================

# Fracture toughness (ASSUMED MPa * sqrt(m))
K_IC_MPa_sqrt_m = 5.0            # SiC typical order of magnitude
K_IC = K_IC_MPa_sqrt_m * 1e6     # convert to Pa * sqrt(m)

# Elastic modulus (plane strain approx)
E_GPa = 450.0                    # SiC Young's modulus
nu = 0.17                        # Poisson ratio
E = E_GPa * 1e9
E_prime = E / (1 - nu**2)

# Atomic spacing (Si–C bond length)
a = 1.89e-10                     # meters

# =========================
# METHOD 1: REPORTED BOND ENERGY
# =========================

# Reported Si–C bond energy
bond_energy_kJ_per_mol = 318     # typical literature value
bond_energy_J = bond_energy_kJ_per_mol * 1e3 / 6.022e23

# =========================
# METHOD 2: COULOMB ESTIMATE
# =========================

# Effective ionic charge estimate
e = 1.602e-19
epsilon_0 = 8.854e-12
epsilon_r = 9.7                  # SiC relative permittivity

Z_eff = 3.0                      # effective partial charge (adjustable)

coulomb_energy_J = (
    (Z_eff * e)**2 /
    (4 * math.pi * epsilon_0 * epsilon_r * a)
)

# =========================
# FRACTURE TOUGHNESS → ENERGY
# =========================

# Griffith energy release rate
G_c = K_IC**2 / E_prime           # J/m^2

# One-atom-thick areal energy
atomic_area = a**2
fracture_energy_per_atom = G_c * atomic_area

# =========================
# OUTPUT
# =========================

print("\n=== INPUT ASSUMPTIONS ===")
print(f"K_IC: {K_IC_MPa_sqrt_m:.2f} MPa·√m (ASSUMED)")
print(f"E': {E_prime/1e9:.1f} GPa")
print(f"Atomic spacing: {a*1e10:.2f} Å")

print("\n=== BOND ENERGIES ===")
print(f"Reported Si–C bond energy: {bond_energy_J:.2e} J")
print(f"Coulomb implied bond energy: {coulomb_energy_J:.2e} J")

print("\n=== FRACTURE ENERGY ===")
print(f"Griffith energy release rate G_c: {G_c:.2f} J/m²")
print(f"Fracture energy per atom (1 bond thick): {fracture_energy_per_atom:.2e} J")

print("\n=== RATIOS (Fracture / Bond) ===")
print(f"vs reported bond: {fracture_energy_per_atom / bond_energy_J:.2e}")
print(f"vs Coulomb bond: {fracture_energy_per_atom / coulomb_energy_J:.2e}")