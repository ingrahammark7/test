import numpy as np

# Constants
G = 6.67430e-11         # m^3 kg^-1 s^-2
c = 3e8                 # m/s
eV_to_J = 1.602176634e-19  # J/eV

def photon_gravity(E_eV, n, t=1e1):
    """
    Compute photon gravitational properties:
    - Schwarzschild radius
    - Maximum encounter radius for given photon density and travel time
    """
    # Convert energy to Joules
    E = E_eV * eV_to_J
    
    # Equivalent mass
    m = E / c**2
    
    # Schwarzschild radius
    Rs = 2 * G * m / c**2
    
    # Distance traveled in time t
    L = c * t
    nr=L/Rs
    nc=nr**(1/3)
    nc*=Rs
    print(nc,"maximum radius photons of ev ", E_eV, "start and within seconds ",t,"enter radius ",Rs)
    # Maximum encounter radius for 1 expected encounter
    R_max = np.sqrt(1 / (np.pi * n * L))
    print(R_max)
    
    return Rs, R_max

# Example usage:

# 1 eV photon, realistic density
E_eV = 1
t_sec = 1.0       # 1 second travel

Rs, R_max = photon_gravity(E_eV, t_sec)

print(f"Photon energy: {E_eV} eV")
print(f"  Schwarzschild radius: {Rs:.3e} m")


# You can now vary E_eV, n, or t to explore other scenarios