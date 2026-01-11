import numpy as np

# ----------------------------
# Physical constants
# ----------------------------
c = 3.0e8                 # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
eV = 1.602176634e-19      # J
N_A = 6.02214076e23       # Avogadro's number
planck_mass = 2.176e-8    # kg

# ----------------------------
# Adjustable parameters
# ----------------------------
photon_energy_eV = 0.1        # photon energy in eV
v_brownian = 6.19e4           # m/s
time_step_us = 0.1             # microsecond step
total_time_us = 10.0           # total capture window
photonpop = 1e20               # base photon population

# Laser initiation parameters
laser_energy_J = 3.0           # total laser energy applied

# ----------------------------
# Explosive materials: name, density [kg/m^3], hotspot radius [mm], molar mass [kg/mol]
# ----------------------------
materials = [
    ("TATB", 1900, 0.3, 0.337),
    ("RDX", 1750, 0.5, 0.222),
    ("HMX", 1900, 13.0, 0.296)
]

# ----------------------------
# Compute dynamic feedback factor
# ----------------------------
def dynamic_feedback(hotspot_mass):
    factor = planck_mass / hotspot_mass
    factor = np.clip(factor * 1000, 1, 1000)
    return factor

# ----------------------------
# Compute trapped photons and energy
# ----------------------------
def compute_trapped_photons(density, radius_mm, photon_energy_eV, capture_time_us, M):
    r = radius_mm * 1e-3
    volume = (4/3) * np.pi * r**3
    mass = density * volume
    g = G * mass / r**2

    photon_energy = photon_energy_eV * eV
    capture_time = capture_time_us * 1e-6
    escape_time = v_brownian / g

    photons_trapped = capture_time / escape_time * photonpop
    feedback_factor = dynamic_feedback(mass)
    photons_trapped_feedback = photons_trapped * feedback_factor

    equivalent_energy = photons_trapped_feedback * photon_energy
    n_atoms = int((mass / M) * N_A)
    photons_per_atom = photons_trapped_feedback / n_atoms

    return mass, g, photons_trapped_feedback, equivalent_energy, photons_per_atom, n_atoms

# ----------------------------
# Console output with threshold table
# ----------------------------
print("----- Hotspot Photon Containment vs Laser-Equivalent Fraction -----\n")

for name, density, radius_mm, M in materials:
    print(f"Material: {name}, Radius: {radius_mm} mm")
    print(f"{'Time(us)':>8} | {'Photons trapped':>18} | {'Energy (J)':>12} | {'Photons/atom':>14} | {'Laser frac (%)':>15}")
    print("-"*90)

    threshold_reached = False
    t = 0.0
    while t <= total_time_us:
        mass, g, photons_trapped, eq_energy, photons_per_atom, n_atoms = compute_trapped_photons(
            density, radius_mm, photon_energy_eV, t, M
        )
        laser_frac = (eq_energy / laser_energy_J) * 100

        print(f"{t:8.2f} | {photons_trapped:18.3e} | {eq_energy:12.3e} | {photons_per_atom:14.3e} | {laser_frac:15.3f}")

        if not threshold_reached and eq_energy >= laser_energy_J:
            print(f"*** Threshold reached at t = {t:.3f} μs ***")
            threshold_reached = True

        t += time_step_us
    print("\n")