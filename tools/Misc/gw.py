import numpy as np

# ----------------------------
# Physical constants
# ----------------------------
c = 3.0e8                 # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
eV = 1.602176634e-19      # J

# ----------------------------
# Adjustable parameters
# ----------------------------
# Materials dictionary: name -> density (kg/m^3)
materials = {
    "TATB": 1900,
    "RDX": 1800,
    "HMX": 1900,
    "Carbon": 2267
}

photon_energy_eV = 1.0        # photon energy for calculation
photon_energy = photon_energy_eV * eV
capture_time = 1e-6           # 1 microsecond window
v_brownian = 6.19e4           # m/s, from previous model

# Laser initiation reference (photons)
laser_photons_ref = 1e12       # typical microjoule laser

# Planck mass reference
m_planck = 2.176e-8           # kg

# ----------------------------
# Function to compute photon trapping
# ----------------------------
def photon_trapping(radius_mm, density, photon_energy, v_brownian, capture_time):
    r = radius_mm * 1e-3  # convert mm -> m
    volume = (4/3) * np.pi * r**3
    mass = density * volume

    # Gravitational acceleration at center
    g = G * mass / r**2

    # Photon population estimate (arbitrary large number for scaling)
    photonpop = 1e20

    # Escape time
    escape_time = v_brownian / g

    # Trapped photons in capture_time
    photons_trapped = capture_time / escape_time * photonpop

    # Equivalent energy
    equivalent_energy = photons_trapped * photon_energy

    return photons_trapped, equivalent_energy, mass, g

# ----------------------------
# Run for all materials
# ----------------------------
print("----- Hotspot Photon Containment vs Laser -----")
print(f"{'Material':>6} | {'Radius(mm)':>10} | {'Mass(kg)':>10} | {'g(m/s^2)':>10} | {'Photons trapped':>15} | {'Energy(J)':>12} | {'Laser equiv':>12}")
print("-"*90)

for name, density in materials.items():
    # Use Planck-mass radius for first approximation
    # r = (3 m / (4 pi rho))^(1/3)
    r_planck = ((3*m_planck)/(4*np.pi*density))**(1/3)
    radius_mm = r_planck * 1e3

    photons_trapped, energy, mass, g = photon_trapping(radius_mm, density, photon_energy, v_brownian, capture_time)
    laser_equiv = energy / photon_energy

    print(f"{name:>6} | {radius_mm:10.3e} | {mass:10.3e} | {g:10.3e} | {photons_trapped:15.3e} | {energy:12.3e} | {laser_equiv:12.3e}")