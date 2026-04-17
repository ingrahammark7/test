import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Parameters
# ----------------------------
DT = 0.02
SIM_SPEED = 995

ATTACKER_SPEED = 320.0
INTERCEPTOR_SPEED = 1500.0

NAV_GAIN = 3.5

HIT_RADIUS = 80.0

LAUNCH_RADIUS = 250000.0
MIN_CLOSING = 50.0

LATENCY_SECONDS = 0.10


# ----------------------------
# Asset (defended target)
# ----------------------------
class Asset:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = np.array([50000.0, 0.0], dtype=float)
        self.vel = np.array([0.0, 0.0], dtype=float)

    def step(self):
        self.pos += self.vel * DT


# ----------------------------
# Attacker (fuel + anisotropy)
# ----------------------------
class Attacker:
    def __init__(self, asset):
        self.asset = asset
        self.reset()

    def reset(self):
        self.pos = np.array([200000.0, 80000.0], dtype=float)
        self.vel = np.array([-ATTACKER_SPEED, 0.0], dtype=float)
        self.fuel = 1.0
        self.done = False

    def step(self):
        if self.done:
            return

        rel = self.asset.pos - self.pos
        dist = np.linalg.norm(rel)

        los = rel / (dist + 1e-9)
        rel_vel = self.asset.vel - self.vel

        closing = -np.dot(rel_vel, los)

        los_rate = (rel[0]*rel_vel[1] - rel[1]*rel_vel[0]) / (dist**2 + 1e-9)

        # ----------------------------
        # ATTACKER FUEL + ANISOTROPY
        # ----------------------------
        self.fuel = max(0.0, self.fuel - 0.006 * DT)

        thrust_scale = 0.35 + 0.65 * self.fuel

        guidance = NAV_GAIN * closing * los_rate

        thrust_dir = los + np.random.randn(2) * 0.12 * self.fuel
        thrust_dir /= np.linalg.norm(thrust_dir + 1e-9)

        thrust = 25.0 * thrust_scale * thrust_dir

        acc = guidance * np.array([-los[1], los[0]]) + thrust
        acc = np.clip(acc, -35.0, 35.0)

        self.vel += acc * DT
        self.pos += self.vel * DT

        if dist < HIT_RADIUS:
            self.done = True


# ----------------------------
# Interceptor (WITH COMMAND LATENCY)
# ----------------------------
class Interceptor:
    def __init__(self, attacker):
        self.attacker = attacker
        self.reset()

    def reset(self):
        self.pos = np.array([0.0, 0.0], dtype=float)
        self.vel = np.array([INTERCEPTOR_SPEED, 0.0], dtype=float)

        self.done = False
        self.fuel = 1.0

        # ----------------------------
        # LATENCY SYSTEM (REAL)
        # ----------------------------
        self.latency_steps = int(LATENCY_SECONDS / DT)
        self.history = []

    def step(self):
        if self.done:
            return

        # ----------------------------
        # record attacker state history
        # ----------------------------
        self.history.append(
            (self.attacker.pos.copy(), self.attacker.vel.copy())
        )

        if len(self.history) > self.latency_steps + 10:
            self.history.pop(0)

        # ----------------------------
        # delayed perception (THIS IS THE LATENCY)
        # ----------------------------
        if len(self.history) > self.latency_steps:
            target_pos, target_vel = self.history[-self.latency_steps]
        else:
            target_pos, target_vel = self.attacker.pos, self.attacker.vel

        # ----------------------------
        # guidance computation
        # ----------------------------
        rel = target_pos - self.pos
        dist = np.linalg.norm(rel)

        los = rel / (dist + 1e-9)
        rel_vel = target_vel - self.vel

        closing = -np.dot(rel_vel, los)

        self.fuel = max(0.0, self.fuel - 0.01 * DT)
        gain = NAV_GAIN * (0.4 + 0.6 * self.fuel)

        los_rate = (rel[0]*rel_vel[1] - rel[1]*rel_vel[0]) / (dist**2 + 1e-9)

        acc = gain * closing * los_rate
        acc = np.clip(acc, -40.0, 40.0)

        perp = np.array([-los[1], los[0]])

        self.vel += acc * perp * DT
        self.pos += self.vel * DT

        if dist < HIT_RADIUS:
            self.done = True


# ----------------------------
# Game controller
# ----------------------------
class Game:
    def __init__(self):
        self.asset = Asset()
        self.attacker = Attacker(self.asset)
        self.interceptor = None

        self.attacker_wins = 0
        self.defender_wins = 0
        self.shots = 0

    def reset_round(self):
        self.asset = Asset()
        self.attacker = Attacker(self.asset)
        self.interceptor = None

    def should_launch(self):
        rel = self.attacker.pos
        dist = np.linalg.norm(rel)

        rel_dir = -rel / (dist + 1e-9)
        closing = np.dot(self.attacker.vel, rel_dir)

        return dist < LAUNCH_RADIUS and closing > MIN_CLOSING

    def step(self):
        self.asset.step()
        self.attacker.step()

        if self.interceptor:
            self.interceptor.step()

        # ----------------------------
        # WIN CONDITIONS
        # ----------------------------
        if self.attacker.done:
            self.attacker_wins += 1
            self.reset_round()
            return

        if self.interceptor and self.interceptor.done:
            self.defender_wins += 1
            self.reset_round()
            return

        if self.interceptor is None and self.should_launch():
            self.interceptor = Interceptor(self.attacker)
            self.shots += 1


# ----------------------------
# Simulation
# ----------------------------
game = Game()

fig, ax = plt.subplots()
ax.set_xlim(-250000, 250000)
ax.set_ylim(-250000, 250000)

asset_dot, = ax.plot([], [], 'go', markersize=10)
attacker_dot, = ax.plot([], [], 'ro', markersize=7)
interceptor_dot, = ax.plot([], [], 'bo', markersize=6)

line_a, = ax.plot([], [], 'r--', alpha=0.4)
line_i, = ax.plot([], [], 'b--', alpha=0.4)

text = ax.text(0.02, 0.95, "", transform=ax.transAxes)


def update(_):
    for _ in range(SIM_SPEED):
        game.step()

    a = game.attacker.pos
    s = game.asset.pos
    i = game.interceptor.pos if game.interceptor else None

    attacker_dot.set_data([a[0]], [a[1]])
    asset_dot.set_data([s[0]], [s[1]])

    if i is not None:
        interceptor_dot.set_data([i[0]], [i[1]])
        line_i.set_data([0, i[0]], [0, i[1]])
    else:
        interceptor_dot.set_data([], [])
        line_i.set_data([], [])

    line_a.set_data([a[0], s[0]], [a[1], s[1]])

    total = game.attacker_wins + game.defender_wins

    text.set_text(
        f"Attacker Wins: {game.attacker_wins}\n"
        f"Defender Wins: {game.defender_wins}\n"
        f"Rounds: {total}\n"
        f"Shots: {game.shots}\n"
        f"Attacker Fuel: {game.attacker.fuel:.2f}\n"
        f"Interceptor Fuel: {game.interceptor.fuel if game.interceptor else 0:.2f}"
    )

    return asset_dot, attacker_dot, interceptor_dot, line_a, line_i, text


ani = FuncAnimation(fig, update, interval=30, blit=False)
plt.title("Interceptor Simulation (Attacker + Fuel + Anisotropy + 100ms Latency)")
plt.show()