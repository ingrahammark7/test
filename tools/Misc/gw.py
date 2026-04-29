import numpy as np

def droplet_cutoff_size(gamma, rho, v, we_crit=12):
    """
    Estimate maximum stable droplet size after breakup cascade.

    gamma: surface tension (N/m)
    rho: density (kg/m^3)
    v: velocity (m/s)
    we_crit: critical Weber number (~10–50)
    """
    return (we_crit * gamma) / (rho * v**2)


def spray_distribution(gamma, rho, v, we_crit=12):
    """
    Generate a simple droplet size distribution:
    - cutoff sets upper scale
    - log-normal spread below cutoff
    """
    d_max = droplet_cutoff_size(gamma, rho, v, we_crit)

    # log-spaced distribution below cutoff
    sizes = np.logspace(np.log10(d_max/50), np.log10(d_max), 200)

    # simple synthetic PDF (not empirical CFD, but physically consistent shape)
    pdf = np.exp(- (np.log(sizes / (d_max/5))**2))

    return sizes, pdf, d_max


# Fuel properties
fuels = {
    "RP-1": {"gamma": 0.025, "rho": 800},
    "Water": {"gamma": 0.072, "rho": 1000},
    "LOX": {"gamma": 0.013, "rho": 1140},
}

velocities = [20, 50, 100]  # m/s

print("Droplet cutoff sizes (microns)\n")

for name, props in fuels.items():
    print(f"\n{name}")
    for v in velocities:
        d = droplet_cutoff_size(props["gamma"], props["rho"], v)
        print(f"  v={v:3d} m/s -> d_max = {d*1e6:.2f} µm")