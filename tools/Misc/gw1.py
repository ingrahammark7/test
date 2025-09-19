import math

# -------------------------
# Material database
# -------------------------
materials = {
    "steel": {"density": 7850, "yield_strength": 1e9, "hardness": 500e6, "spall_factor": 0.8},
    "tungsten": {"density": 19250, "yield_strength": 1.5e9, "hardness": 700e6, "spall_factor": 0.7},
    "depleted_uranium": {"density": 19050, "yield_strength": 0.75e9, "hardness": 600e6, "spall_factor": 0.65},
    "ceramic": {"density": 3800, "yield_strength": 5e9, "hardness": 4e9, "spall_factor": 0.5}
}

# -------------------------
# Projectile inputs
# -------------------------
projectile = {
    "material": "tungsten",
    "mass": 10.0,        # kg
    "length": 1.2,       # meters
    "diameter": 0.03,    # meters
    "velocity": 1500,    # m/s
    "tip_type": "pointed"
}

# -------------------------
# Armor definition (layered)
# Each layer: (material, thickness_m, angle_deg)
# -------------------------
armor_layers = [
    ("steel", 0.15, 0),
    ("ceramic", 0.05, 0),
    ("steel", 0.1, 0)
]

# -------------------------
# Derived projectile properties
# -------------------------
proj = materials[projectile["material"]]
proj_density = proj["density"]
proj_area = math.pi * (projectile["diameter"]/2)**2
proj_rod_ratio = projectile["length"] / projectile["diameter"]
proj_velocity = projectile["velocity"]
proj_tip_type = projectile["tip_type"]
proj_mass = projectile["mass"]
proj_length = projectile["length"]

# -------------------------
# Simulation parameters
# -------------------------
block_size = 0.01  # 1 cm blocks for armor discretization
penetration_total = 0.0
rod_remaining_length = proj_length
remaining_velocity = proj_velocity

# -------------------------
# Pseudo-FEM Block-based Penetration
# -------------------------
for layer_index, (mat_name, thickness, angle) in enumerate(armor_layers):
    armor = materials[mat_name]
    rho_a = armor["density"]
    yield_a = armor["yield_strength"]
    hardness = armor["hardness"]
    spall = armor["spall_factor"]
    
    # Number of blocks in this layer
    n_blocks = max(1, int(thickness / block_size))
    block_thickness = thickness / n_blocks
    
    for block_index in range(n_blocks):
        if remaining_velocity <= 0 or rod_remaining_length <= 0:
            break
        
        # 1. Base kinetic energy
        KE = 0.5 * proj_mass * remaining_velocity**2
        
        # 2. Base penetration estimate
        P = KE / (proj_area * yield_a)
        
        # 3. Hydrodynamic/rod scaling
        P *= (proj_density / rho_a) * (0.9 + 0.1 * proj_rod_ratio)
        
        # 4. Angle effect
        P *= math.cos(math.radians(angle))
        
        # 5. Tip factor
        tip_factor = 1.0
        if proj_tip_type == "pointed":
            tip_factor = 1.1
        elif proj_tip_type == "blunt":
            tip_factor = 0.9
        P *= tip_factor
        
        # 6. Spall factor
        P *= spall
        
        # 7. Hardness correction
        P *= (yield_a / hardness)**0.25
        
        # 8. Limit penetration to current block
        actual_pen = min(P, block_thickness)
        penetration_total += actual_pen
        
        # 9. Energy absorbed by block
        energy_absorbed = KE * (actual_pen / P) if P > 0 else 0
        
        # 10. Update remaining projectile velocity
        remaining_velocity = math.sqrt(max(0, 2 * (KE - energy_absorbed) / proj_mass))
        
        # 11. Rod erosion (tip shortening proportional to block penetration)
        erosion_factor = 0.05  # 5% of block thickness per step as approximation
        rod_erosion = erosion_factor * block_thickness
        rod_remaining_length = max(0, rod_remaining_length - rod_erosion)
        
        # 12. Rod bending (simplified): reduce effective penetration
        bending_factor = 1.0 - 0.01 * (block_index / n_blocks)
        actual_pen *= bending_factor
        
        # Optional: print block debug info
        # print(f"Layer {layer_index+1} Block {block_index+1}: Penetration={actual_pen:.4f} m, Velocity={remaining_velocity:.1f} m/s, Rod length={rod_remaining_length:.3f} m")
    
    # Stop if projectile stopped
    if remaining_velocity <= 0 or rod_remaining_length <= 0:
        print(f"Projectile stopped in layer {layer_index+1}")
        break

# -------------------------
# Output summary
# -------------------------
print(f"Total penetration: {penetration_total:.3f} meters")
total_armor_thickness = sum(layer[1] for layer in armor_layers)
if penetration_total >= total_armor_thickness:
    print("Projectile fully penetrated all layers!")
else:
    print("Projectile did not fully penetrate all layers.")

print("\nNotes: This pseudo-FEM model includes:")
print("- Block discretization of armor layers")
print("- Sequential energy propagation and velocity reduction")
print("- Rod tip erosion and shortening")
print("- Rod bending effect")
print("- Multi-material, multi-layer armor")
print("- Tip type, obliquity, spall, hardness, and geometry corrections")
print("- Approximate and cannot replace full FEM/hydrodynamic simulations")