import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34

def schwarzschild_radius(mass):
    return 2 * G * mass / c**2

def photon_energy_confined(R):
    # Approximate photon energy when confined to radius R
    # E ~ ħ c / R
    return hbar * c / R

def run_simulation(N=1e30, R0=1e-20, f=0.55, leak_rate=0.0, dt=1e-22, steps=2000):
    R = R0
    v = 0.0
    t = 0.0

    for i in range(steps):
        # Photon energy depends on confinement
        E_ph = photon_energy_confined(R)

        # Total energy
        E = N * E_ph

        # Mass equivalent
        M = E / c**2

        # Schwarzschild radius
        Rs = schwarzschild_radius(M)

        # Energy density
        u = E / ((4/3) * np.pi * R**3)
        rho = u / c**2

        # Gravity acceleration
        a_grav = -G * M / R**2

        # Radiation pressure in radial direction (anisotropic)
        # f = inward fraction of photons
        P_rad = (2*f - 1) * u

        # Pressure acceleration
        a_rad = P_rad / (rho * R)

        # Net acceleration
        a = a_grav + a_rad

        # Integrate
        v += a * dt
        R += v * dt
        t += dt

        # Leakage
        N *= (1 - leak_rate)

        # Output every 200 steps
        if i % 200 == 0:
            print(f"Step {i}: R={R:.3e}, v={v:.3e}, a={a:.3e}, Rs={Rs:.3e}, E_ph={E_ph:.3e}")

        if R <= 0:
            print(f"Collapse at step {i}, time {t:.3e} s")
            break

        if R < 1e-20:
            print("Stopping: radius too small for approximation.")
            break

if __name__ == "__main__":
    run_simulation()