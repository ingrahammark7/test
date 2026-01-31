# Parameters
hh = 0.0127         # object thickness in meters
hl = 511e3          # reference energy in eV
ro = 2.5e-12        # scaling constant for HVL

# Direct calculation of crossover
# h1 / fl = ra -> hh / fl = ro * fl -> fl^2 = hh / ro -> fl = sqrt(hh / ro)
fl_crossover = (hh / ro) ** 0.5

# Energy at crossover
crossover_energy = hl / fl_crossover

print("Crossover energy (eV):", crossover_energy)