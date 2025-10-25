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

hr=53e-12
ec=1.60217663e-19
k=8.98755179227e9
cr=(ec*ec*k)/(hr**2)
#force vetween two charges
cc3=cr**3
#initially get energy cubed to get fluctuatiin
ema=0.51099895000*10e5
#index mass to electron mass energy
cc3/=ema
#only energy in one axis
cc3/=2/3
ef=ema*ec
ef/=9e16
print(cc3)
print(ef)

#error in electron mass diminants

hr = 5.3e-11  # Bohr radius, meters
ec = 1.60217663e-19  # Coulomb
k = 8.98755179227e9  # Coulomb constant

# Potential energy of electron-proton in hydrogen atom
U = k * ec**2 / hr  # Joules

# Convert to eV
U_eV = U / ec

print(U)      # Joules
print(U_eV)   # eV