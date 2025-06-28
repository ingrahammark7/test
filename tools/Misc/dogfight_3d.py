import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
import gc

# Constants
SPEED = 1.0
TURN_RATE = np.radians(2.5)
ENERGY_LOSS_PER_TURN = 0.01
WORLD_LIMIT = 30
AVOID_EDGE_DIST = 10
COLLISION_DIST = 2.5
MISSILE_SPEED = 400.0
MISSILE_TURN = np.radians(5)
MISSILE_HIT_DIST = 2.0
MISSILE_DAMAGE = 40
MISSILE_MASS = 200.0
MISSILE_TOTAL_TURN_ENERGY = 300e6
MISSILE_MAX_RANGE = 2000
MISSILE_BURN_FRAMES = 90
RESPAWN_DELAY = 60
CAMERA_ORBIT_RADIUS = 50
CAMERA_SPEED = 0.02
SLOWMO_FRAMES = 30
VICTORY_SCORE = 5
MAX_HEALTH = 100
MAX_TRAIL = 200
MAX_PATH = 100

# Gun parameters
GUN_FIRE_PROB = 0.2
GUN_RANGE = 400.0
GUN_ARC_COS = 0.98
GUN_DAMAGE = 4
GUN_FLASH_DURATION = 3  # frames

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

class Missile:
    def __init__(self, position, velocity, target, color):
        self.position = np.array(position)
        self.velocity = normalize(velocity) * MISSILE_SPEED
        self.target = target
        self.alive = True
        self.path = [self.position.copy()]
        self.color = color
        self.fuel = MISSILE_TOTAL_TURN_ENERGY
        self.burn_frames = MISSILE_BURN_FRAMES
        self.range_left = MISSILE_MAX_RANGE

    def update(self):
        if not self.alive or not self.target.alive:
            self.alive = False
            return

        if self.burn_frames > 0:
            to_target = normalize(self.target.position - self.position)
            dot = np.clip(np.dot(self.velocity, to_target), -1.0, 1.0)
            angle = np.arccos(dot)
            if angle > 1e-3:
                axis = normalize(np.cross(self.velocity, to_target))
                turn_angle = min(angle, MISSILE_TURN)
                self.velocity = normalize(rotation_matrix(axis, turn_angle) @ self.velocity)
                turn_work = 0.5 * MISSILE_MASS * (MISSILE_SPEED ** 2) * (turn_angle / (2 * np.pi))
                self.fuel -= turn_work
                self.burn_frames -= 1
                if self.fuel <= 0:
                    self.burn_frames = 0

        self.position += self.velocity / 20.0
        self.path.append(self.position.copy())
        self.path = self.path[-MAX_PATH:]
        self.range_left -= np.linalg.norm(self.velocity) / 20.0

        if self.range_left <= 0:
            self.alive = False

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
        self.poly_artists = []
        self.reset()

    def reset(self):
        self.position = np.array(self.init_pos, dtype=float)
        self.velocity = normalize(np.array(self.init_vel, dtype=float)) * SPEED
        self.trail = [self.position.copy()]
        self.energy = 1.0
        self.health = MAX_HEALTH
        self.alive = True
        self.respawn_timer = 0
        self.missiles = []
        self.gun_flash_timer = 0  # For simple gun flash animation
        if self.type == "fast":
            self.max_missiles = 2
            self.evasion_chance = 0.5
        else:
            self.max_missiles = 4
            self.evasion_chance = 0.1

    def update(self, enemy):
        global kill_message, kill_message_timer
        if not self.alive:
            self.respawn_timer += 1
            if self.respawn_timer > RESPAWN_DELAY:
                self.reset()
            return

        to_enemy = enemy.position - self.position
        dist = np.linalg.norm(to_enemy)
        if dist < 12 and len(self.missiles) < self.max_missiles and np.random.rand() < 0.05:
            self.fire(enemy)

        # Gun fire: simple flash + damage
        alignment = np.dot(normalize(self.velocity), normalize(to_enemy))
        if alignment > GUN_ARC_COS and dist < GUN_RANGE and np.random.rand() < GUN_FIRE_PROB:
            enemy.take_damage(GUN_DAMAGE)
            self.gun_flash_timer = GUN_FLASH_DURATION

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
        self.trail = self.trail[-MAX_TRAIL:]

        for i in range(3):
            if abs(self.position[i]) > WORLD_LIMIT - AVOID_EDGE_DIST:
                self.velocity[i] -= 0.1 * np.sign(self.position[i])

        for m in self.missiles:
            m.update()
        self.missiles = [m for m in self.missiles if m.alive]

    def fire(self, target):
        self.missiles.append(Missile(self.position.copy(), self.velocity.copy(), target, self.color))

    def take_damage(self, amount):
        global kill_message, kill_message_timer
        self.health -= amount
        if self.health <= 0:
            self.explode()
            kill_message = f"{self.name} KILLED!"
            kill_message_timer = 50  # show for ~2.5 seconds

    def explode(self):
        self.alive = False
        self.respawn_timer = 0

