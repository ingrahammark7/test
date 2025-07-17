import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import gc

# Constants
SPEED = 1.0
TURN_RATE = np.radians(2.5)
ENERGY_LOSS_PER_TURN = 0.01
ENERGY_RECOVERY = 0.005
WORLD_LIMIT = 30
AVOID_EDGE_DIST = 10
MISSILE_SPEED = 2.0
MISSILE_TURN = np.radians(5)
MISSILE_HIT_DIST = 2.0
MISSILE_DAMAGE = 40
RESPAWN_DELAY = 60
CAMERA_SPEED = 0.02
VICTORY_SCORE = 5
MAX_HEALTH = 100
MAX_TRAIL_LENGTH = 50

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

class Missile:
    def __init__(self, position, velocity, target, color):
        self.position = np.array(position)
        self.velocity = normalize(velocity) * MISSILE_SPEED
        self.target = target
        self.alive = True
        self.path = [self.position.copy()]
        self.color = color

    def update(self):
        if not self.alive or not self.target.alive:
            self.alive = False
            return
        to_target = normalize(self.target.position - self.position)
        axis = normalize(np.cross(self.velocity, to_target))
        angle = np.arccos(np.clip(np.dot(self.velocity, to_target), -1.0, 1.0))
        angle = min(angle, MISSILE_TURN)
        if np.linalg.norm(axis) > 1e-6:
            self.velocity = normalize(np.dot(rotation_matrix(axis, angle), self.velocity))
        self.position += self.velocity
        self.path.append(self.position.copy())

        if np.linalg.norm(self.position - self.target.position) < MISSILE_HIT_DIST:
            self.target.take_damage(MISSILE_DAMAGE)
            self.alive = False

class Aircraft:
    def __init__(self, position, velocity, color, name, aircraft_type, model):
        self.init_pos = position
        self.init_vel = velocity
        self.color = color
        self.name = name
        self.type = aircraft_type  # "fast" or "heavy"
        self.model = model
        self.score = 0
        self.reset()
        self.trail = []

    def reset(self):
        self.position = np.array(self.init_pos, dtype=float)
        self.velocity = normalize(np.array(self.init_vel, dtype=float)) * SPEED
        self.trail = [self.position.copy()]
        self.energy = 1.0
        self.health = MAX_HEALTH
        self.alive = True
        self.respawn_timer = 0
        self.missiles = []
        self.explosion_timer = 0
        self.explosion_pos = None
        if self.type == "fast":
            self.max_missiles = 2
            self.evasion_chance = 0.5
        else:
            self.max_missiles = 4
            self.evasion_chance = 0.1

    def update(self, enemy):
        if not self.alive:
            if self.explosion_timer > 0:
                self.explosion_timer -= 1
            self.respawn_timer += 1
            if self.respawn_timer > RESPAWN_DELAY:
                self.reset()
            return

        to_enemy = enemy.position - self.position
        dist = np.linalg.norm(to_enemy)
        if dist < 12 and len(self.missiles) < self.max_missiles and np.random.rand() < 0.05:
            self.fire(enemy)

        if dist < 5 and np.random.rand() < self.evasion_chance:
            offset = np.random.normal(scale=2.0, size=3)
            target_pos = self.position - to_enemy + offset
        else:
            target_pos = enemy.position

        to_target = normalize(target_pos - self.position)
        dot = np.dot(self.velocity, to_target)
        if dot < 0.999:
            axis = normalize(np.cross(self.velocity, to_target))
            angle = min(TURN_RATE, np.arccos(dot))
            self.velocity = normalize(np.dot(rotation_matrix(axis, angle), self.velocity))
            self.energy -= ENERGY_LOSS_PER_TURN * angle / TURN_RATE
            self.energy = max(self.energy, 0.1)
        else:
            # Recover energy slowly when flying straight
            self.energy = min(self.energy + ENERGY_RECOVERY, 1.0)

        self.position += self.velocity * self.energy
        self.trail.append(self.position.copy())
        if len(self.trail) > MAX_TRAIL_LENGTH:
            self.trail.pop(0)

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def fire(self, target):
        print(f"{self.name} fires missile at {target.name}!")
        missile = Missile(self.position.copy(), self.velocity.copy(), target, self.color)
        self.missiles.append(missile)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and self.alive:
            self.explode()

    def explode(self):
        print(f"{self.name} has been destroyed!")
        self.alive = False
        self.respawn_timer = 0
        self.explosion_timer = 10  # frames to show explosion
        self.explosion_pos = self.position.copy()

def transform_points(points, position, direction):
    forward = normalize(direction)
    if abs(np.dot(forward, np.array([0, 0, 1]))) > 0.99:
        up = np.array([0, 1, 0])
    else:
        up = np.array([0, 0, 1])
    right = np.cross(up, forward)
    right = normalize(right)
    up = np.cross(forward, right)
    rot_matrix = np.column_stack((forward, right, up))
    transformed = [position + rot_matrix @ np.array(p) for p in points]
    return transformed

