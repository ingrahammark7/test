import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    return np.array([[a*a + b*b - c*c - d*d, 2*(b*c - a*d),     2*(b*d + a*c)],
                     [2*(b*c + a*d),     a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
                     [2*(b*d - a*c),     2*(c*d + a*b),     a*a + d*d - b*b - c*c]])

class Dogfight3DFullRot:
    def __init__(self):
        self.fig = plt.figure(figsize=(10,8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-30, 30)
        self.ax.set_ylim(-30, 30)
        self.ax.set_zlim(-15, 15)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title("3D Dogfight with Full Rotation (Yaw, Pitch, Roll)")

        # Initial positions (float)
        self.pos1 = np.array([-15.0, 0.0, 0.0], dtype=float)
        self.pos2 = np.array([15.0, 0.0, 0.0], dtype=float)

        # Initial facing directions (normalized)
        self.dir1 = np.array([1.0, 0.0, 0.0], dtype=float)
        self.dir2 = np.array([-1.0, 0.0, 0.0], dtype=float)

        # Speed magnitudes
        self.speed1 = 0.7
        self.speed2 = 0.7

        # Orientation matrices (start aligned with dir vectors)
        # For each aircraft: 3x3 rotation matrix representing body frame relative to world frame
        # Start with identity rotated to initial direction
        self.orient1 = self.direction_to_matrix(self.dir1)
        self.orient2 = self.direction_to_matrix(self.dir2)

        # Angular velocities in radians per frame for yaw, pitch, roll
        # Positive yaw: turn left (CCW looking down Z)
        self.angular_vel1 = np.radians([3, 1, 5])  # yaw, pitch, roll
        self.angular_vel2 = np.radians([-3, -1, -5])

        # Trails for visualization
        self.trail1_x, self.trail1_y, self.trail1_z = [self.pos1[0]], [self.pos1[1]], [self.pos1[2]]
        self.trail2_x, self.trail2_y, self.trail2_z = [self.pos2[0]], [self.pos2[1]], [self.pos2[2]]

        # Plot elements
        self.quiv1 = None
        self.quiv2 = None
        self.trail1_line, = self.ax.plot([], [], [], 'r-', linewidth=1.5, label='Aircraft 1 Trail')
        self.trail2_line, = self.ax.plot([], [], [], 'b-', linewidth=1.5, label='Aircraft 2 Trail')

        self.info_text = self.ax.text2D(0.02, 0.95, "", transform=self.ax.transAxes)
        self.frame_count = 0

    def direction_to_matrix(self, direction):
        """
        Create a rotation matrix for an orientation facing the given direction,
        with 'up' vector roughly along Z-axis.
        """
        forward = direction / np.linalg.norm(direction)
        # Assume global up is Z-axis
        up = np.array([0, 0, 1])
        # Compute right vector (perp to forward and up)
        right = np.cross(up, forward)
        if np.linalg.norm(right) < 1e-6:  # forward and up colinear
            up = np.array([0,1,0])  # choose different up
            right = np.cross(up, forward)
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)
        rot_matrix = np.column_stack((forward, right, up))  # columns are body axes in world frame
        return rot_matrix

    def apply_rotation(self, rot_matrix, angular_vel):
        """
        Apply yaw, pitch, roll rotations in order on rotation matrix.
        angular_vel = (yaw, pitch, roll) in radians/frame
        Yaw around Z (world up), pitch around body right, roll around body forward
        """
        yaw, pitch, roll = angular_vel

        # Yaw: rotate around world Z axis
        R_yaw = rotation_matrix(np.array([0,0,1]), yaw)
        rot_matrix = R_yaw @ rot_matrix

        # Pitch: rotate around body's right axis (2nd column)
        right_axis = rot_matrix[:,1]
        R_pitch = rotation_matrix(right_axis, pitch)
        rot_matrix = R_pitch @ rot_matrix

        # Roll: rotate around body's forward axis (1st column)
        forward_axis = rot_matrix[:,0]
        R_roll = rotation_matrix(forward_axis, roll)
        rot_matrix = R_roll @ rot_matrix

        return rot_matrix

    def update(self, frame):
        self.frame_count += 1

        # Update orientation matrices by angular velocity
        self.orient1 = self.apply_rotation(self.orient1, self.angular_vel1)
        self.orient2 = self.apply_rotation(self.orient2, self.angular_vel2)

        # Velocity = forward vector * speed
        vel1 = self.orient1[:,0] * self.speed1
        vel2 = self.orient2[:,0] * self.speed2

        # Update positions
        self.pos1 += vel1
        self.pos2 += vel2

        # Append trails
        self.trail1_x.append(self.pos1[0])
        self.trail1_y.append(self.pos1[1])
        self.trail1_z.append(self.pos1[2])
        self.trail2_x.append(self.pos2[0])
        self.trail2_y.append(self.pos2[1])
        self.trail2_z.append(self.pos2[2])

        # Limit trail length
        max_trail_len = 60
        if len(self.trail1_x) > max_trail_len:
            self.trail1_x.pop(0)
            self.trail1_y.pop(0)
            self.trail1_z.pop(0)
        if len(self.trail2_x) > max_trail_len:
            self.trail2_x.pop(0)
            self.trail2_y.pop(0)
            self.trail2_z.pop(0)

        # Remove previous arrows
        if self.quiv1:
            self.quiv1.remove()
        if self.quiv2:
            self.quiv2.remove()

        # Draw new velocity arrows
        self.quiv1 = self.ax.quiver(self.pos1[0], self.pos1[1], self.pos1[2],
                                   vel1[0], vel1[1], vel1[2],
                                   length=5, color='red', normalize=True)
        self.quiv2 = self.ax.quiver(self.pos2[0], self.pos2[1], self.pos2[2],
                                   vel2[0], vel2[1], vel2[2],
                                   length=5, color='blue', normalize=True)

        # Update trails
        self.trail1_line.set_data(self.trail1_x, self.trail1_y)
        self.trail1_line.set_3d_properties(self.trail1_z)
        self.trail2_line.set_data(self.trail2_x, self.trail2_y)
        self.trail2_line.set_3d_properties(self.trail2_z)

        # Update info text
        self.info_text.set_text(
            f"Frame: {self.frame_count}\n"
            f"Aircraft 1 Pos: {self.pos1.round(2)}\n"
            f"Aircraft 2 Pos: {self.pos2.round(2)}"
        )

        return self.quiv1, self.quiv2, self.trail1_line, self.trail2_line, self.info_text

    def run(self):
        self.ax.legend()
        self.ani = FuncAnimation(self.fig, self.update, frames=1000, interval=50, blit=False)
        plt.show()

if __name__ == "__main__":
    sim = Dogfight3DFullRot()
    sim.run()