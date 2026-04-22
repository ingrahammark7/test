import numpy as np

# Physical constants
h = 6.626e-34
c = 3e8

# -----------------------------
# Optical source parameters (generic)
# -----------------------------
P = 1e-3          # optical power (W)
lam = 500e-9      # wavelength (m)

# Detector parameters
A = 1e-4          # detector area (m^2)
t = 1e1         # integration time (s)

# -----------------------------
# Photon-limited range
# -----------------------------
R = np.sqrt((P * lam * A * t) / (4 * np.pi * h * c))

print("Photon-limited range (m):", R)
print("Photon-limited range (km):", R / 1000)

# -----------------------------
# Photon flux vs range curve
# -----------------------------
ranges = np.linspace(1, R*2, 1000)

flux = (P * lam) / (4 * np.pi * h * c * ranges**2)
photons = flux * A * t

# threshold crossing
threshold_idx = np.where(photons >= 1)[0]

if len(threshold_idx) > 0:
    print("1-photon threshold reached up to:",
          ranges[threshold_idx[-1]], "m")
else:
    print("No detection region under 1-photon criterion")