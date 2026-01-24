import numpy as np

# Constants
c = 299792458.0              # speed of light (m/s)
G = 6.67430e-11              # gravitational constant (m^3 kg^-1 s^-2)
h = 6.62607015e-34           # Planck constant (J s)

def photon_energy(wavelength_m):
    """Energy of one photon (J)"""
    return h * c / wavelength_m

def schwarzschild_radius(mass_kg):
    """Schwarzschild radius (m)"""
    return 2 * G * mass_kg / c**2

def gravitational_acceleration(mass_kg, radius_m):
    """Newtonian gravitational acceleration at radius (m/s^2)"""
    return G * mass_kg / radius_m**2

def main():
    # Default values (no user input)
    N = 1e20               # number of photons
    wavelength_nm = 500    # photon wavelength in nm
    radius_m = 1e-10       # confinement radius in meters (1 Å)
    time_s = 1.0           # time to compute drift speed after 1 second

    wavelength_m = wavelength_nm * 1e-9
    E_total = N * photon_energy(wavelength_m)
    mass_equiv = E_total / c**2
    Rs = schwarzschild_radius(mass_equiv)
    ag = gravitational_acceleration(mass_equiv, radius_m)

    drift_speed = ag * time_s
    drift_distance = 0.5 * ag * time_s**2

    print("\n--- Results ---")
    print(f"Total photon energy: {E_total:.3e} J")
    print(f"Mass equivalent: {mass_equiv:.3e} kg")
    print(f"Schwarzschild radius: {Rs:.3e} m")
    print(f"Confinement radius: {radius_m:.3e} m")
    print(f"Gravity acceleration at radius: {ag:.3e} m/s^2")
    print(f"Drift speed after 1 s: {drift_speed:.3e} m/s")
    print(f"Drift distance after 1 s: {drift_distance:.3e} m")
    f=ag/radius_m
    print("collapses due to confinement in ",f,"secs")

if __name__ == "__main__":
    main()