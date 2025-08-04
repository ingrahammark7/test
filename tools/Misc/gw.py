import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal

# --- Constants ---
hbarc = 197.327  # MeV·fm
m_nucleon = 938.92  # MeV/c^2

# --- Woods–Saxon parameters ---
V0 = 50.0       # Potential depth (MeV)
r0 = 1.25       # fm
a = 0.65        # Surface diffuseness (fm)
A = 40          # Mass number (Ca-40)
R = r0 * A**(1/3)  # Nuclear radius (fm)

# Spin-orbit coupling strength (MeV·fm^2)
lam = 15.0

# Radial grid
r_min = 0.01  # fm (avoid r=0 singularity)
r_max = 15.0  # fm
N = 2000      # Number of points
r = np.linspace(r_min, r_max, N)
dr = r[1] - r[0]

# Woods–Saxon potential
def woods_saxon(r):
    return -V0 / (1 + np.exp((r - R) / a))

# Numerical derivative of Woods-Saxon for spin-orbit term
def dV_dr(r):
    delta = 1e-3
    return (woods_saxon(r + delta) - woods_saxon(r - delta)) / (2 * delta)

# Calculate l·s for given l and j
def l_dot_s(l, j):
    return 0.5 * (j*(j+1) - l*(l+1) - 0.75)

# Construct radial Hamiltonian matrix (tridiagonal)
def radial_hamiltonian(l, j):
    # Kinetic energy part (finite difference)
    diag = np.zeros(N)
    offdiag = np.ones(N-1) * (-hbarc**2/(2*m_nucleon*dr**2))
    diag[:] = hbarc**2/(m_nucleon*dr**2)
    
    # Add centrifugal barrier l(l+1)/r^2
    diag += hbarc**2 * l*(l+1) / (2 * m_nucleon * r**2)
    
    # Add Woods–Saxon potential
    Vws = woods_saxon(r)
    diag += Vws
    
    # Add spin-orbit potential
    ls = l_dot_s(l, j)
    Vso = lam * (1/r) * dV_dr(r) * ls
    diag += Vso
    
    return diag, offdiag

# Solve radial equation for given l,j: eigenenergies and wavefunctions
def solve_radial(l, j, n_levels=5):
    diag, offdiag = radial_hamiltonian(l, j)
    energies, vecs = eigh_tridiagonal(diag, offdiag)
    bound_idx = np.where(energies < 0)[0]
    bound_idx = bound_idx[:n_levels]
    return energies[bound_idx], vecs[:, bound_idx]

# Calculate and collect energy levels for l=0..4 and corresponding j
def compute_levels(max_l=4):
    levels = []
    for l in range(max_l+1):
        js = [l + 0.5]
        if l > 0:
            js.append(l - 0.5)
        for j in js:
            energies, _ = solve_radial(l, j, n_levels=5)
            for e in energies:
                levels.append({'E': e, 'l': l, 'j': j})
    levels.sort(key=lambda x: x['E'])
    return levels

# Pauli filling: 2 nucleons per level
def fill_levels(levels, N_nucleons):
    filled_levels = []
    remaining = N_nucleons
    for level in levels:
        capacity = 2  # spin degeneracy
        if remaining <= 0:
            level['occupied'] = 0
        elif remaining >= capacity:
            level['occupied'] = capacity
            remaining -= capacity
        else:
            level['occupied'] = remaining
            remaining = 0
        filled_levels.append(level)
    return filled_levels

# Simple pairing correction (BCS-like): lowers energy by pairing gap Δ for pairs occupied
def pairing_correction(levels, delta=1.0):  # MeV, typical pairing gap
    corrected_levels = []
    for lvl in levels:
        pairs = lvl['occupied'] // 2
        corr_E = lvl['E'] - pairs * delta
        lvl_corr = lvl.copy()
        lvl_corr['E_corr'] = corr_E
        corrected_levels.append(lvl_corr)
    return corrected_levels

# Plot levels and occupation
def plot_levels(levels, title="Nuclear Single Particle Levels"):
    plt.figure(figsize=(10, 8))
    y_vals = [lvl['E'] for lvl in levels]
    occ = [lvl.get('occupied', 0) for lvl in levels]
    labels = [f"l={lvl['l']} j={lvl['j']:.1f}" for lvl in levels]
    
    for i, (y, o) in enumerate(zip(y_vals, occ)):
        color = 'C0' if o == 0 else ('C1' if o == 1 else 'C2')
        plt.hlines(y, 0, 1, colors=color, linewidth=2)
        plt.text(1.05, y, labels[i], verticalalignment='center')
        if o > 0:
            plt.scatter([0.5]*o, [y]*o, color=color, s=30)
    
    plt.xlabel("")
    plt.xticks([])
    plt.ylabel("Energy (MeV)")
    plt.title(title)
    plt.grid(True, axis='y')
    plt.show()

# Main run for a nucleus
N_protons = 20
N_neutrons = 20

# Compute single-particle levels
levels = compute_levels(max_l=4)

# Fill levels with neutrons and protons separately (same spectrum assumed)
filled_levels_neutrons = fill_levels(levels, N_neutrons)
filled_levels_protons = fill_levels(levels, N_protons)

# Apply pairing corrections
paired_neutrons = pairing_correction(filled_levels_neutrons, delta=1.2)
paired_protons = pairing_correction(filled_levels_protons, delta=1.0)

# Plot neutron and proton levels side by side
plot_levels(paired_neutrons, title="Neutron Single Particle Levels (Ca-40)")
plot_levels(paired_protons, title="Proton Single Particle Levels (Ca-40)")