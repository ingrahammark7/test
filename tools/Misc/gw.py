import numpy as np

# constants
R = 8.314
M_NO = 30.01        # g/mol
M_HNO3 = 63.01      # g/mol

# reaction energy estimate (approx energy needed per mole NO formed)
ENERGY_PER_MOL_NO = 180e3   # J/mol (rough plasma estimate)

def nitric_production(power_watts, efficiency=0.01):
    """
    Estimate NO and HNO3 production from electrical power.

    power_watts : electrical input power
    efficiency  : fraction converted into NO formation
    """

    useful_power = power_watts * efficiency

    mol_NO_per_sec = useful_power / ENERGY_PER_MOL_NO

    g_NO_per_sec = mol_NO_per_sec * M_NO

    # stoichiometry: ~1 mol NO -> ~1 mol HNO3 eventually
    mol_HNO3_per_sec = mol_NO_per_sec
    g_HNO3_per_sec = mol_HNO3_per_sec * M_HNO3

    return g_NO_per_sec, g_HNO3_per_sec


# test across power levels
powers = [10, 50, 100, 500, 1000]  # watts

for p in powers:
    no_rate, acid_rate = nitric_production(p)
    print(f"{p} W:")
    print(f"  NO production   ≈ {no_rate*3600:.3f} g/hour")
    print(f"  HNO3 potential  ≈ {acid_rate*3600:.3f} g/hour\n")