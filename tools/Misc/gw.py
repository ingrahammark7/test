import numpy as np
import matplotlib.pyplot as plt

# Plate thickness relative to HVL (0 to 2 HVL)
thickness = np.linspace(0, 2, 300)

# ----------------------------
# Conceptual model:
# - Perturbation: strongest at very thin plates, decreases as absorption rises
# - Absorption: negligible at <1 HVL, rises with thickness
# - Net downstream damage = perturbation - absorption_effect (simplified)
# ----------------------------

# Perturbation: decreases gradually with thickness
perturbation = np.exp(-thickness/0.5)

# Absorption: rises slowly, significant only near 1 HVL
absorption = np.clip((thickness - 0.8)/0.5, 0, 1)  # starts around 0.8 HVL

# Net damage factor: perturbation minus absorbed fraction
net_damage = perturbation * (1 - absorption)

plt.figure(figsize=(8,5))
plt.plot(thickness, perturbation, label="Perturbation (yaw effect)")
plt.plot(thickness, absorption, label="Absorption fraction")
plt.plot(thickness, net_damage, label="Net downstream damage", linewidth=2, color='red')
plt.axvline(1, color='gray', linestyle='--', label="1 HVL threshold")

plt.xlabel("Plate thickness (HVL)")
plt.ylabel("Relative effect (arbitrary units)")
plt.title("Conceptual Interaction of Perturbation and Absorption vs Plate Thickness")
plt.grid(True)
plt.legend()
plt.show()