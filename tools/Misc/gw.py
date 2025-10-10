import math

# --------------------------
# Constants
# --------------------------
g = 9.81                  # gravity (m/s^2)
m_P = 2.176e-8            # Planck mass (kg)
rho_s = 2500              # particle density (kg/m^3)
theta_deg = 45            # launch angle (degrees)

# --------------------------
# Particle geometry
# --------------------------
r = (3 * m_P / (4 * math.pi * rho_s))**(1/3)  # radius in meters
A = math.pi * r**2                             # cross-sectional area in m^2

# --------------------------
# First grain: characteristic distance
# --------------------------
rho_air = 1.225  # air density kg/m^3 (for reference)
# Approximate “grain distance” based on density ratio
grain_distance = (rho_s / rho_air) * r  # meters

# --------------------------
# Launch velocity for 45° ballistic trajectory
# --------------------------
theta_rad = math.radians(theta_deg)
v0 = math.sqrt(grain_distance * g)

# Maximum horizontal range at 45°
R_max = (v0**2 / g) * math.sin(2 * theta_rad)

# --------------------------
# Output results
# --------------------------
print(f"Particle radius: {r*1000:.6f} mm")
print(f"Grain distance (first grain): {grain_distance:.6f} m")
print(f"Launch velocity (v0) for 45°: {v0:.6f} m/s")
print(f"Maximum horizontal range (R_max): {R_max:.6f} m")