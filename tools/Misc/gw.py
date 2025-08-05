import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
import matplotlib.pyplot as plt

# --- Constants ---
hbar_c = 197.3  # MeV*fm
mu = 469.0      # MeV/c^2 reduced mass n-p

# --- Parameters ---
r_c = 0.4       # fm hard core radius
r_max = 15.0    # fm max integration radius
m_pi = 0.684    # fm^-1 pion mass scale
g_pi2 = 176.0   # pion coupling squared
m_rho = 3.9     # fm^-1 rho meson mass scale
g_rho2 = 80.0   # rho coupling squared

# --- Potential definitions ---
def V_repulsive(r):
    """Strong short-range repulsive core, approximate infinite barrier"""
    return 1e6 if r < r_c else 0.0

def V_pi(r):
    if r < r_c:
        return 1e6
    return -g_pi2 * np.exp(-m_pi * r) / r

def V_rho(r):
    if r < r_c:
        return 1e6
    return g_rho2 * np.exp(-m_rho * r) / r

def V_central(r):
    return V_repulsive(r) + V_pi(r) + V_rho(r)

def V_tensor(r):
    if r < r_c:
        return 0.0
    x = m_pi * r
    if x == 0:
        return 0.0
    return (1/3) * (g_pi2 / (4 * np.pi)) * (m_pi**2 / r) * (1 + 3/x + 3/(x**2)) * np.exp(-x)

# --- Coupled ODEs ---
def coupled_odes(r, y, E):
    u0, u2, du0, du2 = y
    centrifugal = (hbar_c**2 * 6) / (2 * mu * r**2) if r != 0 else 0
    V00 = V_central(r)
    V22 = V_central(r)
    VT = V_tensor(r)
    d2u0 = (2*mu / hbar_c**2) * ((V00 - E) * u0 + VT * u2)
    d2u2 = (2*mu / hbar_c**2) * ((V22 + centrifugal - E) * u2 + VT * u0)
    return [du0, du2, d2u0, d2u2]

# --- Integration function ---
def integrate(E, alpha):
    y0 = [0.0, 0.0, 1.0, alpha]  # initial slopes at r_c
    r_span = (r_c, r_max)
    r_eval = np.linspace(r_c, r_max, 1000)
    sol = solve_ivp(coupled_odes, r_span, y0, args=(E,), t_eval=r_eval, max_step=0.05)
    return sol

# --- Boundary condition for root finder ---
def boundary_conditions(x):
    E, alpha = x
    sol = integrate(E, alpha)
    u0_end = sol.y[0, -1]
    u2_end = sol.y[1, -1]
    return [u0_end, u2_end]

# --- Find E, alpha by root finding ---
E_guess = -2.0
alpha_guess = 0.1
sol_root = root(boundary_conditions, [E_guess, alpha_guess], method='hybr', tol=1e-6)

if sol_root.success:
    E_sol, alpha_sol = sol_root.x
    print(f"Binding energy: {E_sol:.6f} MeV")
    print(f"D-wave initial slope ratio alpha: {alpha_sol:.6f}")

    # Final integration and wavefunctions
    sol = integrate(E_sol, alpha_sol)
    r = sol.t
    u0 = sol.y[0]
    u2 = sol.y[1]

    # Normalize wavefunctions
    norm = np.trapz(u0**2 + u2**2, r)
    u0 /= np.sqrt(norm)
    u2 /= np.sqrt(norm)

    # Calculate observables
    P_D = np.trapz(u2**2, r)  # D-state probability
    rms = np.sqrt(np.trapz(r**2 * (u0**2 + u2**2), r))  # RMS radius

    # Quadrupole moment approx (fm^2)
    Q_integral = np.trapz(u0 * u2 * r**2, r)
    Q = 1.2 * Q_integral  # scaling factor approx

    print(f"D-state probability: {P_D*100:.3f} %")
    print(f"RMS radius: {rms:.3f} fm")
    print(f"Quadrupole moment (approx): {Q:.4f} fm^2")

    # Plot wavefunctions
    plt.plot(r, u0, label='S-wave u0(r)')
    plt.plot(r, u2, label='D-wave u2(r)')
    plt.xlabel('r (fm)')
    plt.ylabel('Normalized radial wavefunctions')
    plt.title(f'Deuteron Wavefunctions (E={E_sol:.4f} MeV, D-state={P_D*100:.3f}%)')
    plt.legend()
    plt.grid()
    plt.show()
else:
    print("Root finding failed:", sol_root.message)