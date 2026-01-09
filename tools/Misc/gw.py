# -----------------------------
# Realistic steel crack tip simulation
# Tip temperature scales physically with crack length
# -----------------------------
import math

# Material parameters
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 1e-2 # eV per bond-length
a = 0.25e-9                  # atomic spacing (m)
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # eV/K per atom
Tmelt = 1800
Tion = 1.5e5
alpha = 1e-5                 # m^2/s

# Steel parameters
c_s = 3200                    # m/s, shear wave speed
gamma = 0.5                   # fraction of sound speed for crack tip
v_tip = gamma * c_s           # m/s

# -----------------------------
# Heated region grows with crack length
# We assume heated region ~ L^(2/3) atoms (to keep volume scaling)
def N_heated(L_atoms):
    return max(heated_layers**3, int(L_atoms**(2/3)))  # minimum 1000 atoms

heated_layers = 10  # initial cube

# -----------------------------
# Cooling crossover (t_cool = t_growth)
# L_heated = alpha / v_tip
L_heated_crossover = alpha / v_tip       # meters
crossover_length_atoms = L_heated_crossover / a

# -----------------------------
# Tip temperature
def T_tip(L_atoms):
    E = elastic_energy_density * L_atoms
    return 300 + E / (cv * N_heated(L_atoms))

# -----------------------------
# Melting crossover: solve T_tip(L) = Tmelt
def melting_length():
    L = 1
    while T_tip(L) < Tmelt:
        L *= 1.1
    return L

# -----------------------------
# Plasma crossover: practically never reached in steel
def plasma_length():
    L = 1
    while T_tip(L) < Tion:
        L *= 1.1
        if L > 1e12:  # stop at very long cracks
            return None
    return L

melting_L_atoms = melting_length()
melting_L_m = melting_L_atoms * a
T_melting = T_tip(melting_L_atoms)

plasma_L_atoms = plasma_length()
plasma_L_m = plasma_L_atoms * a if plasma_L_atoms else None
T_plasma = T_tip(plasma_L_atoms) if plasma_L_atoms else None

# Tip temperature at L=1
T_max = T_tip(1)

# -----------------------------
# Console output
print("Physically realistic steel crack tip simulation")
print(f"Crack tip speed: {v_tip:.1f} m/s")
print(f"Cooling crossover: {crossover_length_atoms:.0f} atoms ({L_heated_crossover*1e6:.3f} µm)")
print(f"Melting crossover: {melting_L_atoms:.0f} atoms ({melting_L_m*1e6:.3f} µm), T_tip = {T_melting:.1f} K")
if plasma_L_atoms:
    print(f"Plasma crossover: {plasma_L_atoms:.0f} atoms ({plasma_L_m*1e3:.3f} mm), T_tip = {T_plasma:.1f} K")
else:
    print("Plasma crossover: not reached (physically unlikely in steel)")
print(f"Maximum tip temperature (L=1 atom): {T_max:.1f} K")