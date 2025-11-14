import math

# -------------------------------
# Fixed parameters
# -------------------------------
U_tensile = 50e6     # J/kg
E_mass = 10e9        # J/kg
D = 0.03             # m, fixed diameter
rho_air = 1.2        # kg/m^3
C_d = 1.2
v_wind = 4          # m/s
N_gusts = 1        # number of gusts per year

# -------------------------------
# Wind factor k = 0.5 * rho_air * C_d * v^2
# -------------------------------
k = 0.5 * rho_air * C_d * v_wind**2

# -------------------------------
# Maximum height for fixed D
# -------------------------------
L_max = (U_tensile * D**4 / (N_gusts * k**2))**0.25

# -------------------------------
# L/D ratio
# -------------------------------
L_D_ratio = L_max / D

# -------------------------------
# Results
# -------------------------------
print(f"Fixed diameter D: {D:.3f} m")
print(f"Maximum height L_max: {L_max:.2f} m")
print(f"L/D ratio: {L_D_ratio:.2f}")