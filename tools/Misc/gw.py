import numpy as np

# -----------------------------
# Parameters (with implicit units)
# -----------------------------
Phi_B = 1e18   # atoms / m^2 / s
Phi_0 = 2e18   # atoms / m^2 / s
ns    = 1e19   # atoms / m^2
v0    = 1.0    # m / s
alpha = 1.0    # dimensionless
t     = 1e-9   # s
y     = 0.5    # normalized depth [0,1]
thermalvelocity=500#m/s
atomradius=.2e-9#m
etchrate=4e-6 #m/s
etchrate/=atomradius
therm=thermalvelocity/atomradius

# -----------------------------
# Dimensionless exposure
# -----------------------------
H_B = (Phi_B * t) / ns
H_I = (Phi_0 * (1 + alpha * y) * t) / ns
ratio=therm/etchrate
pow=ratio**(1/3)
print("number of atoms hit before slowing to etch rate",pow)
print("size nanometers",pow*atomradius*1e9)
# -----------------------------
# Velocity law
# -----------------------------
v_B = v0 / (1 + H_B**3)
v_I = v0 / (1 + H_I**3)


# -----------------------------
# Output
# -----------------------------
print("Brownian velocity:", v_B, "m/s")
print("Ion-directed velocity:", v_I, "m/s")
print("Ion > Brown:", v_I > v_B)