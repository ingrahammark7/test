# -----------------------------
# Closed-form, fast, realistic crack tip simulation
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
alpha = 1e-5

# Heated region (fixed cube)
heated_layers = 10
N_heated_atoms = heated_layers**3

# -----------------------------
# Functions
# -----------------------------
def T_tip(L):
    """Tip temperature for crack length L (atoms)"""
    E = elastic_energy_density * L  # linear scaling
    return 300 + E / (cv * N_heated_atoms)

def t_growth(L):
    """Bond-limited crack growth time"""
    E = elastic_energy_density * L
    tau = bond_energy / E
    return max(tau, 1e-13)

def t_cool(L):
    """Cooling time for heated region"""
    L_m = L * a
    return L_m**2 / alpha

# -----------------------------
# Cooling crossover (t_cool = t_growth)
# Solve L^2 * a^2 / alpha = bond_energy / (elastic_energy_density * L)
# => L^3 = bond_energy * alpha / (elastic_energy_density * a^2)
cooling_crossover_L = (bond_energy * alpha / (elastic_energy_density * a**2))**(1/3)

# Melting crossover: T_tip >= Tmelt and t_cool >= t_growth
melting_L_temp = (Tmelt - 300) * cv * N_heated_atoms / elastic_energy_density
melting_L = max(melting_L_temp, cooling_crossover_L)

# Plasma crossover: T_tip >= Tion and t_cool >= t_growth
plasma_L_temp = (Tion - 300) * cv * N_heated_atoms / elastic_energy_density
plasma_L = max(plasma_L_temp, cooling_crossover_L)

# Tip temperatures at crossovers
T_melting = T_tip(melting_L)
T_plasma = T_tip(plasma_L)
T_max = T_tip(1)  # maximum temperature for smallest crack

# -----------------------------
# Console output
# -----------------------------
print("Closed-form crack tip simulation (linear elastic energy)")
print(f"Cooling crossover length: {cooling_crossover_L:.0f} atoms")
print(f"Melting crossover length: {melting_L:.0f} atoms, T_tip = {T_melting:.1f} K")
print(f"Plasma crossover length: {plasma_L:.0f} atoms, T_tip = {T_plasma:.1f} K")
print(f"Maximum tip temperature (L=1 atom): {T_max:.1f} K")