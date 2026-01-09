import numpy as np

# -----------------------------
# Material parameters (flax fiber)
# -----------------------------
a = 0.5e-9                    # bond spacing ~ cellulose monomer (m)
cv = 2e-3                     # eV/K per monomer
G_c = 0.2                      # eV per bond (cohesive energy)
elastic_modulus = 30e9        # Pa
density = 1500                # kg/m^3
Tmelt = 700                   # K, thermal decomposition
Tion = 1.5e5                  # K, unreachable

# -----------------------------
# Crack / simulation parameters
# -----------------------------
max_crack_length = 100000      # number of bonds
v_tip = 100                     # m/s, typical flax crack speed
alpha = 1e-7                   # m^2/s, thermal diffusivity
heated_layers_min = 10         # minimum cube of heated bonds

# -----------------------------
# Heated region
# -----------------------------
def N_heated(L_atoms):
    return max(heated_layers_min**3, int(L_atoms**(2/3)))

# -----------------------------
# Tip temperature
# -----------------------------
def T_tip(L_atoms):
    E_tip = G_c * L_atoms
    return 300 + E_tip / (cv * N_heated(L_atoms))

# -----------------------------
# Cooling crossover: t_cool = t_growth
# -----------------------------
L_heated_m = (N_heated(max_crack_length))**(1/3) * a
t_cool = L_heated_m**2 / alpha
t_growth = (max_crack_length * a) / v_tip
cooling_crossover_atoms = max_crack_length if t_cool >= t_growth else (t_growth * v_tip / a)
E_cooling_eV = G_c * cooling_crossover_atoms

# -----------------------------
# Melting / decomposition crossover
# -----------------------------
def melting_length():
    L = 1
    while T_tip(L) < Tmelt:
        L *= 1.05
        if L > 1e12:
            break
    return L

melting_L_atoms = melting_length()
melting_L_m = melting_L_atoms * a
T_melting = T_tip(melting_L_atoms)
E_melting_eV = G_c * melting_L_atoms

# -----------------------------
# Plasma (theoretical / unreachable)
# -----------------------------
def plasma_length():
    L = 1
    while T_tip(L) < Tion:
        L *= 1.05
        if L > 1e12:
            return None
    return L

plasma_L_atoms = plasma_length()
plasma_L_m = plasma_L_atoms * a if plasma_L_atoms else None
T_plasma = T_tip(plasma_L_atoms) if plasma_L_atoms else None
E_plasma_eV = G_c * plasma_L_atoms if plasma_L_atoms else None

# Tip temperature at smallest bond
T_max = T_tip(1)
E_max_eV = G_c

# -----------------------------
# Console output
# -----------------------------
print("Flax fiber crack tip simulation (pull-apart model)")
print(f"Crack tip speed: {v_tip:.1f} m/s")
print(f"Cooling crossover: {cooling_crossover_atoms:.0f} atoms ({L_heated_m*1e6:.3f} µm), total energy = {E_cooling_eV:.2e} eV")
print(f"Melting / decomposition crossover: {melting_L_atoms:.0f} atoms ({melting_L_m*1e6:.3f} µm), T_tip = {T_melting:.1f} K, total energy = {E_melting_eV:.2e} eV")
if plasma_L_atoms:
    print(f"Plasma crossover (theoretical): {plasma_L_atoms:.0f} atoms ({plasma_L_m*1e3:.3f} mm), T_tip = {T_plasma:.1f} K, total energy = {E_plasma_eV:.2e} eV")
else:
    print("Plasma crossover: not reached (physically impossible in flax)")
print(f"Maximum tip temperature (L=1 bond): {T_max:.1f} K, total energy = {E_max_eV:.2e} eV")
print("Note: triboelectric sparks may occur at much smaller cracks empirically.")