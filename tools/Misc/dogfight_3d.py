import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import random
import gc

# Constants
NUM_PARTICLES = 60
WORLD_LIMIT = 100
TRAIL_LENGTH = 50
ACCEL_LIMIT = 0.3
VEL_LIMIT = 1.5
TURN_DRIFT = 0.05
FORMATION_SCALE = 4.0

# Particle properties
particles = np.zeros((NUM_PARTICLES, 3))
velocities = np.random.randn(NUM_PARTICLES, 3) * 0.1
accelerations = np.zeros((NUM_PARTICLES, 3))
colors = np.tile(np.array([0.0, 1.0, 1.0, 1.0]), (NUM_PARTICLES, 1))
history = np.zeros((NUM_PARTICLES, TRAIL_LENGTH, 3))
ml_vectors = np.random.randn(NUM_PARTICLES, 3) * 0.5  # Simulated learned behavior vector

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def update_ai(i):
    for j in range(NUM_PARTICLES):
        pos = particles[j]
        vel = velocities[j]
        acc = accelerations[j]
        ml_dir = normalize(ml_vectors[j])

        # Flocking behavior simulation
        center = np.mean(particles, axis=0)
        to_center = normalize(center - pos)

        separation = np.zeros(3)
        for k in range(NUM_PARTICLES):
            if k != j:
                diff = particles[j] - particles[k]
                dist = np.linalg.norm(diff)
                if dist < 10:
                    separation += normalize(diff) / (dist + 1e-5)

        alignment = np.mean(velocities, axis=0)
        alignment = normalize(alignment)

        acc = 0.5 * to_center + 0.3 * separation + 0.2 * alignment
        acc += ml_dir * 0.1
        acc += np.random.randn(3) * TURN_DRIFT
        acc = normalize(acc) * ACCEL_LIMIT
        velocities[j] += acc
        speed = np.linalg.norm(velocities[j])
        if speed > VEL_LIMIT:
            velocities[j] = velocities[j] / speed * VEL_LIMIT
        particles[j] += velocities[j]

        # Boundaries
        for d in range(3):
            if particles[j, d] < -WORLD_LIMIT or particles[j, d] > WORLD_LIMIT:
                velocities[j, d] *= -1

        # Trail history
        history[j, :-1] = history[j, 1:]
        history[j, -1] = particles[j]

def update_plot(frame):
    update_ai(frame)
    scat._offsets3d = (particles[:, 0], particles[:, 1], particles[:, 2])
    
    for j in range(NUM_PARTICLES):
        lines[j].set_data(history[j, :, 0], history[j, :, 1])
        lines[j].set_3d_properties(history[j, :, 2])
    
    gc.collect()
    return scat, *lines

# Visualization setup
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_facecolor('black')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.grid(False)

# Particle scatter
scat = ax.scatter(particles[:, 0], particles[:, 1], particles[:, 2],
                  c=colors, s=50, alpha=0.8)

# Trails
lines = [ax.plot([], [], [], color='cyan', alpha=0.3)[0] for _ in range(NUM_PARTICLES)]

ani = FuncAnimation(fig, update_plot, frames=1000, interval=30, blit=False)
plt.show()