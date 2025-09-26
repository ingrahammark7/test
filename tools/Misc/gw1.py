import scipy.constants as const

# Fundamental constants
alpha0 = const.alpha        # fine-structure constant
e = const.e                 # elementary charge
hbar = const.hbar
c = const.c
m_e = const.m_e
epsilon0 = const.epsilon_0

processes = [
    {"name": "Hydrogen bond (DNA & proteins)", "alpha_min":5.8663e-3, "alpha_max":3.7102e-2, "q1":0.42*e, "q2":0.42*e, "r":0.28e-9, "epsilon_r":1},
    {"name": "Base stacking (DNA)", "alpha_min":5.2470e-3, "alpha_max":2.8739e-2, "C6":1e-77, "r":0.34e-9},  # van der Waals approx
    {"name": "Covalent bond (C–C/C–N)", "alpha_min":3.9664e-3, "alpha_max":2.8046e-2, "r":0.154e-9},
    {"name": "ATP hydrolysis", "alpha_min":5.1600e-3, "alpha_max":1.0320e-2, "q1":e, "q2":-e, "r":0.15e-9, "epsilon_r":80},
    {"name": "Photosynthetic transition", "alpha_min":3.6487e-3, "alpha_max":9.6535e-3, "transition_energy":2.0},  # eV approx
    {"name": "Water H-bond (solvent)", "alpha_min":4.6153e-3, "alpha_max":9.6535e-3, "q1":0.42*e, "q2":0.42*e, "r":0.096e-9, "epsilon_r":80},
]

for p in processes:
    α_min = p["alpha_min"]
    α_max = p["alpha_max"]
    α_geo = (α_min*α_max)**0.5
    frac_tol_down = α_geo / α_min
    frac_tol_up = α_max / α_geo

    # Compute energy at α_geo using physical formulas
    if p["name"] in ["Hydrogen bond (DNA & proteins)", "ATP hydrolysis", "Water H-bond (solvent)"]:
        q1 = p["q1"]
        q2 = p["q2"]
        r = p["r"]
        epsilon_r = p.get("epsilon_r",1)
        E = (α_geo/alpha0)**2 * (q1*q2)/(4*const.pi*epsilon0*epsilon_r*r)
    elif p["name"] == "Base stacking (DNA)":
        # London dispersion approx: E = C6 / r^6 scaled by (α/α0)^2
        E = (α_geo/alpha0)**2 * p["C6"] / p["r"]**6
    elif p["name"] == "Covalent bond (C–C/C–N)":
        # Approximate bond energy ~ α^2 * m_e c^2
        E = (α_geo/alpha0)**2 * m_e * c**2
    elif p["name"] == "Photosynthetic transition":
        # Photon energy, scaled by α^2
        E = (α_geo/alpha0)**2 * p["transition_energy"] * const.e  # convert eV → J

    # CLI output
    print(f"Process: {p['name']}")
    print(f"  α_opt (geometric/log midpoint) = {α_geo:.6e}")
    print(f"  E(α_opt) = {E:.6e} J")
    print(f"  Fractional tolerance: Down={frac_tol_down:.4f}×, Up={frac_tol_up:.4f}×")
    print("-"*60)