def transform_points(points, position, direction):
    forward = normalize(direction)
    up = np.array([0, 1, 0]) if abs(np.dot(forward, [0, 0, 1])) > 0.99 else np.array([0, 0, 1])
    right = normalize(np.cross(up, forward))
    up = np.cross(forward, right)
    rot_matrix = np.column_stack((forward, right, up))
    return [position + rot_matrix @ np.array(p) for p in points]

def plot_aircraft(ax, aircraft):
    if not aircraft.poly_artists:
        for part in aircraft.model.values():
            poly = Poly3DCollection([[[0, 0, 0]]], facecolor=aircraft.color, alpha=0.7)
            ax.add_collection3d(poly)
            aircraft.poly_artists.append(poly)

    for poly, part in zip(aircraft.poly_artists, aircraft.model.values()):
        pts = transform_points(part, aircraft.position, aircraft.velocity)
        poly.set_verts([pts + [pts[0]]])

fighter_models = json.loads("""
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
""")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_ylim(-WORLD_LIMIT, WORLD_LIMIT)
ax.set_zlim(-WORLD_LIMIT, WORLD_LIMIT)

ac1 = Aircraft([-10, -10, 0], [1, 0.5, 0.2], 'blue', 'Blue', 'fast', fighter_models['F-16'])
ac2 = Aircraft([10, 10, 0], [-1, -0.5, 0.2], 'red', 'Red', 'heavy', fighter_models['MiG-21'])

t1, = ax.plot([], [], [], 'b-', linewidth=1)
t2, = ax.plot([], [], [], 'r-', linewidth=1)
missile_lines = []
gun_flash_dots = []
status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

kill_message = ""
kill_message_timer = 0

def update(frame):
    global missile_lines, gun_flash_dots, kill_message, kill_message_timer

    # Remove old missile lines
    for line in missile_lines:
        line.remove()
    missile_lines.clear()

    # Remove old gun flashes
    for dot in gun_flash_dots:
        dot.remove()
    gun_flash_dots.clear()

    ac1.update(ac2)
    ac2.update(ac1)

    gun_flashes = []
    for ac in [ac1, ac2]:
        if ac.gun_flash_timer > 0:
            flash_pos = ac.position + normalize(ac.velocity) * 1.5
            dot, = ax.plot([flash_pos[0]], [flash_pos[1]], [flash_pos[2]], 'yo', markersize=8)
            gun_flash_dots.append(dot)
            ac.gun_flash_timer -= 1

    for ac in [ac1, ac2]:
        for m in ac.missiles:
            if len(m.path) >= 2:
                path = np.array(m.path)
                l, = ax.plot(path[:, 0], path[:, 1], path[:, 2], color=m.color, linestyle='--', linewidth=1)
                missile_lines.append(l)

    plot_aircraft(ax, ac1)
    plot_aircraft(ax, ac2)

    if not ac1.alive and ac1.respawn_timer == 0:
        ac2.score += 1
    if not ac2.alive and ac2.respawn_timer == 0:
        ac1.score += 1

    t1.set_data([p[0] for p in ac1.trail], [p[1] for p in ac1.trail])
    t1.set_3d_properties([p[2] for p in ac1.trail])
    t2.set_data([p[0] for p in ac2.trail], [p[1] for p in ac2.trail])
    t2.set_3d_properties([p[2] for p in ac2.trail])

    cam_angle = frame * CAMERA_SPEED
    ax.view_init(elev=20, azim=np.degrees(cam_angle))

    status = (
        f"{ac1.name} ({ac1.type}) | HP: {ac1.health} | Score: {ac1.score} | Missiles: {len(ac1.missiles)}\n"
        f"{ac2.name} ({ac2.type}) | HP: {ac2.health} | Score: {ac2.score} | Missiles: {len(ac2.missiles)}"
    )

    if kill_message_timer > 0:
        status_text.set_text(status + "\n\n" + kill_message)
        kill_message_timer -= 1
    else:
        status_text.set_text(status)

    return [t1, t2, status_text] + missile_lines + gun_flash_dots + ac1.poly_artists + ac2.poly_artists

ani = FuncAnimation(fig, update, frames=2000, interval=50, blit=False)
plt.show()