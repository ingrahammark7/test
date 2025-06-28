# dogfight_3d.py (Battle Royale with guns and metadata support)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json, random, gc

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
CAMERA_SPEED = 0.01
VICTORY_SCORE = 3
MAX_HEALTH = 100
GUN_RANGE = 5.0
GUN_ARC_COS = 0.985
GUN_HIT_PROB = 0.3
GUN_TRACE_LIFETIME = 5

with open("fightermodels.json") as f:
    fighter_models = json.load(f)
with open("fighters.json") as f:
    fighter_metadata = json.load(f)

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
        self.lifetime = 180

    def update(self):
        if not self.alive or not self.target.alive or self.lifetime <= 0:
            self.alive = False
            return
        to_target = normalize(self.target.position - self.position)
        axis = normalize(np.cross(self.velocity, to_target))
        angle = min(np.arccos(np.clip(np.dot(self.velocity, to_target), -1.0, 1.0)), MISSILE_TURN)
        if np.linalg.norm(axis) > 1e-6:
            self.velocity = normalize(rotation_matrix(axis, angle) @ self.velocity)
        self.position += self.velocity
        self.path.append(self.position.copy())
        self.lifetime -= 1
        if np.linalg.norm(self.position - self.target.position) < MISSILE_HIT_DIST:
            self.target.take_damage(MISSILE_DAMAGE)
            self.alive = False

class Aircraft:
    def __init__(self, name, position, velocity, color, aircraft_type, model):
        self.name = name
        self.init_pos = position
        self.init_vel = velocity
        self.color = color
        self.type = aircraft_type
        self.model = model
        self.score = 0
        self.reset()
        self.artists = []
        self.gun_traces = []

    def reset(self):
        self.position = np.array(self.init_pos, dtype=float)
        self.velocity = normalize(np.array(self.init_vel, dtype=float)) * SPEED
        self.trail = [self.position.copy()]
        self.energy = 1.0
        self.health = MAX_HEALTH
        self.alive = True
        self.respawn_timer = 0
        self.missiles = []
        self.max_missiles = 2 if self.type == "fast" else 4
        self.evasion_chance = 0.5 if self.type == "fast" else 0.1

    def update(self, enemies):
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer > RESPAWN_DELAY:
                self.reset()
            return
        enemies_alive = [e for e in enemies if e.alive and e != self]
        if not enemies_alive: return
        target = min(enemies_alive, key=lambda e: np.linalg.norm(e.position - self.position))
        to_target = target.position - self.position
        dist = np.linalg.norm(to_target)

        # Guns
        aim_dot = np.dot(normalize(self.velocity), normalize(to_target))
        if dist < GUN_RANGE and aim_dot > GUN_ARC_COS:
            if random.random() < GUN_HIT_PROB:
                target.take_damage(10)
            self.gun_traces.append([self.position.copy(), target.position.copy(), GUN_TRACE_LIFETIME])

        # Missiles
        if dist < 12 and len(self.missiles) < self.max_missiles and random.random() < 0.05:
            self.missiles.append(Missile(self.position.copy(), self.velocity.copy(), target, self.color))

        if dist < 5 and random.random() < self.evasion_chance:
            target_pos = self.position - to_target + np.random.normal(scale=2.0, size=3)
        else:
            target_pos = target.position

        steer = normalize(target_pos - self.position)
        axis = normalize(np.cross(self.velocity, steer))
        angle = min(TURN_RATE, np.arccos(np.clip(np.dot(self.velocity, steer), -1.0, 1.0)))
        if np.linalg.norm(axis) > 1e-6:
            self.velocity = normalize(rotation_matrix(axis, angle) @ self.velocity)
            self.energy = max(self.energy - ENERGY_LOSS_PER_TURN * angle / TURN_RATE, 0.1)

        self.position += self.velocity * self.energy
        self.trail.append(self.position.copy())

        for m in self.missiles: m.update()
        self.missiles = [m for m in self.missiles if m.alive]
        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        for trace in self.gun_traces: trace[2] -= 1
        self.gun_traces = [t for t in self.gun_traces if t[2] > 0]

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.respawn_timer = 0

def transform_points(points, pos, dir):
    forward = normalize(dir)
    up = np.array([0, 1, 0]) if abs(np.dot(forward, [0, 0, 1])) > 0.99 else np.array([0, 0, 1])
    right = normalize(np.cross(up, forward))
    up = np.cross(forward, right)
    rot = np.column_stack((forward, right, up))
    return [pos + rot @ np.array(p) for p in points]

def plot_aircraft(ax, ac):
    for poly in ac.artists: poly.remove()
    ac.artists.clear()
    for part in ["body", "wing", "tail", "engine"]:
        if part in ac.model:
            pts = transform_points(ac.model[part], ac.position, ac.velocity)
            poly = Poly3DCollection([pts], alpha=0.7, facecolor=ac.color)
            ax.add_collection3d(poly)
            ac.artists.append(poly)

# Game setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)

colors = ['red','blue','green','orange','purple','cyan','magenta','yellow']
plane_names = list(fighter_models.keys())
N = 6
planes = []
for i in range(N):
    name = random.choice(plane_names)
    meta = fighter_metadata.get(name, {})
    ac = Aircraft(
        name=name,
        position=np.random.uniform(-15, 15, size=3),
        velocity=normalize(np.random.normal(size=3)),
        color=colors[i % len(colors)],
        aircraft_type="fast" if meta.get("in_service", 1980) > 1970 else "heavy",
        model=fighter_models[name]
    )
    planes.append(ac)

status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)
missile_lines = []
gun_lines = []
trails = [ax.plot([], [], [], c.color, lw=1)[0] for c in planes]

def update(frame):
    global missile_lines, gun_lines
    for ac in planes: ac.update(planes)
    for l in missile_lines + gun_lines: l.remove()
    missile_lines.clear(); gun_lines.clear()
    for i, ac in enumerate(planes):
        plot_aircraft(ax, ac)
        trails[i].set_data([p[0] for p in ac.trail], [p[1] for p in ac.trail])
        trails[i].set_3d_properties([p[2] for p in ac.trail])
        for m in ac.missiles:
            if len(m.path) >= 2:
                path = np.array(m.path)
                l, = ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)
                missile_lines.append(l)
        for trace in ac.gun_traces:
            pts = np.array([trace[0], trace[1]])
            g, = ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=ac.color, linestyle='-', linewidth=0.5)
            gun_lines.append(g)

    alive = [p.name for p in planes if p.alive]
    if len(alive) == 1:
        status_text.set_text(f"Winner: {alive[0]}")
    else:
        status_text.set_text("Alive: " + ", ".join(alive))

    ax.view_init(elev=20, azim=frame * CAMERA_SPEED * 60)
    gc.collect()
    return missile_lines + gun_lines + [status_text] + [t for t in trails] + [a for p in planes for a in p.artists]

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()


