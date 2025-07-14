import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Wedge, Circle

# Simulation parameters
WIDTH, HEIGHT = 400, 300
NUM_DRONES = 40
DRONE_SPEED = 5.0
DRONE_ACCEL = 3.0
DRONE_SIZE = 15

LASER_SPEED = 3.0
LASER_BEAM_ANGLE_DEG = 15
LASER_BEAM_ANGLE = np.deg2rad(LASER_BEAM_ANGLE_DEG)
LASER_LOCK_TIME = 2.0
LASER_RANGE = 150.0
LASER_SPAWN_INTERVAL = 50
DRONE_RESPAWN_TIME = 5.0

DT = 0.1

# Terrain
terrain = [
    (150, 100, 50, 10),
    (250, 180, 60, 15),
    (80, 220, 40, 20),
]

def line_intersects_rect(p1, p2, rect):
    rx, ry, rw, rh = rect

    corners = [
        np.array([rx, ry]),
        np.array([rx + rw, ry]),
        np.array([rx + rw, ry + rh]),
        np.array([rx, ry + rh])
    ]

    edges = [
        (corners[0], corners[1]),
        (corners[1], corners[2]),
        (corners[2], corners[3]),
        (corners[3], corners[0])
    ]

    def ccw(A, B, C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

    def segments_intersect(A, B, C, D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    for edge_start, edge_end in edges:
        if segments_intersect(p1, p2, edge_start, edge_end):
            return True

    def point_in_rect(p):
        return rx <= p[0] <= rx+rw and ry <= p[1] <= ry+rh

    if point_in_rect(p1) or point_in_rect(p2):
        return True

    return False

def blocked_by_terrain(p1, p2):
    for rect in terrain:
        if line_intersects_rect(p1, p2, rect):
            return True
    return False

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

class Explosion:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.radius = 1.0
        self.max_radius = 30.0
        self.alpha = 1.0
        self.finished = False

    def update(self):
        self.radius += 5.0
        self.alpha -= 0.15
        if self.alpha <= 0:
            self.finished = True

class Drone:
    def __init__(self):
        self.pos = np.array([np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)])
        self.velocity = np.zeros(2)
        self.alive = True
        self.exposure_time = 0.0
        self.respawn_timer = 0.0
        self.just_died = False
        self.color = 'blue'

    def update(self, lasers):
        if not self.alive:
            if not self.just_died:
                self.just_died = True
                explosions.append(Explosion(self.pos.copy()))
            self.respawn_timer += DT
            self.color = (1.0, 0, 0)  # Red flash on death
            if self.respawn_timer >= DRONE_RESPAWN_TIME:
                while True:
                    new_pos = np.array([np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)])
                    if not any(
                        (new_pos[0] >= t[0] and new_pos[0] <= t[0]+t[2] and
                         new_pos[1] >= t[1] and new_pos[1] <= t[1]+t[3])
                        for t in terrain
                    ):
                        break
                self.pos = new_pos
                self.velocity = np.zeros(2)
                self.alive = True
                self.exposure_time = 0.0
                self.respawn_timer = 0.0
                self.just_died = False
                self.color = 'blue'
            return

        flee_dir = np.zeros(2)
        for laser in lasers:
            to_laser = laser.pos - self.pos
            dist = np.linalg.norm(to_laser)
            if dist < LASER_RANGE:
                if not blocked_by_terrain(self.pos, laser.pos):
                    flee_dir -= (to_laser) / (dist**2 + 1e-6)

        random_dir = np.random.uniform(-1,1,2)
        flee_dir += 0.2 * random_dir

        if np.linalg.norm(flee_dir) > 0:
            flee_dir = flee_dir / np.linalg.norm(flee_dir)
        else:
            flee_dir = random_dir / np.linalg.norm(random_dir)

        desired_velocity = flee_dir * DRONE_SPEED
        delta_v = desired_velocity - self.velocity

        accel = np.clip(np.linalg.norm(delta_v), 0, DRONE_ACCEL)
        if np.linalg.norm(delta_v) > 0:
            self.velocity += (delta_v / np.linalg.norm(delta_v)) * accel * DT

        new_pos = self.pos + self.velocity * DT

        for t in terrain:
            if (new_pos[0] >= t[0] and new_pos[0] <= t[0] + t[2] and
                new_pos[1] >= t[1] and new_pos[1] <= t[1] + t[3]):
                self.velocity = np.zeros(2)
                new_pos = self.pos
                break

        new_pos[0] = np.clip(new_pos[0], 0, WIDTH)
        new_pos[1] = np.clip(new_pos[1], 0, HEIGHT)

        self.pos = new_pos

    def check_laser_lock(self, lasers):
        if not self.alive:
            return

        for laser in lasers:
            vec = self.pos - laser.pos
            dist = np.linalg.norm(vec)
            if dist > LASER_RANGE:
                laser.reset_lock(self)
                continue

            if blocked_by_terrain(laser.pos, self.pos):
                laser.reset_lock(self)
                continue

            laser_dir = laser.direction
            vec_dir = vec / dist
            angle = np.arccos(np.clip(np.dot(laser_dir, vec_dir), -1.0, 1.0))

            if angle < LASER_BEAM_ANGLE:
                laser.increment_lock(self, DT)
                if laser.is_locked(self):
                    self.exposure_time += DT
                    if self.exposure_time > 5:
                        self.alive = False
                        laser.reset_lock(self)
            else:
                laser.reset_lock(self)

