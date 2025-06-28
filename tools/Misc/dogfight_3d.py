
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
import time
import gc
from CameraFocusManager import CameraFocusManager  # Make sure this file is in same dir

# Constants
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

# Helper functions
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

# Classes for Missile, Aircraft, GunParticle as before
class Missile:
    def __init__(self, position, velocity, target, color):
        self.position = np.array(position)
        self.velocity = normalize(velocity) * MISSILE_SPEED
        self.target = target
        self.alive = True
        self.path = [self.position.copy()]
        self.color = color
        self.fuel = 18  # realistic fuel time for missile in frames (~18 frames)

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

        self.fuel -= 1
        if self.fuel <= 0:
            self.alive = False
            return

        if np.linalg.norm(self.position - self.target.position) < MISSILE_HIT_DIST:
            self.target.take_damage(MISSILE_DAMAGE)
            self.alive = False

class GunParticle:
    def __init__(self, position, velocity, lifespan=10):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.lifespan = lifespan
        self.age = 0

    def update(self):
        self.position += self.velocity
        self.age += 1
        return self.age < self.lifespan

class Aircraft:
    def __init__(self, position, velocity, color, name, aircraft_type, model, gun_params):
        self.init_pos = position
        self.init_vel = velocity
        self.color = color
        self.name = name
        self.type = aircraft_type  # "fast" or "heavy"
        self.model = model
        self.gun_params = gun_params  # dict, e.g. {'rate': 0.1, 'range': 5, 'damage': 10, 'particles': 5}
        self.score = 0
        self.reset()
        self.artists = []

    def reset(self):
        self.position = np.array(self.init_pos, dtype=float)
        self.velocity = normalize(np.array(self.init_vel, dtype=float)) * SPEED
        self.trail = [self.position.copy()]
        self.energy = 1.0
        self.health = MAX_HEALTH
        self.alive = True
        self.respawn_timer = 0
        self.missiles = []
        self.gun_cooldown = 0
        self.gun_particles = []
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
        # Missile fire logic
        if dist < 12 and len(self.missiles) < self.max_missiles and np.random.rand() < 0.05:
            self.fire_missile(enemy)

        # Gun fire if lined up (simple dot product check)
        if dist < self.gun_params['range'] and self.gun_cooldown <= 0:
            direction_to_enemy = normalize(to_enemy)
            alignment = np.dot(normalize(self.velocity), direction_to_enemy)
            if alignment > 0.95:  # roughly facing the enemy
                self.fire_gun(direction_to_enemy)
                self.gun_cooldown = int(1 / self.gun_params['rate'])  # cooldown in frames

        if self.gun_cooldown > 0:
            self.gun_cooldown -= 1

        # Evasion or normal target following
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

        # Avoid edges
        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        # Update missiles
        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

        # Update gun particles
        self.gun_particles = [p for p in self.gun_particles if p.update()]

    def fire_missile(self, target):
        missile = Missile(self.position.copy(), self.velocity.copy(), target, self.color)
        self.missiles.append(missile)

    def fire_gun(self, direction):
        # Spawn particles in a cone in front
        count = self.gun_params.get('particles', 5)
        speed = 5
        spread = 0.1
        base_pos = self.position + normalize(self.velocity) * 1.5
        for _ in range(count):
            # random spread direction
            offset = np.random.normal(scale=spread, size=3)
            vel = normalize(direction + offset) * speed
            self.gun_particles.append(GunParticle(base_pos.copy(), vel))

        # Chance to damage enemy if close and aligned
        # This will be handled in main update loop or optionally here

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

def plot_aircraft(ax, aircraft):
    for poly in aircraft.artists:
        poly.remove()
    aircraft.artists.clear()

    for part_name in ['body', 'wing', 'tail', 'engine']:
        if part_name in aircraft.model:
            pts = transform_points(aircraft.model[part_name], aircraft.position, aircraft.velocity)
            poly_pts = [list(pt) for pt in pts] + [list(pts[0])]
            poly = Poly3DCollection([poly_pts], alpha=0.7, facecolor=aircraft.color)
            ax.add_collection3d(poly)
            aircraft.artists.append(poly)

# Sample fighter models JSON (or load from file)
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

# Sample gun parameters by aircraft type (tweak as needed)
gun_parameters = {
    'fast': {'rate': 10, 'range': 5, 'damage': 10, 'particles': 10},  # rate = shots per second (approx)
    'heavy': {'rate': 5, 'range': 7, 'damage': 12, 'particles': 15}
}

# Setup scene
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)

# Create aircraft
ac1 = Aircraft(position=[-10, -10, 0], velocity=[1, 0.5, 0.2], color='blue', name='Blue', aircraft_type='fast', model=fighter_models['F-16'], gun_params=gun_parameters['fast'])
ac2 = Aircraft(position=[10, 10, 0], velocity=[-1, -0.5, 0.2], color='red', name='Red', aircraft_type='heavy', model=fighter_models['MiG-21'], gun_params=gun_parameters['heavy'])

# Plotting helpers
p1 = plt.Line2D([], [], color='blue', marker='o', linestyle='', markersize=8)
p2 = plt.Line2D([], [], color='red', marker='o', linestyle='', markersize=8)
ax.add_line(p1)
ax.add_line(p2)

t1, = ax.plot([], [], [], 'b-', linewidth=1)
t2, = ax.plot([], [], [], 'r-', linewidth=1)
missile_lines = []
gun_particle_lines = []
status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

# Create camera focus manager with both aircraft
camera_manager = CameraFocusManager(ax, [ac1, ac2], missile_lines)

def update(frame):
    global missile_lines, gun_particle_lines, p1, p2

    ac1.update(ac2)
    ac2.update(ac1)

    # Remove old missile lines
    for line in missile_lines:
        line.remove()
    missile_lines.clear()

    # Remove old gun particle lines
    for line in gun_particle_lines:
        line.remove()
    gun_particle_lines.clear()

    # Draw missiles
    for ac in [ac1, ac2]:
        for m in ac.missiles:
            if len(m.path) >= 2:
                path = np.array(m.path)
                l, = ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)
                missile_lines.append(l)

    # Draw gun particles
    for ac in [ac1, ac2]:
        for p in ac.gun_particles:
            l, = ax.plot([p.position[0]], [p.position[1]], [p.position[2]], 'o', color=ac.color, markersize=3, alpha=0.7)
            gun_particle_lines.append(l)

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

    # Points for aircraft centers
    if ac1.alive:
        p1.set_data([ac1.position[0]], [ac1.position[1]])
    if ac2.alive:
        p2.set_data([ac2.position[0]], [ac2.position[1]])

    # Update camera focus and transform
    camera_manager.update(frame)

    gc.collect()

    status = (
        f"{ac1.name} ({ac1.type}) | HP: {ac1.health} | Score: {ac1.score} | Missiles: {len(ac1.missiles)} | Guns: {len(ac1.gun_particles)}\n"
        f"{ac2.name} ({ac2.type}) | HP: {ac2.health} | Score: {ac2.score} | Missiles: {len(ac2.missiles)} | Guns: {len(ac2.gun_particles)}"
    )
    if ac1.score >= VICTORY_SCORE:
        status += "\nBlue Wins!"
    elif ac2.score >= VICTORY_SCORE:
        status += "\nRed Wins!"
    status_text.set_text(status)

    # Return all artists for blitting if needed (set blit=True)
    return [p1, p2, t1, t2, status_text] + missile_lines + gun_particle_lines + ac1.artists + ac2.artists

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()


