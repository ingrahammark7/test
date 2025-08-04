import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import bisect

# Constants and parameters
hbarc = 197.327  # MeV·fm
m_nucleon = 938.92  # MeV/c^2
V0 = 50.0  # Woods–Saxon potential depth (MeV)
r0 = 1.25  # fm
a = 0.65  # diffuseness fm
A = 40  # Mass number
R = r0 * A**(1/3)  # Nuclear radius fm
lam = 15.0  # Spin-orbit strength MeV·fm^2
r_min = 0.01  # fm, avoid r=0 singularity
r_max = 15.0  # fm
N = 2000  # radial grid points
r = np.linspace(r_min, r_max, N)
dr = r[1] - r[0]
Z = 20  # Proton number for Ca-40
N_n = 20  # Neutron number for Ca-40
pairing_gap = 1.2  # MeV, pairing gap

def woods_saxon(r):
    return -V0 / (1 + np.exp((r - R) / a))

def dV_dr(r):
    delta = 1e-3
    return (woods_saxon(r + delta) - woods_saxon(r - delta)) / (2 * delta)

def l_dot_s(l, j):
    return 0.5 * (j*(j+1) - l*(l+1) - 0.75)

def radial_hamiltonian(l, j):
    diag = np.zeros(N)
    offdiag = np.ones(N-1) * (-hbarc**2/(2*m_nucleon*dr**2))
    diag[:] = hbarc**2/(m_nucleon*dr**2)
    diag += hbarc**2 * l*(l+1) / (2 * m_nucleon * r**2)
    Vws = woods_saxon(r)
    diag += Vws
    with np.errstate(divide='ignore', invalid='ignore'):
        ls = l_dot_s(l, j)
        Vso = lam * (1/r) * dV_dr(r) * ls
        Vso[r == 0] = 0
    diag += Vso
    return diag, offdiag

def coulomb_potential(r, Z):
    e2 = 1.44  # MeV·fm
    Rc = R
    Vc = np.zeros_like(r)
    inside = r < Rc
    outside = ~inside
    Vc[inside] = (e2 * Z / (2*Rc)) * (3 - (r[inside]/Rc)**2)
    Vc[outside] = e2 * Z / r[outside]
    return Vc

def radial_hamiltonian_proton(l, j, Z):
    diag, offdiag = radial_hamiltonian(l, j)
    Vc = coulomb_potential(r, Z)
    diag += Vc
    return diag, offdiag

def solve_radial(l, j, proton=False, Z=0, n_levels=5):
    if proton:
        diag, offdiag = radial_hamiltonian_proton(l, j, Z)
    else:
        diag, offdiag = radial_hamiltonian(l, j)
    energies, vecs = eigh_tridiagonal(diag, offdiag)
    bound_idx = np.where(energies < 0)[0]
    bound_idx = bound_idx[:n_levels]
    return energies[bound_idx], vecs[:, bound_idx]

def compute_levels(proton=False, Z=0, max_l=4):
    levels = []
    for l in range(max_l+1):
        js = [l + 0.5]
        if l > 0:
            js.append(l - 0.5)
        for j in js:
            energies, vecs = solve_radial(l, j, proton=proton, Z=Z)
            for idx, e in enumerate(energies):
                levels.append({'E': e, 'l': l, 'j': j, 'wf': vecs[:, idx]})
    levels.sort(key=lambda x: x['E'])
    return levels

def find_magic_numbers(levels, threshold=3.0):
    energies = np.array([lvl['E'] for lvl in levels])
    gaps = energies[1:] - energies[:-1]
    magic_idxs = np.where(gaps > threshold)[0]
    magic_numbers = [2*(i+1) for i in magic_idxs]
    print("Detected magic numbers and gap sizes (MeV):")
    for n, g in zip(magic_numbers, gaps[magic_idxs]):
        print(f"Magic number: {n}, gap: {g:.2f} MeV")
    return magic_numbers, gaps[magic_idxs]

def normalize_wavefunction(u, r):
    norm = np.sqrt(np.trapz(u**2, r))
    return u / norm

def fill_levels_simple(levels, N_nucleons):
    remaining = N_nucleons
    for lvl in levels:
        capacity = 2
        if remaining >= capacity:
            lvl['occupied'] = capacity
            remaining -= capacity
        else:
            lvl['occupied'] = remaining
            remaining = 0
    return levels

