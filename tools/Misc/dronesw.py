

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

laser_power = 5.0  # Watts (laser pointer power)
absorptivity = 0.9  # Fraction of laser energy absorbed by drone surface

# --- PHYSICAL CONSTANTS FOR DAMAGE MODEL ---
# Surface absorption layer assumptions for drone material (e.g. aluminum-like)
ABSORPTION_DEPTH = 1e-5  # meters (10 microns, realistic for laser penetration depth)
DRONE_SURFACE_AREA = 0.01  # m² (approximate exposed surface area)
DRONE_SURFACE_DENSITY = 2700  # kg/m³ (aluminum)
DRONE_SURFACE_MASS = DRONE_SURFACE_AREA * ABSORPTION_DEPTH * DRONE_SURFACE_DENSITY  # kg

SPECIFIC_HEAT = 10  # J/kg·K (Aluminum specific heat)
INITIAL_TEMP = 20    # °C ambient temperature
MELTING_TEMP = 660   # °C aluminum melting point
LATENT_HEAT = 3# J/kg aluminum latent heat of fusion (melting)

# Energy to heat + melt the surface layer = mass*c*ΔT + mass*latent heat
ENERGY_TO_MELT_SURFACE = (
    DRONE_SURFACE_MASS * SPECIFIC_HEAT * (MELTING_TEMP - INITIAL_TEMP) +
    DRONE_SURFACE_MASS * LATENT_HEAT
)  # Joules

# For reference:
# DRONE_SURFACE_MASS ≈ 0.00027 kg (0.27 grams)
# ENERGY_TO_MELT_SURFACE ≈ 158 Joules

print(f"Drone surface mass (kg): {DRONE_SURFACE_MASS:.6f}")
print(f"Energy to melt surface layer (J): {ENERGY_TO_MELT_SURFACE:.1f}")

# === UTILITIES ===
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def interpolate_color(progress):
    # Map progress [0,1] to color gradient blue → yellow → red
    if progress < 0.5:
        t = progress / 0.5
        r = t
        g = t
        b = 1 - t
    else:
        t = (progress - 0.5) / 0.5
        r = 1
        g = 1 - t
        b = 0
    return (r, g, b)

# === CLASSES ===
class ExplosionParticle:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.velocity = np.random.uniform(-1,1,2)*3
        self.radius = np.random.uniform(1.5,4)
        self.life = np.random.uniform(20,35)
        self.age = 0
        self.alpha = 1.0
        self.color = (1.0, 0.5 + 0.5*np.random.rand(), 0)  # orange-yellowish

    def update(self):
        self.pos += self.velocity * 0.6
        self.velocity *= 0.85
        self.age += 1
        self.alpha = max(0, 1 - self.age/self.life)
        self.radius *= 0.96
        return self.age < self.life

class Explosion:
    def __init__(self, pos):
        self.particles = [ExplosionParticle(pos) for _ in range(35)]

    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0