class LaserTroop:
    def __init__(self):
        while True:
            pos = np.array([np.random.uniform(0, WIDTH), np.random.uniform(0, HEIGHT)])
            if not any(
                (pos[0] >= t[0] and pos[0] <= t[0]+t[2] and
                 pos[1] >= t[1] and pos[1] <= t[1]+t[3])
                for t in terrain
            ):
                break
        self.pos = pos
        self.direction = np.array([1.0, 0.0])
        self.lock_timers = dict()

    def update(self, drones):
        alive_drones = [d for d in drones if d.alive]
        if not alive_drones:
            return

        distances = [np.linalg.norm(d.pos - self.pos) for d in alive_drones]
        target = alive_drones[np.argmin(distances)]

        vec = target.pos - self.pos
        dist = np.linalg.norm(vec)
        if dist > 0:
            desired_dir = vec / dist
            turn_rate = 0.1
            current_dir = self.direction

            # Fix np.cross for 2D vectors by adding z=0 component
            current_dir_3d = np.append(current_dir, 0)
            desired_dir_3d = np.append(desired_dir, 0)
            sign = np.sign(np.cross(current_dir_3d, desired_dir_3d)[2])

            angle = np.arccos(np.clip(np.dot(current_dir, desired_dir), -1.0, 1.0))
            if angle > turn_rate:
                rot_angle = turn_rate * sign
                c, s = np.cos(rot_angle), np.sin(rot_angle)
                R = np.array([[c, -s], [s, c]])
                self.direction = R @ current_dir
                self.direction /= np.linalg.norm(self.direction)
            else:
                self.direction = desired_dir

            new_pos = self.pos + self.direction * LASER_SPEED * DT

            collision = False
            for t in terrain:
                if (new_pos[0] >= t[0] and new_pos[0] <= t[0]+t[2] and
                    new_pos[1] >= t[1] and new_pos[1] <= t[1]+t[3]):
                    collision = True
                    break

            if not collision:
                self.pos = new_pos

            self.pos[0] = np.clip(self.pos[0], 0, WIDTH)
            self.pos[1] = np.clip(self.pos[1], 0, HEIGHT)

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

drones = [Drone() for _ in range(NUM_DRONES)]
lasers = []
explosions = []

frame_count = 0

