import numpy as np

# Constants
c = 299792458.0              # speed of light (m/s)
G = 6.67430e-11              # gravitational constant (m^3 kg^-1 s^-2)
h = 6.62607015e-34           # Planck constant (J s)

def photon_energy(wavelength_m):
    return h * c / wavelength_m

def schwarzschild_radius(mass_kg):
    return 2 * G * mass_kg / c**2

def gravitational_acceleration(mass_kg, radius_m):
    return G * mass_kg / radius_m**2

def main():
    # Default values
    N = 1e20               # number of photons
    wavelength_nm = 500    # photon wavelength in nm
    radius_m = 1e-10       # confinement radius (1 Å)
    time_s = 1.0

    wavelength_m = wavelength_nm * 1e-9
    E_total = N * photon_energy(wavelength_m)
    mass_equiv = E_total / c**2
    Rs = schwarzschild_radius(mass_equiv)
    ag = gravitational_acceleration(mass_equiv, radius_m)

    drift_speed = ag * time_s
    drift_distance = 0.5 * ag * time_s**2

    # time to travel radius under constant acceleration
    t_collapse = np.sqrt(2 * radius_m / ag)

    print("\n--- Results ---")
    print(f"Total photon energy: {E_total:.3e} J")
    print(f"Mass equivalent: {mass_equiv:.3e} kg")
    print(f"Schwarzschild radius: {Rs:.3e} m")
    print(f"Confinement radius: {radius_m:.3e} m")
    print(f"Gravity acceleration at radius: {ag:.3e} m/s^2")
    print(f"Drift speed after 1 s: {drift_speed:.3e} m/s")
    print(f"Drift distance after 1 s: {drift_distance:.3e} m")
    print(f"Time to move {radius_m:.3e} m under constant acceleration: {t_collapse:.3e} s")
    halv=radius_m/c
    ra=t_collapse/halv
    refl=.5
    ra*=refl
    print("photon population to collapse one pair",ra)

if __name__ == "__main__":
    main()