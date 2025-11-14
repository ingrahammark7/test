import math

# -------------------------------
# Parameters (J/kg convention)
# -------------------------------
U_tensile = 1e6 # J/kg
g = 9.81  # m/s^2
rho = 1000  # kg/m^3, corn stalk density
rho_air = 1.2  # kg/m^3
C_d = 1.2  # drag coefficient
v_wind = 4  # m/s
N_gusts = 30e6  # effective gusts per year
hvl=.01
hvlsur=rho*hvl*U_tensile

# -------------------------------
# Step 1: Maximum height from gravity
# -------------------------------
L_max = U_tensile / g

# -------------------------------
# Step 2: Minimum diameter for cumulative wind
# -------------------------------
k = 0.5 * rho_air * C_d * v_wind**2
# D^4 = (128 * k^2 * L^4 * N_gusts) / (3 * pi^2 * rho * E * U_tensile)
D_min = ((128 * k**2 * L_max**4 * N_gusts) / (3 * math.pi**2 * rho * (U_tensile*hvlsur)))**(1/4)

# -------------------------------
# Step 3: L/D ratio
# -------------------------------
L_D_ratio = L_max / D_min

# -------------------------------
# Results
# -------------------------------
print(f"Maximum height (L_max): {L_max:.2f} m")
print(f"Minimum diameter (D_min): {D_min:.6f} m")
print(f"L/D ratio: {L_D_ratio:.2f}")