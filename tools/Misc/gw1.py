import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Missile Parameters
# ----------------------------
missile_mass = 1.0          # kg
missile_speed_init = 400.0  # m/s
total_fuel_energy = 10e6    # J (10 MJ)
turn_efficiency = 0.5       # fraction of fuel used efficiently for turns
missile_radius_m = 0.1      # 10 cm radius
missile_area = np.pi * missile_radius_m**2  # m^2
air_density = 1.2           # kg/m^3

# ----------------------------
# Target Parameters
# ----------------------------
target_speed = 200.0        # m/s
target_turn_rate_deg_s = 20 # deg/s
target_initial_pos = np.array([10000.0, 0.0, 0.0])  # 10 km ahead
target_direction = np.array([1.0, 0.0, 0.0])        # initial velocity direction

# ----------------------------
# Simulation Parameters
# ----------------------------
dt = 0.1                   # s timestep
max_time = 100             # seconds
missile_pos = np.array([0.0, 0.0, 0.0])
missile_vel = missile_speed_init * np.array([1.0, 0.0, 0.0])
KE_current = 0.5 * missile_mass * missile_speed_init**2
remaining_fuel = total_fuel_energy

# Records for plotting
positions_missile = []
positions_target = []
fuel_record = []
KE_record = []
separation_record = []

# ----------------------------
# Helper Functions
# ----------------------------
def unit_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def turn_energy(delta_v, mass, efficiency):
    """Energy required for a velocity change delta_v with efficiency"""
    return 0.5 * mass * np.linalg.norm(delta_v)**2 / efficiency

# ----------------------------
# Simulation Loop
# ----------------------------
for t in np.arange(0, max_time, dt):
    # Missile-target vector
    rel_vec = target_initial_pos - missile_pos
    distance = np.linalg.norm(rel_vec)
    if distance < 10.0:  # impact threshold
        print(f"Impact at t = {t:.1f} s, distance = {distance:.2f} m")
        break

    # Record data
    positions_missile.append(missile_pos.copy())
    positions_target.append(target_initial_pos.copy())
    fuel_record.append(remaining_fuel / 1e6)
    KE_record.append(KE_current / 1e6)
    separation_record.append(distance)

    # Target maneuver (rotate around Z-axis for simplicity)
    turn_angle_rad = np.radians(target_turn_rate_deg_s * dt)
    rot_matrix = np.array([
        [np.cos(turn_angle_rad), -np.sin(turn_angle_rad), 0],
        [np.sin(turn_angle_rad), np.cos(turn_angle_rad), 0],
        [0, 0, 1]
    ])
    target_direction = rot_matrix @ target_direction
    target_initial_pos += target_direction * target_speed * dt

    # Desired missile velocity direction
    desired_dir = unit_vector(target_initial_pos - missile_pos)
    desired_vel = missile_speed_init * desired_dir

    # Delta-v for turn
    delta_v = desired_vel - missile_vel
    E_turn = turn_energy(delta_v, missile_mass, turn_efficiency)

    # Drag energy loss (scalar)
    v_mag = np.linalg.norm(missile_vel)
    E_drag = 0.5 * air_density * missile_area * v_mag**3 * dt

    # Total energy required this step
    E_spent = E_turn + E_drag

    # Update missile velocity and fuel
    if remaining_fuel > 0:
        if remaining_fuel >= E_spent:
            missile_vel += delta_v
            remaining_fuel -= E_spent
        else:
            scale = remaining_fuel / E_spent
            missile_vel += delta_v * scale
            remaining_fuel = 0
    else:
        # No fuel: missile coasts, drag slows it down
        if v_mag > 0:
            drag_acc = 0.5 * air_density * missile_area * v_mag**2 / missile_mass
            missile_vel -= unit_vector(missile_vel) * drag_acc * dt

    # Update kinetic energy and position
    KE_current = 0.5 * missile_mass * np.linalg.norm(missile_vel)**2
    missile_pos += missile_vel * dt

# ----------------------------
# Plot Results
# ----------------------------
positions_missile = np.array(positions_missile)
positions_target = np.array(positions_target)

plt.figure(figsize=(10,6))
plt.plot(positions_missile[:,0], positions_missile[:,1], label="Missile Path")
plt.plot(positions_target[:,0], positions_target[:,1], label="Target Path")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("3D Missile vs Target Simulation (Top View)")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()

plt.figure(figsize=(10,6))
plt.plot(fuel_record, label="Remaining Fuel (MJ)")
plt.plot(KE_record, label="Missile KE (MJ)")
plt.plot(separation_record, label="Missile-Target Separation (m)")
plt.xlabel("Time Steps")
plt.ylabel("Energy / Distance")
plt.title("Missile Fuel, KE, and Separation Over Time")
plt.legend()
plt.grid(True)
plt.show()