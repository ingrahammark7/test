import math
eps0 = 8.8541878128e-12
mu0  = 4*math.pi*1e-7
e = 1.602176634e-19
me = 9.10938356e-31
kB = 1.380649e-23

# --- utility functions ---
def plasma_freq(ne):
    return math.sqrt(ne * e*e / (eps0 * me))

def debye_length(ne, Te):   # Te in K
    return math.sqrt(eps0 * kB * Te / (ne * e*e))

def skin_depth(sigma, omega):
    return math.sqrt(2.0 / (mu0 * sigma * max(omega, 1e-30)))

def temp_rise(E_dep_J, mass_kg, cp):
    if mass_kg <= 0 or cp <= 0:
        return 0.0
    return E_dep_J / (mass_kg * cp)

# crude spitzer conductivity (order of magnitude) - Te in eV:
def spitzer_sigma(Te_eV, Z=1, lnLambda=10):
    # Te_eV -> J
    Te = Te_eV * 1.602e-19
    # simplified prefactor (units check approximate)
    return ( (4*math.pi*eps0)**2 * (Te**1.5) ) / ( e*e * math.sqrt(me) * Z * lnLambda + 1e-30 )

# confinement factor heuristic:
def confinement_from_B(B, rho, v):
    pB = B*B / (2*mu0)
    pdyn = rho * v*v
    # if pB comparable to pdyn, strong pinch
    return max(0.0, pB / (pdyn + 1e-30))

# simple step update (very compact)
def flux_step(E_remain_J, area_m2, dx_m, material, proj, hvl_cm, omega, Te_guess=1.0):
    # material: must give rho, cp, ionization_energy_eV, atomic_mass_kg
    vol = area_m2 * dx_m
    mass = vol * material.rho
    # energy deposited in step (using HVL)
    hvl_m = hvl_cm / 100.0
    frac_deposited = 1 - 2**(-dx_m / hvl_m)   # small-step approx
    E_dep = E_remain_J * frac_deposited
    # temperature and ionization proxy
    dT = temp_rise(E_dep, mass, material.cp)
    Te = max(Te_guess + dT, 0.1)  # K
    # electron density proxy (assume solid -> n_free ~ Z * atom_density)
    atom_density = material.rho / material.atomic_mass_kg   # atoms per m3
    ne = atom_density * material.Z_free  # free electrons per atom
    # conductivity: if ionized use spitzer else metallic sigma
    if E_dep / (mass+1e-30) > material.ionization_energy_eV * 1.602e-19:
        sigma = spitzer_sigma(max(Te/11600.0, 1.0), Z=material.atomic_number)
    else:
        sigma = material.sigma_solid  # ~1e7 S/m

    delta = skin_depth(sigma, omega)
    # guess current & B (very heuristic)
    I = (E_dep / 1e3) * 1e3  # placeholder mapping energy -> current amplitude
    r = math.sqrt(area_m2/math.pi)
    B = mu0 * I / (2*math.pi*max(r,1e-12))
    conf = confinement_from_B(B, material.rho, proj.v)
    # apply confinement to hvl
    hvl_eff_cm = hvl_cm / max(1.0, 1.0 + conf*material.hvl_confinement_coeff)
    # return diagnostics and leftover energy
    E_remain_J -= E_dep
    return E_remain_J, hvl_eff_cm, {'E_dep':E_dep,'dT':dT,'sigma':sigma,'delta_m':delta,'B':B,'conf':conf}