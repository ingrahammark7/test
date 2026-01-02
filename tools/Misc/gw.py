import json
import numpy as np
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
# 2. Prepare arrays
# ----------------------------
masses = []
times = []
species_list = []
types_list = []

for entry in data:
    mass = entry["mass_kg"]
    leukemia_type = entry["type"]
    species = entry["species"]
    
    latency = entry["latency_observed_days"]
    ttd = entry["time_to_death_observed_days"]
    
    # skip entries with null/None data
    if latency[0] is None or ttd[0] is None:
        continue
    
    # median total time
    latency_median = np.median(latency)
    ttd_median = np.median(ttd)
    total_time = latency_median + ttd_median
    
    masses.append(float(mass))
    times.append(float(total_time))
    species_list.append(species)
    types_list.append(leukemia_type)

masses = np.array(masses)
times = np.array(times)

# ----------------------------
# 3. Fit power-law t = a * M^b
# ----------------------------
def power_law(M, a, b):
    return a * M**b

params, _ = curve_fit(power_law, masses, times)
a_fit, b_fit = params

# ----------------------------
# 4. Print numeric results
# ----------------------------
print("Species\tType\tMass(kg)\tTotalTime(days)")
for s, t_type, m, total_time in zip(species_list, types_list, masses, times):
    print(f"{s}\t{t_type}\t{m:.3f}\t{total_time:.1f}")

print("\nPower-law fit: t = a * M^b")
print(f"a = {a_fit:.3f}, b = {b_fit:.3f}")

print("\nPredicted times from fit (days):")
for s, m in zip(species_list, masses):
    predicted = power_law(m, a_fit, b_fit)
    print(f"{s}\t{predicted:.1f}")