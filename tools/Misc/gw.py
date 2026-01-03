import math

# Constants
sigma = 5.67e-8  # Stefan-Boltzmann constant, W/m²K⁴

# Hose properties
hose_melting_C = 180          # °C
hose_melting_K = hose_melting_C + 273.15

# Fire properties
T_fire_C = 1000               # Fire temperature
T_fire_K = T_fire_C + 273.15

def safe_distance_from_fire(T_fire_K, T_hose_max_K, fire_radius_m=0.5):
    """
    Estimate minimum safe distance from fire where hose won't melt.
    Using simplified radiation model: Q = sigma * T_fire^4 * (R^2 / d^2)
    """
    # Assuming radiative flux at distance d equals safe temperature flux
    # Q_received = sigma * T_hose_max^4
    d_min = fire_radius_m * math.sqrt((T_fire_K / T_hose_max_K)**4)
    return d_min

d_safe = safe_distance_from_fire(T_fire_K, hose_melting_K)
print(f"Minimum safe distance from fire: {d_safe:.2f} m")