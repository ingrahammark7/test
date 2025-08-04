import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import bisect
import scipy.special

# Constants and parameters
hbarc = 197.327  # MeV·fm
m_nucleon = 938.92  # MeV/c^2
V0 = 50.0  # Woods–Saxon depth (MeV)
r0 = 1.25  # fm
a = 0.65  # diffuseness fm
A = 40  # Mass number (Ca-40)
R = r0 * A**(1/3)  # Nuclear radius fm
lam = 15.0  # Spin-orbit strength MeV·fm^2
r_min = 0.01  # fm, avoid singularity
r_max = 15.0  # fm
N = 2000  # radial points
r = np.linspace(r_min, r_max, N)
dr = r[1] - r[0]
e2 = 1.44  # MeV·fm Coulomb constant
k_B = 8.617333262e-11  # MeV/K Boltzmann constant, tiny but for demonstration

# Input nuclear composition and physics params
Z = 20  # protons Ca-40
N_n = 20  # neutrons Ca-40
pairing_gap = 1.2  # MeV typical pairing gap
temperature = 0.0  # MeV (T=0 cold)
beta2 = 0.25  # deformation parameter moderate
chi_quad = 1.0  # residual quadrupole strength
odd_neutron = False  # change to True for odd neutron number
odd_proton = False  # same for protons

# --- Helper functions ---
def y20(theta):
    return np.sqrt(5/(16*np.pi)) * (3*np.cos(theta)**2 - 1)

def deformed_radius(theta, beta2):
    return R * (1 + beta2 * y20(theta))

def deformed_potential(r, beta2):
    thetas = np.linspace(0, np.pi, 50)
    ws_vals = []
    for theta in thetas:
        R_theta = deformed_radius(theta, beta2)
        ws = -V0 / (1 + np.exp((r - R_theta)/a))
        ws_vals.append(ws)
    ws_vals = np.array(ws_vals)
    return np.mean(ws_vals, axis=0)

def dV_dr(r, V):
    delta = 1e-3
    return (np.interp(r+delta, r, V) - np.interp(r-delta, r, V)) / (2*delta)

def spin_orbit_strength(r):
    width = 0.5
    return lam * np.exp(-((r - R)/width)**2)

def l_dot_s(l, j):
    return 0.5 * (j*(j+1) - l*(l+1) - 0.75)

def coulomb_potential(r, Z):
    Rc = R
    Vc = np.zeros_like(r)
    inside = r < Rc
    outside = ~inside
    Vc[inside] = (e2 * Z / (2*Rc)) * (3 - (r[inside]/Rc)**2)
    Vc[outside] = e2 * Z / r[outside]
    return Vc

def quadrupole_perturbation(l, beta2, chi=chi_quad):
    return -chi * beta2 * (2*l + 1)

def normalize_wavefunction(u, r):
    norm = np.sqrt(np.trapz(u**2, r))
    return u / norm if norm > 0 else u

# --- Radial Hamiltonian ---
def radial_hamiltonian(l, j, proton=False, Z=0, beta2=0):
    Vws = deformed_potential(r, beta2)
    diag = np.zeros(N)
    offdiag = np.ones(N-1) * (-hbarc**2/(2*m_nucleon*dr**2))
    diag[:] = hbarc**2/(m_nucleon*dr**2)
    diag += hbarc**2 * l*(l+1) / (2 * m_nucleon * r**2)
    diag += Vws
    if proton:
        diag += coulomb_potential(r, Z)
    dV = dV_dr(r, Vws)
    with np.errstate(divide='ignore', invalid='ignore'):
        ls = l_dot_s(l, j)
        Vso = spin_orbit_strength(r) * (1/r) * dV * ls
        Vso[r == 0] = 0
    diag += Vso
    diag += quadrupole_perturbation(l, beta2)
    return diag, offdiag

