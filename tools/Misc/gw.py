import math

def droplet_size(surface_tension, density, velocity):
    """
    Estimate droplet diameter from surface tension balance.

    Parameters:
    surface_tension (gamma): N/m
    density (rho): kg/m^3
    velocity (v): m/s

    Returns:
    droplet diameter in meters
    """
    d = surface_tension / (density * velocity**2)
    return d


# Example fuels at STP-ish conditions

fuels = {
    "RP-1 (kerosene)": {
        "gamma": 0.025,   # N/m
        "rho": 800        # kg/m^3
    },
    "Water (reference)": {
        "gamma": 0.072,
        "rho": 1000
    },
    "Liquid oxygen": {
        "gamma": 0.013,
        "rho": 1140
    }
}

# injector velocities (typical ranges)
velocities = [20, 50, 100]  # m/s

for fuel, props in fuels.items():
    print(f"\n{fuel}")
    for v in velocities:
        d = droplet_size(props["gamma"], props["rho"], v)
        print(f"  v = {v:3d} m/s -> d = {d*1e6:.2f} µm")