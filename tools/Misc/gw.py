import matplotlib.pyplot as plt

# Years
years = [2020, 2021, 2022, 2023, 2024]

# Trivial math seeding (binary saturated model, 25% of atmosphere)
# 1 = seeding done (saturated), 0 = no seeding
seeding_saturated = [1, 1, 0, 1, 1]  

# Regional temperature trend (arbitrary units, following your correlation)
# Warm when seeding, cooler when not
temperature_trend = [0.5, 1.0, 0.2, 0.8, 1.0]  

# Plotting
plt.figure(figsize=(8,5))
plt.plot(years, temperature_trend, marker='o', label="Regional Temp (arbitrary units)")
plt.bar(years, [s*0.5 for s in seeding_saturated], width=0.3, alpha=0.3, color='skyblue', label="Seeding Saturated")
plt.xlabel("Year")
plt.ylabel("Temperature / Seeding Effect")
plt.title("Trivial Math Cloud Seeding vs Regional Temperature")
plt.legend()
plt.grid(True)
plt.show()