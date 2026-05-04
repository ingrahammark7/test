import math

# ----------------------------
# energy per operation (J/op)
# ----------------------------

# CMOS (modern digital logic)
E_cmos = 1e-12

# RF system in mm-robust, low-precision regime
E_rf_mm = 1e-9

# ----------------------------
# optional: power-normalized compute (same result ratio)
# ----------------------------

# assume same power budget for comparison
P = 1.0  # arbitrary normalization

ops_cmos = P / E_cmos
ops_rf = P / E_rf_mm

# ----------------------------
# ratios
# ----------------------------
ratio_energy = E_rf_mm / E_cmos
ratio_compute = ops_rf / ops_cmos

# ----------------------------
# output
# ----------------------------
print("\n--- MM-ROBUST RF vs CMOS COMPUTE ---\n")

print("CMOS energy per op (J):", E_cmos)
print("RF mm-robust energy per op (J):", E_rf_mm)

print("\nCMOS ops per watt:", ops_cmos)
print("RF ops per watt:", ops_rf)

print("\nRF / CMOS energy per op ratio:", ratio_energy)
print("RF / CMOS compute efficiency ratio:", ratio_compute)