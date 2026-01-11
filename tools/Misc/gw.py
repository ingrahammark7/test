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
v_ideal = J_ideal / rho_Al

# 3. Thermal diffusion limit
alpha_Al = k_Al / (rho_Al * c_p)
v_thermal_limit = alpha_Al / radii

# 4. Convection limit
h_conv = 100  # W/m^2/K
v_conv_limit = h_conv * (T_particle - T_surface) / (rho_Al * L_vap)

# 5. Combine burn limits (ideal, thermal, convection separate)
v_burn = np.minimum(v_ideal, v_thermal_limit)  # ideal+thermal
v_burn = np.minimum(v_burn, v_conv_limit)      # apply convection limit

# 6. Mass loss rates
mass_rate = 4 * np.pi * radii**2 * rho_Al * v_burn

# 7. Time to full burn
t_burn = radii / (3 * v_burn)

# 8. DDT stages (scalar logic)
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

# 9. Print main table
print(f"\n{'Radius (m)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15} | {'t_burn (s)':>12} | {'DDT stages':>25}")
print("-"*100)
for r, v, m, t, vt, vc in zip(radii, v_burn, mass_rate, t_burn, v_thermal_limit, np.full_like(radii, v_conv_limit)):
    print(f"{r:12.6e} | {v:12.6e} | {m:15.6e} | {t:12.6e} | {ddt_stages(v, vc, vt):>25}")

# 10. Second table: closeness to each regime (%)
thermal_pct = v_burn / v_thermal_limit * 100
conv_pct = v_burn / v_conv_limit * 100
ideal_pct = v_burn / v_ideal * 100

print(f"\n{'Radius (m)':>12} | {'% thermal':>10} | {'% conv':>10} | {'% ideal':>10}")
print("-"*55)
for r, t, c, i in zip(radii, thermal_pct, conv_pct, ideal_pct):
    print(f"{r:12.6e} | {t:10.2f} | {c:10.2f} | {i:10.2f}")