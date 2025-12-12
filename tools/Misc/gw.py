# Effective nuclear charge and screened Coulomb energy for iron valence electrons

# Constants
k_e = 8.988e9         # N·m²/C², Coulomb constant
e = 1.602e-19         # C, elementary charge
r_valence = 2.48e-10  # m, typical Fe bond length in bcc lattice

# Iron configuration: [Ar] 3d6 4s2
# Valence electrons: 3d6 + 4s2 = 8 electrons

Z = 26  # Nuclear charge

# Slater's rules: shielding constants (approx)
# Core electrons (1s-3p): shield fully S=18
# Same shell 3d: 0.35 per electron (excluding self)
# 4s electrons: 0.35 for other 4s, 0.35 for 3d? Approximate as 0.35 per other valence
S_core = 18
S_3d = 0.35 * (6-1)  # 5 other 3d electrons
S_4s = 0.35 * (2-1 + 6)  # other 4s + all 3d electrons

# Effective nuclear charges
Z_eff_3d = Z - (S_core + S_3d)
Z_eff_4s = Z - (S_core + S_4s)

print(f"Effective nuclear charge Z_eff (3d electrons): {Z_eff_3d:.2f}")
print(f"Effective nuclear charge Z_eff (4s electrons): {Z_eff_4s:.2f}")

# Screened Coulomb energy between two valence electrons (extreme case: one atom vs another)
# E = k_e * (Z_eff e)^2 / r
E_3d = k_e * (Z_eff_3d * e)**2 / r_valence
E_4s = k_e * (Z_eff_4s * e)**2 / r_valence

print(f"Screened Coulomb energy per atom pair (3d): {E_3d:.3e} J")
print(f"Screened Coulomb energy per atom pair (4s): {E_4s:.3e} J")

# Compare with bond energy ~4.28 eV per atom
E_bond = 4.28 * e
factor_3d = E_bond / E_3d
factor_4s = E_bond / E_4s

print(f"Bond energy / screened Coulomb (3d) = {factor_3d:.3e}")
print(f"Bond energy / screened Coulomb (4s) = {factor_4s:.3e}")