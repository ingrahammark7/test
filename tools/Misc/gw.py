# Simulate the user's original discrete model faithfully and compute energy vs velocity

hs = 5
m = 1
d = 100000

mf = hs * hs * m * 0.5  # constant per step energy addition

def doer(v):
    x = 0
    en = 0.5 * v * v * m
    steps = 0
    
    # discrete stepping until reaching distance
    while x < d and steps < 10_000_000:
        x += v
        en += mf
        steps += 1
    
    return en, steps

results = []

for v in range(1, 201):
    en, steps = doer(v)
    results.append((v, en, steps))

# find minimum energy
best = min(results, key=lambda x: x[1])

print(best, results[:10])