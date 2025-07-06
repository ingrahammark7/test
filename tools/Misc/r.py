import math

# Constants
ev = 1.60218e-19  # J
planck = 1e-34    # J
en = 1e50         # Total input energy in joules
depth_cm = 1e6    # Shield depth in cm
base_hvl = 1      # HVL at 0.5 MeV in cm
grain_mev = 0.5   # Reference photon energy for HVL scaling
grain_ev = grain_mev * 1e6

def scaled_hvl(energy_ev):
    """Scale HVL based on energy (assume square root scaling)."""
    if energy_ev < grain_ev:
        return base_hvl
    factor = math.sqrt(energy_ev / grain_ev)
    return base_hvl * factor

def photon_count(total_energy_j, photon_energy_ev):
    """Photon count for a given energy band (grain-corrected)."""
    photon_energy_j = photon_energy_ev * ev
    if photon_energy_j < planck:
        return total_energy_j / planck
    correction = math.sqrt(photon_energy_ev / grain_ev)
    return total_energy_j / photon_energy_j / correction

def penetration_fraction(hvl_cm, depth_cm):
    """Energy attenuation fraction after given depth."""
    attenuation = 2 ** (depth_cm / hvl_cm)
    return 1 / attenuation

def delivered_energy_at_depth(total_energy_j, depth_cm, steps=200):
    """Integrate over log spectrum to compute delivered energy."""
    log_min = math.log10(grain_ev)
    log_max = math.log10(1e21)  # up to ZeV
    step = (log_max - log_min) / steps

    total_delivered = 0.0

    for i in range(steps):
        log_ev = log_min + i * step
        mid_ev = 10 ** log_ev
        width_ev = (10 ** (log_ev + step)) - (10 ** log_ev)

        photons = photon_count(total_energy_j, mid_ev)
        hvl = scaled_hvl(mid_ev)
        frac = penetration_fraction(hvl, depth_cm)
        energy_delivered = photons * mid_ev * ev * frac
        total_delivered += energy_delivered

    return total_delivered

# Run example
result = delivered_energy_at_depth(en, depth_cm)
print(f"Delivered energy at {depth_cm:.0e} cm shielding: {result:.3e} J")
print(f"Fraction delivered: {result / en:.3e}")