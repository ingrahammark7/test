# Simple simulation of a coupled regional population system with:
# - intrinsic growth pressure (r)
# - tightening constraints that reduce r over time
# - local extinction threshold (MVP)
# - migration between regions

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# Parameters
num_regions = 20
timesteps = 200

initial_pop = 1000
mvp = 50

# intrinsic growth pressure
base_r = 1.05

# constraint tightening rate (reduces effective r over time)
constraint_rate = 0.002

# migration rate between regions
migration_rate = 0.01

# initialize populations
pop = np.full(num_regions, initial_pop, dtype=float)

# track totals
total_pop = []
alive_regions = []

for t in range(timesteps):
    # effective growth rate decreases over time (constraints tighten)
    r_effective = base_r - constraint_rate * t
    r_effective = max(r_effective, 0.5)  # cannot go below 0.5 in this model
    
    # growth step
    pop = pop * r_effective
    
    # migration (simple diffusion-like mixing)
    migration = migration_rate * (np.mean(pop) - pop)
    pop = pop + migration
    
    # local extinction threshold
    pop[pop < mvp] = 0
    
    total_pop.append(np.sum(pop))
    alive_regions.append(np.sum(pop > 0))

# Plot results
plt.figure()
plt.plot(total_pop)
plt.title("Total Population Over Time")
plt.xlabel("Time")
plt.ylabel("Population")

plt.figure()
plt.plot(alive_regions)
plt.title("Number of Surviving Regions Over Time")
plt.xlabel("Time")
plt.ylabel("Regions")

plt.show()

# Final summary
final_total = total_pop[-1]
final_alive = alive_regions[-1]

final_total, final_alive