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

# Particle radii (m)
radii = np.logspace(-6, np.log10(HVL_thickness), 50)

# 1. Heat-limited flux
J_max = k_Al * (T_particle - T_surface) / (L_vap * radii)

# 2. Kinetic-theory flux (ideal)
k_B = 1.380649e-23
N_A = 6.02214076e23
m_Al_atom = M_Al / N_A
P0 = 1e5
J_ideal = P0 / np.sqrt(2 * np.pi * m_Al_atom * k_B * T_particle)

# 3. Effective flux limited by heat
J_eff = J_ideal / (1 + J_ideal / J_max)

# 4. Raw burn velocity
v_burn_ideal = J_eff / rho_Al

# 5. Thermal diffusion limit
alpha_Al = k_Al / (rho_Al * c_p)
v_thermal_limit = alpha_Al / radii

# 6. Convection limit (floor)
h_conv = 100  # W/m^2/K
v_conv_limit = h_conv * (T_particle - T_surface) / (rho_Al * L_vap)

# 7. Combine limits
v_burn = np.minimum(v_burn_ideal, v_thermal_limit)
v_burn = np.maximum(v_burn, v_conv_limit)

# 8. Mass loss rates
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn
particle_mass = 4/3 * np.pi * radii**3 * rho_Al

# 9. Time to full burn
t_burn = radii / (3 * v_burn)

# 10. DDT stages
def ddt_stages(v, v_conv_scalar, v_thermal_scalar):
    stages = []
    if v >= v_thermal_scalar:
        stages.append("fast")
        stages.append("coupling_possible")
    elif v <= v_conv_scalar:
        stages.append("convection")
        stages.append("diffusion_limited")
    else:
        stages.append("slow")
        stages.append("heat_limited")
    return ",".join(stages)

# 11. Shock coupling
v_shock = 2000  # m/s, example detonation velocity
t_shock = 2 * radii / v_shock
shock_fraction = np.minimum(1, t_shock / t_burn)
P_shock_particle = shock_fraction * (L_vap / t_burn)  # W/kg per particle

# 12. Total MW-scale shock power
# Weight by particle mass and integrate over all sizes
total_power_W = np.sum(P_shock_particle * particle_mass)  # Watts
total_power_MW = total_power_W / 1e6

print(f"Estimated total MW-scale shock power: {total_power_MW:.2f} MW\n")

# 13. Print table
print(f"{'Radius (m)':>12} | {'v_burn (m/s)':>12} | {'t_burn (s)':>12} | {'DDT stages':>25} | {'% shock energy':>15}")
print("-"*110)
for r, v, t, vt, vc, f in zip(radii, v_burn, t_burn, v_thermal_limit, np.full_like(radii, v_conv_limit), shock_fraction):
    print(f"{r:12.6e} | {v:12.6e} | {t:12.6e} | {ddt_stages(v, vc, vt):>25} | {f*100:15.2f}")