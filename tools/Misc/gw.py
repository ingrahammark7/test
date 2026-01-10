import numpy as np

# -----------------------------
# System parameters (realistic)
# -----------------------------
total_mass = 10.0           # kg, total material
initial_radius = 1e-3       # m, initial particle radius 1 mm
target_radius = 1e-6        # m, target particle radius (we'll respect min radius)
system_power = 1000.0       # W, mechanical input power
gamma_eff = 20.0            # J/m^2, effective adhesion + surface energy
density = 2700.0            # kg/m^3, aluminum density
mechanical_efficiency = 0.15 # fraction of power actually used for fragmentation
min_radius = 1e-6           # m, sticking-limited minimum radius

# -----------------------------
# Energy per kg to fragment particle
# -----------------------------
def energy_per_mass(radius, gamma_eff, density):
    return (3 * gamma_eff) / (density * radius)

# Make sure we respect sticking-limited minimum
if target_radius < min_radius:
    target_radius = min_radius

E_per_mass = energy_per_mass(target_radius, gamma_eff, density)
E_per_mass /= mechanical_efficiency  # adjust for real efficiency

print(f"Energy per kg to fragment one particle (adjusted for efficiency): {E_per_mass:.2f} J/kg\n")

# -----------------------------
# Batch size optimization
# -----------------------------
batch_sizes = np.linspace(0.1, total_mass, 10)

print("Batch_mass(kg) | Time_to_target(s) | Mass_rate(kg/s)")
print("-----------------------------------------------")

for M_batch in batch_sizes:
    # Time to fragment batch
    t_target = E_per_mass * M_batch / system_power
    # Mass production rate
    R_mass = M_batch / t_target
    print(f"{M_batch:12.2f} | {t_target:15.2f} | {R_mass:13.2f}")