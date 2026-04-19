import math

# -----------------------------
# State
# -----------------------------
m = 50.0          # dry mass (kg)
mach = 4.0
a0 = 340.0        # speed of sound approx
v = mach * a0     # velocity magnitude (m/s)

# -----------------------------
# Atmospheric model (simple)
# -----------------------------
rho0 = 1.225

def rho(h):
    return rho0 * math.exp(-h / 8500)

h = 10000
density = rho(h)

# -----------------------------
# Heating model (energy flux)
# -----------------------------
k = 1.83e-4
rn = 0.09

q_dot = k * math.sqrt(density / rn) * v**3  # W/m^2

# assume effective heating area
A = 0.12

P_heat = q_dot * A  # W = J/s

# -----------------------------
# Energy-limited momentum change bound
# -----------------------------
# interpret heat as limiting rate of kinetic energy dissipation
E_dot_max = P_heat

# convert energy rate into velocity vector change magnitude
# E = 1/2 m v^2 => dE/dt = m v dv/dt
dvdt_max = E_dot_max / (m * v)

# -----------------------------
# Turn rate from kinematics only (no forces assumed)
# ω = |dv_perp| / v
# -----------------------------
omega = dvdt_max / v  # rad/s (pure kinematic bound)
omega_deg = math.degrees(omega)

# lateral acceleration equivalent (derived quantity only)
a_lat = dvdt_max

print("Velocity (m/s):", v)
print("Heat power (W):", P_heat)
print("Max dv/dt (m/s^2):", dvdt_max)
print("Turn rate bound (deg/s):", omega_deg)
print("Equivalent lateral accel (m/s^2):", a_lat)