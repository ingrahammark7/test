import numpy as np

# -----------------------------
# Constants
# -----------------------------
mu0 = 4*np.pi*1e-7

# -----------------------------
# Reader + coupling model
# -----------------------------
reader_power = 1.0          # W (typical upper bound)
coupling_efficiency = 0.01   # 1% (strong but realistic near-field coupling)

P_tag_available = reader_power * coupling_efficiency  # W delivered to tag

# -----------------------------
# Tag electrical model
# -----------------------------
R_load = 20.0               # ohm (effective rectifier + logic load)

# antenna geometry (for current density estimate)
trace_width = 10e-6         # 10 µm
trace_thickness = 0.5e-6
A_cross = trace_width * trace_thickness

# -----------------------------
# Derived electrical quantities
# -----------------------------

# Power-limited current (THIS replaces invalid EM induction formula)
I_rms = np.sqrt(P_tag_available / R_load)

V_rms = I_rms * R_load

P_dissipated = I_rms**2 * R_load

# -----------------------------
# Current density
# -----------------------------
J = I_rms / A_cross

# Electromigration threshold (typical IC metal)
J_em_threshold = 1e10  # A/m^2

# -----------------------------
# Thermal model
# -----------------------------
mass = 1e-6         # 1 mg fob scale (includes package, not just chip)
c = 900
C_th = mass * c

h = 10              # W/m^2K (air + weak convection)
A_surface = 1e-4    # m^2 small device

T_env = 300
T = 300

# steady-state temperature rise
T_rise = P_dissipated / (h * A_surface)

# -----------------------------
# Time evolution (optional transient)
# -----------------------------
dt = 1e-4
steps = 50000

temps = []

for i in range(steps):
    dT = (P_dissipated / C_th - (T - T_env) * (h * A_surface / C_th)) * dt
    T += dT
    temps.append(T)

# -----------------------------
# Output
# -----------------------------
print("=== RFID CONSTRAINED MODEL ===")
print("Available tag power (W):", P_tag_available)
print("RMS voltage (V):", V_rms)
print("RMS current (A):", I_rms)
print("Current density (A/m^2):", J)
print("EM threshold ratio:", J / J_em_threshold)
print("Steady-state temperature rise (K):", T_rise)
print("Max transient temperature (K):", max(temps))