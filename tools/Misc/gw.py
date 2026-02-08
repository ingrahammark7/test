import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Utility functions
# -----------------------------

def norm(v):
    return np.linalg.norm(v)

def unit(v):
    n = norm(v)
    return v / n if n > 1e-9 else v

def rot90(v):
    return np.array([-v[1], v[0]])

# -----------------------------
# Vehicle models
# -----------------------------

class Vehicle:
    def __init__(self, pos, vel, a_lat_max):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(vel, dtype=float)
        self.a_lat_max = a_lat_max

    def speed(self):
        return norm(self.vel)

    def turn_rate_max(self):
        return self.a_lat_max / max(self.speed(), 1e-6)

# -----------------------------
# Target maneuver model
# -----------------------------

def target_accel(target, t):
    """
    High‑g evasive maneuver:
    bang‑bang lateral acceleration
    """
    sign = np.sign(np.sin(2 * np.pi * 0.5 * t))
    return sign * target.a_lat_max * unit(rot90(target.vel))

# -----------------------------
# Guidance laws
# -----------------------------

def pure_pursuit(missile, target):
    los = target.pos - missile.pos
    return unit(los)

def lead_pursuit(missile, target):
    los = target.pos - missile.pos
    closing = target.vel - missile.vel
    lead = los + closing * 0.5
    return unit(lead)

def proportional_navigation(missile, target, N=3):
    los = target.pos - missile.pos
    los_unit = unit(los)

    rel_vel = target.vel - missile.vel
    los_rate = np.cross(np.append(los_unit,0), np.append(rel_vel,0))[2] / max(norm(los),1e-6)

    a_cmd = N * missile.speed() * los_rate
    return np.clip(a_cmd, -missile.a_lat_max, missile.a_lat_max)

# -----------------------------
# Simulation
# -----------------------------

def simulate(
    dt=0.01,
    t_max=20,
    guidance="PN"
):
    # Target: race‑car‑like
    target = Vehicle(
        pos=[0, 0],
        vel=[60, 0],
        a_lat_max=100     # ~10 g
    )

    # Missile: generic interceptor
    missile = Vehicle(
        pos=[-1000, -50],
        vel=[300, 0],
        a_lat_max=300     # ~30 g
    )

    history = {
        "target": [],
        "missile": [],
        "range": [],
        "los_rate": [],
        "missile_turn_cap": []
    }

    t = 0
    while t < t_max:
        r = target.pos - missile.pos
        R = norm(r)

        if R < 5:
            break

        # --- Target update ---
        a_t = target_accel(target, t)
        target.vel += a_t * dt
        target.pos += target.vel * dt

        # --- Missile guidance ---
        if guidance == "PP":
            dir_cmd = pure_pursuit(missile, target)
            a_m = missile.a_lat_max * unit(rot90(missile.vel)) * np.sign(np.dot(dir_cmd, rot90(missile.vel)))
        elif guidance == "LP":
            dir_cmd = lead_pursuit(missile, target)
            a_m = missile.a_lat_max * unit(rot90(missile.vel)) * np.sign(np.dot(dir_cmd, rot90(missile.vel)))
        else:
            # PN
            los_unit = unit(r)
            rel_vel = target.vel - missile.vel
            los_rate = np.cross(np.append(los_unit,0), np.append(rel_vel,0))[2] / max(R,1e-6)
            a_mag = np.clip(3 * missile.speed() * los_rate, -missile.a_lat_max, missile.a_lat_max)
            a_m = a_mag * unit(rot90(missile.vel))

        missile.vel += a_m * dt
        missile.pos += missile.vel * dt

        # --- Logging ---
        history["target"].append(target.pos.copy())
        history["missile"].append(missile.pos.copy())
        history["range"].append(R)
        history["los_rate"].append(abs(los_rate) if 'los_rate' in locals() else 0)
        history["missile_turn_cap"].append(missile.turn_rate_max())

        t += dt

    return history

# -----------------------------
# Run and plot
# -----------------------------

hist = simulate(guidance="PN")

target_traj = np.array(hist["target"])
missile_traj = np.array(hist["missile"])

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(target_traj[:,0], target_traj[:,1], label="Target")
plt.plot(missile_traj[:,0], missile_traj[:,1], label="Interceptor")
plt.legend()
plt.title("Trajectories")
plt.axis("equal")

plt.subplot(1,2,2)
plt.plot(hist["los_rate"], label="LOS rate")
plt.plot(hist["missile_turn_cap"], label="Missile max turn rate")
plt.legend()
plt.title("Angular demand vs capability")

plt.tight_layout()
plt.show()