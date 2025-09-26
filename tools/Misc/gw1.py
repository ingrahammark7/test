import matplotlib.pyplot as plt
import numpy as np

# Layers and fragility values (arbitrary scale: 1=very stable, 10=extremely fragile)
layers = [
    "Fundamental constants",
    "Chemistry & reactions",
    "Stellar physics",
    "Stellar arrangement",
    "Planetary habitability",
    "Cosmological features"
]

fragility = [1, 2, 5, 8, 9, 10]  # Increasing sensitivity
colors = ['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728', '#9467bd']

# Vertical positions for bars
y_pos = np.arange(len(layers))

plt.figure(figsize=(8,6))
plt.barh(y_pos, fragility, color=colors, edgecolor='black')
plt.yticks(y_pos, layers)
plt.xlabel("Fragility / Sensitivity (1=stable, 10=extreme)")
plt.title("Hierarchy of Fine-Tuning and Fragility in the Universe")
plt.gca().invert_yaxis()  # Top layer at top
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Add numeric labels on bars
for i, v in enumerate(fragility):
    plt.text(v + 0.2, i, str(v), color='black', va='center')

plt.show()