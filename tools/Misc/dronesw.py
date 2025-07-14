import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Rectangle, Wedge, Ellipse
from matplotlib.colors import LinearSegmentedColormap

# === PARAMETERS ===
WIDTH, HEIGHT = 700, 450
NUM_DRONES = 40
DRONE_MAX_SPEED = 5.0
DRONE_MAX_ACCEL = 3.0
LASER_SPEED = 3.5
LASER_LOCK_TIME = 1.8
LASER_RANGE = 180.0
LASER_BEAM_ANGLE_DEG = 14
DT = 0.1

# Terrain shapes with gradual coloring & shadows
terrain_rects = [
    (160, 110, 90, 20, (0.25, 0.35, 0.10)),  # dark olive green soil patch
    (330, 260, 110, 35, (0.30, 0.45, 0.12)), 
    (90, 335, 80, 40, (0.28, 0.40, 0.13)),
]

terrain_circles = [
    (110, 190, 28, (0.20, 0.45, 0.12)),  # forest patch
    (410, 110, 45, (0.35, 0.30, 0.15)),
    (260, 370, 35, (0.23, 0.40, 0.10)),
]

fog_patches = [
    Ellipse((210, 210), 180, 85, angle=30, color='lightsteelblue', alpha=0.12),
    Ellipse((365, 170), 200, 100, angle=15, color='lightsteelblue', alpha=0.10),
]

# Mission zone - drone target area (green patch)
MISSION_ZONE = (WIDTH - 80, HEIGHT - 80, 60, 60)  # x, y, w, h

laser_power = 5  # Watts emitted by laser pointer
absorptivity = 0.9  # Fraction of laser energy absorbed by drone

scoreboard = {"escaped": 0, "destroyed": 0}

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

def line_of_sight(start, end, terrain_rects, terrain_circles, step=4):
    # Check if line start->end intersects terrain
    vec = end - start
    dist = np.linalg.norm(vec)
    if dist == 0:
        return True
    dir = vec / dist
    steps = int(dist / step)
    for i in range(1, steps+1):
        point = start + dir * i * step
        x, y = point
        # Rect check
        for rx, ry, rw, rh, _ in terrain_rects:
            if rx <= x <= rx + rw and ry <= y <= ry + rh:
                return False
        # Circle check
        for cx, cy, r, _ in terrain_circles:
            if np.linalg.norm(point - np.array([cx, cy])) < r:
                return False
    return True

# === CLASSES ===
class ExplosionParticle:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.velocity = np.random.uniform(-1,1,2)*3
        self.radius = np.random.uniform(2.5,5)
        self.life = np.random.uniform(25,40)
        self.age = 0
        self.alpha = 1.0
        self.color = (1.0, 0.6 + 0.4*np.random.rand(), 0)  # bright orange-yellowish

    def update(self):
        self.pos += self.velocity * 0.7
        self.velocity *= 0.85
        self.age += 1
        self.alpha = max(0, 1 - self.age/self.life)
        self.radius *= 0.94
        return self.age < self.life

class Explosion:
    def __init__(self, pos):
        self.particles = [ExplosionParticle(pos) for _ in range(45)]

    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0

