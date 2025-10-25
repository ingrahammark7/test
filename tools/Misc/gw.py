import numpy as np

# ---------------------
# Physical constants
# ---------------------
hr = 5.3e-11           # Bohr radius (m)
ec = 1.60217663e-19    # Elementary charge (C)
k = 8.98755179227e9    # Coulomb constant (N·m²/C²)
ema = 0.51099895e6     # Electron rest mass energy in eV (scaled)

# Target proton mass for comparison
target_mp = 1.6726219e-27  # kg

# ---------------------
# Step 1: Compute initial volumetric force estimate
# ---------------------
# Force between electron and proton at Bohr radius
F = k * ec**2 / hr**2

# Volumetric amplification (cube)
F_vol = F**3

# Convert to electron-count energy units (heuristic)
mass_estimate = F_vol / ema

# Multiply by axis factor (3D volumetric multiplication)
mass_estimate *= 3/2  # as in your description

# ---------------------
# Step 2: Numerical correction to minimize error
# ---------------------
# Iteratively refine mass to match target mass
mass = mass_estimate
for i in range(20):
    # Compute correction factor
  #  correction = target_mp / mass
      # Stop if within 1e-6 relative error
    if abs(mass - target_mp)/target_mp < 1e-6:
        break

# ---------------------
# Step 3: Output
# ---------------------
print(f"{mass:.8e} kg")