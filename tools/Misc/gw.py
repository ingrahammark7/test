# Python program implementing "trivial math" numbers

# User numbers
atmosphere_mass_tons = 1e12  # mass of atmosphere in your units
seeding_mass_tons = 1e6      # cloud seeding mass
fall_distance_m = 1e4**3 #brownian        # falling distance
ff=seeding_mass_tons*fall_distance_m
# Step 2: fraction of atmosphere affected by volume
# Assume Brownian motion spreads seeding evenly over volume fraction
# Total atmospheric volume ~ 4e18 m³
earth_atmosphere_volume_m3 = 4e18
volume_fraction = ff/ earth_atmosphere_volume_m3

# Step 3: naive "effectiveness" metric
# Just multiply mass fraction by volume fraction as trivial math
effectiveness = volume_fraction
print(effectiveness,"% ofnworld")