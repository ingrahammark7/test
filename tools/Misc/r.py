import math
from scipy.integrate import quad

# Constants
en = 1e50              # total input energy (joules)
ev = 1e-19             # 1 eV in joules
hvlamec = 0.5e6        # reference photon energy (eV)
hvla = 1.0             # HVL base (cm)
depth = 1e5            # depth in cm
ml_min = 1e6           # 1 MeV

log2 = math.log(2)

# Determine ml_max from expected photon count = 1
ml_max = (en**2 * ev * hvlamec)**(1/3)
log_min = math.log10(ml_min)
log_max = math.log10(ml_max)

# HVL and attenuation model
def hvl(ml):
    return hvla if ml < hvlamec else hvla * math.sqrt(ml / hvlamec)

# Energy integrand (attenuation × ev / ml)
def energy_integrand(ml):
    if ml <= 0:
        return 0
    attenuation = math.exp(-depth / hvl(ml) * log2)
    return ev * attenuation / ml

# Photon count integrand (∝ 1/ml / sqrt(ml))
def count_integrand(ml):
    if ml <= 0:
        return 0
    return 1 / (ml * math.sqrt(ml / hvlamec))

# Normalization
log_norm = math.log(ml_max / ml_min)
E_total, _ = quad(energy_integrand, ml_min, ml_max, limit=1000)
delivered_energy = en * E_total / log_norm
C_total, _ = quad(count_integrand, ml_min, ml_max, limit=1000)

# Header
print(f"Total delivered energy: {delivered_energy:.5e} J")
print(f"Fraction of input energy: {delivered_energy / en:.5e}\n")

print(f"{'Threshold (eV)':>18} | {'Energy >%':>9} | {'Energy <%':>9} | {'Count >%':>9}")
print("-" * 60)

# Table: 10 log bins
for i in range(10):
    log_threshold = log_min + (log_max - log_min) * i / 10
    threshold = 10**log_threshold

    E_above, _ = quad(energy_integrand, threshold, ml_max, limit=1000)
    C_above, _ = quad(count_integrand, threshold, ml_max, limit=1000)

    frac_energy_above = E_above / E_total if E_total != 0 else 0
    frac_energy_below = 1 - frac_energy_above
    frac_count_above = C_above / C_total if C_total != 0 else 0

    print(f"{threshold:18.3e} |"
          f" {frac_energy_above*100:8.3f}% |"
          f" {frac_energy_below*100:8.3f}% |"
          f" {frac_count_above*100:8.3f}%")