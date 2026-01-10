import numpy as np

# -------------------------------
# Aluminum combustion parameters
# -------------------------------
rho_Al = 2700             # kg/m^3
c_Al = 900                # J/kg/K
q_comb = 31e6             # J/kg (combustion energy)
T_ignition = 933 + 100    # K, small particle heating above melting point
R_gas = 8.314             # J/mol/K
E_a_eff = 30e3             # J/mol, effective surface activation energy (realistic)
v0 = 1.0                  # m/s, pre-exponential factor

threshold_mass_loss = 1e-6  # kg/s per particle

# -------------------------------
# Particle radii: 1 μm to 1 mm
# -------------------------------
particle_radii = np.logspace(-6, -3, 100)  # meters

# -------------------------------
# Heat diffusion factor
# Small particles heat almost instantly
# Larger particles have surface-limited burning
# -------------------------------
r0 = 1e-5  # characteristic diffusion length (~10 μm)
T_eff = T_ignition * (r0 / (r0 + particle_radii)) + 300 * (particle_radii / (r0 + particle_radii))

# -------------------------------
# Arrhenius burn velocity (surface-limited)
# -------------------------------
v_burn = v0 * np.exp(-E_a_eff / (R_gas * T_eff))

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
print(f"{'Radius (μm)':>12} | {'v_burn (m/s)':>12} | {'Burn rate (kg/s)':>15}")
print("-"*45)
for r, v, m_dot in zip(particle_radii, v_burn, particle_mass_rate):
    print(f"{r*1e6:12.4f} | {v:12.4e} | {m_dot:15.6e}")

if critical_radius:
    print("\nCritical particle radius (burn rate below threshold): "
          f"{critical_radius*1e6:.4f} μm")
else:
    print("\nAll particle sizes burn faster than the threshold.")