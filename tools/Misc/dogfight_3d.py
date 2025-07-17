import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import gc

# Constants
SPEED = 1.0
TURN_RATE = np.radians(2.5)
ENERGY_LOSS_PER_TURN = 0.01
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
TRAIL_FADE_LENGTH = 60  # frames

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
        self.type = aircraft_type
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
        if self.type == "fast":
            self.max_missiles = 2
            self.evasion_chance = 0.5
        else:
            self.max_missiles = 4
            self.evasion_chance = 0.1

    def update(self, enemy):
        if not self.alive:
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

        self.position += self.velocity * self.energy
        self.trail.append(self.position.copy())
        if len(self.trail) > TRAIL_FADE_LENGTH:
            self.trail.pop(0)

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def fire(self, target):
        missile = Missile(self.position.copy(), self.velocity.copy(), target, self.color)
        self.missiles.append(missile)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.explode()

    def explode(self):
        self.alive = False
        self.respawn_timer = 0

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
    for part_name in ['body', 'wing', 'tail', 'engine']:
        if part_name in aircraft.model:
            pts = transform_points(aircraft.model[part_name], aircraft.position, aircraft.velocity)
            poly_pts = [list(pt) for pt in pts] + [list(pts[0])]
            poly = Poly3DCollection([poly_pts], alpha=0.8, facecolor=aircraft.color, edgecolor='k')
            ax.add_collection3d(poly)

def draw_missiles(ax, missiles):
    for m in missiles:
        if len(m.path) >= 2:
            path = np.array(m.path)
            # Missile trail
            ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)
            # Missile tip glow
            ax.scatter(m.position[0], m.position[1], m.position[2], color=m.color, s=50, alpha=0.6)

def draw_trail(ax, trail, color):
    if len(trail) >= 2:
        trail_np = np.array(trail)
        # Trail fades from full color to transparent
        for i in range(len(trail_np) - 1):
            alpha = (i + 1) / len(trail_np)
            ax.plot(trail_np[i:i+2, 0], trail_np[i:i+2, 1], trail_np[i:i+2, 2],
                    color=color, alpha=alpha*0.7, linewidth=2)

def draw_ground_grid(ax):
    # Simple grid on X-Y plane for spatial reference
    grid_range = np.arange(-WORLD_LIMIT, WORLD_LIMIT+1, 5)
    for x in grid_range:
        ax.plot([x]*len(grid_range), grid_range, [0]*len(grid_range), color='gray', alpha=0.1, linewidth=0.5)
    for y in grid_range:
        ax.plot(grid_range, [y]*len(grid_range), [0]*len(grid_range), color='gray', alpha=0.1, linewidth=0.5)

# Sample models (can be replaced with JSON-loaded models)
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

fig = plt.figure(figsize=(10,8))
ax_main = fig.add_subplot(111, projection='3d')

ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue', name='Blue', aircraft_type='fast', model=fighter_models['F-16'])
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red', name='Red', aircraft_type='heavy', model=fighter_models['MiG-21'])

def update(frame):
    ax_main.clear()

    ax_main.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
    ax_main.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
    ax_main.set_zlim(0, WORLD_LIMIT)  # keep above ground
    ax_main.set_title("3D Dogfight Simulation")

    draw_ground_grid(ax_main)

    ac1.update(ac2)
    ac2.update(ac1)

    draw_aircraft(ax_main, ac1)
    draw_aircraft(ax_main, ac2)

    draw_missiles(ax_main, ac1.missiles)
    draw_missiles(ax_main, ac2.missiles)

    draw_trail(ax_main, ac1.trail, ac1.color)
    draw_trail(ax_main, ac2.trail, ac2.color)

    if not ac1.alive and ac1.respawn_timer == 0:
        ac2.score += 1
    if not ac2.alive and ac2.respawn_timer == 0:
        ac1.score += 1

    cam_angle = frame * CAMERA_SPEED
    ax_main.view_init(elev=20, azim=np.degrees(cam_angle))

    status = (
        f"{ac1.name} ({ac1.type}) | HP: {int(ac1.health)} | Score: {ac1.score} | Missiles: {len(ac1.missiles)}\n"
        f"{ac2.name} ({ac2.type}) | HP: {int(ac2.health)} | Score: {ac2.score} | Missiles: {len(ac2.missiles)}"
    )
    ax_main.text2D(0.02, 0.95, status, transform=plt.gcf().transFigure, fontsize=10, color='black')

    gc.collect()
    return []

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()