import numpy as np

# ============================================================
# Constants
# ============================================================
c = 3e8
k = 1.380649e-23
pi = np.pi
AU = 1.496e11

# ============================================================
# Mission parameters
# ============================================================
mission_years = 50
seconds = mission_years * 365.25 * 24 * 3600
t = np.linspace(0, seconds, 30000)

# Distance evolution (Voyager-like)
r_start = 5 * AU
r_end = 160 * AU
r = r_start + (r_end - r_start) * (t / seconds)

# ============================================================
# Operational efficiencies
# ============================================================
dsn_availability = 0.25      # Fraction of DSN time allocated
ops_duty_cycle = 0.7         # Instrument + ops duty cycle
coding_efficiency = 0.35     # Fraction of Shannon (Turbo/LDPC)

total_efficiency = dsn_availability * ops_duty_cycle * coding_efficiency

# ============================================================
# Transmitter degradation
# ============================================================
P_tx_initial = 23.0  # W
power_half_life_years = 35
P_tx = P_tx_initial * 0.5 ** (t / (power_half_life_years * 365.25 * 24 * 3600))

# ============================================================
# Antenna model
# ============================================================
def antenna_gain(D, lam, eta):
    return eta * (pi * D / lam) ** 2

D_tx = 3.7
D_rx = 70.0
eta_tx = 0.55
eta_rx = 0.55

# ============================================================
# Shannon rate with bandwidth cap
# ============================================================
def shannon_rate(P_rx, T_sys, B):
    N = k * T_sys * B
    snr = P_rx / N
    return B * np.log2(1 + snr)

# ============================================================
# Radio configuration options
# ============================================================
configs = {
    "X-band": {
        "freq": 8.4e9,
        "bandwidth": 20e3,
        "T_sys": 20
    },
    "Ka-band": {
        "freq": 32e9,
        "bandwidth": 100e3,
        "T_sys": 35
    }
}

# Optical comms
optical = {
    "wavelength": 1550e-9,
    "P_tx": 5.0,
    "D_tx": 0.2,
    "D_rx": 10.0,
    "T_sys": 500,   # photon noise equivalent
    "bandwidth": 1e9
}

# ============================================================
# Simulation
# ============================================================
def simulate_radio(cfg):
    lam = c / cfg["freq"]
    G_tx = antenna_gain(D_tx, lam, eta_tx)
    G_rx = antenna_gain(D_rx, lam, eta_rx)

    P_rx = P_tx * G_tx * G_rx * (lam / (4 * pi * r)) ** 2
    rate = shannon_rate(P_rx, cfg["T_sys"], cfg["bandwidth"])
    bits = np.trapz(rate * total_efficiency, t)
    return bits

def simulate_optical(cfg):
    lam = cfg["wavelength"]
    G_tx = antenna_gain(cfg["D_tx"], lam, 0.6)
    G_rx = antenna_gain(cfg["D_rx"], lam, 0.6)

    P_rx = cfg["P_tx"] * G_tx * G_rx * (lam / (4 * pi * r)) ** 2
    rate = shannon_rate(P_rx, cfg["T_sys"], cfg["bandwidth"])
    bits = np.trapz(rate * total_efficiency, t)
    return bits

# ============================================================
# Results
# ============================================================
print("\n===== TOTAL DATA RETURN ESTIMATES =====\n")

for name, cfg in configs.items():
    bits = simulate_radio(cfg)
    print(f"{name:7s}: {bits/1e9:8.2f} Gb   ({bits/1e12:6.2f} Tb)")

opt_bits = simulate_optical(optical)
print(f"Optical: {opt_bits/1e9:8.2f} Gb   ({opt_bits/1e12:6.2f} Tb)")