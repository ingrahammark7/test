import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Parameters
SPEED = 1.0
TURN_RATE = np.radians(2.5)
WORLD_LIMIT = 30
AVOID_EDGE_DIST = 10
COLLISION_DIST = 3
ENERGY_LOSS_PER_TURN = 0.01
CAMERA_ORBIT_RADIUS = 50
CAMERA_SPEED = 0.02

np.random.seed(42)

# Utility functions
def normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def rotation_matrix(axis, angle):
    axis = normalize(axis)
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    I = np.identity(3)
    return I + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)

# Aircraft class
class Aircraft:
    def __init__(self, position, velocity, color):
        self.position = np.array(position, dtype=float)
        self.velocity = normalize(np.array(velocity, dtype=float)) * SPEED
        self.color = color
        self.trail = [self.position.copy()]
        self.energy = 1.0
        self.alive = True

    def update(self, target_pos):
        if not self.alive:
            return

        to_target = normalize(target_pos - self.position)
        dot = np.dot(self.velocity, to_target)
        if dot < 0.999:
            axis = normalize(np.cross(self.velocity, to_target))
            angle = min(TURN_RATE, np.arccos(dot))
            rot_matrix = rotation_matrix(axis, angle)
            self.velocity = normalize(np.dot(rot_matrix, self.velocity))
            self.energy -= ENERGY_LOSS_PER_TURN * angle / TURN_RATE
            self.energy = max(self.energy, 0.1)

        self.position += self.velocity * self.energy
        self.trail.append(self.position.copy())

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

    def explode(self):
        self.alive = False

# Setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)

ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue')
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red')

p1, = ax.plot([], [], [], 'bo')
p2, = ax.plot([], [], [], 'ro')
t1, = ax.plot([], [], [], 'b-', linewidth=1)
t2, = ax.plot([], [], [], 'r-', linewidth=1)
status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)
explosion_marker, = ax.plot([], [], [], 'y*', markersize=20)

# Animation
def update(frame):
    dist = np.linalg.norm(ac1.position - ac2.position)

    if dist < COLLISION_DIST and ac1.alive and ac2.alive:
        ac1.explode()
        ac2.explode()
        explosion_marker.set_data([ac1.position[0]], [ac1.position[1]])
        explosion_marker.set_3d_properties([ac1.position[2]])
    elif ac1.alive and ac2.alive:
        if dist < 10:
            ac1.update(ac2.position + np.random.normal(scale=1.0, size=3))
            ac2.update(ac1.position + np.random.normal(scale=1.0, size=3))
        else:
            ac1.update(ac2.position)
            ac2.update(ac1.position)

    # Trails
    t1.set_data([p[0] for p in ac1.trail], [p[1] for p in ac1.trail])
    t1.set_3d_properties([p[2] for p in ac1.trail])
    t2.set_data([p[0] for p in ac2.trail], [p[1] for p in ac2.trail])
    t2.set_3d_properties([p[2] for p in ac2.trail])

    # Positions
    p1.set_data([ac1.position[0]], [ac1.position[1]])
    p1.set_3d_properties([ac1.position[2]])
    p2.set_data([ac2.position[0]], [ac2.position[1]])
    p2.set_3d_properties([ac2.position[2]])

    # Camera movement
    cam_angle = frame * CAMERA_SPEED
    ax.view_init(elev=20, azim=np.degrees(cam_angle))

    # HUD
    status_text.set_text(f"Dist: {dist:.1f}\nE1: {ac1.energy:.2f}  E2: {ac2.energy:.2f}")
    return p1, p2, t1, t2, status_text, explosion_marker

ani = FuncAnimation(fig, update, frames=1000, interval=50, blit=False)
plt.show()