import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Parameters
total_hops = 50
jam_prob = 0.5  # Probability each hop is jammed

# Range of tolerable jammed hops (missile resilience)
tolerable_jams = np.arange(0, total_hops + 1)

# Calculate hit probability for each K (max jammed hops tolerated)
hit_probabilities = [binom.cdf(K, total_hops, jam_prob) for K in tolerable_jams]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(tolerable_jams, hit_probabilities, label='Hit Probability', color='blue')
plt.axhline(0.5, color='gray', linestyle='--', label='50% Threshold')
plt.title('Missile Hit Probability vs. Tolerable Jammed Hops')
plt.xlabel('Maximum Jammed Hops Tolerated (K)')
plt.ylabel('Hit Probability')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()