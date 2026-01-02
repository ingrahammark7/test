import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ----------------------------
# 1. Load JSON
# ----------------------------
data_json = """
{
  "leukemia_allometry": [
    {"species":"Mouse","mass_kg":0.025,"type":"Acute","latency_observed_days":[1,2],"time_to_death_observed_days":[6,10]},
    {"species":"Rat","mass_kg":0.25,"type":"Acute","latency_observed_days":[14,28],"time_to_death_observed_days":[7,14]},
    {"species":"Dog","mass_kg":15,"type":"Acute","latency_observed_days":[12,60],"time_to_death_observed_days":[14,56]},
    {"species":"Human","mass_kg":70,"type":"Acute","latency_observed_days":[180,180],"time_to_death_observed_days":[180,180]},
    {"species":"Mouse","mass_kg":0.025,"type":"Chronic","latency_observed_days":[null,null],"time_to_death_observed_days":[null,null]},
    {"species":"Rat","mass_kg":0.25,"type":"Chronic","latency_observed_days":[null,null],"time_to_death_observed_days":[null,null]},
    {"species":"Dog","mass_kg":15,"type":"Chronic","latency_observed_days":[180,1825],"time_to_death_observed_days":[210,1825]},
    {"species":"Human","mass_kg":70,"type":"Chronic","latency_observed_days":[1825,3650],"time_to_death_observed_days":[1825,3650]}
  ]
}
"""

data = json.loads(data_json)["leukemia_allometry"]

# ----------------------------
# 2. Prepare data arrays
# ----------------------------
masses = []
times = []
types = []

for entry in data:
    mass = entry["mass_kg"]
    leukemia_type = entry["type"]
    # Use median observed latency + time to death for plotting
    latency = entry["latency_observed_days"]
    ttd = entry["time_to_death_observed_days"]
    
    # skip entries with null data
    if latency[0] is None or ttd[0] is None:
        continue
    
    # total time from experiment to death = median(latency + ttd)
    latency_median = np.median(latency)
    ttd_median = np.median(ttd)
    total_time = latency_median + ttd_median
    
    masses.append(mass)
    times.append(total_time)
    types.append(leukemia_type)

masses = np.array(masses)
times = np.array(times)

# ----------------------------
# 3. Fit power-law: t = a * M^b
# ----------------------------
def power_law(M, a, b):
    return a * M**b

params, covariance = curve_fit(power_law, masses, times)
a_fit, b_fit = params
print(f"Fitted power-law: t = {a_fit:.2f} * M^{b_fit:.2f}")

# ----------------------------
# 4. Plotting
# ----------------------------
plt.figure(figsize=(8,6))

# Scatter points with different colors for Acute vs Chronic
for leukemia_type in set(types):
    idx = [i for i, t in enumerate(types) if t == leukemia_type]
    plt.scatter(masses[idx], times[idx], label=leukemia_type, s=100)

# Plot fitted curve
mass_range = np.linspace(min(masses)*0.8, max(masses)*1.2, 100)
plt.plot(mass_range, power_law(mass_range, a_fit, b_fit), 'k--', label=f"Fit: t = {a_fit:.1f} M^{b_fit:.2f}")

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Body Mass (kg)")
plt.ylabel("Time from experiment to death (days)")
plt.title("Allometric Fit of Induced Leukemia Progression")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.show()