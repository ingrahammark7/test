import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
DT = 0.05  # time step (s)
MAX_THRUST = 30000  # N (approx F-16 max thrust)
MASS = 9000  # kg (empty+pilot+fuel)
FRONTAL_AREA = 7.0  # m^2 approx F-16 frontal area
AIR_DENSITY = 1.225  # kg/m^3 at sea level
DRAG_COEFF = 0.02  # simplified drag coeff
MAX_G = 9.81 * 9  # max sustained g (9g turn)
GUN_RANGE = 1000  # meters effective gun range
GUN_ARC = np.deg2rad(15)  # +/- 15 deg firing arc from nose
GUN_RELOAD = 1.0  # seconds between shots
BULLET_HIT_CHANCE_AT_CLOSE = 0.8

def wrap_angle(angle):
    """Keep angle between -pi and pi"""
    while angle > np.pi:
        angle -= 2*np.pi
    while angle < -np.pi:
        angle += 2*np.pi
    return angle

class Aircraft:
    def __init__(self, name, x, y, heading, velocity):
        self.name = name
        self.pos = np.array([x, y], dtype=float)
        self.heading = heading  # radians
        self.velocity = velocity  # m/s scalar
        self.turn_rate = 0.0  # radians per second
        self.gun_cooldown = 0.0
        self.alive = True
        self.damage = 0
        self.history = []

    def update_physics(self, throttle, turn_input):
        # Thrust power approximation (throttle 0-1)
        thrust = throttle * MAX_THRUST  # N

        # Drag force Fd = 0.5 * Cd * A * rho * v^2
        drag = 0.5 * DRAG_COEFF * FRONTAL_AREA * AIR_DENSITY * self.velocity**2

        # Net force forward
        net_force = thrust - drag
        acceleration = net_force / MASS

        # Update velocity with acceleration
        self.velocity += acceleration * DT
        if self.velocity < 50:  # stall speed approx
            self.velocity = 50

        # Calculate max turn rate from g-limit
        max_turn_rate = MAX_G * 9.81 / self.velocity  # rad/s approx
        desired_turn_rate = turn_input * max_turn_rate
        # Smooth turn rate change
        self.turn_rate += (desired_turn_rate - self.turn_rate) * 0.2

        # Update heading
        self.heading += self.turn_rate * DT
        self.heading = wrap_angle(self.heading)

        # Update position
        dx = self.velocity * np.cos(self.heading) * DT
        dy = self.velocity * np.sin(self.heading) * DT
        self.pos += np.array([dx, dy])

        # Gun cooldown timer
        if self.gun_cooldown > 0:
            self.gun_cooldown -= DT
        if self.gun_cooldown < 0:
            self.gun_cooldown = 0

        self.history.append(self.pos.copy())

    def try_fire_gun(self, target):
        if self.gun_cooldown > 0 or not self.alive:
            return False

        # Calculate relative position and angle to target
        vec_to_target = target.pos - self.pos
        distance = np.linalg.norm(vec_to_target)
        if distance > GUN_RANGE:
            return False  # out of range

        angle_to_target = np.arctan2(vec_to_target[1], vec_to_target[0])
        angle_diff = wrap_angle(angle_to_target - self.heading)

        if abs(angle_diff) > GUN_ARC:
            return False  # target out of firing arc

        # Hit chance falls off linearly with distance
        hit_prob = BULLET_HIT_CHANCE_AT_CLOSE * max(0, (GUN_RANGE - distance) / GUN_RANGE)

        if np.random.random() < hit_prob:
            # Hit! Increase damage
            target.damage += 10
            if target.damage >= 100:
                target.alive = False
            self.gun_cooldown = GUN_RELOAD
            return True
        else:
            self.gun_cooldown = GUN_RELOAD
            return False

    def ai_control(self, enemy):
        if not self.alive:
            return 0, 0  # no control

        # Simple AI:
        # Throttle full ahead if velocity < 300 m/s else 0.7
        throttle = 1.0 if self.velocity < 300 else 0.7

        # Turn towards enemy
        vec_to_enemy = enemy.pos - self.pos
        angle_to_enemy = np.arctan2(vec_to_enemy[1], vec_to_enemy[0])
        angle_diff = wrap_angle(angle_to_enemy - self.heading)

        # Turn input proportional to angle_diff but capped [-1, 1]
        turn_input = np.clip(angle_diff * 2, -1, 1)

        return throttle, turn_input

def simulate_fight():
    # Initialize aircraft
    ac1 = Aircraft("Eagle", 0, 0, np.deg2rad(0), 200)
    ac2 = Aircraft("Falcon", 3000, 1000, np.deg2rad(180), 200)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-2000, 4000)
    ax.set_ylim(-2000, 4000)
    ax.set_aspect('equal')
    ax.set_title("2D Dogfight Simulator")
    text_status = ax.text(0, 3700, "", fontsize=12)

    # Plotting aircraft
    line1, = ax.plot([], [], 'bo-', lw=2, label=ac1.name)
    line2, = ax.plot([], [], 'ro-', lw=2, label=ac2.name)
    gunshot_text = ax.text(0, 3500, '', fontsize=14, color='red', ha='center')

    def update(frame):
        if not ac1.alive or not ac2.alive:
            winner = ac1.name if ac1.alive else ac2.name
            text_status.set_text(f"{winner} wins! Fight over.")
            return line1, line2, text_status, gunshot_text

        # AI decides throttle and turn
        throttle1, turn1 = ac1.ai_control(ac2)
        throttle2, turn2 = ac2.ai_control(ac1)

        # Update physics
        ac1.update_physics(throttle1, turn1)
        ac2.update_physics(throttle2, turn2)

        # Try to fire guns
        shot1 = ac1.try_fire_gun(ac2)
        shot2 = ac2.try_fire_gun(ac1)

        # Update gunshot text
        if shot1 and shot2:
            gunshot_text.set_text("Both fired and hit!")
        elif shot1:
            gunshot_text.set_text(f"{ac1.name} fired and hit!")
        elif shot2:
            gunshot_text.set_text(f"{ac2.name} fired and hit!")
        else:
            gunshot_text.set_text("")

        # Update lines (showing last 10 positions)
        history_len = 10
        line1.set_data(*zip(*ac1.history[-history_len:]))
        line2.set_data(*zip(*ac2.history[-history_len:]))

        # Update status text with info
        status = (
            f"{ac1.name} HP: {100 - ac1.damage:.0f} | Speed: {ac1.velocity:.0f} m/s | Heading: {np.rad2deg(ac1.heading):.0f}°\n"
            f"{ac2.name} HP: {100 - ac2.damage:.0f} | Speed: {ac2.velocity:.0f} m/s | Heading: {np.rad2deg(ac2.heading):.0f}°"
        )
        text_status.set_text(status)

        return line1, line2, text_status, gunshot_text

    ani = FuncAnimation(fig, update, interval=50)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    simulate_fight()