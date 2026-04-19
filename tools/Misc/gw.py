import math

# -----------------------------
# Constants (sea level approx)
# -----------------------------
gamma = 1.4
R = 287.0  # J/(kg·K)
T0 = 288.15  # K
a0 = math.sqrt(gamma * R * T0)  # speed of sound ~340 m/s
rho0 = 1.225  # kg/m^3

# -----------------------------
# Inputs (generic vehicle)
# -----------------------------
mach = 4.0
velocity = mach * a0  # m/s

length = 4.0  # m (generic slender body length)
diameter = 0.18  # m (generic reference diameter)

# Reference surface area (cylinder approximation)
radius = diameter / 2
side_area = 2 * math.pi * radius * length
nose_area = math.pi * radius**2
surface_area = side_area + nose_area

# -----------------------------
# Atmospheric density model (very simplified exponential)
# -----------------------------
def density_altitude(h):
    scale_height = 8500.0
    return rho0 * math.exp(-h / scale_height)

altitude = 10000.0  # m
rho = density_altitude(altitude)

# -----------------------------
# Convective heating (Sutton–Graves simplified form)
# q_dot ≈ k * sqrt(rho / R_n) * v^3
# -----------------------------
k = 1.83e-4  # empirical constant (SI form approximation)
nose_radius = radius

q_dot = k * math.sqrt(rho / nose_radius) * velocity**3  # W/m^2

total_heat_rate = q_dot * nose_area  # W

# -----------------------------
# Thermal capacity (generic material)
# -----------------------------
specific_heat = 900  # J/(kg·K) (aluminum-like)
mass = 50.0  # kg (generic structure)

temp_rise_rate = total_heat_rate / (mass * specific_heat)  # K/s

# -----------------------------
# Turning dynamics (generic aircraft relation)
# load factor n = L / (mg)
# turn rate omega = g * sqrt(n^2 - 1) / v
# -----------------------------
g = 9.81

load_factor = 5.0  # assumed structural limit (generic)
turn_rate_rad_s = g * math.sqrt(load_factor**2 - 1) / velocity
turn_rate_deg_s = math.degrees(turn_rate_rad_s)

# lateral acceleration equivalent
lateral_accel = velocity * turn_rate_rad_s

# -----------------------------
# Output
# -----------------------------
print("Velocity (m/s):", velocity)
print("Reference surface area (m^2):", surface_area)
print("Heat flux (W/m^2):", q_dot)
print("Total heating rate (W):", total_heat_rate)
print("Temperature rise rate (K/s):", temp_rise_rate)
print("Turn rate (deg/s):", turn_rate_deg_s)
print("Lateral acceleration (g):", lateral_accel / g)