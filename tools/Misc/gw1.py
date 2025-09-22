import numpy as np
import sympy as sp

m_n = 1.675e-27
G = 6.674e-11
r_nucleus = 1e-15

f_n = 1e22
phase_prob = 1/(f_n**.5)
proximity_factor = 3e8/r_nucleus
cumulative_factor = f_n * phase_prob

def effective_force(m1, m2, r, proximity, cumulative):
    F_newton = G * m1 * m2 / r**2
    F_effective = F_newton * proximity * cumulative
    return F_effective

def binding_energy(N):
    E_total = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            F_eff = effective_force(m_n, m_n, r_nucleus, proximity_factor, cumulative_factor)
            E_pair = F_eff * r_nucleus
            E_total += E_pair
    E_total_MeV = E_total * 6.242e12
    return (E_total_MeV*2**sp.GoldenRatio.evalf())*(1+1/12)

N_carbon = 12
E_carbon = binding_energy(N_carbon)
print(f"Predicted binding energy for Carbon-12: {E_carbon:.2e} MeV")