def draw_aircraft(ax, aircraft):
    # Draw explosion effect if active
    if aircraft.explosion_timer > 0 and aircraft.explosion_pos is not None:
        explosion_radius = (10 - aircraft.explosion_timer) * 0.3
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = explosion_radius * np.cos(u) * np.sin(v) + aircraft.explosion_pos[0]
        y = explosion_radius * np.sin(u) * np.sin(v) + aircraft.explosion_pos[1]
        z = explosion_radius * np.cos(v) + aircraft.explosion_pos[2]
        ax.plot_surface(x, y, z, color='orange', alpha=0.6)

    if not aircraft.alive:
        return

    for part_name in ['body', 'wing', 'tail', 'engine']:
        if part_name in aircraft.model:
            pts = transform_points(aircraft.model[part_name], aircraft.position, aircraft.velocity)
            poly_pts = [list(pt) for pt in pts] + [list(pts[0])]
            poly = Poly3DCollection([poly_pts], alpha=0.7, facecolor=aircraft.color)
            ax.add_collection3d(poly)

def draw_missiles(ax, missiles):
    for m in missiles:
        if len(m.path) >= 2:
            path = np.array(m.path)
            ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)

def draw_trail(ax, trail, color):
    if len(trail) >= 2:
        trail_np = np.array(trail)
        ax.plot(trail_np[:, 0], trail_np[:, 1], trail_np[:, 2], color=color, linewidth=1)

# Sample models (replace with loaded JSON if you want)
fighter_models = {
  "F-16": {
    "body": [[0, 0, 0], [1, 0, 0.1], [3, 0, 0], [1, 0, -0.1]],
    "wing": [[1, -1.5, 0], [2, 0, 0], [1, 1.5, 0]],
    "tail": [[2.8, 0, 0], [3, 0.2, 0.5], [3, -0.2, 0.5]],
    "engine": [[0, -0.2, -0.1], [0, 0.2, -0.1], [-0.5, 0.2, -0.1], [-0.5, -0.2, -0.1]]
  },
  "MiG-21": {
    "body": [[0, 0, 0], [0.5, 0, 0.05], [3, 0, 0], [0.5, 0, -0.05]],
    "wing": [[1.2, -1.2, 0], [2.2, 0, 0], [1.2, 1.2, 0]],
    "tail": [[2.9, 0, 0], [3.1, 0.2, 0.3], [3.1, -0.2, 0.3]],
    "engine": [[-0.4, -0.15, -0.05], [-0.4, 0.15, -0.05], [-0.8, 0.15, -0.05], [-0.8, -0.15, -0.05]]
  }
}

fig = plt.figure()
ax_main = fig.add_subplot(111, projection='3d')

ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue', name='Blue', aircraft_type='fast', model=fighter_models['F-16'])
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red', name='Red', aircraft_type='heavy', model=fighter_models['MiG-21'])

def get_camera_angle(frame):
    period = 200
    angle_range = 45
    phase = (frame % period) / period
    # Oscillate camera angle smoothly between -angle_range/2 and +angle_range/2 degrees
    angle = angle_range * np.sin(2 * np.pi * phase)
    return angle

def update(frame):
    ax_main.clear()  # Clear whole 3D scene

    # Reset limits and title after clear
    ax_main.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
    ax_main.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
    ax_main.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)
    ax_main.set_title("3D Dogfight")

    # Update aircraft state
    ac1.update(ac2)
    ac2.update(ac1)

    # Draw aircraft, missiles, trails
    draw_aircraft(ax_main, ac1)
    draw_aircraft(ax_main, ac2)

    draw_missiles(ax_main, ac1.missiles)
    draw_missiles(ax_main, ac2.missiles)

    draw_trail(ax_main, ac1.trail, ac1.color)
    draw_trail(ax_main, ac2.trail, ac2.color)

    # Score increment on kills
    if not ac1.alive and ac1.respawn_timer == 0:
        ac2.score += 1
    if not ac2.alive and ac2.respawn_timer == 0:
        ac1.score += 1

    # Camera rotation with smooth oscillation
    cam_angle = get_camera_angle(frame)
    ax_main.view_init(elev=20, azim=cam_angle)

    # Display status text with energy added
    status = (
        f"{ac1.name} ({ac1.type}) | HP: {int(ac1.health)} | Energy: {ac1.energy:.2f} | Score: {ac1.score} | Missiles: {len(ac1.missiles)}\n"
        f"{ac2.name} ({ac2.type}) | HP: {int(ac2.health)} | Energy: {ac2.energy:.2f} | Score: {ac2.score} | Missiles: {len(ac2.missiles)}"
    )
    ax_main.text2D(0.05, 0.95, status, transform=plt.gcf().transFigure)

    gc.collect()
    return []

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()