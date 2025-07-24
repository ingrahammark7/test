
import numpy as np

# Load mag.csv
mag = np.loadtxt("mag.csv", delimiter=",")

# Convert to nT
nt = (mag - 128) * 1.64

# Save to file
np.savetxt("mag_nt.csv", nt, delimiter=",")

import numpy as np
import matplotlib.pyplot as plt

# Load the nT data
nt = np.loadtxt("mag_nt.csv", delimiter=",")

# Create the plot
plt.figure(figsize=(10, 8))
im = plt.imshow(nt, cmap='seismic', origin='upper')  # 'seismic' is good for diverging values
plt.colorbar(im, label="Magnetic field (nT)")
plt.title("Mercury Magnetic Field (nT)")
plt.xlabel("Longitude Pixels")
plt.ylabel("Latitude Pixels")
plt.tight_layout()

# Show the plot
plt.show()