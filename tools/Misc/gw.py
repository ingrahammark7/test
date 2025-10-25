import numpy as np
from scipy.integrate import solve_ivp

# ---------------------
# Physical constants
# ---------------------
G = 6.67430e-11
k_B = 1.380649e-23
hbar = 1.054571817e-34
sigma = 5.670374419e-8
a_rad = 4*sigma/3
X_H = 0.7

# ---------------------
# Stellar parameters
# ---------------------
M_star = 1.989e30   # kg
R_star = 6.963e8    # m

# ---------------------
# Nuclear fusion: pp-chain (simplified)
# ---------------------
def epsilon_pp(rho, T, m_p):
    S0 = 4.01e-22
    E_G = (2*np.pi*1.602e-19)**2 * m_p / (2 * hbar**2)
    return rho * X_H**2 * S0 * np.exp(-(3*E_G / (k_B * T))**(1/3))

# ---------------------
# Opacity: Kramers law
# ---------------------
def opacity(rho, T):
    kappa_0 = 4e25
    return kappa_0 * rho * T**-3.5

# ---------------------
# EOS: ideal gas + radiation
# ---------------------
def pressure(rho, T, m_p):
    return rho * k_B * T / m_p + a_rad * T**4

# ---------------------
# Stellar structure ODEs
# ---------------------
def stellar_odes(r, y, m_p):
    m, P, L, T = y
    r_safe = max(r, 1e-10)
    rho = max((P - a_rad * T**4) * m_p / (k_B * T), 1e-10)
    kappa = opacity(rho, T)
    eps = epsilon_pp(rho, T, m_p)
    dm_dr = 4 * np.pi * r_safe**2 * rho
    dP_dr = -G * m * rho / r_safe**2
    dL_dr = 4 * np.pi * r_safe**2 * rho * eps
    dT_dr = - (3 * kappa * rho * L) / (16 * np.pi * sigma * T**3 * r_safe**2)
    return [dm_dr, dP_dr, dL_dr, dT_dr]

# ---------------------
# Solve star for a given core temperature
# ---------------------
def solve_star(T_core, m_p):
    rho_c = 1.62e5 * (T_core / 1.57e7)  # rough scaling
    P_c = pressure(rho_c, T_core, m_p)
    y0 = [0, P_c, 0, T_core]
    r0 = 1e3
    sol = solve_ivp(stellar_odes, [r0, R_star], y0, args=(m_p,), max_step=1e6, rtol=1e-6)
    T_surf = sol.y[3, -1]
    return T_surf

# ---------------------
# Find self-consistent T_core for a given proton mass
# ---------------------
def find_stable_T_core(m_p):
    T_low = 1e6
    T_high = 1e8
    for _ in range(20):
        T_mid = (T_low + T_high) / 2
        T_surf = solve_star(T_mid, m_p)
        if T_surf < 1.2e4:  # slightly relaxed surface temp criterion
            T_high = T_mid
        else:
            T_low = T_mid
    T_final = (T_low + T_high) / 2
    T_surf_final = solve_star(T_final, m_p)
    if T_surf_final < 1.2e4:
        return True
    return False

# ---------------------
# Scan proton masses to find optimal
# ---------------------
m_p_values = np.linspace(1.5e-27, 1.8e-27, 20)
optimal_m_p = None

for i in range(1, len(m_p_values)):
    if not find_stable_T_core(m_p_values[i-1]) and find_stable_T_core(m_p_values[i]):
        # bisection to refine optimal m_p
        mp_low = m_p_values[i-1]
        mp_high = m_p_values[i]
        for _ in range(20):
            mp_mid = (mp_low + mp_high)/2
            if find_stable_T_core(mp_mid):
                mp_high = mp_mid
            else:
                mp_low = mp_mid
        optimal_m_p = (mp_low + mp_high)/2
        break

# ---------------------
# Output
# ---------------------
if optimal_m_p is not None:
    print(f"{optimal_m_p:.5e}")
else:
    print("No stable proton mass found in scanned range")