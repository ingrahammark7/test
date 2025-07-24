import numpy as np

# Load the magnetic field grid (nanotesla)
B_nt = np.loadtxt("mag.csv", delimiter=",")

height, width = B_nt.shape

# Mercury radius and circumference in meters
R_mercury = 2_440_000  # meters
circumference = 2 * np.pi * R_mercury  # ~15,340,000 m

# Assuming the csv covers the **full equatorial circumference** of Mercury:
physical_width_m = circumference  # meters

# Calculate pixel size (meters per pixel)
pixel_size_x = physical_width_m / width
pixel_size_y = pixel_size_x  # Assuming square pixels for simplicity

print(f"Grid size (pixels): width={width}, height={height}")
print(f"Estimated pixel size (meters): dx={pixel_size_x:.1f}, dy={pixel_size_y:.1f}")

# Convert B to Tesla
B = B_nt * 1e-9

# Compute gradient in Tesla per meter using pixel_size
dB_dx_raw, dB_dy_raw = np.gradient(B)
dB_dx = dB_dx_raw / pixel_size_x
dB_dy = dB_dy_raw / pixel_size_y

# Use Mercury's total magnetic dipole moment (A·m^2)
m_total = 3.5e19

# Distribute dipole moment proportionally by B strength
B_sum = np.sum(B)
m_grid = m_total * (B / B_sum)

# Compute force per pixel in Newtons
F_x = m_grid * dB_dx
F_y = m_grid * dB_dy

# Sum force vectors
F_total_x = np.sum(F_x)
F_total_y = np.sum(F_y)
F_total_mag = np.sqrt(F_total_x**2 + F_total_y**2)

print(f"Total dipole force vector (Newtons): ({F_total_x:.3e}, {F_total_y:.3e})")
print(f"Total dipole force magnitude (Newtons): {F_total_mag:.3e}")