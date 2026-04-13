import matplotlib.pyplot as plt

decades = ["1950s","1960s","1970s","1980s","1990s","2000s","2010s","2020s"]

# ----------------------------
# Base airframe-level model
# ----------------------------
airframe_aircraft = [25, 20, 15, 18, 12, 12, 14, 12]
airframe_missiles = [18, 22, 22, 22, 16, 22, 28, 28]
airframe_sam      = [6, 10, 10, 10, 8, 10, 12, 15]
airframe_uav      = [0, 0, 0, 0, 3, 10, 20, 25]

# ----------------------------
# US-style (variant-rich expansion)
# ----------------------------
us_aircraft = [int(x*1.6) for x in airframe_aircraft]
us_missiles = [int(x*1.4) for x in airframe_missiles]
us_sam      = [int(x*1.3) for x in airframe_sam]
us_uav      = [int(x*1.2) for x in airframe_uav]

# ----------------------------
# Russian-style (family collapse)
# ----------------------------
ru_aircraft = [int(x*0.6) for x in airframe_aircraft]
ru_missiles = [int(x*0.7) for x in airframe_missiles]
ru_sam      = [int(x*0.7) for x in airframe_sam]
ru_uav      = [int(x*0.8) for x in airframe_uav]

# ----------------------------
# Strict airframe-only model
# ----------------------------
strict_aircraft = [int(x*0.5) for x in airframe_aircraft]
strict_missiles = [int(x*0.5) for x in airframe_missiles]
strict_sam      = [int(x*0.5) for x in airframe_sam]
strict_uav      = [int(x*0.6) for x in airframe_uav]

# ----------------------------
# Plot
# ----------------------------
fig, axs = plt.subplots(3, 1, figsize=(11, 12), sharex=True)

axs[0].stackplot(decades, us_aircraft, us_missiles, us_sam, us_uav,
                 labels=["Aircraft","Missiles","SAM","UAV"])
axs[0].set_title("US-style (Variant-rich classification)")
axs[0].legend(loc="upper left")

axs[1].stackplot(decades, ru_aircraft, ru_missiles, ru_sam, ru_uav,
                 labels=["Aircraft","Missiles","SAM","UAV"])
axs[1].set_title("Russian-style (Family-based classification)")
axs[1].legend(loc="upper left")

axs[2].stackplot(decades, strict_aircraft, strict_missiles, strict_sam, strict_uav,
                 labels=["Aircraft","Missiles","SAM","UAV"])
axs[2].set_title("Strict airframe-only classification")
axs[2].legend(loc="upper left")

plt.xticks(rotation=45)
plt.xlabel("Decade")
plt.tight_layout()
plt.show()