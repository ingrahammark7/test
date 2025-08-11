import numpy as np

# Parameters
num_investors = 1000
num_steps = 5000
pair_size = 20

# Initial moves: alternating +1 and -1 deterministically
moves = np.array([1 if i % 2 == 0 else -1 for i in range(num_investors)])

# Track pair inversion states
pair_inverted = np.zeros(num_investors // pair_size, dtype=bool)

# Shift offset for pair groupings
pair_offset = 0

# Store market totals over time
market_totals = []

for t in range(num_steps):
    new_moves = moves.copy()

    # Get current pair groupings with offset
    pairs = [
        ((i + pair_offset) % num_investors,
         (i + 1 + pair_offset) % num_investors)
        for i in range(0, num_investors, pair_size)
    ]

    new_pair_inverted = np.zeros_like(pair_inverted)

    for p_idx, (i1, i2) in enumerate(pairs):
        if i1 % 2 == 1:
            new_moves[i1] = moves[(i1 - 1) % num_investors]
        else:
            new_moves[i1] = -moves[(i1 - 1) % num_investors]

        if i2 % 2 == 0:
            new_moves[i2] = -moves[(i2 - 1) % num_investors]
        else:
            new_moves[i2] = moves[(i2 - 1) % num_investors]

        prev_inverted = pair_inverted[p_idx - 1] if p_idx > 0 else pair_inverted[-1]
        if prev_inverted:
            new_moves[i1] *= -1
            new_moves[i2] *= -1
            new_pair_inverted[p_idx] = True

    moves = new_moves
    pair_inverted = new_pair_inverted

    # Invert all moves every 3rd step (step 3, 6, 9, ...)
    if (t + 1) % 3 == 0:
        moves *= -1

    mt = moves.sum()
    market_totals.append(mt)

    pair_offset = (pair_offset + 1) % num_investors

market_totals = np.array(market_totals)

def autocorrelation(x, lag):
    n = len(x)
    if lag == 0:
        return 1.0
    x_mean = np.mean(x)
    numerator = np.sum((x[:n - lag] - x_mean) * (x[lag:] - x_mean))
    denominator = np.sum((x - x_mean) ** 2)
    if denominator == 0:
        return 0
    return numerator / denominator

max_lag = min(20, len(market_totals) - 1)
autocorr_vals = [autocorrelation(market_totals, lag) for lag in range(max_lag + 1)]

# Print autocorrelation values for each lag
print("Lag\tAutocorrelation")
for lag, val in enumerate(autocorr_vals):
    print(f"{lag}\t{val:.4f}")

# Compute overall autocorrelation: average of all non-zero lags
overall_autocorr = np.mean(autocorr_vals[1:])
print(f"\nOverall autocorrelation (average over lags 1 to {max_lag}): {overall_autocorr:.4f}")