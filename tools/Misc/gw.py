import math

# ---- HARDCODED INPUTS ----
B_surface = 0.5        # Tesla (typical strong neodymium magnet surface field)
distance = 0.02        # meters (2 cm away)
steel_thickness = 0.005 # meters (5 mm steel)
mu_r = 200             # relative permeability of steel

# ---- CONSTANTS ----
mu0 = 4 * math.pi * 1e-7  # vacuum permeability

# ---- FIELD DECAY (dipole approximation) ----
B_distance = B_surface / (1 + distance**3)

# ---- SIMPLE SHIELDING MODEL ----
shield_factor = 1 / (1 + mu_r * steel_thickness * 50)

B_after_steel = B_distance * shield_factor

# ---- OUTPUT ----
print("--- RESULTS ---")
print("Surface field:", B_surface, "T")
print("Distance:", distance, "m")
print("Steel thickness:", steel_thickness, "m")
print("Relative permeability:", mu_r)
print()
print("Field at distance:", round(B_distance, 6), "T")
print("Shielding factor:", round(shield_factor, 6))
print("Field after steel:", round(B_after_steel, 6), "T")