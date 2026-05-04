import numpy as np

k_B = 1.380649e-23  # Boltzmann constant

# ----------------------------
# Physical environment model
# ----------------------------
def thermal_noise(bandwidth, temperature=300):
    """Thermal noise power (W)"""
    return k_B * temperature * bandwidth


def snr(received_power, bandwidth, temperature=300):
    noise = thermal_noise(bandwidth, temperature)
    return received_power / noise


def shannon_capacity(bandwidth, snr_value):
    """bits/sec"""
    return bandwidth * np.log2(1 + snr_value)


# ----------------------------
# EM propagation model
# ----------------------------
def received_power_fspl(pt, wavelength, distance):
    """
    Free-space path loss model (simplified)
    pt: transmit power (W)
    wavelength: meters
    distance: meters
    """
    if distance == 0:
        return pt
    return pt * (wavelength / (4 * np.pi * distance))**2


# ----------------------------
# Node switching model
# ----------------------------
def node_switch_probability(v_rf, v_th, noise_sigma=0.1):
    """
    Soft switching probability (logistic-like diode behavior)
    """
    x = (v_rf - v_th) / noise_sigma
    return 1 / (1 + np.exp(-x))


# ----------------------------
# Geometry scaling model
# ----------------------------
def node_density_limit(wavelength, coupling_factor=0.1):
    """
    Estimate max node density before EM cross-talk dominates.
    """
    # heuristic: nodes must be spaced > fraction of wavelength
    min_spacing = coupling_factor * wavelength
    return 1 / (min_spacing**3)  # nodes per m^3


# ----------------------------
# System evaluator
# ----------------------------
def evaluate_system(
    pt=1e-3,           # transmit power (W)
    freq=2.4e9,        # Hz
    distance=0.1,      # m
    bandwidth=1e6,     # Hz
    v_th=0.2           # switching threshold (V proxy)
):
    c = 3e8
    wavelength = c / freq

    pr = received_power_fspl(pt, wavelength, distance)
    snr_val = snr(pr, bandwidth)

    capacity = shannon_capacity(bandwidth, snr_val)

    density = node_density_limit(wavelength)

    # crude RF voltage proxy
    v_rf = np.sqrt(pr * 50)  # assume 50 ohm system

    switch_p = node_switch_probability(v_rf, v_th)

    return {
        "wavelength_m": wavelength,
        "received_power_w": pr,
        "snr": snr_val,
        "capacity_bits_s": capacity,
        "node_density_per_m3": density,
        "rf_voltage_proxy": v_rf,
        "switch_probability": switch_p
    }


# ----------------------------
# Sweep example
# ----------------------------
def sweep_distance():
    results = []
    for d in np.logspace(-3, 1, 20):
        r = evaluate_system(distance=d)
        results.append((d, r["capacity_bits_s"], r["switch_probability"]))
    return results


if __name__ == "__main__":
    res = evaluate_system()
    print("SYSTEM EVALUATION:")
    for k, v in res.items():
        print(f"{k}: {v:.6e}" if isinstance(v, float) else f"{k}: {v}")

    print("\nDistance sweep (distance, capacity, switch_prob):")
    for row in sweep_distance():
        print(row)