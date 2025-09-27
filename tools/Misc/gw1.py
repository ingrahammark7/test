import numpy as np
from mpmath import mp

# Set maximum precision (100 decimal digits)
mp.dps = 100

# ATP parameters
alpha_min = mp.mpf('5.16e-3')
alpha_max = mp.mpf('1.032e-2')

# Compute geometric/log midpoint at maximum precision
alpha_opt = mp.sqrt(alpha_min * alpha_max)

# Current CODATA alpha
alpha_0 = mp.mpf('7.2973525693e-3')

# Fractional difference
frac_diff = (alpha_opt - alpha_0) / alpha_0

print(alpha_opt, frac_diff)