import numpy as np

# ----------------------------
# Physical constants
# ----------------------------
c = 3e8                # m/s
G = 6.67430e-11        # m^3/kg/s^2
eV = 1.602176634e-19   # J
laser_photons = 3.125e12  # laser-equivalent photon count

# ----------------------------
# Adjustable parameters
# ----------------------------
density = 1800           # kg/m^3, generic explosive
photon_energy_eV = 1.0   # eV per photon
photon_energy = photon_energy_eV * eV
v_brownian = 6.19e4      # m/s, from prior calculation
capture_time = 1e-6      # 1 microsecond

# ----------------------------
# Hotspot radii to scan (mm)
# ----------------------------
radii_mm = np.array([0.1, 0.3, 0.5, 1.0, 5.0, 13.0])
radii_m = radii_mm * 1e-3

# ----------------------------
# Loop through radii
# ----------------------------
print("Radius(mm) | Mass(kg)    | g_photon(m/s^2) | Photons/μs    | Laser-equiv photons | Gravity/Laser Ratio")
print("-"*95)
for r in radii_m:
    volume = (4/3) * np.pi * r**3
    mass = density * volume
    g_photon = G * mass / r**2
    
    # Number of photons trapped per microsecond
    # Assume photon population proportional to mass
    photonpop = 1e20 * (mass / 0.001)  # scale from 1g carbon example
    escape_time = v_brownian / g_photon
    photons_trapped = capture_time / escape_time * photonpop
    
    equivalent_energy = photons_trapped * photon_energy
    laser_equiv = equivalent_energy / photon_energy
    
    gravity_ratio = photons_trapped / laser_photons
    
    print(f"{r*1e3:10.3f} | {mass:10.3e} | {g_photon:14.3e} | {photons_trapped:13.3e} | {laser_equiv:17.3e} | {gravity_ratio:17.3e}")