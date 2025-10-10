# Analytic (fast) model for hit probability using variance integration (no per-event Monte Carlo)
import math, numpy as np, pandas as pd, matplotlib.pyplot as plt

# Parameters (same as before, editable)
v_proj = 1000.0
diameter = 0.05
LD = 30.0
proj_length = LD * diameter
hill_size = 0.03
base_air_speed = 1.5
occupancy = 0.5
alpha = 0.12
sigma_aim = 0.02
target_radius = 0.3

# Derived
turb_frac_base = hill_size / proj_length
events_per_meter = occupancy / hill_size
amp_factor = math.exp(alpha * LD)
sigma_event = turb_frac_base * base_air_speed * amp_factor

ranges = np.array([50, 100, 200, 300, 500, 800, 1000, 1500, 2000], dtype=float)

results = []
for R in ranges:
    N = events_per_meter * R  # expected number of events (can be non-integer)
    # For uniform event positions, E[(R-x)^2] = R^2 / 3
    var_from_events = N * (sigma_event**2) * (R**2) / (3 * v_proj**2)
    var_total = sigma_aim**2 + var_from_events
    sigma_total = math.sqrt(var_total)
    # Hit probability assuming Gaussian lateral offset with sigma_total
    from math import erf, sqrt
    hit_prob = 0.5*(1 + math.erf(target_radius / (math.sqrt(2)*sigma_total))) - 0.5*(1 + math.erf(-target_radius / (math.sqrt(2)*sigma_total)))
    # simplify: hit_prob = erf(target / (sqrt(2)*sigma_total))
    hit_prob = math.erf(target_radius / (math.sqrt(2)*sigma_total))
    results.append({
        "range_m": R,
        "hit_prob": hit_prob,
        "sigma_total_m": sigma_total,
        "var_events": var_from_events,
        "N_expected": N,
        "sigma_event_m_s": sigma_event,
        "amp_factor": amp_factor,
        "proj_length_m": proj_length
    })

df = pd.DataFrame(results)

# Save CSV and plot
csv_path = "/mnt/data/apfsds_hitprob_analytic.csv"
df.to_csv(csv_path, index=False)

plt.figure(figsize=(8,4))
plt.plot(df['range_m'], df['hit_prob'], marker='o')
plt.xlabel("Range (m)")
plt.ylabel("Hit probability")
plt.title("Estimated hit probability vs range (analytic turbulence model)")
plt.grid(True)
plt.tight_layout()
plot_path = "/mnt/data/hit_prob_analytic.png"
plt.savefig(plot_path)

print("Parameters:")
print(f"v_proj={v_proj} m/s, diameter={diameter} m, LD={LD}, proj_length={proj_length:.3f} m")
print(f"hill_size={hill_size} m, base_air_speed={base_air_speed} m/s, occupancy={occupancy}")
print(f"turb_frac_base={turb_frac_base:.6f}, amp_factor={amp_factor:.3e}, sigma_event={sigma_event:.6f} m/s")
print()
print(df.to_string(index=False))
print()
print(f"CSV saved to: {csv_path}")
print(f"Plot saved to: {plot_path}")