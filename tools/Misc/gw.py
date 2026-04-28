import numpy as np

P = 1.0  # watt
T0 = 300.0  # K
Tmelt = 1687.0  # K
dT = Tmelt - T0

materials = {
    "Aluminum": 237.0,
    "Tungsten": 1703.0
}

def L_critical(k):
    return P / (k * dT)

sizes = np.logspace(-8, -4, 200)  # 10 nm to 100 µm

for name, k in materials.items():
    Lcrit = L_critical(k)
    print(f"{name}: L_crit ≈ {Lcrit*1e6:.2f} µm")

    temps = T0 + P / (k * sizes)

    # find where melting is exceeded
    idx = np.where(temps >= Tmelt)[0]
    if len(idx) > 0:
        print(f"{name}: melts below ~{sizes[idx[0]]*1e6:.2f} µm cube size")
    else:
        print(f"{name}: no melting in range")