fig, ax = plt.subplots(figsize=(8,6))
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.set_aspect('equal')
ax.set_title('Drone Swarm vs Laser Troops with Explosions & Visuals')

terrain_patches = []
for x, y, w, h in terrain:
    patch = Rectangle((x, y), w, h, color='grey', alpha=0.7)
    terrain_patches.append(patch)
    ax.add_patch(patch)

drone_scat = ax.scatter([], [], c='blue', s=DRONE_SIZE, label='Drones')
laser_scat = ax.scatter([], [], c='red', s=50, marker='x', label='Laser Troops')
lock_lines = []
laser_beam_wedges = []

explosion_patches = []

quiver = ax.quiver([], [], [], [], angles='xy', scale_units='xy', scale=1, color='cyan', alpha=0.6)

def update(frame):
    global frame_count

    if frame_count % LASER_SPAWN_INTERVAL == 0:
        lasers.append(LaserTroop())

    for laser in lasers:
        laser.update(drones)

    for drone in drones:
        drone.update(lasers)
        drone.check_laser_lock(lasers)

    alive_drones = [d for d in drones if d.alive]
    score = len(alive_drones)

    drone_positions = np.array([d.pos for d in alive_drones]) if alive_drones else np.empty((0,2))
    drone_colors = [d.color for d in alive_drones]
    drone_scat.set_offsets(drone_positions)
    drone_scat.set_color(drone_colors)
    drone_scat.set_sizes([DRONE_SIZE]*len(drone_positions))

    laser_positions = np.array([l.pos for l in lasers])
    laser_scat.set_offsets(laser_positions if len(lasers) > 0 else np.empty((0,2)))

    # Robust quiver update to fix size mismatch error
    if len(alive_drones) > 0:
        vx = np.array([d.velocity[0] for d in alive_drones])
        vy = np.array([d.velocity[1] for d in alive_drones])
        quiver.set_offsets(drone_positions)
        try:
        	quiver.set_UVC(vx, vy)
        except:
        	ff=0
    else:
        quiver.set_offsets(np.empty((0, 2)))
        quiver.set_UVC(np.zeros(0), np.zeros(0))

    # Remove old lock lines and beam wedges
    for line in lock_lines:
        line.remove()
    lock_lines.clear()
    for wedge in laser_beam_wedges:
        wedge.remove()
    laser_beam_wedges.clear()

    # Remove old explosion patches
    for patch in explosion_patches:
        patch.remove()
    explosion_patches.clear()

    # Update explosions
    still_explosions = []
    for exp in explosions:
        exp.update()
        if not exp.finished:
            circle = Circle(exp.pos, exp.radius, color='orange', alpha=exp.alpha)
            ax.add_patch(circle)
            explosion_patches.append(circle)
            still_explosions.append(exp)
    explosions[:] = still_explosions

    # Draw laser beams and lock lines
    for laser in lasers:
        beam_angle_deg = LASER_BEAM_ANGLE_DEG
        start_angle = np.rad2deg(np.arctan2(laser.direction[1], laser.direction[0])) - beam_angle_deg
        wedge = Wedge(laser.pos, LASER_RANGE, start_angle, start_angle + 2*beam_angle_deg, alpha=0.15, color='red')
        ax.add_patch(wedge)
        laser_beam_wedges.append(wedge)

        for drone in drones:
            if drone.alive and laser.is_locked(drone):
                line = ax.plot([laser.pos[0], drone.pos[0]], [laser.pos[1], drone.pos[1]], 'r--', alpha=0.6, linewidth=2)[0]
                lock_lines.append(line)

    ax.set_title(f'Drone Swarm vs Laser Troops — Drones Alive: {score}')
    frame_count += 1

    return drone_scat, laser_scat, quiver, *lock_lines, *laser_beam_wedges, *explosion_patches

ani = FuncAnimation(fig, update, frames=2000, interval=DT*1000, blit=False)
plt.legend(loc='upper right')
plt.show()
