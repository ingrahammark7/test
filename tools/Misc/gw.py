import numpy as np

# Constants
c = 299792458.0
G = 6.67430e-11
h = 6.62607015e-34

# Photon energy (500 nm)
lambda_m = 500e-9
E_ph = h * c / lambda_m

def n_min_for_collapse(V1):
    return (c**4 / (2 * G * E_ph)) * ((3 * V1) / (4 * np.pi))**(1/3)

def poisson_tail(lambda_val, k_min, max_terms=100000):
    # computes P(n >= k_min) for Poisson(lambda_val)
    # using log-sum to avoid overflow

    log_term = -lambda_val  # start with n=0 term
    # compute log(P0)
    log_p0 = log_term
    tail = 0.0

    # compute Poisson terms incrementally
    term = np.exp(log_p0)
    for n in range(0, k_min):
        # build up to k_min (ignore them)
        term *= lambda_val / (n + 1)

    # now term = P(k_min)
    tail += term

    for n in range(k_min, k_min + max_terms):
        term *= lambda_val / (n + 1)
        tail += term
        if term < 1e-50:
            break

    return tail

def collapse_probability(N, V0, V1):
    lam = N * (V1 / V0)
    nmin = int(np.ceil(n_min_for_collapse(V1)))

    return poisson_tail(lam, nmin)

def run_example():
    N = 1e30
    R0 = 1e-15
    R1 = 1e-20

    V0 = (4/3) * np.pi * R0**3
    V1 = (4/3) * np.pi * R1**3

    prob = collapse_probability(N, V0, V1)
    print("Collapse probability:", prob)

if __name__ == "__main__":
    run_example()