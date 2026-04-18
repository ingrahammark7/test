import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# PARAMETERS
# =========================================================

Rgas = 8.314
rho = 1200
cp = 1000
L = 0.1

u0 = 20.0
T_in = 1500

A = 1e6
Ea = 80000
dH = 2e6

T0 = 300.0
C0 = 1.0

dt = 0.05
steps = 1200

# =========================================================
# SCALING CONSTANTS (KEY FIX)
# =========================================================

T_scale = 500.0
T_max_plot = 2000.0

# =========================================================
# MODEL
# =========================================================

def reaction(C, T):
    T = np.clip(T, 200, 4000)  # prevents numerical overflow
    return A * C * np.exp(-Ea / (Rgas * T))

def simulate(theta):

    T = T0
    C = C0

    Tn = []
    Rn = []

    for _ in range(steps):

        R = reaction(C, T)

        jet = (u0 * np.cos(theta) / L) * (T_in - T)

        dT = jet + (dH / (rho * cp)) * R
        dC = -R

        T += dt * dT
        C += dt * dC

        # =====================================================
        # STABLE NORMALIZATION
        # =====================================================

        Theta = (T - T_in) / T_scale

        Rlog = np.log10(R + 1e-12)
        Rlog = np.clip(Rlog, -12, 6)

        Tn.append(Theta)
        Rn.append(Rlog)

        # safety cap for visualization stability
        if T > 5000:
            break

    return np.array(Tn), np.array(Rn)

# =========================================================
# ANGLE SWEEP
# =========================================================

angles = [0, np.pi/6, np.pi/3, np.pi/2]

plt.figure(figsize=(10,6))

for th in angles:
    Tn, _ = simulate(th)
    plt.plot(Tn, label=f"{np.degrees(th):.0f}°")

plt.axhline(0, linestyle="--", color="black")
plt.title("Stable Scaled Temperature Evolution")
plt.xlabel("time step")
plt.ylabel("Θ (nondimensional T)")
plt.legend()
plt.grid()
plt.show()

# =========================================================
# REACTION STRENGTH (ROBUST LOG SCALE)
# =========================================================

plt.figure(figsize=(10,6))

for th in angles:
    _, Rn = simulate(th)
    plt.plot(Rn, label=f"{np.degrees(th):.0f}°")

plt.title("Bounded Log Reaction Rate (no collapse / no blow-up)")
plt.xlabel("time step")
plt.ylabel("log10(R) clipped")
plt.legend()
plt.grid()
plt.show()