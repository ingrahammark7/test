import numpy as np
import random
import matplotlib.pyplot as plt

# Constants
c = 3e8
k = 1.38e-23
T0 = 290
NF = 5

def noise_power(B, T=T0, NF_db=NF):
    NF = 10 ** (NF_db / 10)
    return k * T * B * NF

def received_power(Pt, Gt, Gr, wavelength, RCS, R):
    return (Pt * Gt * Gr * wavelength**2 * RCS) / ((4 * np.pi)**3 * R**4)

def detection_probability(SNR_db):
    return 1 / (1 + np.exp(-1.5 * (SNR_db - 5)))

def hit_probability(SNR_db):
    return 0.1 + 0.8 * (1 / (1 + np.exp(-0.5 * (SNR_db - 7))))

def simulate_engagement(num_missiles, jammer_power, jammer_bandwidth,
                        radar_hop_bandwidth, jammer_prediction_prob,
                        num_radar_hops=10):
    Pt = 1e3
    Gt = Gr = 500
    freq = 10e9
    wavelength = c / freq
    RCS = 0.5
    max_range = 100000
    noise_floor_base = noise_power(radar_hop_bandwidth)

    hits = 0

    # Number of radar hops jammer bandwidth overlaps (rounded up)
    hops_covered = max(1, int(np.ceil(jammer_bandwidth / radar_hop_bandwidth)))

    for _ in range(num_missiles):
        # Missile range skewed to longer distances
        R = random.triangular(30000, max_range, max_range)
        Pr = received_power(Pt, Gt, Gr, wavelength, RCS, R)

        # Radar hop sequence (random)
        hop_sequence = list(range(num_radar_hops))
        random.shuffle(hop_sequence)

        detection_probs = []

        for hop_index in hop_sequence:
            if random.random() < jammer_prediction_prob:
                # Jammer predicts hop, concentrates power on this hop
                jammer_power_on_hop = jammer_power
            else:
                # Jammer power spread across all hops it covers
                jammer_power_on_hop = jammer_power / hops_covered

            # Jammer PSD on this hop (W/Hz)
            jammer_psd = jammer_power_on_hop / radar_hop_bandwidth

            noise_power_total = noise_floor_base + jammer_psd * radar_hop_bandwidth

            SNR = Pr / noise_power_total
            SNR_db = 10 * np.log10(SNR) if SNR > 0 else -100
            detect_prob = detection_probability(SNR_db)
            detection_probs.append(detect_prob)

        # Aggregate detection over hops (max)
        overall_detection_prob = max(detection_probs)

        tracked = random.random() < overall_detection_prob
        hp = hit_probability(10 * np.log10(Pr / noise_floor_base)) if tracked else 0.05
        if random.random() < hp:
            hits += 1

    return hits

def run_sweep(simulations=50, num_missiles=20,
              jammer_power=1e-7, radar_hop_bandwidth=200e3,
              jammer_bandwidths=None, prediction_probs=None):
    if jammer_bandwidths is None:
        jammer_bandwidths = np.logspace(np.log10(2e4), np.log10(5e6), 10)  # 20 kHz to 5 MHz
    if prediction_probs is None:
        prediction_probs = np.linspace(0, 1, 11)

    results = np.zeros((len(jammer_bandwidths), len(prediction_probs)))

    for i, jb in enumerate(jammer_bandwidths):
        print(f"Testing jammer bandwidth {jb/1e3:.1f} kHz...")
        for j, p in enumerate(prediction_probs):
            hits_accum = 0
            for _ in range(simulations):
                hits_accum += simulate_engagement(num_missiles, jammer_power, jb,
                                                  radar_hop_bandwidth, p)
            avg_hits = hits_accum / simulations
            results[i, j] = avg_hits

    return jammer_bandwidths, prediction_probs, results

if __name__ == "__main__":
    jammer_bandwidths, prediction_probs, results = run_sweep()

    import matplotlib.pyplot as plt

    # Plot heatmap of avg hits (lighter=more hits, worse EW)
    plt.figure(figsize=(10, 6))
    X, Y = np.meshgrid(prediction_probs, jammer_bandwidths / 1e3)
    cp = plt.contourf(X, Y, results, levels=20, cmap='viridis_r')
    plt.colorbar(cp, label='Average Missile Hits out of 20')
    plt.xlabel('Jammer Prediction Probability')
    plt.ylabel('Jammer Instantaneous Bandwidth (kHz)')
    plt.title('Missile Hits vs Jammer Bandwidth and Prediction')
    plt.show()