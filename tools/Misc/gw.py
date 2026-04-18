import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# CONSTANTS
# =========================================================

Rgas = 8.314

rho = 1200
cp = 1000
L = 0.1
V = 1e-3

u0 = 20.0
T_in = 1500
T_env = 300

# Chemistry
A1 = 5e5
A2 = 1e6
E1 = 70000
E2 = 90000

dH = 2e6

# feedback parameters
gamma_A = 0.002
beta_cool = 1e-4
cool_exp = 2.2

# stochasticity
sigma_noise = 0.02

# time
dt = 0.05
steps = 1200

# =========================================================
# CORE FUNCTIONS
# =========================================================

def A_eff(T):
    return A1 * (1 + gamma_A * (T - T_env))

def reaction(C, T):

    T = np.clip(T, 200, 4000)

    R1 = A_eff(T) * np.exp(-E1 / (Rgas * T))
    R2 = A2 * C**2 * np.exp(-E2 / (Rgas * T))

    return R1 + R2

def damkohler(R, theta):
    flow = u0 * max(np.cos(theta), 0.01) / L
    return R / (flow + 1e-9)

def cooling(T):
    return beta_cool * (T - T_env) ** cool_exp

# =========================================================
# SIMULATION
# =========================================================

def simulate(theta):

    T = T_env
    C = 1.0

    T_hist = []
    R_hist = []
    Da_hist = []

    tau_memory = 0.0

    for _ in range(steps):

        R = reaction(C, T)

        # Damköhler feedback
        Da = damkohler(R, theta)
        R_eff = R * (1 + 0.8 * Da)

        # jet residence time (memory effect)
        tau_res = L / (u0 * max(np.cos(theta), 0.01))
        tau_memory += dt * (tau_res - tau_memory) / (tau_res + 1e-6)

        jet = (u0 * np.cos(theta) / L) * (T_in - T) * (tau_memory / (tau_res + 1e-6))

        # nonlinear cooling
        Q_cool = cooling(T)

        # stochastic ignition noise
        noise = sigma_noise * np.random.randn()

        # temperature update
        dT = jet + (dH / (rho * cp)) * R_eff - Q_cool + noise
        dC = -R_eff

        T += dt * dT
        C += dt * dC

        # store
        T_hist.append(T)
        R_hist.append(np.log10(R + 1e-12))
        Da_hist.append(Da)

        if T > 5000 or C < 0:
            break

    return np.array(T_hist), np.array(R_hist), np.array(Da_hist)

# =========================================================
# ANGLE SWEEP
# =========================================================

angles = [0, np.pi/8, np.pi/4, np.pi/2.2]

plt.figure(figsize=(10,6))

for th in angles:
    T, _, _ = simulate(th)
    plt.plot(T, label=f"{np.degrees(th):.0f}°")

plt.title("Augmented Jet–Arrhenius Ignition Model (Temperature)")
plt.xlabel("time step")
plt.ylabel("Temperature (K)")
plt.legend()
plt.grid()
plt.show()

# =========================================================
# REACTION STRENGTH (LOG SCALE)
# =========================================================

plt.figure(figsize=(10,6))

for th in angles:
    _, R, _ = simulate(th)
    plt.plot(R, label=f"{np.degrees(th):.0f}°")

plt.title("Log Reaction Rate with Damköhler Feedback")
plt.xlabel("time step")
plt.ylabel("log10(R)")
plt.legend()
plt.grid()
plt.show()

# =========================================================
# DAMKÖHLER EVOLUTION
# =========================================================

plt.figure(figsize=(10,6))

for th in angles:
    _, _, Da = simulate(th)
    plt.plot(Da, label=f"{np.degrees(th):.0f}°")

plt.title("Damköhler Number Evolution (Ignition Indicator)")
plt.xlabel("time step")
plt.ylabel("Da")
plt.legend()
plt.grid()
plt.show()

# =========================================================
# SUMMARY OUTPUT
# =========================================================

for th in angles:
    T, R, Da = simulate(th)
    print(f"{np.degrees(th):.0f}° → max T={np.max(T):.1f} K | max Da={np.max(Da):.2f}")