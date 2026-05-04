import math

# ----------------------------
# Constants
# ----------------------------
k_B = 1.380649e-23     # J/K
T = 300.0              # K
c = 3e8                # m/s
pi = math.pi

# ----------------------------
# Input parameters (edit freely)
# ----------------------------
P_t = 1e-3     # transmit power (W)
f = 2.4e9      # frequency (Hz)
r = 0.1        # distance (m)
B = 1e6       # bandwidth (Hz)
R = 50.0      # ohm system
V_th = 0.2    # switching threshold (V)

# ----------------------------
# 1. Thermal noise
# ----------------------------
N = k_B * T * B

# ----------------------------
# 2. Wavelength
# ----------------------------
wavelength = c / f

# ----------------------------
# 3. Received power (free-space)
# P_r = P_t * (λ / (4πr))^2
# ----------------------------
P_r = P_t * (wavelength / (4 * pi * r))**2

# ----------------------------
# 4. SNR
# ----------------------------
SNR = P_r / N

# ----------------------------
# 5. Shannon capacity
# C = B log2(1 + SNR)
# ----------------------------
C = B * math.log2(1 + SNR)

# ----------------------------
# 6. RF voltage proxy
# V = sqrt(P_r * R)
# ----------------------------
V_rf = math.sqrt(P_r * R)

# ----------------------------
# 7. Switching probability (soft diode model)
# logistic approximation
# ----------------------------
noise_sigma = 0.1
switch_prob = 1 / (1 + math.exp(-(V_rf - V_th) / noise_sigma))

# ----------------------------
# 8. Max switching distance (solve closed form)
# r_max = (c / (4πf)) * sqrt(P_t * R / V_th^2)
# ----------------------------
r_max = (c / (4 * pi * f)) * math.sqrt(P_t * R / (V_th ** 2))

# ----------------------------
# 9. Node density limit
# rho_max = (10f / c)^3
# ----------------------------
rho_max = (10 * f / c) ** 3

# ----------------------------
# PRINT RESULTS
# ----------------------------
print("\n--- FULLY EVALUATED RF COMPUTATION LIMITS ---\n")

print("Thermal noise N (W):", N)
print("Wavelength (m):", wavelength)

print("Received power P_r (W):", P_r)
print("SNR:", SNR)

print("Capacity C (bits/s):", C)

print("RF voltage proxy (V):", V_rf)
print("Switch probability:", switch_prob)

print("Max switching distance r_max (m):", r_max)

print("Node density limit (nodes/m^3):", rho_max)