import numpy as np

g = 10
m = 1
hs = 5

# example cost structure (replace with your real one if needed)
def C(v):
    kinetic = 0.5 * m * v**2
    gravity_term = hs * hs * m * 0.5  # your mf structure
    return kinetic + gravity_term

def energy(v, d):
    return d * (C(v) / v)

for i in range(1, 200):
    v = i
    print("v =", v, "E =", energy(v, 10000))