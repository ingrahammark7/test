import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.colors import hsv_to_rgb

# --- Settings ---
NUM_AIRCRAFT = 9  # multiple of 3 for grouping
FRAME_INTERVAL = 50  # ms
TRAIL_LENGTH = 30
WORLD_LIMIT = 40

# --- AI Parameters ---
MAX_SPEED = 2.0
MAX_ACCEL = 0.07
NEIGHBOR_RADIUS = 12.0
SEPARATION_DISTANCE = 5.0
DRAG_FACTOR = 0.95

# --- Obstacles ---
OBSTACLES = [
    {"center": np.array([10, -10, 5]), "radius": 6},
    {"center": np.array([-15, 15, -8]), "radius": 5},
]
OBSTACLE_AVOID_DIST = 8.0

# --- Linear Regression "ML" model placeholder ---
class LinearRegressionModel:
    def __init__(self, input_dim, output_dim):
        np.random.seed(123)
        self.weights = np.random.uniform(-0.3, 0.3, (output_dim, input_dim))
        self.bias = np.random.uniform(-0.05, 0.05, output_dim)

    def predict(self, x):
        return self.weights @ x + self.bias

linreg = LinearRegressionModel(6, 3)

# --- Simulation state ---
np.random.seed(42)
positions = np.random.uniform(-WORLD_LIMIT, WORLD_LIMIT, (NUM_AIRCRAFT, 3))
velocities = np.random.uniform(-1, 1, (NUM_AIRCRAFT, 3))
trails = np.zeros((NUM_AIRCRAFT, TRAIL_LENGTH, 3))

GROUPS = 3
group_ids = np.array([i % GROUPS for i in range(NUM_AIRCRAFT)])

formation_centers = np.array([
    np.array([0.0, 0.0, 0.0]),
    np.array([15.0, 15.0, 5.0]),
    np.array([-15.0, -15.0, -5.0]),
])
formation_velocities = np.array([
    np.array([0.05, 0.04, 0.02]),
    np.array([-0.04, 0.03, -0.02]),
    np.array([0.03, -0.05, 0.01]),
])

behavior_weights = np.ones((NUM_AIRCRAFT, 5))
weight_phases = np.zeros((NUM_AIRCRAFT, 5))
weight_speeds = np.full((NUM_AIRCRAFT, 5), 0.01)

# --- Plot setup ---
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(projection='3d')

ax.set_xlim([-WORLD_LIMIT, WORLD_LIMIT])
ax.set_ylim([-WORLD_LIMIT, WORLD_LIMIT])
ax.set_zlim([-WORLD_LIMIT, WORLD_LIMIT])
ax.grid(False)

# Initial camera angles
cam_elev = 25
cam_azim = 50
cam_azim_speed = 0.3  # degrees per frame

# State toggles
show_trails = True
show_arrows = True

def toggle_trails(event):
    global show_trails
    show_trails = not show_trails

def toggle_arrows(event):
    global show_arrows
    show_arrows = not show_arrows

# Buttons
ax_trails_btn = plt.axes([0.7, 0.02, 0.1, 0.04])
btn_trails = Button(ax_trails_btn, 'Toggle Trails')
btn_trails.on_clicked(toggle_trails)

ax_arrows_btn = plt.axes([0.81, 0.02, 0.1, 0.04])
btn_arrows = Button(ax_arrows_btn, 'Toggle Arrows')
btn_arrows.on_clicked(toggle_arrows)

# Create scatter and trail elements
scatters = []
for _ in range(NUM_AIRCRAFT):
    base = ax.plot([], [], [], 'o', markersize=6, alpha=0.8)[0]
    glow1 = ax.plot([], [], [], 'o', markersize=10, alpha=0.2)[0]
    glow2 = ax.plot([], [], [], 'o', markersize=14, alpha=0.12)[0]
    scatters.append((base, glow1, glow2))

trail_lines = []
for _ in range(NUM_AIRCRAFT):
    line, = ax.plot([], [], [], '-', lw=1, solid_capstyle='round')
    trail_lines.append(line)

shadows = []
for _ in range(NUM_AIRCRAFT):
    shadow = ax.plot([], [], [], 'o', color='gray', markersize=6, alpha=0.3)[0]
    shadows.append(shadow)

arrows = []

def update_trails(trails, positions):
    trails[:, 1:] = trails[:, :-1]
    trails[:, 0] = positions
    return trails

def limit_vector(vec, max_length):
    length = np.linalg.norm(vec)
    if length > max_length:
        return vec / length * max_length
    return vec

