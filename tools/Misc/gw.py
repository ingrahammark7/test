import math

# ----------------------------
# constants
# ----------------------------
c = 3e8
pi = math.pi

# ----------------------------
# parameters
# ----------------------------
f = 2.4e9        # Hz
B = 1e6          # Hz

# realistic spectral efficiency in dense RF interference
eta_rf = 3.0     # bits/s/Hz (collapsed from ideal Shannon)

# conventional compute density (silicon-scale order)
C_conv_density = 1e14  # bits/s/m^3

# ----------------------------
# 1. EM mode density (interference-limited)
# rho = (2f/c)^3
# ----------------------------
rho_modes = (2 * f / c) ** 3

# ----------------------------
# 2. RF computation density
# ----------------------------
C_rf_density = rho_modes * B * eta_rf

# ----------------------------
# 3. ratio
# ----------------------------
ratio = C_rf_density / C_conv_density

# ----------------------------
# output
# ----------------------------
print("\n--- REALISTIC RF vs CONVENTIONAL COMPUTE DENSITY ---\n")

print("Mode density (1/m^3):", rho_modes)
print("RF compute density (bits/s/m^3):", C_rf_density)
print("Conventional compute density (bits/s/m^3):", C_conv_density)
print("RF / conventional ratio:", ratio)