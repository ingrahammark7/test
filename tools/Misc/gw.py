import numpy as np

# Physical constants
R_univ = 8.3145        # J/mol/K
M_Al = 0.02698         # kg/mol
rho_Al = 2700          # kg/m^3
L_vap = 10.8e6         # J/kg
k_Al = 237             # W/m/K
T_surface = 300         # K
T_particle = 3000       # K

# HVL reference
HVL_thickness = 0.03    # m (3 cm)
HVL_mass = HVL_thickness**3 * rho_Al
print(f"HVL particle mass ~ {HVL_mass:.3f} kg")

# Particle radii (m) from 1 μm to HVL scale
radii = np.logspace(-6, np.log10(HVL_thickness), 50)

# 1. Heat-limited flux (J/kg/s)
J_max = k_Al * (T_particle - T_surface) / (L_vap * radii)  # kg/(m^2·s)

# 2. Kinetic-theory flux (for completeness)
k_B = 1.380649e-23  # J/K
N_A = 6.02214076e23
m_Al_atom = M_Al / N_A
P0 = 1e5  # Pa, placeholder
J_ideal = P0 / np.sqrt(2 * np.pi * m_Al_atom * k_B * T_particle)

# 3. Effective flux limited by heat
J_eff = J_ideal / (1 + J_ideal / J_max)

# 4. Raw burn velocity
v_burn_raw = J_eff / rho_Al

# 5. Thermal-diffusion-limited sustained velocity
# Characteristic thermal penetration velocity: v ~ alpha / r, where alpha = thermal diffusivity
alpha_Al = k_Al / (rho_Al * 900)  # thermal diffusivity, 900 J/kg/K heat capacity
v_thermal_limit = alpha_Al / radii

# 6. Sustained burn velocity is min(heat-limited, diffusion-limited)
v_burn_sustained = np.minimum(v_burn_raw, v_thermal_limit)

# Optional: cap small-particle speed to realistic upper limit (~5 m/s)
v_max_realistic = 5.0
v_burn_sustained = np.minimum(v_burn_sustained, v_max_realistic)

# 7. Mass loss rate
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn_sustained

# 8. Print table
print(f"{'Radius (m)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*45)
for r, v, m in zip(radii, v_burn_sustained, mass_rate):
    print(f"{r:12.6e} | {v:12.6e} | {m:15.6e}")