class Drone:
    def __init__(self):
        self.pos = np.array([np.random.uniform(0, WIDTH/3), np.random.uniform(0, HEIGHT)])
        self.velocity = np.zeros(2)
        self.angle = 0
        self.alive = True
        self.energy_absorbed = 0.0
        self.damage_energy_threshold = 9.0
        self.cloaked = False
        self.cloak_cooldown = 0
        self.cloak_duration = 0
        self.cloak_max_duration = 1.8
        self.spread_dir = np.random.uniform(-1,1,2)

    def update(self, lasers, drones):
        if not self.alive:
            return
        
        # Cloak cooldown logic
        if self.cloak_cooldown > 0:
            self.cloak_cooldown -= DT
        else:
            # Chance to activate cloak if laser nearby
            for laser in lasers:
                if np.linalg.norm(laser.pos - self.pos) < LASER_RANGE:
                    if np.random.rand() < 0.015:
                        self.cloaked = True
                        self.cloak_duration = self.cloak_max_duration
                        self.cloak_cooldown = 5.0
                        break

        if self.cloaked:
            self.cloak_duration -= DT
            if self.cloak_duration <= 0:
                self.cloaked = False
        
        # Evade lasers if visible
        evade_force = np.zeros(2)
        for laser in lasers:
            vec_to_laser = laser.pos - self.pos
            dist = np.linalg.norm(vec_to_laser)
            if dist > LASER_RANGE:
                continue
            # Check LOS for laser detection
            if not line_of_sight(laser.pos, self.pos, terrain_rects, terrain_circles):
                continue
            # Add evade force away from laser if laser roughly facing drone
            laser_facing = laser.direction
            drone_dir = normalize(self.pos - laser.pos)
            angle_to_laser = np.arccos(np.clip(np.dot(laser_facing, drone_dir), -1, 1))
            if angle_to_laser < np.deg2rad(LASER_BEAM_ANGLE_DEG + 15):
                evade_force -= normalize(vec_to_laser) / (dist ** 1.4 + 1e-8)
        
        # Seek mission zone if low damage or cloaked
        to_mission = np.array([MISSION_ZONE[0] + MISSION_ZONE[2]/2, MISSION_ZONE[1] + MISSION_ZONE[3]/2]) - self.pos

        # Seek cover if threatened: move toward nearest terrain patch edge
        cover_force = np.zeros(2)
        threat_level = self.energy_absorbed / self.damage_energy_threshold + (1 if self.cloaked else 0)
        if threat_level > 0.3:
            cover_points = []
            # Gather edges of terrain rectangles (corners)
            for rx, ry, rw, rh, _ in terrain_rects:
                cover_points.extend([
                    np.array([rx, ry]),
                    np.array([rx+rw, ry]),
                    np.array([rx, ry+rh]),
                    np.array([rx+rw, ry+rh]),
                ])
            # Gather perimeter points on terrain circles (approximate as 8 points per circle)
            for cx, cy, r, _ in terrain_circles:
                for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
                    cover_points.append(np.array([cx + r*np.cos(a), cy + r*np.sin(a)]))
            # Select closest cover point
            cover_points = np.array(cover_points)
            dists = np.linalg.norm(cover_points - self.pos, axis=1)
            nearest_cover = cover_points[np.argmin(dists)]
            cover_force = normalize(nearest_cover - self.pos) * 1.5

        # Combine movement vectors with some randomness and spread
        move_dir = normalize(evade_force + cover_force + 0.9*normalize(to_mission) + 0.2*self.spread_dir)

        desired_velocity = move_dir * DRONE_MAX_SPEED
        delta_v = desired_velocity - self.velocity
        accel = np.clip(np.linalg.norm(delta_v), 0, DRONE_MAX_ACCEL)
        if np.linalg.norm(delta_v) > 0:
            self.velocity += (delta_v / np.linalg.norm(delta_v)) * accel * DT
        
        self.pos += self.velocity * DT

        speed = np.linalg.norm(self.velocity)
        if speed > 0.1:
            self.angle = np.arctan2(self.velocity[1], self.velocity[0])

        # Keep in bounds
        self.pos[0] = np.clip(self.pos[0], 0, WIDTH)
        self.pos[1] = np.clip(self.pos[1], 0, HEIGHT)

        # Terrain collision - bounce
        for rx, ry, rw, rh, _ in terrain_rects:
            if rx <= self.pos[0] <= rx + rw and ry <= self.pos[1] <= ry + rh:
                self.velocity = -self.velocity * 0.4
                self.pos += self.velocity * DT * 2
        for cx, cy, r, _ in terrain_circles:
            if np.linalg.norm(self.pos - np.array([cx, cy])) < r:
                self.velocity = -self.velocity * 0.4
                self.pos += self.velocity * DT * 2

        # Check escape mission zone
        if (MISSION_ZONE[0] <= self.pos[0] <= MISSION_ZONE[0] + MISSION_ZONE[2]
            and MISSION_ZONE[1] <= self.pos[1] <= MISSION_ZONE[1] + MISSION_ZONE[3]
            and self.alive):
            self.alive = False
            scoreboard["escaped"] += 1

    def absorb_energy(self, energy):
        if self.cloaked:
            energy *= 0.3
        self.energy_absorbed += energy
        if self.energy_absorbed > self.damage_energy_threshold:
            self.energy_absorbed = self.damage_energy_threshold

    def draw(self, ax):
        size = 11
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
            base_color = tuple(min(1.0, c+0.45) for c in base_color)
            alpha = 0.55 + 0.35*np.sin(10 * self.energy_absorbed + 0.4)
        else:
            alpha = 1.0

        drone_poly = Polygon(pts_rot, closed=True, color=base_color, alpha=alpha, zorder=5)
        ax.add_patch(drone_poly)

        # Thruster flicker effect (rear)
        thruster_pos = self.pos - normalize(self.velocity) * 7 if np.linalg.norm(self.velocity)>0 else self.pos - np.array([7,0])
        thruster_color = (1, 0.55 + 0.45*np.random.rand(), 0)
        ax.add_patch(Circle(thruster_pos, radius=3.8, color=thruster_color, alpha=0.7))

        # Energy bar above drone
        bar_width = 20
        bar_height = 3.6
        bar_x = self.pos[0] - bar_width/2
        bar_y = self.pos[1] + 18
        ax.add_patch(FancyBboxPatch((bar_x, bar_y), bar_width, bar_height,
                                   boxstyle="round,pad=0.1", linewidth=0, facecolor='gray', alpha=0.55, zorder=8))
        ax.add_patch(FancyBboxPatch((bar_x, bar_y), bar_width*progress, bar_height,
                                   boxstyle="round,pad=0.1", linewidth=0, facecolor=base_color, alpha=alpha, zorder=9))

