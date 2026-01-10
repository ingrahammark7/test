import numpy as np

# -------------------------------
# Aluminum combustion parameters
# -------------------------------
rho_Al = 2700            # kg/m^3
k_Al = 237               # W/m/K
c_Al = 900               # J/kg/K
q_comb = 31e6            # J/kg
T_ambient = 3000          # K
E_a = 150e3              # J/mol
R_gas = 8.314            # J/mol/K
v0 = 1.0                 # m/s, pre-exponential surface burn rate factor
threshold_mass_loss = 1e-6 # kg/s per particle

# -------------------------------
# Particle radii: 1 μm to 1 mm
# -------------------------------
particle_radii = np.logspace(-6, -3, 100)  # meters

# -------------------------------
# Heat diffusion factor
# -------------------------------
# Biot number approximation for small spheres: Bi ~ h*r/k, here h ~ q_comb / r
# Simple model: effective temperature drop due to heat diffusion
# Smaller particle → T_eff ~ T_ambient + q_comb / (c*rho)  (fast heating)
# Larger particle → T_eff reduced by diffusion factor ~ 1 / (1 + r/r0)
r0 = 1e-5  # m, characteristic diffusion length (~10 μm)
T_eff = T_ambient + (q_comb / (c_Al * rho_Al)) * (r0 / (r0 + particle_radii))

# -------------------------------
# Arrhenius burn velocity
# -------------------------------
v_burn = v0 * np.exp(-E_a / (R_gas * T_eff))

# -------------------------------
# Mass burn rate per particle
# -------------------------------
particle_mass_rate = 4 * np.pi * particle_radii**2 * rho_Al * v_burn

# -------------------------------
# Find critical radius
# -------------------------------
critical_indices = np.where(particle_mass_rate < threshold_mass_loss)[0]
critical_radius = particle_radii[critical_indices[0]] if len(critical_indices) > 0 else None

# -------------------------------
# Console output
# -------------------------------
print(f"{'Radius (μm)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*35)
for r, m_dot in zip(particle_radii, particle_mass_rate):
    print(f"{r*1e6:12.4f} | {m_dot:15.6e}")

if critical_radius:
    print("\nCritical particle radius (burn rate below threshold): "
          f"{critical_radius*1e6:.4f} μm")
else:
    print("\nAll particle sizes burn faster than the threshold.")