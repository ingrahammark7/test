import numpy as np
import pandas as pd

m = 1
hs = 5

# ----------------------------
# simulator (faithful)
# ----------------------------
def simulate(v, d, dt):
    x = 0.0
    t = 0.0

    mf = 0.5 * m * hs * hs
    en = 0.5 * m * v * v

    while x < d:
        x += v * dt
        en += mf * dt
        t += dt

        if t > 1e7:
            break

    return en


def v_star(d, dt, v_max=200, n_samples=200):
    best_v = None
    best_e = float("inf")

    for v in np.linspace(1, v_max, n_samples):
        e = simulate(v, d, dt)
        if e < best_e:
            best_e = e
            best_v = v

    return best_v


# ----------------------------
# sweep
# ----------------------------
ds = np.array([200, 500, 1000, 2000, 5000, 10000], dtype=float)
dts = [1.0, 0.5, 0.1, 0.05, 0.01]

results = {}

for dt in dts:
    vs = np.array([v_star(d, dt) for d in ds], dtype=float)

    # log-log fit: v = a d^alpha
    logd = np.log(ds)
    logv = np.log(vs)

    alpha, intercept = np.polyfit(logd, logv, 1)

    results[dt] = {
        "alpha": alpha,
        "vs": vs
    }


# ----------------------------
# readable output
# ----------------------------
print("\nLOG–LOG EXPONENTS (v* ~ d^alpha)\n")
for dt in dts:
    print(f"dt = {dt:>4}: alpha = {results[dt]['alpha']:.4f}")

print("\nRaw v* values:\n")

table = pd.DataFrame(
    {f"dt={dt}": results[dt]["vs"] for dt in dts},
    index=ds
)

print(table)