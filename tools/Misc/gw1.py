import numpy as np

# --- Parameters ---
rho = 1060.0                 # blood density (kg/m^3)
P_heart_mmHg = 120.0          # nominal capillary driving pressure (mmHg)
P_heart = P_heart_mmHg * 133.322368  # Pa
L = 1.0e-3                   # capillary length (m)
h = 1.5                      # vertical head from heart to capillary (m)
eta = 3.5e-3                 # blood viscosity (Pa·s)

# --- Functions ---
def deltaP_from_tau(r, tau):
    return 2.0 * L * tau / r

def g_and_Q_for_tau_and_r(r, tau):
    dP = deltaP_from_tau(r, tau)
    if dP <= 0 or dP > P_heart:
        return np.nan, np.nan
    g = (P_heart - dP) / (rho * h)
    if g < 0:
        return np.nan, np.nan
    Q = (np.pi * r**4 * dP) / (8.0 * eta * L)
    return g, Q

# --- CLI Sweep ---
radii = np.linspace(2e-6, 12e-6, 11)  # radii 2–12 µm in steps
tau_targets = [0.5, 1.0, 2.0]          # shear stress targets in Pa

print(f"{'Radius(µm)':>10} | {'Tau(Pa)':>6} | {'g(m/s²)':>8} | {'Q(pL/s)':>10} | Feasible")
print("-"*55)

for tau in tau_targets:
    for r in radii:
        g, Q = g_and_Q_for_tau_and_r(r, tau)
        feasible = True if not np.isnan(g) else False
        Q_pl_s = Q*1e12 if not np.isnan(Q) else np.nan
        print(f"{r*1e6:10.2f} | {tau:6.2f} | {g:8.3f} | {Q_pl_s:10.3f} | {feasible}")