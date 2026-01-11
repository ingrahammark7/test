import numpy as np

# Physical constants
R_univ = 8.3145        # J/mol/K
M_Al = 0.02698         # kg/mol
rho_Al = 2700          # kg/m^3
L_vap = 10.8e6         # J/kg
k_Al = 237             # W/m/K
T_surface = 300        # K
T_particle = 3000      # K
c_p = 900              # J/kg/K
L_fus = 397e3          # J/kg
T_melt = 933           # K

# HVL reference
HVL_thickness = 0.03    # m (3 cm)
HVL_mass = HVL_thickness**3 * rho_Al
print(f"HVL particle mass ~ {HVL_mass:.3f} kg")

# Particle radii (m) from 1 μm to HVL scale
radii = np.logspace(-6, np.log10(HVL_thickness), 50)

# 1. Heat-limited flux (J/kg/s)
J_max = k_Al * (T_particle - T_surface) / (L_vap * radii)

# 2. Kinetic-theory flux (ideal, simplified)
k_B = 1.380649e-23  # J/K
N_A = 6.02214076e23
m_Al_atom = M_Al / N_A
P0 = 1e5  # Pa, placeholder
J_ideal = P0 / np.sqrt(2 * np.pi * m_Al_atom * k_B * T_particle)

# 3. Effective flux limited by heat
J_eff = J_ideal / (1 + J_ideal / J_max)

# 4. Raw burn velocity
v_burn_ideal = J_eff / rho_Al

# 5. Thermal-diffusion-limited velocity
alpha_Al = k_Al / (rho_Al * c_p)  # thermal diffusivity
v_thermal_limit = alpha_Al / radii

# 6. Latent heat / melting limit
E_total = c_p*(T_melt - T_surface) + L_fus + L_vap
v_melt_limit = J_max / (rho_Al * E_total / L_vap)

# 7. Convective limit (vectorized)
h_conv = 100  # W/m^2/K
v_conv_limit = np.full_like(radii, h_conv * (T_particle - T_surface) / (rho_Al * L_vap))

# 8. Combine burn velocities
v_burn = v_burn_ideal.copy()

# Always limited by thermal diffusion
v_burn = np.minimum(v_burn, v_thermal_limit)

# Apply melt and convection limits only for large particles (r > 1 mm)
large_idx = radii > 1e-3
v_burn[large_idx] = np.minimum(v_burn[large_idx], v_melt_limit[large_idx])
v_burn[large_idx] = np.minimum(v_burn[large_idx], v_conv_limit[large_idx])

# 9. Mass loss rates
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn

# 10. Print table
print(f"{'Radius (m)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*50)
for r, v, m in zip(radii, v_burn, mass_rate):
    print(f"{r:12.6e} | {v:12.6e} | {m:15.6e}")