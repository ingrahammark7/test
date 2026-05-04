import sympy as sp

# ----------------------------
# Constants (fully defined)
# ----------------------------
k_B = 1.380649e-23      # Boltzmann constant
T = 300                 # Kelvin (room temp)
c = 3e8                 # speed of light
pi = sp.pi

# ----------------------------
# Symbols
# ----------------------------
P_t, f, r, B, R, V_th = sp.symbols('P_t f r B R V_th', positive=True)

# ----------------------------
# 1. Thermal noise (closed form)
# ----------------------------
N = k_B * T * B
N_eval = sp.N(N)

# ----------------------------
# 2. Received power (free space)
# ----------------------------
P_r = P_t * (c / (4 * pi * f * r))**2
P_r_simplified = sp.simplify(P_r)

# ----------------------------
# 3. SNR closed form
# ----------------------------
SNR = P_r / (k_B * T * B)
SNR_simplified = sp.simplify(SNR)

# ----------------------------
# 4. Shannon capacity
# ----------------------------
C = B * sp.log(1 + SNR, 2)
C_simplified = sp.simplify(C)

# ----------------------------
# 5. Switching condition (diode-like node)
# V_rf = sqrt(P_r * R)
# ----------------------------
V_rf = sp.sqrt(P_r * R)
switch_condition = sp.Eq(V_rf, V_th)

# Solve for max distance r
r_max = sp.solve(switch_condition, r)[0]
r_max_simplified = sp.simplify(r_max)

# ----------------------------
# 6. Node density limit
# spacing ~ λ/10, λ = c/f
# ----------------------------
d_min = c / (10 * f)
rho_max = 1 / d_min**3
rho_simplified = sp.simplify(rho_max)

# ----------------------------
# Human-readable printing
# ----------------------------
def print_results():
    print("\n--- THERMAL NOISE ---")
    print("N = kTB =", N_eval, "watts per Hz")

    print("\n--- RECEIVED POWER ---")
    print("P_r =", P_r_simplified)

    print("\n--- SNR ---")
    print("SNR =", SNR_simplified)

    print("\n--- SHANNON CAPACITY ---")
    print("C =", C_simplified)

    print("\n--- MAX SWITCHING DISTANCE ---")
    print("r_max =", r_max_simplified)

    print("\n--- NODE DENSITY LIMIT ---")
    print("rho_max =", rho_simplified)

# ----------------------------
# Optional: numeric example
# ----------------------------
def example():
    values = {
        P_t: 1e-3,   # 1 mW
        f: 2.4e9,    # WiFi band
        r: 0.1,      # 10 cm
        B: 1e6,      # 1 MHz
        R: 50,       # ohm system
        V_th: 0.2    # threshold
    }

    print("\n--- NUMERIC EXAMPLE ---")

    print("SNR =", float(SNR.subs(values)))
    print("Capacity (bits/s) =", float(C.subs(values)))
    print("r_max (m) =", float(r_max.subs(values)))
    print("Node density (1/m^3) =", float(rho_max.subs(values)))


if __name__ == "__main__":
    print_results()
    example()