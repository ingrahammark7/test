import math

# -------------------------
# Material database (simplified but expanded)
# -------------------------
materials = {
    "steel": {"density": 7850, "yield_strength": 1e9, "hardness": 500e6, "spall_factor": 0.8},
    "tungsten": {"density": 19250, "yield_strength": 1.5e9, "hardness": 700e6, "spall_factor": 0.7},
    "depleted_uranium": {"density": 19050, "yield_strength": 0.75e9, "hardness": 600e6, "spall_factor": 0.65},
    "ceramic": {"density": 3800, "yield_strength": 5e9, "hardness": 4e9, "spall_factor": 0.5}
}

# -------------------------
# Input: Projectile
# -------------------------
projectile_material = "tungsten"
mass = 10.0           # kg
length = 1.2          # m
diameter = 0.03       # m
velocity = 1500       # m/s
impact_angle = 0      # degrees
tip_type = "pointed"  # options: "pointed", "blunt"

# -------------------------
# Input: Armor
# -------------------------
armor_material = "steel"
armor_thickness = 0.3  # meters
armor_layers = 1       # number of layers (homogeneous)
armor_angle = 0        # angle of armor plate

# -------------------------
# Derived properties
# -------------------------
proj = materials[projectile_material]
armor = materials[armor_material]

proj_density = proj["density"]
armor_density = armor["density"]
armor_yield = armor["yield_strength"]
armor_hardness = armor["hardness"]
spall_factor = armor["spall_factor"]

area = math.pi * (diameter/2)**2
KE = 0.5 * mass * velocity**2

# -------------------------
# Penetration model (advanced)
# -------------------------

# 1. Base kinetic energy penetration
P_ke = KE / (area * armor_yield)

# 2. Density ratio scaling (hydrodynamic effect)
P_density = P_ke * (proj_density / armor_density)

# 3. Rod geometry factor (long-rod effect)
rod_ratio = length / diameter
P_geom = P_density * (0.9 + 0.1 * rod_ratio)

# 4. Impact obliquity
P_angle = P_geom * math.cos(math.radians(impact_angle + armor_angle))

# 5. Tip effect
tip_factor = 1.0
if tip_type == "pointed":
    tip_factor = 1.1
elif tip_type == "blunt":
    tip_factor = 0.9
P_tip = P_angle * tip_factor

# 6. Spalling effect
P_spall = P_tip * spall_factor

# 7. Multiple layers reduction
P_layers = P_spall / math.sqrt(armor_layers)

# 8. Hardness correction (simplified)
P_hardness = P_layers * (armor_yield / armor_hardness)**0.25

# -------------------------
# Output
# -------------------------
print(f"Estimated penetration depth: {P_hardness:.3f} meters")
if P_hardness >= armor_thickness:
    print("Penetration likely!")
else:
    print("Penetration unlikely.")

print("\nNotes:")
print("- Fully approximate. Includes kinetic energy, density ratio, rod geometry, impact angle, tip shape, spall, multiple layers, and hardness correction.")
print("- Cannot replace FEM, hydrodynamic simulations, or detailed material models.")