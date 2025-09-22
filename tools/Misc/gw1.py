import numpy as np
import sympy as sp

m_n = 1.675e-27
G = 6.674e-11
r_nucleus = 1.2e-15

# Neutron rest-mass frequency
m_n = 1.67492749804e-27  # kg, CODATA 2018
c = 299_792_458           # m/s, exact
h = 6.62607015e-34        # J·s, exact

# Calculate frequency
f_n = (m_n * c**2) / h

# Relative uncertainty from neutron mass
delta_m_n = 0.00000000095e-27  # kg
rel_uncertainty = delta_m_n / m_n
delta_f_n = f_n * rel_uncertainty

print(f"Neutron rest-mass frequency: {f_n:.6e} Hz ± {delta_f_n:.2e} Hz")

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
    return ((E_total_MeV*2**sp.GoldenRatio.evalf())*(2**sp.GoldenRatio.evalf()))/12

N_carbon = 12
E_carbon = binding_energy(N_carbon)
actual=7.67
print(f"Predicted binding energy for Carbon-12: {E_carbon:.2e} MeV")
print("error ",E_carbon/actual)