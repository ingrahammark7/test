import numpy as np, matplotlib.pyplot as plt

# Define density range and threshold
rho = np.logspace(-3, 3, 400)  # arbitrary units
rho_c = 1.0  # threshold
D0 = 1.0
G0 = 1.0

# Drag model: binary
D = np.where(rho < rho_c, D0, 0.0)

# Gravity model: assume constant for simplicity (since binding is separate)
G = G0 * np.ones_like(rho)

# Ratio (avoid division by zero)
ratio = np.where(G > 0, D/G, np.nan)

plt.figure(figsize=(7,3))
plt.loglog(rho, D, label="Drag D(ρ)")
plt.axvline(rho_c, color='k', linestyle='--', label="ρ_c (threshold)")
plt.xlabel("Ether density ρ (arb. units)")
plt.ylabel("Drag magnitude")
plt.title("Binary drag vs density (ether density controls drag)")
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(7,3))
plt.loglog(rho, ratio, label="D/G ratio")
plt.axvline(rho_c, color='k', linestyle='--', label="ρ_c")
plt.xlabel("Ether density ρ (arb. units)")
plt.ylabel("Drag-to-Gravity ratio")
plt.title("Drag-to-gravity ratio vs ether density")
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()