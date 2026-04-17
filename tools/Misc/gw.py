import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Parameters
# ----------------------------
DT = 0.02
TIME_SCALE = 59.0

INTERCEPT_RADIUS = 60.0
FAIL_DISTANCE = -80000.0

TARGET_SPEED = 300.0
MISSILE_SPEED = 1500.0

NAV_GAIN = 3.5
BURN_TIME = 6.0

MAX_LAUNCH_RANGE = 250000.0
MIN_CLOSING = 80.0


# ----------------------------
# Target (simple physics only)
# ----------------------------
class Target:
    def __init__(self):
        angle = np.random.uniform(-0.6, 0.6)
        radius = np.random.uniform(60000, 120000)

        self.pos = np.array([
            radius * np.cos(angle),
            radius * np.sin(angle)
        ])

        self.vel = np.array([-TARGET_SPEED, 0.0])
        self.vel = self.vel / np.linalg.norm(self.vel) * TARGET_SPEED

    def step(self):
        noise = 3.0 * np.random.randn(2)

        self.vel += noise * DT * 0.1
        self.vel = self.vel / np.linalg.norm(self.vel) * TARGET_SPEED

        self.pos += self.vel * DT


# ----------------------------
# Missile (FIXED PN GUIDANCE)
# ----------------------------
class Missile:
    def __init__(self, target):
        self.pos = np.array([0.0, 0.0])
        self.vel = np.array([MISSILE_SPEED, 0.0])

        self.target = target

        self.burn = BURN_TIME
        self.done = False
        self.hit = False

    def step(self):
        if self.done:
            return

        rel = self.target.pos - self.pos
        dist = np.linalg.norm(rel)

        if dist < 1e-6:
            return

        # ----------------------------
        # STABLE PN CORE (FIX)
        # ----------------------------

        los_hat = rel / (dist + 1e-9)

        rel_vel = self.target.vel - self.vel

        # LOS rate (stable 2D cross product form)
        los_rate = (rel[0] * rel_vel[1] - rel[1] * rel_vel[0]) / (dist**2 + 1e-9)

        # closing velocity
        closing = -np.dot(rel_vel, los_hat)

        # PN acceleration magnitude
        acc_mag = NAV_GAIN * closing * los_rate

        # perpendicular direction (rotate LOS +90°)
        perp = np.array([-los_hat[1], los_hat[0]])

        # apply acceleration
        self.vel += acc_mag * perp * DT

        # speed constraint (fuel effect)
        speed = np.linalg.norm(self.vel)
        limit = MISSILE_SPEED if self.burn > 0 else MISSILE_SPEED * 0.7

        if speed > limit:
            self.vel = self.vel / speed * limit

        self.pos += self.vel * DT

        if self.burn > 0:
            self.burn -= DT

        # ----------------------------
        # termination
        # ----------------------------
        if dist < INTERCEPT_RADIUS:
            self.done = True
            self.hit = True


# ----------------------------
# Fire control (single missile rule)
# ----------------------------
class FireControl:
    def __init__(self, target):
        self.target = target
        self.missile = None

        self.shots = 0
        self.kills = 0
        self.escapes = 0

    def should_launch(self):
        rel = self.target.pos
        dist = np.linalg.norm(rel)

        closing = np.dot(self.target.vel, -rel / (dist + 1e-9))

        return dist < MAX_LAUNCH_RANGE and closing > MIN_CLOSING

    def step(self):
        # launch only if no active missile
        if self.missile is None or self.missile.done:
            if self.missile and self.missile.done:
                if self.missile.hit:
                    self.kills += 1
                else:
                    self.escapes += 1
                self.missile = None

            if self.should_launch():
                self.missile = Missile(self.target)
                self.shots += 1

        # update missile if active
        if self.missile:
            self.missile.step()


# ----------------------------
# Simulation
# ----------------------------
target = Target()
fc = FireControl(target)

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots()

ax.set_xlim(-150000, 150000)
ax.set_ylim(-150000, 150000)

t_dot, = ax.plot([], [], 'ro')
m_dot, = ax.plot([], [], 'bo')
line, = ax.plot([], [], 'k--', alpha=0.4)

text = ax.text(0.02, 0.95, "", transform=ax.transAxes)


# ----------------------------
# auto view
# ----------------------------
def view(t, m):
    mid = (t + m) / 2
    span = np.linalg.norm(t - m) + 60000

    ax.set_xlim(mid[0] - span, mid[0] + span)
    ax.set_ylim(mid[1] - span, mid[1] + span)


# ----------------------------
# update loop
# ----------------------------
def update(_):
    for _ in range(int(TIME_SCALE)):
        target.step()
        fc.step()

    t = target.pos

    if fc.missile:
        m = fc.missile.pos
    else:
        m = np.array([0.0, 0.0])

    t_dot.set_data([t[0]], [t[1]])
    m_dot.set_data([m[0]], [m[1]])
    line.set_data([t[0], m[0]], [t[1], m[1]])

    view(t, m)

    pk = (fc.kills / fc.shots * 100) if fc.shots else 0.0

    text.set_text(
        f"Shots: {fc.shots}\n"
        f"Kills: {fc.kills}\n"
        f"Escapes: {fc.escapes}\n"
        f"Pk: {pk:.1f}%\n"
        f"Active missile: {1 if fc.missile else 0}\n"
        f"Burn: {fc.missile.burn if fc.missile else 0:.1f}"
    )

    return t_dot, m_dot, line, text


ani = FuncAnimation(fig, update, interval=30, blit=False)
plt.title("Stable PN Interceptor (Correct Physics, Single-Shot Control)")
plt.show()