class Drone:
    def __init__(self):
        self.pos = np.array([np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)])
        self.velocity = np.zeros(2)
        self.angle = 0
        self.alive = True
        self.damage_energy_threshold = ENERGY_TO_MELT_SURFACE
        self.energy_absorbed = 0.0
        self.cloaked = False
        self.cloak_timer = 0
        self.cloak_duration = np.random.uniform(2, 5)

    def update(self, lasers, drones):
        if not self.alive:
            return

        # Cloak toggle logic (makes drone partially resistant)
        self.cloak_timer += DT
        if self.cloak_timer > self.cloak_duration:
            self.cloaked = not self.cloaked
            self.cloak_timer = 0
            self.cloak_duration = np.random.uniform(2, 5)

        # Predictive evasion from lasers
        evade_force = np.zeros(2)
        for laser in lasers:
            to_laser = laser.pos - self.pos
            dist = np.linalg.norm(to_laser)
            if dist < LASER_RANGE:
                predicted_laser_pos = laser.pos + laser.direction * LASER_SPEED * 0.5
                evade_dir = self.pos - predicted_laser_pos
                evade_dist = np.linalg.norm(evade_dir)
                if evade_dist > 0:
                    evade_force += normalize(evade_dir) / (evade_dist**1.5 + 1e-6)

        # Group cohesion for swarm movement
        neighbor_positions = []
        for d in drones:
            if d is self or not d.alive:
                continue
            if np.linalg.norm(d.pos - self.pos) < 60:
                neighbor_positions.append(d.pos)
        cohesion_force = np.zeros(2)
        if neighbor_positions:
            avg_pos = np.mean(neighbor_positions, axis=0)
            cohesion_dir = avg_pos - self.pos
            cohesion_force = normalize(cohesion_dir) * 0.5

        # Combine forces + randomness
        random_dir = np.random.uniform(-1,1,2)
        move_dir = normalize(evade_force + cohesion_force + 0.3 * random_dir)

        desired_velocity = move_dir * DRONE_MAX_SPEED
        delta_v = desired_velocity - self.velocity
        accel = np.clip(np.linalg.norm(delta_v), 0, DRONE_MAX_ACCEL)
        if np.linalg.norm(delta_v) > 0:
            self.velocity += (delta_v / np.linalg.norm(delta_v)) * accel * DT

        self.pos += self.velocity * DT
        speed = np.linalg.norm(self.velocity)
        if speed > 0.1:
            self.angle = np.arctan2(self.velocity[1], self.velocity[0])

        # Boundaries & terrain avoidance
        self.pos[0] = np.clip(self.pos[0], 0, WIDTH)
        self.pos[1] = np.clip(self.pos[1], 0, HEIGHT)
        for x,y,w,h in terrain_rects:
            if x <= self.pos[0] <= x+w and y <= self.pos[1] <= y+h:
                self.velocity = -self.velocity * 0.5
                self.pos += self.velocity * DT * 2
        for cx,cy,r in terrain_circles:
            if np.linalg.norm(self.pos - np.array([cx,cy])) < r:
                self.velocity = -self.velocity * 0.5
                self.pos += self.velocity * DT * 2

    def absorb_energy(self, energy):
        # Cloak reduces absorption, simulating some shielding or camouflage
        if self.cloaked:
            energy *= 0.3
        self.energy_absorbed += energy
        self.energy_absorbed = min(self.energy_absorbed, self.damage_energy_threshold)

    def draw(self, ax):
        size = 10
        points = np.array([
            [size, 0],
            [-size*0.6, size*0.6],
            [-size*0.6, -size*0.6]
        ])
        c, s = np.cos(self.angle), np.sin(self.angle)
        R = np.array([[c, -s], [s, c]])
        pts_rot = points @ R.T + self.pos

        progress = self.energy_absorbed / self.damage_energy_threshold
        base_color = interpolate_color(progress)
        if self.cloaked:
            base_color = tuple(min(1.0, c+0.4) for c in base_color)
            alpha = 0.6
        else:
            alpha = 1.0

        drone_poly = Polygon(pts_rot, closed=True, color=base_color, alpha=alpha)
        ax.add_patch(drone_poly)

        # Energy bar
        bar_width = 20
        bar_height = 4
        bar_x = self.pos[0] - bar_width/2
        bar_y = self.pos[1] + 15
        ax.add_patch(FancyBboxPatch((bar_x, bar_y), bar_width, bar_height,
                                   boxstyle="round,pad=0.1", linewidth=0, facecolor='gray', alpha=0.5))
        ax.add_patch(FancyBboxPatch((bar_x, bar_y), bar_width*progress, bar_height,
                                   boxstyle="round,pad=0.1", linewidth=0, facecolor=base_color, alpha=alpha))

class LaserTroop:
    def __init__(self):
        while True:
            pos = np.array([np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)])
            if not any((pos[0]>=x and pos[0]<=x+w and pos[1]>=y and pos[1]<=y+h) for x,y,w,h in terrain_rects):
                if all(np.linalg.norm(pos - np.array([cx,cy])) > r for cx,cy,r in terrain_circles):
                    break
        self.pos = pos
        self.direction = np.array([1.0, 0.0])
        self.lock_timers = dict()
        self.angle = 0
        self.pulse = 0.0

    def update(self, drones):
        alive = [d for d in drones if d.alive]
        if not alive:
            return
        dists = [np.linalg.norm(d.pos - self.pos) for d in alive]
        target = alive[np.argmin(dists)]

        vec = target.pos - self.pos
        dist = np.linalg.norm(vec)
        if dist > 0:
            desired_dir = vec / dist
            current_dir = self.direction
            angle_diff = np.arctan2(desired_dir[1], desired_dir[0]) - np.arctan2(current_dir[1], current_dir[0])
            angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi
            max_turn = 0.1
            angle_change = np.clip(angle_diff, -max_turn, max_turn)
            c, s = np.cos(angle_change), np.sin(angle_change)
            R = np.array([[c, -s], [s, c]])
            self.direction = R @ current_dir
            self.direction /= np.linalg.norm(self.direction)
            self.angle = np.arctan2(self.direction[1], self.direction[0])

            new_pos = self.pos + self.direction * LASER_SPEED * DT

            collision = False
            for x,y,w,h in terrain_rects:
                if x <= new_pos[0] <= x+w and y <= new_pos[1] <= y+h:
                    collision = True
                    break
            for cx,cy,r in terrain_circles:
                if np.linalg.norm(new_pos - np.array([cx,cy])) < r:
                    collision = True
                    break
            if not collision:
                self.pos = new_pos

            self.pos[0] = np.clip(self.pos[0], 0, WIDTH)
            self.pos[1] = np.clip(self.pos[1], 0, HEIGHT)

        self.pulse += DT * 10
        if self.pulse > 2*np.pi:
            self.pulse -= 2*np.pi

    def increment_lock(self, drone, dt):
        drone_id = id(drone)
        self.lock_timers[drone_id] = self.lock_timers.get(drone_id, 0) + dt

    def reset_lock(self, drone):
        drone_id = id(drone)
        if drone_id in self.lock_timers:
            del self.lock_timers[drone_id]

    def is_locked(self, drone):
        drone_id = id(drone)
        return self.lock_timers.get(drone_id, 0) >= LASER_LOCK_TIME

    def draw(self, ax):
        # Base dot
        ax.plot(self.pos[0], self.pos[1], 'ro', markersize=10)

        # Glowing aura
        glow = Circle(self.pos, radius=18, color='red', alpha=0.15 + 0.15 * np.sin(self.pulse * 3))
        ax.add_patch(glow)

        # Direction arrow
        dx = np.cos(self.angle) * 25
        dy = np.sin(self.angle) * 25
        ax.arrow(self.pos[0], self.pos[1], dx, dy, head_width=7, head_length=10, fc='red', ec='red', alpha=0.9)

        # Laser flare at tip
        flare_pos = self.pos + np.array([dx, dy])
        flare = Circle(flare_pos, radius=4 + 2 * np.sin(self.pulse * 5), color='yellow', alpha=0.8)
        ax.add_patch(flare)

