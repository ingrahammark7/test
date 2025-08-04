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

# Numerical derivative of Woods–Saxon for spin-orbit term
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

# Coulomb potential for protons (uniform charged sphere approx)
def coulomb_potential(r, Z):
    e2 = 1.44  # MeV·fm (elementary charge squared)
    Rc = R  # charge radius approx nuclear radius
    Vc = np.zeros_like(r)
    inside = r < Rc
    outside = ~inside
    Vc[inside] = (e2 * Z / (2*Rc)) * (3 - (r[inside]/Rc)**2)
    Vc[outside] = e2 * Z / r[outside]
    return Vc

# Proton radial Hamiltonian includes Coulomb potential
def radial_hamiltonian_proton(l, j, Z):
    diag, offdiag = radial_hamiltonian(l, j)
    Vc = coulomb_potential(r, Z)
    diag += Vc
    return diag, offdiag

# Solve radial eq for neutrons
def solve_radial_neutron(l, j, n_levels=5):
    diag, offdiag = radial_hamiltonian(l, j)
    energies, vecs = eigh_tridiagonal(diag, offdiag)
    bound_idx = np.where(energies < 0)[0]
    bound_idx = bound_idx[:n_levels]
    return energies[bound_idx], vecs[:, bound_idx]

# Solve radial eq for protons
def solve_radial_proton(l, j, Z, n_levels=5):
    diag, offdiag = radial_hamiltonian_proton(l, j, Z)
    energies, vecs = eigh_tridiagonal(diag, offdiag)
    bound_idx = np.where(energies < 0)[0]
    bound_idx = bound_idx[:n_levels]
    return energies[bound_idx], vecs[:, bound_idx]

# Compute neutron levels
def compute_levels_neutrons(max_l=4):
    levels = []
    for l in range(max_l+1):
        js = [l + 0.5]
        if l > 0:
            js.append(l - 0.5)
        for j in js:
            energies, _ = solve_radial_neutron(l, j, n_levels=5)
            for e in energies:
                levels.append({'E': e, 'l': l, 'j': j})
    levels.sort(key=lambda x: x['E'])
    return levels

# Compute proton levels with Coulomb
def compute_levels_protons(Z, max_l=4):
    levels = []
    for l in range(max_l+1):
        js = [l + 0.5]
        if l > 0:
            js.append(l - 0.5)
        for j in js:
            energies, _ = solve_radial_proton(l, j, Z, n_levels=5)
            for e in energies:
                levels.append({'E': e, 'l': l, 'j': j})
    levels.sort(key=lambda x: x['E'])
    return levels

# Automatic magic number detection based on gaps > threshold (MeV)
def find_magic_numbers(levels, threshold=3.0):
    energies = np.array([lvl['E'] for lvl in levels])
    gaps = energies[1:] - energies[:-1]
    magic_idxs = np.where(gaps > threshold)[0]
    magic_numbers = [2*(i+1) for i in magic_idxs]  # 2 nucleons per level (spin degeneracy)
    print("Detected magic numbers and gap sizes (MeV):")
    for n, g in zip(magic_numbers, gaps[magic_idxs]):
        print(f"Magic number: {n}, gap: {g:.2f} MeV")
    return magic_numbers, gaps[magic_idxs]

# Fill levels applying Pauli principle (2 nucleons max per level)
def fill_levels(levels, N_nucleons):
    remaining = N_nucleons
    for lvl in levels:
        capacity = 2
        if remaining <= 0:
            lvl['occupied'] = 0
        elif remaining >= capacity:
            lvl['occupied'] = capacity
            remaining -= capacity
        else:
            lvl['occupied'] = remaining
            remaining = 0
    return levels

# Plotting single particle levels with occupation
def plot_levels(levels, title="Single Particle Levels"):
    plt.figure(figsize=(10, 8))
    y_vals = [lvl['E'] for lvl in levels]
    occ = [lvl.get('occupied', 0) for lvl in levels]
    labels = [f"l={lvl['l']} j={lvl['j']:.1f}" for lvl in levels]
    
    for i, (y, o) in enumerate(zip(y_vals, occ)):
        color = 'gray'
        if o == 2:
            color = 'blue'
        elif o == 1:
            color = 'orange'
        plt.hlines(y, 0, 1, colors=color, linewidth=2)
        plt.text(1.05, y, labels[i], verticalalignment='center')
        if o > 0:
            plt.scatter([0.5]*o, [y]*o, color=color, s=40, zorder=5)
    
    plt.xlabel("")
    plt.xticks([])
    plt.ylabel("Energy (MeV)")
    plt.title(title)
    plt.grid(True, axis='y')
    plt.xlim(-0.1, 1.5)
    plt.show()

# --- Main Program ---

# Example: Ca-40 (Z=20 protons, N=20 neutrons)
Z = 20
N_n = 20

print("Computing neutron levels...")
levels_n = compute_levels_neutrons()

print("Computing proton levels (with Coulomb)...")
levels_p = compute_levels_protons(Z)

print("\nNeutron magic numbers:")
find_magic_numbers(levels_n)

print("\nProton magic numbers:")
find_magic_numbers(levels_p)

# Fill levels
levels_n = fill_levels(levels_n, N_n)
levels_p = fill_levels(levels_p, Z)

# Plot
plot_levels(levels_n, title="Neutron Single Particle Levels (Ca-40)")
plot_levels(levels_p, title="Proton Single Particle Levels (Ca-40)")