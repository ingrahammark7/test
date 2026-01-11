import numpy as np

# ----------------------------
# Physical constants
# ----------------------------
c = 3.0e8                 # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
h = 6.62607015e-34        # J·s
eV = 1.602176634e-19      # J

# ----------------------------
# Adjustable parameters
# ----------------------------
density = 1800             # kg/m^3 (generic solid)
photon_energy_eV = 0.1     # sub‑eV photons
photon_energy = photon_energy_eV * eV

capture_time = 1e-6        # 1 microsecond window
photonpop = 1e20           # virtual photon population in hotspot

# empirical Brownian photon speed from prior calculation
v_brownian = 6.19e4        # m/s

# ----------------------------
# Hotspot geometry (Planck-mass scale example)
# ----------------------------
radius_mm = 0.3            # mm
r = radius_mm * 1e-3       # m
volume = (4/3) * np.pi * r**3
mass = density * volume

# ----------------------------
# Effective "information gravity" threshold
# ----------------------------
# Treat gravity as controlling coherence/containment, not acceleration
g_info = G * mass / r**2

# Step 1: Crossing factor for photon escape (Brownian)
# Lower factor => photons stay coherent
crossing_factor = (v_brownian / g_info)**(1/3)  # heuristic

# Step 2: Photons effectively contained
photons_contained = photonpop / crossing_factor * (capture_time / 1e-6)  # per microsecond

# Step 3: Energy equivalence
equivalent_energy = photons_contained * photon_energy
laser_equivalent_photons = equivalent_energy / photon_energy

# ----------------------------
# Threshold check (phenomenological)
# ----------------------------
# Minimal number of photons needed to trigger DDT (arbitrary but scalable)
photon_threshold = 1e8
ddt_possible = photons_contained >= photon_threshold

# ----------------------------
# Output
# ----------------------------
print("----- Hotspot Photon Information Model -----")
print(f"Radius: {radius_mm:.3f} mm")
print(f"Mass: {mass:.3e} kg")
print(f"Information gravity factor: {g_info:.3e} m/s^2")
print(f"Photon energy: {photon_energy_eV:.3f} eV")

print("\n--- Photon statistics ---")
print(f"Photons effectively contained per microsecond: {photons_contained:.3e}")
print(f"Equivalent energy: {equivalent_energy:.3e} J")
print(f"Laser-equivalent photons: {laser_equivalent_photons:.3e}")
print(f"DDT possible at this hotspot? {'YES' if ddt_possible else 'NO'}")