# --- Solve radial SE ---
def solve_radial(l, j, proton=False, Z=0, beta2=0, n_levels=5):
    diag, offdiag = radial_hamiltonian(l, j, proton=proton, Z=Z, beta2=beta2)
    energies, vecs = eigh_tridiagonal(diag, offdiag)
    bound_idx = np.where(energies < 0)[0]
    bound_idx = bound_idx[:n_levels]
    return energies[bound_idx], vecs[:, bound_idx]

def compute_levels(proton=False, Z=0, max_l=4, beta2=0):
    levels = []
    for l in range(max_l+1):
        js = [l + 0.5]
        if l > 0:
            js.append(l - 0.5)
        for j in js:
            energies, vecs = solve_radial(l, j, proton=proton, Z=Z, beta2=beta2)
            for idx, e in enumerate(energies):
                levels.append({'E': e, 'l': l, 'j': j, 'wf': vecs[:, idx]})
    levels.sort(key=lambda x: x['E'])
    return levels

# --- Occupation with finite temp BCS and blocking ---
def occupation_bcs(energies, mu, delta, T, blocked_idx=None):
    # Apply blocking: blocked_idx single-particle orbital blocked (occupation=1)
    v2 = np.zeros_like(energies)
    for i, e in enumerate(energies):
        E_gap = np.sqrt((e - mu)**2 + delta**2)
        f = 1 / (1 + np.exp(E_gap / (k_B*T))) if T > 0 else 0
        # BCS occupation with temperature (if T=0 f=0)
        v2_i = 0.5 * (1 - (e - mu)/E_gap * np.tanh(E_gap/(2*T)) if T > 0 else 0.5*(1-(e-mu)/E_gap))
        if i == blocked_idx:
            v2[i] = 0.5  # blocked orbital half occupation
        else:
            v2[i] = v2_i
    v2 = np.clip(v2, 0, 1)
    return v2

def fill_levels_bcs(levels, N_nucleons, delta, T=0, odd=False):
    energies = np.array([lvl['E'] for lvl in levels])
    blocked_idx = None
    if odd:
        # Block orbital closest to Fermi level
        idx_closest = np.argmin(np.abs(energies - np.median(energies)))
        blocked_idx = idx_closest

    def occ_diff(mu):
        v2 = occupation_bcs(energies, mu, delta, T, blocked_idx)
        occ_total = v2.sum() * 2 - (0.5 if blocked_idx is not None else 0)
        return occ_total - N_nucleons

    # Bracket chemical potential search
    mu_min = min(energies) - 5*delta
    mu_max = max(energies) + 5*delta

    try:
        mu = bisect(occ_diff, mu_min, mu_max)
    except ValueError:
        # fallback to simple filling
        mu = None

    if mu is not None:
        v2 = occupation_bcs(energies, mu, delta, T, blocked_idx)
    else:
        # fallback: fill lowest orbitals fully
        v2 = np.zeros_like(energies)
        rem = N_nucleons
        for i in range(len(energies)):
            if rem >= 2:
                v2[i] = 1
                rem -= 2
            else:
                v2[i] = rem/2
                rem = 0
        if odd and blocked_idx is not None and blocked_idx < len(v2):
            v2[blocked_idx] = 0.5

    for lvl, occ in zip(levels, v2):
        lvl['occupied'] = occ * 2  # two nucleons max per level
    return levels, mu

# --- Magic number finder ---
def find_magic_numbers(levels, threshold=3.0):
    energies = np.array([lvl['E'] for lvl in levels])
    gaps = energies[1:] - energies[:-1]
    magic_idxs = np.where(gaps > threshold)[0]
    magic_numbers = [2*(i+1) for i in magic_idxs]
    print("Detected magic numbers and gap sizes (MeV):")
    for n, g in zip(magic_numbers, gaps[magic_idxs]):
        print(f"Magic number: {n}, gap: {g:.2f} MeV")
    return magic_numbers, gaps[magic_idxs]

# --- Calculate rms radius ---
def rms_radius(levels, r):
    r2 = r**2
    total_occ = 0
    total_r2 = 0
    for lvl in levels:
        u = normalize_wavefunction(lvl['wf'], r)
        occ = lvl.get('occupied', 0)
        if occ > 0:
            rho = u**2 / r2
            r_mean2 = np.trapz(r2 * rho, r) / np.trapz(rho, r)
            total_r2 += occ * r_mean2
            total_occ += occ
    return np.sqrt(total_r2 / total_occ) if total_occ > 0 else 0

