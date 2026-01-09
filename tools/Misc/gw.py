# -----------------------------
# Closed-form steel crack tip simulation (physical units)
# -----------------------------
import math

# Material parameters
cohesive_energy = 4.3        # eV per atom
bond_energy = cohesive_energy / 2
elastic_energy_density = 1e-2 # eV per bond-length (linear scaling)
a = 0.25e-9                  # atomic spacing (m)
kB = 8.617e-5                # eV/K
cv = 3 * kB                  # eV/K per atom
Tmelt = 1800
Tion = 1.5e5
alpha = 1e-5                  # m^2/s

# Steel parameters
c_s = 3200                    # m/s, shear wave speed
gamma = 0.5                   # fraction of sound speed for crack tip
v_tip = gamma * c_s            # m/s

# Heated region (fixed cube)
heated_layers = 10
N_heated_atoms = heated_layers**3

# -----------------------------
# Cooling crossover (t_cool = t_growth)
L_heated_crossover = alpha / v_tip       # meters
crossover_length_atoms = L_heated_crossover / a

# -----------------------------
# Tip temperature (linear elastic energy scaling)
def T_tip(L):
    E = elastic_energy_density * L
    return 300 + E / (cv * N_heated_atoms)

# -----------------------------
# Melting crossover
melting_L_atoms = (Tmelt - 300) * cv * N_heated_atoms / elastic_energy_density
melting_L_atoms = max(melting_L_atoms, crossover_length_atoms)
melting_L_m = melting_L_atoms * a

# Plasma crossover
plasma_L_atoms = (Tion - 300) * cv * N_heated_atoms / elastic_energy_density
plasma_L_atoms = max(plasma_L_atoms, crossover_length_atoms)
plasma_L_m = plasma_L_atoms * a

# Tip temperature at crossovers
T_melting = T_tip(melting_L_atoms)
T_plasma = T_tip(plasma_L_atoms)
T_max = T_tip(1)

# -----------------------------
# Console output
print("Steel crack tip simulation (physical units)")
print(f"Crack tip speed: {v_tip:.1f} m/s")
print(f"Cooling crossover: {crossover_length_atoms:.0f} atoms ({L_heated_crossover*1e6:.3f} µm)")
print(f"Melting crossover: {melting_L_atoms:.0f} atoms ({melting_L_m*1e6:.3f} µm), T_tip = {T_melting:.1f} K")
print(f"Plasma crossover: {plasma_L_atoms:.0f} atoms ({plasma_L_m*1e3:.3f} mm), T_tip = {T_plasma:.1f} K")
print(f"Maximum tip temperature (L=1 atom): {T_max:.1f} K")