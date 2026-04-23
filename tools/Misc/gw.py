from math import sqrt

# effective wafer thermal conductivity (normalized units)
k = 150

# backside coupling (helium vs argon)
h_he = 5.0
h_ar = 1.5

def L_crit(k, h):
    return sqrt(k / h)

def Pi(L, h):
    return L * sqrt(h / k)

# critical length scales
L_he = L_crit(k, h_he)
L_ar = L_crit(k, h_ar)

print("L_crit helium:", L_he)
print("L_crit argon:", L_ar)

# test spatial scales
L_test = [0.1, 0.5, 1.0, 2.0, 5.0]

for L in L_test:
    pi_he = Pi(L, h_he)
    pi_ar = Pi(L, h_ar)

    print(
        f"L={L:.2f} | "
        f"Pi_He={pi_he:.3f} | Pi_Ar={pi_ar:.3f} | "
        f"He={'damped' if pi_he > 1 else 'weak'} | "
        f"Ar={'damped' if pi_ar > 1 else 'weak'}"
    )