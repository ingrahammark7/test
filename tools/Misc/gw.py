import time
import numpy as np

def autocorr(series, lag):
    n = len(series)
    mean = np.mean(series)
    c0 = np.sum((series - mean)**2) / n
    return np.sum((series[:n-lag] - mean) * (series[lag:] - mean)) / ((n - lag) * c0)

def ar1_analysis(data, label="Data"):
    x = np.array(data).flatten()
    x_lag = x[:-1]
    y = x[1:]

    beta = np.sum(x_lag * y) / np.sum(x_lag * x_lag)
    y_pred = beta * x_lag
    residuals = y - y_pred

    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot

    print(f"\n{label} AR(1) Analysis:")
    print(f"  Fitted AR(1) coefficient: {beta:.6f}")
    print(f"  AR(1) model R²: {r2:.4f}")
    print(f"  Residuals mean: {np.mean(residuals):.8e}")
    print(f"  Residuals std:  {np.std(residuals):.8e}")

    print("  Residual autocorrelation (lags 1 to 10):")
    for lag in range(1, 11):
        acf_val = autocorr(residuals, lag)
        print(f"    lag {lag}: {acf_val:.6f}")

    last_val = x[-1]
    next_pred = beta * last_val
    print(f"  Predicted next value: {next_pred:.8e}")
    print(f"  Last observed value:  {last_val:.8e}")

# 1. Collect timing jitter RNG data
N = 300
timing_randoms = []
for _ in range(N):
    start = time.perf_counter()
    for _ in range(1000): pass
    delay = time.perf_counter() - start
    timing_randoms.append(delay % 1e-6)

# 2. Generate Middle Square RNG data
def middle_square_rng(seed, n):
    results = []
    x = seed
    for _ in range(n):
        x = (x * x) % 10**8  # 8-digit number
        mid = (x // 10**2) % 10**4  # middle 4 digits
        results.append(mid / 10**4)  # normalize to [0,1)
    return results

ms_seed = 67524891
middle_square_randoms = middle_square_rng(ms_seed, N)

# 3. Run AR(1) analysis on both RNGs
ar1_analysis(timing_randoms, "Timing Jitter RNG")
ar1_analysis(middle_square_randoms, "Middle Square RNG")

# 4. Correlate RNG sequences
timing_array = np.array(timing_randoms)
ms_array = np.array(middle_square_randoms)

min_len = min(len(timing_array), len(ms_array))
timing_array = timing_array[:min_len]
ms_array = ms_array[:min_len]

corr = np.corrcoef(timing_array, ms_array)[0,1]
print(f"\nPearson correlation coefficient between Timing Jitter RNG and Middle Square RNG: {corr:.6f}")