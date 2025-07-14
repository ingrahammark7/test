import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Rectangle, Wedge, Ellipse

# === PARAMETERS ===
WIDTH, HEIGHT = 600, 400
NUM_DRONES = 40
DRONE_MAX_SPEED = 6.0
DRONE_MAX_ACCEL = 4.0
LASER_SPEED = 4.0
LASER_LOCK_TIME = 2.0
LASER_RANGE = 180.0
LASER_BEAM_ANGLE_DEG = 12
DT = 0.1

terrain_rects = [
    (150, 100, 80, 15),
    (320, 250, 90, 25),
    (80, 320, 70, 30),
]

terrain_circles = [
    (100, 180, 25),
    (400, 100, 40),
    (250, 350, 30),
]

fog_patches = [
    Ellipse((200, 200), 150, 70, angle=30, color='lightgray', alpha=0.2),
    Ellipse((350, 150), 180, 90, angle=15, color='lightgray', alpha=0.15),
]

laser_power = 5  # Watts emitted by laser pointer
absorptivity = 0.9  # Fraction of laser energy absorbed by drone

MISSION_ZONE = (WIDTH - 50, HEIGHT - 50, 40, 40)  # x, y, w, h
scoreboard = {"escaped": 0, "destroyed": 0}

# === UTILITIES ===
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def interpolate_color(progress):
    if progress < 0.5:
        t = progress / 0.5
        return (t, t, 1 - t)
    else:
        t = (progress - 0.5) / 0.5
        return (1, 1 - t, 0)

# === CLASSES ===
class Explosion:
    def __init__(self, pos):
        self.particles = [self._create_particle(pos) for _ in range(30)]

    def _create_particle(self, pos):
        return {
            'pos': np.array(pos),
            'vel': np.random.uniform(-1, 1, 2) * 5,
            'radius': np.random.uniform(2, 4),
            'alpha': 1.0,
            'life': np.random.randint(20, 40),
            'age': 0,
            'color': (1.0, 0.6 + 0.4*np.random.rand(), 0)
        }

    def update(self):
        new_particles = []
        for p in self.particles:
            p['pos'] += p['vel'] * 0.5
            p['vel'] *= 0.85
            p['age'] += 1
            p['alpha'] = max(0, 1 - p['age'] / p['life'])
            if p['age'] < p['life']:
                new_particles.append(p)
        self.particles = new_particles
        return bool(self.particles)

class Drone:
    def __init__(self):
        self.pos = np.random.rand(2) * [WIDTH, HEIGHT]
        self.velocity = np.zeros(2)
        self.angle = 0
        self.energy = 0
        self.threshold = 10.0
        self.alive = True

    def update(self, lasers):
        if not self.alive:
            return
        evade = np.zeros(2)
        for laser in lasers:
            delta = laser.pos - self.pos
            dist = np.linalg.norm(delta)
            if dist < LASER_RANGE:
                evade -= normalize(delta) / (dist + 1)
        random_dir = np.random.uniform(-1, 1, 2)
        direction = normalize(evade + 0.5 * random_dir)
        desired_velocity = direction * DRONE_MAX_SPEED
        dv = desired_velocity - self.velocity
        self.velocity += normalize(dv) * DRONE_MAX_ACCEL * DT
        self.pos += self.velocity * DT
        self.angle = np.arctan2(self.velocity[1], self.velocity[0])
        self.pos = np.clip(self.pos, [0, 0], [WIDTH, HEIGHT])

    def absorb(self, energy):
        self.energy += energy
        if self.energy >= self.threshold:
            self.alive = False

    def draw(self, ax):
        if not self.alive:
            return
        size = 10
        points = np.array([[size, 0], [-size, size//2], [-size, -size//2]])
        rot = np.array([[np.cos(self.angle), -np.sin(self.angle)], [np.sin(self.angle), np.cos(self.angle)]])
        pts = (points @ rot.T) + self.pos
        color = interpolate_color(self.energy / self.threshold)
        ax.add_patch(Polygon(pts, closed=True, color=color))

class LaserTroop:
    def __init__(self):
        self.pos = np.array([WIDTH/2, HEIGHT/2])
        self.direction = np.array([1.0, 0.0])
        self.lock = {}

    def update(self, drones):
        targets = [d for d in drones if d.alive]
        if not targets:
            return
        closest = min(targets, key=lambda d: np.linalg.norm(d.pos - self.pos))
        vec = closest.pos - self.pos
        self.direction = normalize(vec)
        self.pos += self.direction * LASER_SPEED * DT
        self.pos = np.clip(self.pos, [0, 0], [WIDTH, HEIGHT])

    def draw(self, ax):
        ax.plot(self.pos[0], self.pos[1], 'ro', markersize=10)
        ax.arrow(self.pos[0], self.pos[1],
                 self.direction[0]*20, self.direction[1]*20,
                 head_width=5, color='red', alpha=0.7)

    def fire(self, drones, explosions):
        for drone in drones:
            if not drone.alive:
                continue
            vec = drone.pos - self.pos
            dist = np.linalg.norm(vec)
            if dist > LASER_RANGE:
                continue
            angle = np.arccos(np.clip(np.dot(normalize(self.direction), normalize(vec)), -1, 1))
            if angle < np.deg2rad(LASER_BEAM_ANGLE_DEG):
                drone.absorb(laser_power * absorptivity * DT)
                if drone.energy >= drone.threshold:
                    drone.alive = False
                    explosions.append(Explosion(drone.pos.copy()))

# === SIMULATION SETUP ===
drones = [Drone() for _ in range(NUM_DRONES)]
lasers = [LaserTroop()]
explosions = []

fig, ax = plt.subplots(figsize=(10, 7))

def update(frame):
    ax.clear()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    ax.set_facecolor('lightblue')

    # Terrain
    for x, y, w, h in terrain_rects:
        ax.add_patch(Rectangle((x, y), w, h, color='gray'))
    for cx, cy, r in terrain_circles:
        ax.add_patch(Circle((cx, cy), r, color='dimgray'))
    for fog in fog_patches:
        ax.add_patch(fog)

    # Mission zone
    mx, my, mw, mh = MISSION_ZONE
    ax.add_patch(Rectangle((mx, my), mw, mh, color='green', alpha=0.2))

    # Update
    for laser in lasers:
        laser.update(drones)
    for drone in drones:
        drone.update(lasers)
    for laser in lasers:
        laser.fire(drones, explosions)
    for laser in lasers:
        laser.draw(ax)
    for drone in drones:
        drone.draw(ax)

    # Explosions
    active_explosions = []
    for exp in explosions:
        if exp.update():
            for p in exp.particles:
                ax.add_patch(Circle(p['pos'], p['radius'], color=p['color'], alpha=p['alpha']))
            active_explosions.append(exp)
    explosions[:] = active_explosions

    ax.set_title(f'Drones Alive: {sum(d.alive for d in drones)}')
    ax.axis('off')

ani = FuncAnimation(fig, update, frames=1000, interval=DT*1000)
plt.show()
