import matplotlib.pyplot as plt
import numpy as np

# Data with representative engines
engines = [
    ("Car engine (3L)", 0.1, 1.0),
    ("Truck (Cummins X15)", 0.4, 1.2),
    ("Locomotive (EMD 710G)", 2.2, 1.5),
    ("Wärtsilä 32", 1.5, 1.6),
    ("MAN 32/44 CR", 3, 2.2),
    ("Wärtsilä 46F", 7, 3.4),
    ("MAN 6S60ME-C", 15, 4.0),
    ("RTA96-C", 80, 5.5)
]

powers = [e[1] for e in engines]
ratios = [e[2] for e in engines]

plt.figure(figsize=(9,6))
plt.scatter(powers, ratios, c='orange', s=80, edgecolors='k')

for name, power, ratio in engines:
    plt.text(power*1.05, ratio, name, fontsize=8, va='center')

plt.xscale('log')
plt.xlabel('Engine power (MW)')
plt.ylabel('Piston mass fraction (%)')
plt.title('Piston-to-engine mass ratio vs. power (with representative engines)')
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.show()