class LaserTroop:
    def __init__(self):
        # Spawn outside terrain patches
        while True:
            pos = np.array([np.random.uniform(WIDTH/2, WIDTH-40), np.random.uniform(40, HEIGHT-40)])
            if not any((pos[0]>=x and pos[0]<=x+w and pos[1]>=y and pos[1]<=y+h) for x,y,w,h,_ in terrain_rects):
                if all(np.linalg.norm(pos - np.array([cx,cy])) > r for cx,cy,r,_ in terrain_circles):
                    break
        self.pos = pos
        self.direction = np.array([1.0, 0.0])
        self.lock_timers = dict()
        self.angle = 0
        self.pulse = 0.0
        self.ammo = 5.0  # seconds of firing
        self.reload_cooldown = 0.0

    def update(self, drones):
        alive = [d for d in drones if d.alive]
        if not alive:
            return

        # If reloading, cooldown timer
        if self.ammo <= 0:
            self.reload_cooldown += DT
            if self.reload_cooldown >= 4.5:
                self.ammo = 5.0
                self.reload_cooldown = 0

        # Find nearest visible drone (LOS + terrain)
        visible_drones = []
        for d in alive:
            dist = np.linalg.norm(d.pos - self.pos)
            if dist > LASER_RANGE:
                continue
            if line_of_sight(self.pos, d.pos, terrain_rects, terrain_circles):
                visible_drones.append((dist, d))
        if not visible_drones:
            # No visible drones: slowly rotate to search
            self.direction = np.array([np.cos(self.angle + 0.03), np.sin(self.angle + 0.03)])
            self.direction /= np.linalg.norm(self.direction)
            self.angle += 0.03
            self.pulse += DT * 10
            if self.pulse > 2*np.pi:
                self.pulse -= 2*np.pi
            return

        visible_drones.sort(key=lambda x: x[0])
        target = visible_drones[0][1]

        # Turn toward target
        vec = target.pos - self.pos
        dist = np.linalg.norm(vec)
        desired_dir = vec / dist
        current_dir = self.direction
        angle_diff = np.arctan2(desired_dir[1], desired_dir[0]) - np.arctan2(current_dir[1], current_dir[0])
        angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi
        max_turn = 0.12
        angle_change = np.clip(angle_diff, -max_turn, max_turn)
        c, s = np.cos(angle_change), np.sin(angle_change)
        R = np.array([[c, -s], [s, c]])
        self.direction = R @ current_dir
        self.direction /= np.linalg.norm(self.direction)
        self.angle = np.arctan2(self.direction[1], self.direction[0])

        # Move slowly forward if ammo available
        if self.ammo > 0:
            self.pos += self.direction * LASER_SPEED * 0.3 * DT
        else:
            # Stationary while reloading
            pass

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
        return self.lock_timers.get(drone_id, 0) >= LASER_LOCK_TIME and self.ammo > 0

    def draw(self, ax):
        # Base dot
        ax.plot(self.pos[0], self.pos[1], 'red', marker='o', markersize=10, zorder=12)

        # Glowing aura
        glow_radius = 20 + 4 * np.sin(self.pulse * 4)
        glow_alpha = 0.15 + 0.15 * np.sin(self.pulse * 3)
        glow = Circle(self.pos, radius=glow_radius, color='red', alpha=glow_alpha, zorder=10)
        ax.add_patch(glow)

                # Direction arrow
        dx = np.cos(self.angle) * 28
        dy = np.sin(self.angle) * 28
        ax.arrow(self.pos[0], self.pos[1], dx, dy, head_width=8, head_length=12,
                 fc='red', ec='red', alpha=0.9, zorder=15)

        # Laser flare at tip
        flare_pos = self.pos + np.array([dx, dy])
        flare_radius = 5 + 3 * np.sin(self.pulse * 5)
        flare = Circle(flare_pos, radius=flare_radius, color='yellow', alpha=0.85, zorder=20)
        ax.add_patch(flare)

# === INITIALIZE SIMULATION OBJECTS ===
drones = [Drone() for _ in range(NUM_DRONES)]
lasers = [LaserTroop()]
explosions = []

# Prepare terrain patches for drawing (with color)
terrain_patches = [Rectangle((x,y), w, h, color=color, alpha=0.85, zorder=2)
                   for x,y,w,h,color in terrain_rects]

terrain_circles_patches = [Circle((cx, cy), r, color=color, alpha=0.85, zorder=2)
                           for cx, cy, r, color in terrain_circles]