# --- Binding energy estimate (sum single-particle energies times occupation) ---
def binding_energy(levels):
    return sum(lvl['E'] * lvl.get('occupied', 0) for lvl in levels)

# --- Plotting functions ---
def plot_levels(levels, title):
    plt.figure(figsize=(10, 8))
    energies = [lvl['E'] for lvl in levels]
    occ = [lvl.get('occupied', 0) for lvl in levels]
    labels = [f"l={lvl['l']} j={lvl['j']:.1f}" for lvl in levels]
    for i, (e, o) in enumerate(zip(energies, occ)):
        color = 'blue' if o > 1.9 else 'orange' if o > 0 else 'gray'
        plt.hlines(e, 0, 1, colors=color, linewidth=2)
        plt.text(1.05, e, labels[i], verticalalignment='center', fontsize=8)
        if o > 0:
            plt.scatter([0.5]*int(round(o)), [e]*int(round(o)), color=color, s=40, zorder=5)
    plt.title(title)
    plt.xlabel("")
    plt.xticks([])
    plt.ylabel("Energy (MeV)")
    plt.xlim(-0.1, 1.5)
    plt.grid(True, axis='y')
    plt.show()

def plot_wavefunction(level, r, title):
    u = normalize_wavefunction(level['wf'], r)
    plt.figure(figsize=(8, 5))
    plt.plot(r, u, label=f"l={level['l']} j={level['j']:.1f} E={level['E']:.2f} MeV")
    plt.title(title)
    plt.xlabel("r (fm)")
    plt.ylabel("Radial wf u(r)")
    plt.grid(True)
    plt.legend()
    plt.show()

# --- Main execution ---

print("Computing neutron levels...")
levels_n = compute_levels(proton=False, beta2=beta2)
print("Computing proton levels (with Coulomb)...")
levels_p = compute_levels(proton=True, Z=Z, beta2=beta2)

print("\nNeutron magic numbers:")
find_magic_numbers(levels_n)

print("\nProton magic numbers:")
find_magic_numbers(levels_p)

levels_n, mu_n = fill_levels_bcs(levels_n, N_n, pairing_gap, T=temperature, odd=odd_neutron)
levels_p, mu_p = fill_levels_bcs(levels_p, Z, pairing_gap, T=temperature, odd=odd_proton)

print(f"\nNeutron chemical potential (mu): {mu_n if mu_n is not None else 'Fallback filling'}")
print(f"Proton chemical potential (mu): {mu_p if mu_p is not None else 'Fallback filling'}")

plot_levels(levels_n, "Neutron Levels with BCS and Deformation")
plot_levels(levels_p, "Proton Levels with BCS, Coulomb, and Deformation")

print("\nPlotting radial wavefunctions near neutron Fermi level:")
for lvl in levels_n[-5:]:
    plot_wavefunction(lvl, r, "Neutron Radial Wavefunction Near Fermi Level")

print("\nPlotting radial wavefunctions near proton Fermi level:")
for lvl in levels_p[-5:]:
    plot_wavefunction(lvl, r, "Proton Radial Wavefunction Near Fermi Level")

rms_n = rms_radius(levels_n, r)
rms_p = rms_radius(levels_p, r)
skin = rms_n - rms_p

print(f"\nNeutron rms radius: {rms_n:.3f} fm")
print(f"Proton rms radius: {rms_p:.3f} fm")
print(f"Neutron skin thickness: {skin:.3f} fm")

bind_n = binding_energy(levels_n)
bind_p = binding_energy(levels_p)
total_bind = bind_n + bind_p

print(f"\nEstimated neutron mean-field binding energy: {bind_n:.2f} MeV")
print(f"Estimated proton mean-field binding energy: {bind_p:.2f} MeV")
print(f"Total approximate binding energy: {total_bind:.2f} MeV")