import numpy as np

# Physical constants
R_univ = 8.3145        # J/mol/K
M_Al = 0.02698         # kg/mol
rho_Al = 2700          # kg/m^3
L_vap = 10.8e6         # J/kg
k_Al = 237             # W/m/K
T_surface = 300        # K
T_particle = 3000      # K

# HVL reference for 511 keV gammas
HVL_thickness = 0.03    # m (3 cm)
HVL_mass = HVL_thickness**3 * rho_Al  # crude cubic approximation
print(f"HVL particle mass ~ {HVL_mass:.3f} kg")

# Particle radii (meters)
# Scale: smallest 1 μm → largest ~ HVL radius
radii = np.logspace(-6, np.log10(HVL_thickness), 50)  # 1 μm → 3 cm

# 1. Heat-limited flux
J_max = k_Al * (T_particle - T_surface) / (L_vap * radii)

# 2. Kinetic flux using Al atomic mass (for completeness)
k_B = 1.380649e-23  # J/K
N_A = 6.02214076e23
m_Al_atom = M_Al / N_A
P0 = 1e5  # Pa, rough placeholder
J_ideal = P0 / np.sqrt(2 * np.pi * m_Al_atom * k_B * T_particle)

# 3. Effective flux
J_eff = J_ideal / (1 + J_ideal / J_max)

# 4. Burn velocity and mass rate
v_burn = J_eff / rho_Al
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn

# 5. Print table
print(f"{'Radius (m)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*45)
for r, v, m in zip(radii, v_burn, mass_rate):
    print(f"{r:12.6e} | {v:12.6e} | {m:15.6e}")