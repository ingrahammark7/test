import numpy as np
import matplotlib.pyplot as plt

# Parameter space
Kn = np.logspace(-2, 2, 200)
eps = np.logspace(-2, 2, 200)

K, E = np.meshgrid(Kn, eps)

# Regime classification (heuristic)
Z = np.zeros_like(K)

# 0 = diffusive
Z[(K < 1) & (E < 1)] = 0

# 1 = transitional
Z[(np.abs(np.log10(K)) <= 0.5) | (np.abs(np.log10(E)) <= 0.5)] = 1

# 2 = ballistic / sputter-dominant
Z[(K > 1) & (E > 1)] = 2

plt.figure()
plt.contourf(np.log10(K), np.log10(E), Z)

plt.xlabel("log10(Kn = λ/L)")
plt.ylabel("log10(ε = ion energy / threshold)")
plt.title("Unified Kn–ε Phase Diagram (η implicit)")

plt.show()