import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Photon energy for 500 nm
lambda_m = 500e-9
E_ph = h * c / lambda_m

def schwarzschild_radius(mass):
    return 2 * G * mass / c**2

def simulate_fluctuation(N=1e30, R0=1e-15, dt=1e-20, steps=50000*10**2):
    R = R0
    v = 0.0

    for i in range(steps):

        # random subpopulation size (fraction)
        n = int(N * np.random.rand() * 1e-6)
        if n < 1:
            n = 1

        # random subradius
        R1 = R * np.random.rand() * 0.5

        # mass of the fluctuation
        E1 = n * E_ph
        M1 = E1 / c**2
        Rs1 = schwarzschild_radius(M1)

        if R1 <= Rs1:
            print("Collapse triggered by fluctuation at step", i)
            print("n=", n, "R1=", R1, "Rs1=", Rs1)
            return True

        # bulk contraction
        M = (N * E_ph) / c**2
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