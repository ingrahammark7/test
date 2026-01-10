import numpy as np

# -----------------------------
# System parameters
# -----------------------------
mass_total = 1.0        # kg of material
initial_radius = 5e-3   # m, initial particle radius (e.g., 5 mm)
target_radius = 1e-6    # m, desired particle radius (1 micron)
system_power = 1000.0   # W, mechanical input power
gamma_eff = 0.05        # J/m^2, effective adhesion + surface energy
density = 2700.0        # kg/m^3, aluminum density
dt = 0.1                # s, time step

# -----------------------------
# Derived parameters
# -----------------------------
volume = (4/3) * np.pi * initial_radius**3
surface_area = 4 * np.pi * initial_radius**2
E_surface_per_particle = gamma_eff * surface_area

# Energy per unit mass needed to fragment one particle
E_per_mass = E_surface_per_particle / (density * volume)

# -----------------------------
# Time evolution loop
# -----------------------------
radius = initial_radius
t = 0.0
step = 0

print("Step | Time (s) | Particle radius (um)")
print("----------------------------------------")
while radius > target_radius:
    # Power per unit mass drives fragmentation
    dE = system_power * dt / mass_total  # energy input per kg per dt
    # Fraction of energy applied to overcome barrier
    frac = dE / E_per_mass
    # Limit maximum shrink per step to avoid overshoot
    if frac > 0.2:
        frac = 0.2
    radius = radius * (1 - frac)
    t += dt
    step += 1
    print(f"{step:4d} | {t:8.2f} | {radius*1e6:12.4f}")

print("\nFinal particle radius: {:.4f} um".format(radius*1e6))
print("Total time to reach target radius: {:.1f} s".format(t))