# === INITIALIZE ===
drones = [Drone() for _ in range(NUM_DRONES)]
lasers = [LaserTroop()]
explosions = []

terrain_patches = [Rectangle((x,y), w, h, color='dimgray', alpha=0.9) for x,y,w,h in terrain_rects]

fig, ax = plt.subplots(figsize=(10,7))

def update(frame):
    ax.clear()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    ax.set_facecolor('lightsteelblue')

    # Draw terrain rectangles
    for patch in terrain_patches:
        ax.add_patch(patch)

    # Draw terrain circles
    for (cx, cy, r) in terrain_circles:
        circle = Circle((cx, cy), r, color='dimgray', alpha=0.85)
        ax.add_patch(circle)

    # Draw fog patches
    for fog in fog_patches:
        ax.add_patch(fog)

    # Update lasers
    for laser in lasers:
        laser.update(drones)

    # Update drones
    for drone in drones:
        drone.update(lasers, drones)

    beam_angle = np.deg2rad(LASER_BEAM_ANGLE_DEG)

    # Laser locking, damage, and visuals
    for laser in lasers:
        # Draw laser cone
        base_angle = np.arctan2(laser.direction[1], laser.direction[0])
        start_angle = np.rad2deg(base_angle - beam_angle)
        end_angle = np.rad2deg(base_angle + beam_angle)
        wedge_alpha = 0.15 + 0.1*np.sin(laser.pulse)
        wedge = Wedge(laser.pos, LASER_RANGE, start_angle, end_angle, color='red', alpha=wedge_alpha)
        ax.add_patch(wedge)

        # Draw laser troop itself
        laser.draw(ax)

        for drone in drones:
            if not drone.alive:
                continue
            vec = drone.pos - laser.pos
            dist = np.linalg.norm(vec)
            if dist > LASER_RANGE:
                laser.reset_lock(drone)
                drone.energy_absorbed = max(0, drone.energy_absorbed - 15 * DT)
                continue

            laser_dir = laser.direction
            vec_dir = vec / dist
            angle = np.arccos(np.clip(np.dot(laser_dir, vec_dir), -1.0, 1.0))

            if angle < beam_angle:
                laser.increment_lock(drone, DT)
                if laser.is_locked(drone):
                    # Energy delivered to drone surface layer per timestep
                    energy_this_step = laser_power * absorptivity * DT
                    drone.absorb_energy(energy_this_step)

                    # Draw thick locking beam
                    ax.plot([laser.pos[0], drone.pos[0]], [laser.pos[1], drone.pos[1]],
                            color='red', linestyle='-', linewidth=3, alpha=0.7)

                    if drone.energy_absorbed >= drone.damage_energy_threshold:
                        drone.alive = False
                        explosions.append(Explosion(drone.pos.copy()))
                        laser.reset_lock(drone)
            else:
                laser.reset_lock(drone)
                drone.energy_absorbed = max(0, drone.energy_absorbed - 10 * DT)

    # Draw drones
    for drone in drones:
        if drone.alive:
            drone.draw(ax)
        else:
            ax.plot(drone.pos[0], drone.pos[1], 'o', color='dimgray', markersize=12, alpha=0.6)

    # Update explosions
    alive_explosions = []
    for explosion in explosions:
        if explosion.update():
            for p in explosion.particles:
                circle = Circle(p.pos, p.radius, color=p.color, alpha=p.alpha)
                ax.add_patch(circle)
            alive_explosions.append(explosion)
    explosions[:] = alive_explosions

    ax.set_title(f'Drone Swarm vs Laser Troops — Drones Alive: {sum(d.alive for d in drones)} | Explosions: {len(explosions)}')

ani = FuncAnimation(fig, update, interval=DT*1000)
plt.show()

