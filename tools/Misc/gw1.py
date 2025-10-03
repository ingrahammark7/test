#!/usr/bin/env python3
import math

def hill_size(v_w=5.0, g=9.8, theta_deg=35):
    """
    Compute self-consistent hill height and horizontal length
    for a given wind speed and slope angle.
    
    Parameters:
        v_w: wind speed [m/s]
        g: gravity [m/s^2]
        theta_deg: slope angle in degrees (angle of repose)
    
    Returns:
        H: hill height [m]
        L: hill horizontal length [m]
    """
    theta = math.radians(theta_deg)
    H = v_w**2 / (2 * g)
    L = H / math.tan(theta)
    return H, L

def main():
    # Default parameters
    wind_speed = 5.0       # m/s
    gravity = 9.8          # m/s^2
    slope_angle = 35       # degrees
    
    H, L = hill_size(v_w=wind_speed, g=gravity, theta_deg=slope_angle)
    
    print(f"Hill height (H): {H:.2f} m")
    print(f"Hill horizontal length (L): {L:.2f} m")

if __name__ == "__main__":
    main()