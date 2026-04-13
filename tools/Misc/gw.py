from matplotlib import pyplot as plt

decades = ["1950s","1960s","1970s","1980s","1990s","2000s","2010s","2020s"]

# -------------------------
# USA estimates (model)
# -------------------------
us_aircraft = [12, 10, 7, 10, 8, 8, 9, 8]
us_missiles = [10, 12, 12, 12, 10, 12, 14, 14]
us_sam      = [3, 5, 5, 5, 4, 5, 6, 7]
us_uav      = [0, 0, 0, 0, 2, 6, 12, 15]

# -------------------------
# USSR/Russia estimates (model)
# -------------------------
ru_aircraft = [8, 5, 3, 5, 2, 2, 3, 2]
ru_missiles = [5, 8, 8, 8, 5, 8, 11, 11]
ru_sam      = [2, 5, 5, 5, 4, 5, 6, 8]
ru_uav      = [0, 0, 0, 0, 1, 4, 8, 10]

# -------------------------
# Plot
# -------------------------
fig, axs = plt.subplots(2, 1, figsize=(11, 10), sharex=True)

# US plot
axs[0].stackplot(
    decades,
    us_aircraft, us_missiles, us_sam, us_uav,
    labels=["Aircraft","Missiles","SAM","UAV"]
)
axs[0].set_title("USA Estimated Weapon System Introduction Complexity")
axs[0].set_ylabel("Systems introduced")
axs[0].legend(loc="upper left")

# USSR/Russia plot
axs[1].stackplot(
    decades,
    ru_aircraft, ru_missiles, ru_sam, ru_uav,
    labels=["Aircraft","Missiles","SAM","UAV"]
)
axs[1].set_title("USSR/Russia Estimated Weapon System Introduction Complexity")
axs[1].set_ylabel("Systems introduced")
axs[1].legend(loc="upper left")

plt.xticks(rotation=45)
plt.xlabel("Decade")
plt.tight_layout()
plt.show()