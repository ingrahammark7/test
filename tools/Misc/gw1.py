import scipy.constants as const
import numpy as np

# Fundamental constants
alpha0 = const.alpha
e = const.e
hbar = const.hbar
c = const.c
m_e = const.m_e
epsilon0 = const.epsilon_0

# Define processes
processes = [
    # Biochemical / atomic
    {"name": "Hydrogen bond (DNA & proteins)", "alpha_min":5.8663e-3, "alpha_max":3.7102e-2,
     "q1":0.42*e, "q2":0.42*e, "r":0.28e-9, "epsilon_r":1},
    {"name": "Base stacking (DNA)", "alpha_min":5.2470e-3, "alpha_max":2.8739e-2,
     "C6":1e-77, "r":0.34e-9},
    {"name": "Covalent bond (C–C/C–N)", "alpha_min":3.9664e-3, "alpha_max":2.8046e-2,
     "r":0.154e-9},
    {"name": "ATP hydrolysis", "alpha_min":5.1600e-3, "alpha_max":1.0320e-2,
     "q1":e, "q2":-e, "r":0.15e-9, "epsilon_r":80},
    {"name": "Photosynthetic transition", "alpha_min":3.6487e-3, "alpha_max":9.6535e-3,
     "transition_energy":2.0},  # eV
    {"name": "Water H-bond (solvent)", "alpha_min":4.6153e-3, "alpha_max":9.6535e-3,
     "q1":0.42*e, "q2":0.42*e, "r":0.096e-9, "epsilon_r":80},
    # Stellar fusion
    {"name": "Proton-proton fusion (stellar)",
     "alpha_min":alpha0*0.95, "alpha_max":alpha0*1.05, "const":30}  # ±5% α range
]

# Compute α_opt and energy or relative rate
for p in processes:
    alpha_min = p["alpha_min"]
    alpha_max = p["alpha_max"]
    alpha_geo = np.sqrt(alpha_min * alpha_max)
    frac_tol_down = alpha_geo / alpha_min
    frac_tol_up = alpha_max / alpha_geo

    if p["name"] == "Proton-proton fusion (stellar)":
        # Relative tunneling probability
        const_tun = p["const"]
        P0 = np.exp(-const_tun * alpha0)
        P_opt = np.exp(-const_tun * alpha_geo)
        energy_repr = P_opt  # use probability as "energy proxy"
        unit = "relative probability"
    elif "q1" in p and "q2" in p:
        q1 = p["q1"]
        q2 = p["q2"]
        r = p["r"]
        epsilon_r = p.get("epsilon_r", 1)
        energy_repr = (alpha_geo/alpha0)**2 * (q1*q2)/(4*np.pi*epsilon0*epsilon_r*r)
        unit = "J"
    elif "C6" in p:
        r = p["r"]
        C6 = p["C6"]
        energy_repr = (alpha_geo/alpha0)**2 * C6 / r**6
        unit = "J"
    elif "transition_energy" in p:
        energy_repr = (alpha_geo/alpha0)**2 * p["transition_energy"] * const.e
        unit = "J"
    else:
        energy_repr = (alpha_geo/alpha0)**2 * m_e * c**2
        unit = "J"

    # CLI output
    print(f"Process: {p['name']}")
    print(f"  α_opt (geometric midpoint) = {alpha_geo:.6e}")
    print(f"  E(α_opt) = {energy_repr:.6e} {unit}")
    print(f"  Fractional tolerance: Down={frac_tol_down:.4f}×, Up={frac_tol_up:.4f}×")
    print("-"*70)