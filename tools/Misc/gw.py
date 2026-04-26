import numpy as np

# ============================================================
# ATMOSPHERE (simple stable approximation)
# ============================================================

def rho(h):
    return 1.225 * np.exp(-h / 8500)

def a_sound(h):
    return 340.0  # fixed for stability on mobile

# ============================================================
# SYSTEM PARAMETERS
# ============================================================

A = 0.015
C_th = 900.0
T_max = 450.0

sigma = 5.67e-8
epsilon = 0.8

# ============================================================
# HEATING MODELS
# ============================================================

def Q_aero(M, h):
    v = M * a_sound(h)
    return 2e-4 * rho(h) * v**3 * A

def Q_elec(P):
    return 50.0 + 0.32 * P

def Q_cool(T):
    return 60.0 * A * (T - 220.0) + epsilon * sigma * A * (T**4 - 220.0**4)

# ============================================================
# TIME SIMULATION
# ============================================================

def simulate(M, h, P, dt=0.05, steps=300):
    T = 300.0

    for _ in range(steps):
        v = M * a_sound(h)

        Qin = Q_aero(M, h) + Q_elec(P)
        Qout = Q_cool(T)

        dT = (Qin - Qout) / C_th
        T += dT * dt

        if T > T_max:
            return False, T

    return True, T

# ============================================================
# GRID OPTIMIZATION (Pydroid-safe replacement for IPOPT)
# ============================================================

h = 5000

M_vals = np.linspace(0.5, 6.0, 40)
P_vals = np.linspace(0, 2000, 40)

best_score = -1
best = None

feasible = np.zeros((len(M_vals), len(P_vals)))

for i, M in enumerate(M_vals):
    for j, P in enumerate(P_vals):

        ok, T_final = simulate(M, h, P)

        feasible[i, j] = 1 if ok else 0

        if ok:
            # simple performance objective
            score = M + 0.0005 * P

            if score > best_score:
                best_score = score
                best = (M, P, T_final)

# ============================================================
# RESULTS
# ============================================================

print("Best feasible point:")
print("Mach:", best[0])
print("Power:", best[1])
print("Final Temp:", best[2])
print("Score:", best_score)