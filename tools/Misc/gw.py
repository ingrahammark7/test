import numpy as np

# ----------------------------
# Physical constants
# ----------------------------
c = 3.0e8
G = 6.67430e-11
eV = 1.602176634e-19

# ----------------------------
# Hotspot parameters
# ----------------------------
density = 1800                # kg/m^3
radius_mm = 0.3               # Planck-scale hotspot
r = radius_mm * 1e-3
volume = (4/3) * np.pi * r**3
mass = density * volume

# ----------------------------
# Photon parameters
# ----------------------------
photon_energy_eV = 0.1
photon_energy = photon_energy_eV * eV
v_brownian = 6.19e4           # m/s
background_photons = 1e20     # ambient photon population

# ----------------------------
# Gravity
# ----------------------------
g = G * mass / r**2
escape_time = v_brownian / g

# ----------------------------
# Feedback + ignition thresholds
# ----------------------------
feedback_gain = 1e7           # runaway amplification
critical_photons = 1e6        # ignition threshold (small!)
max_photons = 1e18            # saturation cap

# ----------------------------
# Time domain
# ----------------------------
dt = 1e-9                     # 1 ns
t_max = 5e-6                  # 5 microseconds
steps = int(t_max / dt)

# ----------------------------
# State variables
# ----------------------------
photons = 0.0
time = 0.0
ignited = False

# ----------------------------
# Simulation loop
# ----------------------------
for i in range(steps):
    time += dt

    # Photon capture rate (gravity)
    capture_rate = background_photons / escape_time
    captured = capture_rate * dt

    # Brownian loss
    loss = photons / escape_time * dt

    # Net change
    photons += captured - loss

    # Threshold feedback
    if photons > critical_photons:
        photons *= (1 + feedback_gain * dt)

    # Saturation clamp
    photons = min(photons, max_photons)

    # Ignition condition
    if photons >= critical_photons and not ignited:
        ignited = True
        print(f"\n🔥 DETONATION TRIGGERED 🔥")
        print(f"Time: {time*1e6:.3f} µs")
        print(f"Photon count: {photons:.3e}")
        break

# ----------------------------
# Final diagnostics
# ----------------------------
equivalent_energy = photons * photon_energy

print("\n--- Final State ---")
print(f"Hotspot radius: {radius_mm:.3f} mm")
print(f"Hotspot mass: {mass:.3e} kg")
print(f"Gravity: {g:.3e} m/s^2")
print(f"Photon energy: {photon_energy_eV:.2f} eV")
print(f"Photon population: {photons:.3e}")
print(f"Equivalent energy: {equivalent_energy:.3e} J")