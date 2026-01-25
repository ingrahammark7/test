import math

# -----------------------------
# ONLY TWO INPUTS (set here)
# -----------------------------
CORN_VERTICAL_AREA_M2 = 10.0      # plant surface area (m^2)
CORN_HORIZONTAL_AREA_M2 = 1.0     # plant footprint area (m^2)

# -----------------------------
# HARD-CODED PHYSICAL CONSTANTS
# -----------------------------
YIELD_PER_PLANT_KG = 0.25         # average corn per plant (kg)
BULK_DENSITY_KG_M3 = 750
MAX_BIN_HEIGHT_M = 3.0

# Mice-proofing constants (example thresholds)
MICE_PROOF_MIN_WEIGHT_KG = 50.0   # minimum mass to discourage mice
MICE_PROOF_MIN_FOOTPRINT_M2 = 0.5 # minimum footprint for physical barriers

# Material embodied energy (MJ/kg)
EMBODIED_ENERGY = {
    "plastic": 45,
    "wood": 12,
    "metal": 70
}

# Transport energy
TRANSPORT_ENERGY_MJ_PER_TON_KM = 0.5
TRANSPORT_DISTANCE_KM = 1.0      # assumed transport distance

# Reuse count
REUSE_COUNT = 10


# -----------------------------
# Calculations
# -----------------------------
# 1) Grain volume per plant
grain_volume_m3 = YIELD_PER_PLANT_KG / BULK_DENSITY_KG_M3

# 2) Bin footprint required (assuming max height)
bin_footprint_m2 = grain_volume_m3 / MAX_BIN_HEIGHT_M

# 3) Land use ratio (how much more space needed)
land_use_ratio = bin_footprint_m2 / CORN_HORIZONTAL_AREA_M2

# 4) Bin dimensions (square)
side_m = math.sqrt(bin_footprint_m2)
height_m = MAX_BIN_HEIGHT_M

# 5) Number of plants per bin (based on footprint)
plants_per_bin = CORN_HORIZONTAL_AREA_M2 / bin_footprint_m2

# 6) Bins needed per plant
bins_needed_per_plant = 1 / plants_per_bin

# 7) Storage space needed per plant
storage_space_needed_m2 = bin_footprint_m2

# 8) Mice-proofing check
mice_proof = (
    (YIELD_PER_PLANT_KG >= MICE_PROOF_MIN_WEIGHT_KG) or
    (bin_footprint_m2 >= MICE_PROOF_MIN_FOOTPRINT_M2)
)

# 9) Embodied energy of bin (per plant)
embodied_energy_mj = (YIELD_PER_PLANT_KG * EMBODIED_ENERGY["plastic"]) / REUSE_COUNT

# 10) Transport energy (per plant)
transport_energy_mj = (YIELD_PER_PLANT_KG / 1000) * TRANSPORT_DISTANCE_KM * TRANSPORT_ENERGY_MJ_PER_TON_KM

# 11) Total energy
total_energy_mj = embodied_energy_mj + transport_energy_mj


# -----------------------------
# Output
# -----------------------------
print("\n--- Corn Plant Storage Optimization ---")
print(f"Corn vertical area (m^2): {CORN_VERTICAL_AREA_M2}")
print(f"Corn horizontal area (m^2): {CORN_HORIZONTAL_AREA_M2}")
print(f"Grain mass per plant (kg): {YIELD_PER_PLANT_KG:.2f}")
print(f"Grain volume per plant (m^3): {grain_volume_m3:.6f}")
print(f"Required bin footprint (m^2): {bin_footprint_m2:.6f}")
print(f"Land use ratio (bin footprint / plant footprint): {land_use_ratio:.6f}")
print(f"Bin dimensions (square): {side_m:.4f} m x {side_m:.4f} m x {height_m:.2f} m")
print(f"Plants per bin: {plants_per_bin:.2f}")
print(f"Bins needed per plant: {bins_needed_per_plant:.6f}")
print(f"Storage space needed per plant (m^2): {storage_space_needed_m2:.6f}")
print(f"Mice-proofing OK? {'YES' if mice_proof else 'NO'}")
print(f"Embodied energy (MJ per plant): {embodied_energy_mj:.2f}")
print(f"Transport energy (MJ per plant): {transport_energy_mj:.2f}")
print(f"Total energy (MJ per plant): {total_energy_mj:.2f}")
print("----------------------------------------\n")