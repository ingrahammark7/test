import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

SPEED = 1.0
TURN_RATE = np.radians(2.5)
WORLD_LIMIT = 30
AVOID_EDGE_DIST = 10
MASS = 1000
G = 9.81

def normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def rotation_matrix(axis, angle):
    axis = normalize(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    I = np.identity(3)
    return I + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)

class Aircraft:
    def __init__(self, position, velocity, color):
        self.position = np.array(position, dtype=float)
        self.velocity = normalize(np.array(velocity, dtype=float)) * SPEED
        self.color = color
        self.trail = [self.position.copy()]
        self.energy = 0.0

    def update(self, target_pos):
        to_target = normalize(target_pos - self.position)
        dot = np.dot(self.velocity, to_target)
        if dot < 0.999:
            axis = normalize(np.cross(self.velocity, to_target))
            angle = min(TURN_RATE, np.arccos(dot))
            rot_matrix = rotation_matrix(axis, angle)
            self.velocity = normalize(np.dot(rot_matrix, self.velocity))

        self.position += self.velocity
        self.trail.append(self.position.copy())

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        speed = np.linalg.norm(self.velocity)
        kinetic = 0.5 * MASS * speed ** 2
        potential = MASS * G * self.position[2]
        self.energy = kinetic + potential

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_title("3D Cinematic Dogfight with Energy")

ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue')
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red')

p1, = ax.plot([], [], [], 'bo')
p2, = ax.plot([], [], [], 'ro')
t1, = ax.plot([], [], [], 'b-', linewidth=1)
t2, = ax.plot([], [], [], 'r-', linewidth=1)
energy_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

def update(frame):
    ac1.update(ac2.position)
    ac2.update(ac1.position)

    pos1 = ac1.position
    pos2 = ac2.position

    p1.set_data([pos1[0]], [pos1[1]])
    p1.set_3d_properties([pos1[2]])
    p2.set_data([pos2[0]], [pos2[1]])
    p2.set_3d_properties([pos2[2]])

    t1.set_data([p[0] for p in ac1.trail], [p[1] for p in ac1.trail])
    t1.set_3d_properties([p[2] for p in ac1.trail])
    t2.set_data([p[0] for p in ac2.trail], [p[1] for p in ac2.trail])
    t2.set_3d_properties([p[2] for p in ac2.trail])

    energy_text.set_text("E1: {:.1f} J   E2: {:.1f} J".format(ac1.energy, ac2.energy))

    # Cinematic camera orbit
    elev = 30
    azim = (frame * 0.8) % 360
    ax.view_init(elev=elev, azim=azim)

    return p1, p2, t1, t2, energy_text

ani = FuncAnimation(fig, update, frames=1000, interval=50, blit=False)
plt.show()