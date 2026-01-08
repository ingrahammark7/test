import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
dt = 0.01            # time step (s)
t_max = 3.0          # terminal engagement time (s)

# Projectile
v_p = 1200.0         # projectile speed (m/s)
a_lat_max = 30.0     # max lateral acceleration (m/s^2)

# Tank
v_t = 12.0           # tank lateral speed (m/s)

# Initial conditions
proj_pos = np.array([0.0, 0.0])
tank_pos = np.array([1500.0, 0.0])

proj_vel = np.array([v_p, 0.0])

proj_path = []
tank_path = []

# -----------------------------
# Simulation loop
# -----------------------------
for t in np.arange(0, t_max, dt):
    # Tank motion (lateral)
    tank_pos[1] += v_t * dt

    # Line-of-sight vector
    los = tank_pos - proj_pos
    los_dir = los / np.linalg.norm(los)

    # Desired velocity direction
    desired_vel = los_dir * v_p

    # Required lateral acceleration
    dv = desired_vel - proj_vel
    a_req = dv / dt

    # Limit lateral acceleration
    a_mag = np.linalg.norm(a_req)
    if a_mag > a_lat_max:
        a_req = a_req / a_mag * a_lat_max

    # Update projectile
    proj_vel += a_req * dt
    proj_vel = proj_vel / np.linalg.norm(proj_vel) * v_p
    proj_pos += proj_vel * dt

    proj_path.append(proj_pos.copy())
    tank_path.append(tank_pos.copy())

# -----------------------------
# Plot
# -----------------------------
proj_path = np.array(proj_path)
tank_path = np.array(tank_path)

plt.figure()
plt.plot(proj_path[:,0], proj_path[:,1], label="Projectile")
plt.plot(tank_path[:,0], tank_path[:,1], label="Tank")
plt.xlabel("Downrange (m)")
plt.ylabel("Lateral (m)")
plt.legend()
plt.title("Projectile vs Moving Tank (Limited Turn Authority)")
plt.show()

# Turn radius estimate
turn_radius = v_p**2 / a_lat_max
print(f"Approximate projectile turn radius: {turn_radius/1000:.2f} km")