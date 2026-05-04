import math

# ----------------------------
# constants
# ----------------------------
k_B = 1.380649e-23
T = 300.0
c = 3e8
pi = math.pi

# ----------------------------
# RF system parameters
# ----------------------------
P_t = 1e-3       # W
f = 2.4e9        # Hz
B = 1e6          # Hz
eta_rf = 3.0     # bits/s/Hz (interference-limited)

# ----------------------------
# material assumptions (important)
# ----------------------------

# RF system material mass per m^3 equivalent structure
# includes antennas, shielding, cavities, support structure
mass_rf_per_m3 = 5.0  # kg/m^3 (light structured RF fabric)

# CMOS system material density (silicon + packaging equivalent active layer)
mass_cmos_per_m3 = 2330.0  # kg/m^3 (silicon bulk density approx)

# conventional compute density (baseline)
C_cmos_density = 1e14  # bits/s/m^3 (from earlier corrected model)

# ----------------------------
# RF mode density (interference-limited)
# ----------------------------
rho_modes = (2 * f / c) ** 3

# ----------------------------
# RF compute density (per volume)
# ----------------------------
C_rf_density = rho_modes * B * eta_rf

# ----------------------------
# convert to per mass
# ----------------------------
C_rf_per_kg = C_rf_density / mass_rf_per_m3
C_cmos_per_kg = C_cmos_density / mass_cmos_per_m3

# ----------------------------
# ratio
# ----------------------------
ratio = C_rf_per_kg / C_cmos_per_kg

# ----------------------------
# output
# ----------------------------
print("\n--- COMPUTE DENSITY PER MASS ---\n")

print("RF compute density (bits/s/m^3):", C_rf_density)
print("RF compute per kg (bits/s/kg):", C_rf_per_kg)

print("CMOS compute density (bits/s/m^3):", C_cmos_density)
print("CMOS compute per kg (bits/s/kg):", C_cmos_per_kg)

print("RF / CMOS ratio (per mass):", ratio)