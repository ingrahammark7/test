import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Constants
hbar_c = 197.3  # MeV·fm
mu = 469.0      # Reduced mass (MeV/c^2)
m_pi = 0.684    # pion mass in fm^-1

# Potential parameters
V0_rep = 400.0    # MeV
alpha = 10.0      # fm^-1

g2 = 176.0        # coupling constant for Yukawa

A_spin = -5.0     # MeV
beta_spin = 1.0   # fm^-1
S_dot = 0.25      # spin factor for triplet

# Normalization factor squared for trial wavefunction N^2 = lambda^3 / pi
def norm_sq(lam):
    return lam**3 / np.pi

# Kinetic energy expectation
def kinetic(lam):
    return (hbar_c**2 * lam**2) / (2 * mu)

# Integral helper: <e^{-c r}> with wavefunction squared ~ r^2 e^{-2 lambda r}
# Using integral: ∫0^∞ r^2 e^{-(2λ + c)r} dr = 2 / (2λ + c)^3
def exp_decay_expectation(lam, c):
    return 2 / (2*lam + c)**3

# Expectation values of potential terms
def V_rep(lam):
    N2 = norm_sq(lam)
    # <V_rep> = V0 * 4pi * N^2 * integral of r^2 e^{-(2λ + alpha)r} dr
    # integral = 2/(2λ + alpha)^3
    integral = exp_decay_expectation(lam, alpha)
    return V0_rep * 4 * np.pi * N2 * integral

def V_att(lam):
    N2 = norm_sq(lam)
    integral = exp_decay_expectation(lam, m_pi)
    return -g2 * 4 * np.pi * N2 * integral

def V_spin(lam):
    N2 = norm_sq(lam)
    integral = exp_decay_expectation(lam, beta_spin)
    return A_spin * S_dot * 4 * np.pi * N2 * integral

# Total energy expectation
def total_energy(lam):
    T = kinetic(lam)
    V = V_rep(lam) + V_att(lam) + V_spin(lam)
    return T + V

# Minimize total energy for positive lambda
res = minimize_scalar(total_energy, bounds=(0.1, 5.0), method='bounded')

lam_opt = res.x
E_min = res.fun

print(f"Optimal λ = {lam_opt:.4f} fm⁻¹")
print(f"Minimum Energy = {E_min:.4f} MeV")

# Plot energy vs lambda
lams = np.linspace(0.1, 5.0, 200)
energies = [total_energy(l) for l in lams]

plt.plot(lams, energies)
plt.xlabel("Variational parameter λ (fm⁻¹)")
plt.ylabel("Energy expectation (MeV)")
plt.title("Variational energy for deuteron model")
plt.grid(True)
plt.show()