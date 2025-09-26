import numpy as np

# --- Blood & capillary parameters ---
rho = 1060.0                  # blood density (kg/m^3)
P_heart_mmHg = 120.0
P_heart = P_heart_mmHg * 133.322368  # Pa
L = 1.0e-3                     # capillary length (m)
h = 1.5                        # vertical head (m)
eta = 3.5e-3                    # blood viscosity (Pa·s)

# --- Endothelial cell properties ---
EC_mass_ng = 1.013             # ng
EC_DNA_fraction = 0.66 / 100.0 # fraction
EC_volume_um3 = 144.0           # um^3

# --- RBC properties (immature/reticulocyte) ---
RBC_mass_pg = 30.11            # pg
RBC_density = 1.33             # g/cm^3
RBC_DNA_fraction = 22.2 / 100.0

# Compute RBC biconcave disk geometry
# Volume V = mass / density
# Convert g/cm³ → pg/µm³: 1 g/cm³ = 1e-12 pg/µm³? Actually: 1 g/cm³ = 1 pg/µm³? Let's compute carefully
# 1 cm³ = 1e12 µm³, 1 g = 1e12 pg → 1 g/cm³ = 1 pg/µm³ ✅
RBC_volume_um3 = RBC_mass_pg / RBC_density  # µm³
# Biconcave disk approximation: V = pi*h/6*(3a^2 + h^2), assume h = 0.25*a
V = RBC_volume_um3
a = (V / (0.127 * np.pi))**(1/3)
RBC_radius_um = a
RBC_diameter_um = 2 * a
RBC_thickness_um = 0.25 * a

# --- Functions ---
def deltaP_from_tau(r, tau):
    """ΔP (Pa) required to produce wall shear tau (Pa) in a cylindrical vessel of radius r and length L."""
    return 2.0 * L * tau / r

def g_and_Q_for_tau_and_r(r, tau):
    """Compute gravitational acceleration g and volumetric flow Q for given radius r (m) and shear tau (Pa)."""
    dP = deltaP_from_tau(r, tau)
    if dP <= 0 or dP > P_heart:
        return np.nan, np.nan
    g = (P_heart - dP) / (rho * h)
    if g < 0:
        return np.nan, np.nan
    Q = (np.pi * r**4 * dP) / (8.0 * eta * L)
    return g, Q

# --- CLI Sweep ---
radii = np.linspace(1e-6, 12e-6, 12)  # radii 1–12 µm
tau_targets = [0.5, 1.0, 2.0]          # shear stress targets in Pa

# --- Print table header ---
header = ("Radius(µm)", "Tau(Pa)", "g(m/s²)", "Q(pL/s)", "Feasible",
          "EC_mass(ng)", "EC_DNA_frac", "EC_volume(µm³)",
          "RBC_mass(pg)", "RBC_DNA_frac", "RBC_diam(µm)", "RBC_thick(µm)")
print(" | ".join(f"{h:>12}" for h in header))
print("-"*150)

# --- Loop over radii and tau ---
for tau in tau_targets:
    for r in radii:
        g, Q = g_and_Q_for_tau_and_r(r, tau)
        feasible = True if not np.isnan(g) else False
        Q_pl_s = Q*1e12 if not np.isnan(Q) else np.nan
        print(f"{r*1e6:12.2f} | {tau:12.2f} | {g:8.3f} | {Q_pl_s:10.3f} | {str(feasible):>8} | "
              f"{EC_mass_ng:12.3f} | {EC_DNA_fraction:12.4f} | {EC_volume_um3:14.1f} | "
              f"{RBC_mass_pg:12.3f} | {RBC_DNA_fraction:12.4f} | {RBC_diameter_um:12.3f} | {RBC_thickness_um:12.3f}")