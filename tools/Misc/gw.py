import numpy as np

# Constants
dt = 0.01  # timestep (s)
rho = 1.225  # air density (kg/m3)
g0 = 9.81  # gravity (m/s^2)

# Missile parameters
missile_mass0 = 150  # kg initial
missile_mass_fuel = 30  # kg fuel
missile_mass = missile_mass0
missile_area = 0.018  # m^2
missile_cd = 0.3
missile_thrust = 4000  # N
burn_time = 5.0  # seconds
max_g = 30
Isp = 250  # s

# Aircraft parameters
aircraft_speed = 200  # m/s
aircraft_g = 4  # lateral g-load for turn
aircraft_mass = 10000  # kg (only for info)
aircraft_cd = 0.02
aircraft_area = 5.0  # m^2

# Guidance parameters
N_pn = 3.0

# Initial conditions
missile_pos = np.array([0.0, 0.0])
missile_speed = 1360  # m/s (Mach ~4)
missile_heading = 0.0

aircraft_pos = np.array([2000.0, 0.0])
# Initialize aircraft velocity vector pointing north
aircraft_vel = np.array([0.0, aircraft_speed])

time = 0.0
max_time = 20.0
intercept_radius = 10

# Fuel consumption rate
mdot = missile_thrust / (Isp * g0)

# Accumulated energy and fuel
total_thrust_work = 0.0
total_drag_work = 0.0
total_fuel_used = 0.0

def unit_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def rotate_vector(v, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])

def drag_force(rho, v, cd, area):
    speed = np.linalg.norm(v)
    return 0.5 * rho * speed**2 * cd * area

# Calculate aircraft turn rate omega (rad/s)
aircraft_omega = (aircraft_g * g0) / aircraft_speed
aircraft_omega_deg = np.degrees(aircraft_omega)
print(f"Aircraft turn rate ω = {aircraft_omega:.4f} rad/s = {aircraft_omega_deg:.2f} °/s")

# Missile initial velocity vector
missile_vel = np.array([missile_speed, 0.0])
missile_mass_fuel_remain = missile_mass_fuel
missile_mass_curr = missile_mass0

while time < max_time:
    rel_pos = aircraft_pos - missile_pos
    distance = np.linalg.norm(rel_pos)
    if distance < intercept_radius:
        print(f"Intercept at time {time:.2f}s, distance {distance:.2f} m")
        break

    rel_vel = aircraft_vel - missile_vel
    los_rate = (rel_pos[0]*rel_vel[1] - rel_pos[1]*rel_vel[0]) / (distance**2)
    closing_vel = -np.dot(rel_vel, unit_vector(rel_pos))

    # Proportional Navigation acceleration command
    a_n = N_pn * closing_vel * los_rate
    max_lat_accel = max_g * g0
    a_n = np.clip(a_n, -max_lat_accel, max_lat_accel)

    v_hat = unit_vector(missile_vel)
    lat_dir = np.array([-v_hat[1], v_hat[0]])

    # Thrust and fuel
    if time < burn_time and missile_mass_fuel_remain > 0:
        thrust_acc = missile_thrust / missile_mass_curr
        fuel_used = mdot * dt
        missile_mass_fuel_remain -= fuel_used
        missile_mass_curr -= fuel_used
        total_fuel_used += fuel_used
    else:
        thrust_acc = 0

    # Drag force and acceleration
    D = drag_force(rho, missile_vel, missile_cd, missile_area)
    drag_acc = D / missile_mass_curr
    drag_acc_vec = -drag_acc * v_hat

    # Total acceleration vector on missile
    acc = thrust_acc * v_hat + a_n * lat_dir + drag_acc_vec

    # Work done (energy)
    speed = np.linalg.norm(missile_vel)
    thrust_power = missile_thrust * speed  # thrust * velocity magnitude (assume aligned)
    thrust_work = thrust_power * dt
    drag_power = D * speed
    drag_work = drag_power * dt

    total_thrust_work += thrust_work
    total_drag_work += drag_work

    # Update missile state
    missile_vel += acc * dt
    missile_pos += missile_vel * dt

    # Update aircraft state by rotating velocity vector
    theta = aircraft_omega * dt
    aircraft_vel = rotate_vector(aircraft_vel, theta)
    aircraft_pos += aircraft_vel * dt

    time += dt

else:
    print("Missile missed target.")

# Final accelerations in g
missile_accel_g = np.linalg.norm(acc) / g0

print(f"Simulation time: {time:.2f} s")
print(f"Missile fuel used: {total_fuel_used:.3f} kg")
print(f"Missile energy from thrust: {total_thrust_work / 1e6:.3f} MJ")
print(f"Missile energy lost to drag: {total_drag_work / 1e6:.3f} MJ")
print(f"Missile final g-load: {missile_accel_g:.2f} g")
print(f"Aircraft turn g-load: {aircraft_g:.2f} g")