import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class Dogfight3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.pos1 = np.array([10.0, 0.0, 0.0])
        self.pos2 = np.array([-10.0, 0.0, 0.0])
        self.orient1 = np.array([-1.0, 0.2, 0.1])
        self.orient2 = np.array([1.0, -0.1, -0.2])
        self.speed = 0.6

        self.quiv1 = None
        self.quiv2 = None

        self.ax.set_xlim(-40, 40)
        self.ax.set_ylim(-40, 40)
        self.ax.set_zlim(-20, 20)
        self.ax.set_title("3D Dogfight Simulation")

        self.ani = FuncAnimation(self.fig, self.update, interval=50)
        plt.show()

    def steer_towards(self, orient, target_vector):
        turn_rate = 0.04
        new_orient = orient + turn_rate * target_vector
        return new_orient / np.linalg.norm(new_orient)

    def boundary_avoidance(self, pos, orient):
        margin = 5.0
        bounds = {'x': (-40, 40), 'y': (-40, 40), 'z': (-20, 20)}
        steer = np.array([0.0, 0.0, 0.0])

        if pos[0] < bounds['x'][0] + margin:
            steer[0] += 1.0
        elif pos[0] > bounds['x'][1] - margin:
            steer[0] -= 1.0
        if pos[1] < bounds['y'][0] + margin:
            steer[1] += 1.0
        elif pos[1] > bounds['y'][1] - margin:
            steer[1] -= 1.0
        if pos[2] < bounds['z'][0] + margin:
            steer[2] += 1.0
        elif pos[2] > bounds['z'][1] - margin:
            steer[2] -= 1.0

        if np.linalg.norm(steer) > 0:
            steer = steer / np.linalg.norm(steer)
            new_dir = orient + steer * 0.3
            return new_dir / np.linalg.norm(new_dir)
        return orient

    def update(self, frame):
        self.ax.cla()
        self.ax.set_xlim(-40, 40)
        self.ax.set_ylim(-40, 40)
        self.ax.set_zlim(-20, 20)
        self.ax.set_title("3D Dogfight Simulation")

        # Update positions
        self.pos1 += self.orient1 * self.speed
        self.pos2 += self.orient2 * self.speed

        # Adjust orientation with boundary
        self.orient1 = self.boundary_avoidance(self.pos1, self.orient1)
        self.orient2 = self.boundary_avoidance(self.pos2, self.orient2)

        # Steer toward opponent
        vec_to_2 = self.pos2 - self.pos1
        vec_to_1 = self.pos1 - self.pos2
        self.orient1 = self.steer_towards(self.orient1, vec_to_2 / np.linalg.norm(vec_to_2))
        self.orient2 = self.steer_towards(self.orient2, vec_to_1 / np.linalg.norm(vec_to_1))

        # Plot updated positions and directions
        self.ax.quiver(*self.pos1, *self.orient1, color='blue', length=4, normalize=True)
        self.ax.quiver(*self.pos2, *self.orient2, color='red', length=4, normalize=True)
        self.ax.scatter(*self.pos1, color='blue', s=40)
        self.ax.scatter(*self.pos2, color='red', s=40)

Dogfight3D()
