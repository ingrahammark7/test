import math

# ---- Given ----
mass_g = 1.0                # grams
mass = mass_g / 1000        # kg
density = 8960              # kg/m^3 (copper)
k = 401                     # W/(m·K)
c = 385                     # J/(kg·K)

# ---- Derived properties ----
alpha = k / (density * c)   # thermal diffusivity (m^2/s)

# Cube size from mass and density
volume = mass / density     # m^3
L = volume ** (1/3)         # cube side length (m)

# ---- 50% heat transfer time ----
# exp(-π² α t / L²) = 0.5
t_50 = (L**2 / (math.pi**2 * alpha)) * math.log(2)

# ---- Output ----
print(f"Cube side length: {L*1e3:.3f} mm")
print(f"Thermal diffusivity: {alpha:.2e} m^2/s")
print(f"50% heat transfer time: {t_50*1000:.2f} ms")