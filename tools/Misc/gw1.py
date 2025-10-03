#!/usr/bin/env python3
import math

# --- Parameters (these are yours) ---
bh = 1             # base hill height (m)
DOF = 6            # degrees of freedom
POWW = 6 + 3       # power for number of hills scaling
meex = 14          # log10 of global domain length
mepow = 10 ** meex # global domain length in m
per = 2 ** POWW    # first tier multiplier
l1 = per * bh      # first tier hill "mass" parameter
mul = 2            # tier multiplier

# --- Your original functions with names/comments ---
def co(mul, mer, l1, per):
    """Compute hill 'mass' scaling per tier."""
    l2 = ((2 * mul) ** DOF)       # your DOF scaling
    lh = l1 * l2
    return lh ** (1/3)            # cube root to go from mass to height

def numt(init, tier, gl, poww):
    """Compute number of hills in domain for this tier."""
    ml = 10 ** gl                 # total domain length
    init = (((2 * tier) ** poww) * init)
    return (ml / init)

def dot(mer, l1, init, tier, gl, poww, per):
    """Return (hill_height, number_of_hills) for a tier."""
    return co(tier, mer, l1, per), numt(init, tier, gl, poww)

def dott(mer, l1, init, gl, poww, per):
    """Loop over tiers and print results."""
    for i in range(1, 20):
        h, n = dot(mer, l1, init, i, gl, poww, per)
        print(f"Tier {i}: Hill height = {h:.2f} m, count = {n:.2e}")

# --- Output ---
print("Largest hill in first tier", l1)
print("Number of base hills globally", mepow / bh)
mer = mepow / bh
dott(mer, l1, bh, meex, POWW, per)