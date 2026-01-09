import numpy as np

# -----------------------------
# Material parameters (flax fiber)
# -----------------------------
a = 0.5e-9                    # bond spacing ~ cellulose monomer (m)
cv = 2e-3                     # eV/K per monomer (approx.)
G_c = 0.2                      # eV per bond (cohesive energy, weak fiber)
elastic_modulus = 30e9        # Pa (30 GPa)
density = 1500                # kg/m^3
Tmelt = 700                   # K, thermal decomposition of flax
Tion = 1.5e5                  # K, still unreachable

# -----------------------------
# Crack / simulation parameters
# -----------------------------
max_crack_length = 100000      # number of bonds (atoms/monomers)
v_tip = 100                     # m/s, typical flax fiber crack speed
alpha = 1e-7                   # m^2/s, thermal diffusivity of flax
heated_layers_min = 10         # minimum cube of heated bonds

# -----------------------------
# Heated region (pull-apart model)
# -----------------------------
def N_heated(L_atoms):
    # assume heated region scales as L^(2/3) but min 1000 bonds
    return max(heated_layers_min**3, int(L_atoms**(2/3)))

# -----------------------------
# Tip temperature (energy per monomer)
# -----------------------------
def T_tip(L_atoms):
    E_tip = G_c * L_atoms                  # total energy released in pull-apart
    return 300 + E_tip / (cv * N_heated(L_atoms))

# -----------------------------
# Cooling crossover: t_cool = t_growth
# -----------------------------
L_heated_m = (N_heated(max_crack_length))**(1/3) * a
t_cool = L_heated_m**2 / alpha
t_growth = (max_crack_length * a) / v_tip

cooling_crossover_atoms = max_crack_length if t_cool >= t_growth else (t_growth * v_tip / a)

# -----------------------------
# Melting / decomposition
# -----------------------------
def melting_length():
    L = 1
    while T_tip(L) < Tmelt:
        L *= 1.05  # small increment for smooth growth
        if L > 1e12:
            break
    return L

melting_L_atoms = melting_length()
melting_L_m = melting_L_atoms * a
T_melting = T_tip(melting_L_atoms)

# -----------------------------
# Plasma (theoretical / unreachable)
# -----------------------------
def plasma_length():
    L = 1
    while T_tip(L) < Tion:
        L *= 1.05
        if L > 1e12:  # cap at huge cracks
            return None
    return L

plasma_L_atoms = plasma_length()
plasma_L_m = plasma_L_atoms * a if plasma_L_atoms else None
T_plasma = T_tip(plasma_L_atoms) if plasma_L_atoms else None

# Tip temperature at smallest bond
T_max = T_tip(1)

# -----------------------------
# Console output
# -----------------------------
print("Flax fiber crack tip simulation (pull-apart model)")
print(f"Crack tip speed: {v_tip:.1f} m/s")
print(f"Cooling crossover: {cooling_crossover_atoms:.0f} atoms ({L_heated_m*1e6:.3f} µm)")
print(f"Melting / decomposition crossover: {melting_L_atoms:.0f} atoms ({melting_L_m*1e6:.3f} µm), T_tip = {T_melting:.1f} K")
if plasma_L_atoms:
    print(f"Plasma crossover (theoretical): {plasma_L_atoms:.0f} atoms ({plasma_L_m*1e3:.3f} mm), T_tip = {T_plasma:.1f} K")
else:
    print("Plasma crossover: not reached (physically impossible in flax)")
print(f"Maximum tip temperature (L=1 bond): {T_max:.1f} K")
print("Note: triboelectric sparks may occur at much smaller cracks empirically.")