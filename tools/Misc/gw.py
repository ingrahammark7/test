import numpy as np

# -------------------------------
# Aluminum properties
# -------------------------------
rho_Al = 2700          # kg/m^3
M_Al = 0.02698         # kg/mol
H_vap = 293e3 * 1e3    # J/kg -> J/m^3 for density later
T_particle = 3000      # K, hot particle temperature
E_a = 150e3            # J/mol, Arrhenius activation
R_gas = 8.314          # J/mol/K
v0 = 1.0               # m/s, pre-exponential
threshold_mass_loss = 1e-6 # kg/s per particle

# -------------------------------
# Particle radii: 1 μm to 1 mm
# -------------------------------
particle_radii = np.logspace(-6, -3, 100)  # meters

# -------------------------------
# Arrhenius surface reaction
# -------------------------------
v_arr = v0 * np.exp(-E_a / (R_gas * T_particle))

# -------------------------------
# Aluminum self-vaporization flux (Clapeyron)
# -------------------------------
def J_vapor(T):
    """
    Returns kg/m^2/s vapor flux.
    Uses Clausius-Clapeyron: P_sat = P0 * exp(-H_vap/(R*T))
    """
    P0 = 1e5             # reference pressure, Pa
    L_mol = 279e3        # J/mol, Al heat of vaporization
    # Saturation vapor pressure
    P_sat = P0 * np.exp(-L_mol / (R_gas * T))
    # Flux using kinetic theory: J = P / sqrt(2 pi m k T)
    m_particle = M_Al / 6.022e23  # kg per atom
    k_B = 1.380649e-23
    return P_sat / np.sqrt(2 * np.pi * m_particle * k_B * T)  # kg/m2/s

v_vapor = J_vapor(T_particle) / rho_Al  # m/s contribution

# -------------------------------
# Total burn velocity and mass rate
# -------------------------------
v_burn = np.full_like(particle_radii, v_arr + v_vapor)
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
    print(f"{r*1e6:12.4f} | {v:12.6e} | {m_dot:15.6e}")

if critical_radius:
    print("\nCritical particle radius (burn rate below threshold): "
          f"{critical_radius*1e6:.4f} μm")
else:
    print("\nAll particle sizes burn faster than the threshold.")