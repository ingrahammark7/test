import math

# -------------------------------
# Parameters (J/kg convention)
# -------------------------------
U_tensile = 50e6      # J/kg, tensile energy per mass
E_mass = 10e9          # J/kg, stiffness per mass
rho_stalk = 200        # kg/m^3, stalk density
D = 0.03               # m, fixed diameter
rho_air = 1.2          # kg/m^3
C_d = 1.2
v_wind = 4             # m/s
N_gusts = 1e6          # number of effective gusts per year

# -------------------------------
# Wind factor
# -------------------------------
k = 0.5 * rho_air * C_d * v_wind**2

# -------------------------------
# Maximum height for fixed D (density included)
# -------------------------------
L_max = ((3 * math.pi**2 * rho_stalk * E_mass * U_tensile * D**6) / (128 * k**2 * N_gusts))**0.25

# -------------------------------
# L/D ratio
# -------------------------------
L_D_ratio = L_max / D

# -------------------------------
# Results
# -------------------------------
print(f"Stalk diameter D: {D:.3f} m")
print(f"Maximum height L_max: {L_max:.2f} m")
print(f"L/D ratio: {L_D_ratio:.2f}")