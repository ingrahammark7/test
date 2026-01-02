import json
import numpy as np
from scipy.optimize import curve_fit

# ----------------------------
# 1. Load JSON (with updated human chronic = 8 years)
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
    {"species":"Dog","mass_kg":15,"type":"Chronic","latency_observed_days":[1010,1010],"time_to_death_observed_days":[1010,1010]},
    {"species":"Human","mass_kg":70,"type":"Chronic","latency_observed_days":[2737,2737],"time_to_death_observed_days":[2737,2737]}
  ]
}
"""

data = json.loads(data_json)["leukemia_allometry"]

# ----------------------------
# 2. Separate Acute vs Chronic
# ----------------------------
def extract_data(leukemia_type):
    masses = []
    times = []
    species_list = []
    for entry in data:
        if entry["type"] != leukemia_type:
            continue
        latency = entry["latency_observed_days"]
        ttd = entry["time_to_death_observed_days"]
        if latency[0] is None or ttd[0] is None:
            continue
        total_time = np.median(latency) + np.median(ttd)
        masses.append(float(entry["mass_kg"]))
        times.append(float(total_time))
        species_list.append(entry["species"])
    return np.array(masses), np.array(times), species_list

# ----------------------------
# 3. Power-law fit function
# ----------------------------
def power_law(M, a, b):
    return a * M**b

# ----------------------------
# 4. Fit and print results
# ----------------------------
for leukemia_type in ["Acute", "Chronic"]:
    masses, times, species_list = extract_data(leukemia_type)
    
    # Fit
    params, _ = curve_fit(power_law, masses, times)
    a_fit, b_fit = params
    
    # Print observed
    print(f"\n{leukemia_type} Leukemia Observed Total Times (days):")
    print("Species\tMass(kg)\tTotalTime(days)")
    for s, m, t in zip(species_list, masses, times):
        print(f"{s}\t{m:.3f}\t{t:.1f}")
    
    # Print fit parameters
    print(f"\n{leukemia_type} Power-law fit: t = a * M^b")
    print(f"a = {a_fit:.3f}, b = {b_fit:.3f}")
    
    # Print predicted times
    print(f"\n{leukemia_type} Predicted Total Times (days):")
    for s, m in zip(species_list, masses):
        predicted = power_law(m, a_fit, b_fit)
        print(f"{s}\t{predicted:.1f}")