def fill_levels_bcs(levels, N_nucleons, delta):
    energies = np.array([lvl['E'] for lvl in levels])
    def occupation(mu):
        v2 = 0.5 * (1 - (energies - mu) / np.sqrt((energies - mu)**2 + delta**2))
        v2 = np.clip(v2, 0, 1)
        return v2.sum() - N_nucleons
    mu_min = min(energies) - 5*delta
    mu_max = max(energies) + 5*delta
    occ_min = occupation(mu_min)
    occ_max = occupation(mu_max)
    attempts = 0
    max_attempts = 20
    expand_factor = 2.0
    while occ_min * occ_max > 0 and attempts < max_attempts:
        mu_min -= expand_factor * delta
        mu_max += expand_factor * delta
        occ_min = occupation(mu_min)
        occ_max = occupation(mu_max)
        attempts += 1
    if occ_min * occ_max > 0:
        print("Warning: Could not find chemical potential with bisection; falling back to simple filling")
        levels = fill_levels_simple(levels, N_nucleons)
        mu = None
        return levels, mu
    mu = bisect(occupation, mu_min, mu_max)
    v2 = 0.5 * (1 - (energies - mu) / np.sqrt((energies - mu)**2 + delta**2))
    v2 = np.clip(v2, 0, 1)
    for lvl, occ in zip(levels, v2):
        lvl['occupied'] = occ * 2
    return levels, mu

def plot_levels(levels, title="Single Particle Levels"):
    plt.figure(figsize=(10, 8))
    y_vals = [lvl['E'] for lvl in levels]
    occ = [lvl.get('occupied', 0) for lvl in levels]
    labels = [f"l={lvl['l']} j={lvl['j']:.1f}" for lvl in levels]
    for i, (y, o) in enumerate(zip(y_vals, occ)):
        if o > 1.9:
            color = 'blue'
        elif o > 0.1:
            color = 'orange'
        else:
            color = 'gray'
        plt.hlines(y, 0, 1, colors=color, linewidth=2)
        plt.text(1.05, y, labels[i], verticalalignment='center')
        if o > 0:
            plt.scatter([0.5]*int(round(o)), [y]*int(round(o)), color=color, s=40, zorder=5)
    plt.xlabel("")
    plt.xticks([])
    plt.ylabel("Energy (MeV)")
    plt.title(title)
    plt.grid(True, axis='y')
    plt.xlim(-0.1, 1.5)
    plt.show()

def plot_wavefunction(level, r, title="Radial Wavefunction u(r)"):
    u = normalize_wavefunction(level['wf'], r)
    plt.figure(figsize=(8,5))
    plt.plot(r, u, label=f"l={level['l']} j={level['j']:.1f} E={level['E']:.2f} MeV")
    plt.xlabel("r (fm)")
    plt.ylabel("u(r)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

def estimate_binding_energy(levels):
    E_sp = sum(lvl['E'] * lvl.get('occupied', 0) for lvl in levels)
    return E_sp

# Main execution
print("Computing neutron levels...")
levels_n = compute_levels(proton=False)
print("Computing proton levels (with Coulomb)...")
levels_p = compute_levels(proton=True, Z=Z)

print("\nNeutron magic numbers:")
find_magic_numbers(levels_n)

print("\nProton magic numbers:")
find_magic_numbers(levels_p)

levels_n, mu_n = fill_levels_bcs(levels_n, N_n, pairing_gap)
levels_p, mu_p = fill_levels_bcs(levels_p, Z, pairing_gap)

print(f"\nNeutron chemical potential (mu): {mu_n if mu_n is not None else 'Fallback filling'}")
print(f"Proton chemical potential (mu): {mu_p if mu_p is not None else 'Fallback filling'}")

plot_levels(levels_n, title="Neutron Single Particle Levels with BCS Occupation (Ca-40)")
plot_levels(levels_p, title="Proton Single Particle Levels with BCS Occupation (Ca-40)")

print("\nPlotting radial wavefunctions near neutron Fermi level:")
for lvl in levels_n[-5:]:
    plot_wavefunction(lvl, r)

print("\nPlotting radial wavefunctions near proton Fermi level:")
for lvl in levels_p[-5:]:
    plot_wavefunction(lvl, r)

print(f"\nEstimated neutron mean field binding energy: {estimate_binding_energy(levels_n):.2f} MeV")
print(f"Estimated proton mean field binding energy: {estimate_binding_energy(levels_p):.2f} MeV")
print(f"Total approx binding energy (mean field): {estimate_binding_energy(levels_n) + estimate_binding_energy(levels_p):.2f} MeV")