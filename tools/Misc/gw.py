import numpy as np

# Physical constants
R_univ = 8.3145        # J/mol/K
M_Al = 0.02698         # kg/mol
rho_Al = 2700          # kg/m^3
L_vap = 10.8e6         # J/kg, Al latent heat of vaporization
k_Al = 237             # W/m/K
T_surface = 300        # K, ambient
T_particle = 3000      # K, hot particle

# Particle radii (meters)
radii = np.logspace(-6, -3, 50)  # 1 μm → 1 mm

# 1. Saturation vapor pressure of Al (Clapeyron approximation)
# ln(P) = -L/(R*T) + constant (rough approximation)
# Use approximate vaporization constant for Al
P0 = 1e5   # Pa, reference pressure
T0 = 2792  # K, boiling point of Al
J_vapor = (P0 / np.sqrt(2 * np.pi * M_Al * R_univ * T_particle))  # kg/m^2/s

# Actually, J_vapor formula:
# J = P_sat / sqrt(2*pi*m*k*T)
m_Al = M_Al  # kg/mol
J_ideal = (P0 / np.sqrt(2 * np.pi * m_Al / 1.0 * R_univ * T_particle))  # crude placeholder

# 2. Heat-limited flux
J_max = k_Al * (T_particle - T_surface) / (L_vap * radii)

# 3. Effective flux with limiting
J_eff = (J_ideal) / (1 + (J_ideal / J_max))

# 4. Burn velocity and mass rate
v_burn = J_eff / rho_Al  # m/s
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn

# 5. Print table
print(f"{'Radius (μm)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*45)
for r, v, m in zip(radii, v_burn, mass_rate):
    print(f"{r*1e6:12.4f} | {v:12.6e} | {m:15.6e}")