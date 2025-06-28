
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
import gc

# Constants (same as your original)
SPEED = 1.0
TURN_RATE = np.radians(2.5)
ENERGY_LOSS_PER_TURN = 0.01
WORLD_LIMIT = 30
AVOID_EDGE_DIST = 10
COLLISION_DIST = 2.5
MISSILE_SPEED = 2.0
MISSILE_TURN = np.radians(5)
MISSILE_HIT_DIST = 2.0
MISSILE_DAMAGE = 40
RESPAWN_DELAY = 60
CAMERA_ORBIT_RADIUS = 50
CAMERA_SPEED = 0.02
SLOWMO_FRAMES = 30
VICTORY_SCORE = 5
MAX_HEALTH = 100
GUN_KILL_CHANCE = 0.1  # Chance to kill if guns fire in range

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
        self.fuel = 18  # realistic limited fuel ticks for turn (adjust as needed)

    def update(self):
        if not self.alive or not self.target.alive or self.fuel <= 0:
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
        self.fuel -= 1

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
        self.model = model  # Loaded polygon model
        self.score = 0
        self.reset()
        self.artists = []  # To keep track of Poly3DCollections
        self.gun_cooldown = 0

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
        self.gun_cooldown = 0

    def update(self, enemy):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer > RESPAWN_DELAY:
                self.reset()
            return

        to_enemy = enemy.position - self.position
        dist = np.linalg.norm(to_enemy)

        # Fire missile if in range and cooldown ok
        if dist < 12 and len(self.missiles) < self.max_missiles and np.random.rand() < 0.05:
            self.fire_missile(enemy)

        # Gun firing logic - simple line-of-sight & cooldown
        if self.gun_cooldown <= 0 and dist < 3:
            # Check alignment by dot product of velocities
            dir_to_enemy = normalize(to_enemy)
            forward = normalize(self.velocity)
            alignment = np.dot(forward, dir_to_enemy)
            if alignment > 0.95:
                # Guns fire - simple kill chance roll
                if np.random.rand() < GUN_KILL_CHANCE:
                    enemy.take_damage(50)
                self.gun_cooldown = 10  # cooldown frames

        self.gun_cooldown = max(0, self.gun_cooldown - 1)

        # Movement & evasion
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

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def fire_missile(self, target):
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
    # To avoid singularity if forward is close to Z-axis
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

def plot_aircraft(ax, aircraft):
    # Remove old polygons
    for poly in aircraft.artists:
        poly.remove()
    aircraft.artists.clear()

    # Draw polygons for each part
    for part_name in ['body', 'wing', 'tail', 'engine']:
        if part_name in aircraft.model:
            pts = transform_points(aircraft.model[part_name], aircraft.position, aircraft.velocity)
            poly_pts = [list(pt) for pt in pts] + [list(pts[0])]  # Close polygon
            poly = Poly3DCollection([poly_pts], alpha=0.7, facecolor=aircraft.color)
            ax.add_collection3d(poly)
            aircraft.artists.append(poly)

# Load fighter models JSON (place this file in the same directory or inline)
fighter_models_json = """
{
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
"""
fighter_models = json.loads(fighter_models_json)

# Setup scene
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)

# Create aircraft with models
ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue', name='Blue', aircraft_type='fast', model=fighter_models['F-16'])
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red', name='Red', aircraft_type='heavy', model=fighter_models['MiG-21'])

# Replace Line2D with scatter for 3D points
p1 = ax.scatter([], [], [], color='blue', s=50)
p2 = ax.scatter([], [], [], color='red', s=50)

t1, = ax.plot([], [], [], 'b-', linewidth=1)
t2, = ax.plot([], [], [], 'r-', linewidth=1)
missile_lines = []
status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

def update(frame):
    global missile_lines

    ac1.update(ac2)
    ac2.update(ac1)

    for line in missile_lines:
        line.remove()
    missile_lines = []
    for ac in [ac1, ac2]:
        for m in ac.missiles:
            if len(m.path) >= 2:
                path = np.array(m.path)
                l, = ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)
                missile_lines.append(l)

    # Update aircraft models
    plot_aircraft(ax, ac1)
    plot_aircraft(ax, ac2)

    # Scoring
    if not ac1.alive and ac1.respawn_timer == 0:
        ac2.score += 1
    if not ac2.alive and ac2.respawn_timer == 0:
        ac1.score += 1

    # Trails
    t1.set_data([p[0] for p in ac1.trail], [p[1] for p in ac1.trail])
    t1.set_3d_properties([p[2] for p in ac1.trail])
    t2.set_data([p[0] for p in ac2.trail], [p[1] for p in ac2.trail])
    t2.set_3d_properties([p[2] for p in ac2.trail])

    # Points for aircraft centers using scatter offsets3d
    if ac1.alive:
        p1._offsets3d = ([ac1.position[0]], [ac1.position[1]], [ac1.position[2]])
    if ac2.alive:
        p2._offsets3d = ([ac2.position[0]], [ac2.position[1]], [ac2.position[2]])

    # Camera rotation
    cam_angle = frame * CAMERA_SPEED
    ax.view_init(elev=20, azim=np.degrees(cam_angle))
    gc.collect()

    status = (
        f"{ac1.name} ({ac1.type}) | HP: {ac1.health} | Score: {ac1.score} | Missiles: {len(ac1.missiles)}\n"
        f"{ac2.name} ({ac2.type}) | HP: {ac2.health} | Score: {ac2.score} | Missiles: {len(ac2.missiles)}"
    )
    if ac1.score >= VICTORY_SCORE:
        status += "\nBlue Wins!"
    elif ac2.score >= VICTORY_SCORE:
        status += "\nRed Wins!"
    status_text.set_text(status)

    return [p1, p2, t1, t2, status_text] + missile_lines + ac1.artists + ac2.artists

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()


