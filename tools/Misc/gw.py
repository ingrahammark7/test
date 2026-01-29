import numpy as np

# ----------------------------
# Material properties (generic steel-like)
# ----------------------------
rho = 7850.0            # density kg/m^3
E = 200e9               # Young's modulus Pa
K_IC = 50e6             # fracture toughness Pa*sqrt(m)
c_crit = 0.01           # critical crack length (m) ~ 1 cm
c0 = 1e-5               # initial microcrack length (m)
heat_capacity = 500.0   # J/(kg*K)

# ----------------------------
# Flight / loading parameters
# ----------------------------
accel = 3e4 * 9.81      # axial acceleration (m/s^2)
lengths = np.linspace(0.1, 5.0, 500)  # structure length sweep (m)
radius = 0.15           # structure radius (m)

# ----------------------------
# Helper functions
# ----------------------------
def stress_axial(rho, a, L):
    """Axial stress from acceleration"""
    return rho * a * L

def stress_intensity(sigma, c):
    """Mode-I stress intensity"""
    return sigma * np.sqrt(np.pi * c)

def thermalized_energy(sigma, volume):
    """Fraction of elastic energy converted to heat after crack saturation"""
    elastic_energy = sigma**2 * volume / (2 * E)
    return 0.9 * elastic_energy  # assume 90% thermalization post-failure

# ----------------------------
# Main evaluation
# ----------------------------
failure_length = None
temperature_rise = None

for L in lengths:
    sigma = stress_axial(rho, accel, L)
    K = stress_intensity(sigma, c0)

    if K >= K_IC:
        failure_length = L
        volume = np.pi * radius**2 * L
        Q = thermalized_energy(sigma, volume)
        mass = rho * volume
        temperature_rise = Q / (mass * heat_capacity)
        break

# ----------------------------
# Output
# ----------------------------
if failure_length:
    print(f"Structural coherence fails at length ≈ {failure_length:.2f} m")
    print(f"Estimated temperature rise from thermalization ≈ {temperature_rise:.1f} K")
else:
    print("No failure within evaluated length range")