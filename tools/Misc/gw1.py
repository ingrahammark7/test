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
EC_volume_um3 = 144.0           # µm³

# --- RBC properties ---
RBC_mass_pg = 30.11            # pg
RBC_density = 1.33             # g/cm³
RBC_DNA_fraction = 22.2 / 100.0

# Compute RBC biconcave disk geometry
RBC_volume_um3 = RBC_mass_pg / RBC_density
V = RBC_volume_um3
a = (V / (0.127 * np.pi))**(1/3)
RBC_radius_um = a
RBC_diameter_um = 2 * a
RBC_thickness_um = 0.25 * a

# --- Functions ---
def compute_tau_Q_g(r, max_flow=False):
    """
    Compute shear tau, volumetric flow Q, and g for a capillary of radius r (m).
    If max_flow=True, assume max possible flow with ΔP = P_heart.
    """
    if max_flow:
        deltaP = P_heart  # full pressure drives flow
    else:
        # For demonstration, assume a moderate physiological flow
        # Let's pick ΔP = 1/2 P_heart to avoid g=0
        deltaP = 0.5 * P_heart
    
    # Poiseuille flow
    Q = (np.pi * r**4 * deltaP) / (8 * eta * L)
    
    # Wall shear
    tau = (r * deltaP) / (2 * L)
    
    # Gravity needed to reduce heart pressure to deltaP
    g = (P_heart - deltaP) / (rho * h)
    
    return tau, Q, g

# --- Capillary radii (µm) ---
radii_um = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]
radii = np.array(radii_um) * 1e-6   # convert µm -> m

# --- Table header ---
header = ("Radius(µm)", "Tau(Pa)", "g(m/s²)", "Q(pL/s)", "Feasible")
print("\n" + " | ".join(f"{h:>12}" for h in header))
print("-"*70)

# --- Loop over radii ---
for i, r in enumerate(radii):
    tau, Q, g = compute_tau_Q_g(r, max_flow=False)
    feasible = True if g >= 0 else False
    Q_pl_s = Q*1e12 if not np.isnan(Q) else np.nan
    print(f"{radii_um[i]:12.2f} | {tau:12.3f} | {g:8.3f} | {Q_pl_s:10.3f} | {str(feasible):>8}")

# --- Reference constants ---
print("\nReference cell properties (constants)")
print(f"Endothelial cell: mass = {EC_mass_ng} ng, DNA fraction = {EC_DNA_fraction*100:.2f}%, volume = {EC_volume_um3} µm³")
print(f"Immature RBC: mass = {RBC_mass_pg} pg, DNA fraction = {RBC_DNA_fraction*100:.2f}%, diameter = {RBC_diameter_um:.3f} µm, thickness = {RBC_thickness_um:.3f} µm, density = {RBC_density} g/cm³")