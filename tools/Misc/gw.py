import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34

def schwarzschild_radius(mass):
    return 2 * G * mass / c**2

def photon_energy_confined(R):
    return hbar * c / R

def simulate_fluctuation(N=1e30, R0=1e-14, dt=1e-20, steps=50000):
    R = R0
    v = 0.0

    for i in range(steps):

        # pick a random fraction of photons
        n = int(N * np.random.rand() * 1e-6)  # up to 0.0001% of N
        if n < 1:
            n = 1

        # pick a random sub-radius (smaller than R)
        R1 = R * np.random.rand() * 0.5  # up to half the radius

        # compute energy of subpopulation
        E1 = n * photon_energy_confined(R1)
        M1 = E1 / c**2
        Rs1 = schwarzschild_radius(M1)

        # check collapse
        if R1 <= Rs1:
            print("Collapse triggered by fluctuation at step", i)
            print("n=", n, "R1=", R1, "Rs1=", Rs1)
            return True

        # bulk contraction (gravity only)
        E_ph = photon_energy_confined(R)
        E = N * E_ph
        M = E / c**2

        a_grav = -G * M / R**2
        v += a_grav * dt
        R += v * dt

        if R <= 0:
            print("Bulk collapse at step", i)
            return True

        if i % 5000 == 0:
            print(f"Step {i}: R={R:.3e}, Rs={schwarzschild_radius(M):.3e}")

    print("No collapse occurred in this run.")
    return False

simulate_fluctuation()