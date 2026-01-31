# Parameters
hh = 0.0127         # object thickness in meters
hl = 511e3          # reference energy in eV
step = 10000        # scaling step
ro = 2.5e-12        # scaling constant for HVL

# Search loop
for i in range(1000):
    fl = step * i * i + 1
    re = hl / fl      # energy in eV
    ra = ro * fl      # scaled HVL
    h1 = hh / fl
    if h1 < ra:
        print("Crossover energy (eV):", re)
        break