fig, ax = plt.subplots(figsize=(12, 7))

def update(frame):
    ax.clear()
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.set_aspect('equal')
    ax.set_facecolor('skyblue')

    # Draw terrain rectangles and circles with shadows
    for patch in terrain_patches:
        ax.add_patch(patch)
        # Draw simple shadow below terrain
        shadow = Rectangle((patch.get_x(), patch.get_y()-6), patch.get_width(), 6,
                           color='black', alpha=0.08, zorder=1)
        ax.add_patch(shadow)
    for patch in terrain_circles_patches:
        ax.add_patch(patch)
        shadow = Circle((patch.center[0], patch.center[1]-6), patch.radius, color='black', alpha=0.07, zorder=1)
        ax.add_patch(shadow)

    # Draw fog patches
    for fog in fog_patches:
        ax.add_patch(fog)

    # Draw mission zone (green tinted)
    mx, my, mw, mh = MISSION_ZONE
    ax.add_patch(Rectangle((mx, my), mw, mh, color='seagreen', alpha=0.35, zorder=3))
    ax.text(mx + mw/2, my + mh/2, "MISSION\nZONE", color='darkgreen',
            fontsize=14, fontweight='bold', ha='center', va='center', alpha=0.6, zorder=4)

    # Update laser troops
    for laser in lasers:
        laser.update(drones)

    # Update drones
    for drone in drones:
        drone.update(lasers, drones)

    beam_angle = np.deg2rad(LASER_BEAM_ANGLE_DEG)

    # Laser locking, damage, and visuals
    for laser in lasers:
        # Draw laser cone if ammo available
        base_angle = np.arctan2(laser.direction[1], laser.direction[0])
        start_angle = np.rad2deg(base_angle - beam_angle)
        end_angle = np.rad2deg(base_angle + beam_angle)
        wedge_alpha = 0.12 + 0.1*np.sin(laser.pulse)
        if laser.ammo > 0:
            wedge = Wedge(laser.pos, LASER_RANGE, start_angle, end_angle, color='red', alpha=wedge_alpha, zorder=6)
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
                drone.energy_absorbed = max(0, drone.energy_absorbed - 18 * DT)
                continue

            laser_dir = laser.direction
            vec_dir = vec / dist
            angle = np.arccos(np.clip(np.dot(laser_dir, vec_dir), -1.0, 1.0))

            # Check line of sight before locking on
            if angle < beam_angle and line_of_sight(laser.pos, drone.pos, terrain_rects, terrain_circles):
                laser.increment_lock(drone, DT)
                if laser.is_locked(drone):
                    energy_this_step = laser_power * absorptivity * DT
                    drone.absorb_energy(energy_this_step)
                    laser.ammo -= DT  # reduce ammo when firing

                    # Draw thick locking beam
                    ax.plot([laser.pos[0], drone.pos[0]], [laser.pos[1], drone.pos[1]],
                            color='red', linestyle='-', linewidth=4, alpha=0.75, zorder=11)

                    if drone.energy_absorbed >= drone.damage_energy_threshold:
                        drone.alive = False
                        explosions.append(Explosion(drone.pos.copy()))
                        laser.reset_lock(drone)
                else:
                    # Thin beam while locking up
                    ax.plot([laser.pos[0], drone.pos[0]], [laser.pos[1], drone.pos[1]],
                            color='red', linestyle='--', linewidth=2, alpha=0.3 + 0.3*np.sin(laser.pulse * 8), zorder=10)
            else:
                laser.reset_lock(drone)
                drone.energy_absorbed = max(0, drone.energy_absorbed - 14 * DT)

    # Draw drones and thruster effects
    for drone in drones:
        if drone.alive:
            drone.draw(ax)
        else:
            # Dead drones become grey blobs
            ax.plot(drone.pos[0], drone.pos[1], 'o', color='dimgray', markersize=13, alpha=0.6, zorder=4)

    # Update and draw explosions
    alive_explosions = []
    for explosion in explosions:
        if explosion.update():
            for p in explosion.particles:
                circle = Circle(p.pos, p.radius, color=p.color, alpha=p.alpha, zorder=20)
                ax.add_patch(circle)
            alive_explosions.append(explosion)
    explosions[:] = alive_explosions

    # Scoreboard display
    ax.text(10, HEIGHT - 25, f"Drones Escaped: {scoreboard['escaped']}", fontsize=13, color='darkgreen', zorder=50)
    ax.text(10, HEIGHT - 50, f"Drones Destroyed: {scoreboard['destroyed'] + len(explosions)}", fontsize=13, color='darkred', zorder=50)

    ax.set_title(f'Drone Swarm vs Laser Troops — Frame {frame}', fontsize=18)
    ax.axis('off')

    return []

ani = FuncAnimation(fig, update, frames=2000, interval=DT*1000, blit=False)
plt.show()