def unit_vector(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

def obstacle_avoidance(pos):
    avoidance = np.zeros(3)
    for obs in OBSTACLES:
        offset = pos - obs["center"]
        dist = np.linalg.norm(offset)
        if dist < OBSTACLE_AVOID_DIST and dist > 0:
            avoidance += offset / (dist * dist)
    return avoidance

def simulate_step(frame):
    global positions, velocities, behavior_weights, weight_phases

    # Move formation centers & bounce in bounds
    for g in range(GROUPS):
        formation_centers[g] += formation_velocities[g]
        for i in range(3):
            if formation_centers[g][i] > WORLD_LIMIT or formation_centers[g][i] < -WORLD_LIMIT:
                formation_velocities[g][i] *= -1

    weight_phases[:] += weight_speeds
    behavior_weights[:] = 0.5 + 0.5 * np.sin(weight_phases)

    for i in range(NUM_AIRCRAFT):
        pos = positions[i]
        vel = velocities[i]

        diffs = positions - pos
        distances = np.linalg.norm(diffs, axis=1)
        neighbors_mask = (distances < 12.0) & (distances > 0)
        neighbors = positions[neighbors_mask]
        neighbor_vels = velocities[neighbors_mask]

        center = formation_centers[group_ids[i]]
        to_center = center - pos
        attraction = unit_vector(to_center) if np.linalg.norm(to_center) > 0 else np.zeros(3)

        separation = np.zeros(3)
        close_neighbors = neighbors_mask & (distances < SEPARATION_DISTANCE)
        for j in np.where(close_neighbors)[0]:
            diff = pos - positions[j]
            dist = distances[j]
            if dist > 0:
                separation += diff / (dist * dist)
        separation = unit_vector(separation) if np.linalg.norm(separation) > 0 else np.zeros(3)

        alignment = np.zeros(3)
        if len(neighbor_vels) > 0:
            avg_vel = np.mean(neighbor_vels, axis=0)
            alignment = unit_vector(avg_vel) if np.linalg.norm(avg_vel) > 0 else np.zeros(3)

        wander = np.array([
            np.sin(frame * 0.02 + i),
            np.cos(frame * 0.015 + 2*i),
            np.sin(frame * 0.018 + 3*i)
        ])
        wander = unit_vector(wander)

        avoid = obstacle_avoidance(pos)
        avoid = unit_vector(avoid) if np.linalg.norm(avoid) > 0 else np.zeros(3)

        input_vec = np.concatenate((pos / WORLD_LIMIT, vel / MAX_SPEED))
        ml_accel = linreg.predict(input_vec) * 0.03

        weights = behavior_weights[i]
        accel = (
            attraction * weights[0] +
            separation * weights[1] +
            alignment * weights[2] +
            wander * weights[3] +
            avoid * 1.5 +
            ml_accel
        )
        accel = limit_vector(accel, MAX_ACCEL)

        # Add wind vector as environmental effect
        wind = np.array([
            0.2 * np.sin(frame * 0.01 + pos[1] * 0.1),
            0.1 * np.cos(frame * 0.015 + pos[0] * 0.05),
            0.05 * np.sin(frame * 0.02 + pos[2] * 0.1)
        ])
        accel += wind * 0.1

        velocities[i] += accel
        velocities[i] *= DRAG_FACTOR
        velocities[i] = limit_vector(velocities[i], MAX_SPEED)

        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], -WORLD_LIMIT, WORLD_LIMIT)

    return positions, velocities

# Fog plane (translucent)
fog_alpha = 0.12
fog_plane = ax.plot_surface(
    np.linspace(-WORLD_LIMIT, WORLD_LIMIT, 2).reshape(2,1),
    np.linspace(-WORLD_LIMIT, WORLD_LIMIT, 2).reshape(1,2),
    np.full((2,2), -WORLD_LIMIT),
    color='white', alpha=fog_alpha)

def update(frame):
    global positions, velocities, trails

    positions, velocities = simulate_step(frame)
    trails = update_trails(trails, positions)

    # Orbit camera around z-axis slowly
    global cam_azim
    cam_azim = (cam_azim + cam_azim_speed) % 360
    ax.view_init(elev=cam_elev, azim=cam_azim)

    # Clear arrows
    for arrow in arrows:
        arrow.remove()
    arrows.clear()

    for i in range(NUM_AIRCRAFT):
        speed = np.linalg.norm(velocities[i])
        size_base = max(5, 5 + speed * 8)

        group_hue_base = (group_ids[i] / GROUPS)
        hue = (frame * 0.01 + group_hue_base + i / NUM_AIRCRAFT) % 1.0
        saturation = 0.9
        value = 1.0
        rgb_color = hsv_to_rgb([hue, saturation, value])

        for idx, scatter in enumerate(scatters[i]):
            scatter.set_data([positions[i, 0]], [positions[i, 1]])
            scatter.set_3d_properties([positions[i, 2]])
            scale = size_base * (1 + idx * 1.4)
            scatter.set_markersize(scale)
            scatter.set_color(rgb_color)
            scatter.set_alpha([0.8, 0.22, 0.12][idx])

        altitude = positions[i, 2]
        shadow_size = max(2, 8 - altitude * 0.15)
        shadows[i].set_data([positions[i, 0]], [positions[i, 1]])
        shadows[i].set_3d_properties([0])
        shadows[i].set_markersize(shadow_size)
        shadows[i].set_alpha(0.2 + 0.3 * (altitude < 0))

        if show_trails:
            trail = trails[i]
            trail_lines[i].set_data(trail[:, 0], trail[:, 1])
            trail_lines[i].set_3d_properties(trail[:, 2])
            trail_lines[i].set_color(rgb_color)
            trail_lines[i].set_alpha(0.5)
        else:
            trail_lines[i].set_data([], [])
            trail_lines[i].set_3d_properties([])

        if show_arrows:
            arrow = ax.quiver(
                positions[i, 0], positions[i, 1], positions[i, 2],
                velocities[i, 0], velocities[i, 1], velocities[i, 2],
                length=6, normalize=True, color='white', alpha=0.4
            )
            arrows.append(arrow)

    return [artist for group in scatters for artist in group] + trail_lines + shadows + arrows + [fog_plane]

if __name__ == "__main__":
    ani = FuncAnimation(fig, update, interval=FRAME_INTERVAL, blit=False, cache_frame_data=False)
    plt.show()