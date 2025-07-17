import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Simulation Settings ===
NUM_AIRCRAFT = 6
FRAME_INTERVAL = 50  # ms
TRAIL_LENGTH = 20

# === World Limits ===
WORLD_LIMIT = 30

# === Aircraft State ===
np.random.seed(0)
positions = np.random.uniform(-WORLD_LIMIT, WORLD_LIMIT, (NUM_AIRCRAFT, 3))
velocities = np.random.uniform(-1, 1, (NUM_AIRCRAFT, 3))
trails = np.zeros((NUM_AIRCRAFT, TRAIL_LENGTH, 3))

# === Figure and Axes ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')
ax.set_xlim([-WORLD_LIMIT, WORLD_LIMIT])
ax.set_ylim([-WORLD_LIMIT, WORLD_LIMIT])
ax.set_zlim([-WORLD_LIMIT, WORLD_LIMIT])
ax.grid(True)
ax.view_init(elev=20, azim=45)

# === Plot Elements ===
scatters = [ax.plot([], [], [], 'o', markersize=6)[0] for _ in range(NUM_AIRCRAFT)]
trail_lines = [ax.plot([], [], [], '-', lw=1, alpha=0.3)[0] for _ in range(NUM_AIRCRAFT)]
shadows = [ax.plot([], [], [], 'o', color='gray', markersize=6, alpha=0.2)[0] for _ in range(NUM_AIRCRAFT)]

# === Utility Functions ===
def update_trails(trails, positions):
    trails[:, 1:] = trails[:, :-1]
    trails[:, 0] = positions
    return trails

# === Animation Update Function ===
def update(frame):
    global positions, velocities, trails

    # Update positions and velocities
    positions += velocities
    velocities += np.random.uniform(-0.1, 0.1, velocities.shape)  # Slight random change
    velocities = np.clip(velocities, -1.5, 1.5)
    positions = np.clip(positions, -WORLD_LIMIT, WORLD_LIMIT)

    # Update trails
    trails = update_trails(trails, positions)

    for i in range(NUM_AIRCRAFT):
        # Size scaling based on Z (fake depth)
        z = positions[i, 2]
        size = max(3, 10 - z / 5)
        color = plt.cm.coolwarm((z + WORLD_LIMIT) / (2 * WORLD_LIMIT))  # Color based on height

        # Update aircraft point (wrap coords in lists!)
        scatters[i].set_data([positions[i, 0]], [positions[i, 1]])
        scatters[i].set_3d_properties([positions[i, 2]])
        scatters[i].set_markersize(size)
        scatters[i].set_color(color)

        # Update shadow (on ground at z=0)
        shadows[i].set_data([positions[i, 0]], [positions[i, 1]])
        shadows[i].set_3d_properties([0])

        # Update trail line
        trail = trails[i]
        trail_lines[i].set_data(trail[:, 0], trail[:, 1])
        trail_lines[i].set_3d_properties(trail[:, 2])
        trail_lines[i].set_color(color)
        trail_lines[i].set_alpha(0.5)

    return scatters + trail_lines + shadows

# === Run Animation ===
ani = FuncAnimation(fig, update, interval=FRAME_INTERVAL, blit=False, cache_frame_data=False)

plt.show()