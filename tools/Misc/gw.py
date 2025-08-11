import numpy as np

# Parameters
num_investors = 1000
num_steps = 5000
group_size = 20  # group size, renamed for clarity

pairs_per_group = group_size // 2  # number of pairs in each group
num_groups = num_investors // group_size
num_pairs = num_groups * pairs_per_group

# Initial moves: alternating +1 and -1 deterministically
moves = np.array([1 if i % 2 == 0 else -1 for i in range(num_investors)])

# Track pair inversion states: one bool per pair
pair_inverted = np.zeros(num_pairs, dtype=bool)

# Shift offset for group start index
group_offset = 0

# Store market totals over time
market_totals = []

for step in range(num_steps):
    new_moves = moves.copy()

    pairs = []
    # Build pairs inside each group of size group_size with offset
    for group_start in range(0, num_investors, group_size):
        group_indices = [(group_start + group_offset + i) % num_investors for i in range(group_size)]
        # create pairs inside group by stepping 2
        for pair_index in range(pairs_per_group):
            idx1 = group_indices[2 * pair_index]
            idx2 = group_indices[2 * pair_index + 1]
            pairs.append((idx1, idx2))

    new_pair_inverted = np.zeros_like(pair_inverted)

    for p_idx, (i1, i2) in enumerate(pairs):
        # Odd investor copies previous investor's move
        if i1 % 2 == 1:
            new_moves[i1] = moves[(i1 - 1) % num_investors]
        else:
            new_moves[i1] = -moves[(i1 - 1) % num_investors]

        # Even investor opposes previous investor's move
        if i2 % 2 == 0:
            new_moves[i2] = -moves[(i2 - 1) % num_investors]
        else:
            new_moves[i2] = moves[(i2 - 1) % num_investors]

        # If previous pair was inverted last step, invert this pair
        prev_p_idx = p_idx - 1 if p_idx > 0 else num_pairs - 1
        if pair_inverted[prev_p_idx]:
            new_moves[i1] *= -1
            new_moves[i2] *= -1
            new_pair_inverted[p_idx] = True

    moves = new_moves
    pair_inverted = new_pair_inverted

    # Invert all moves every 3rd step (steps 3, 6, 9, ...)
    invert_step_interval = 3
    if (step + 1) % invert_step_interval == 0:
        moves *= -1

    mt = moves.sum()
    market_totals.append(mt)

    group_offset = (group_offset + 1) % num_investors

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

max_lag = 20  # max lag to compute autocorrelation for
max_lag = min(max_lag, len(market_totals) - 1)
autocorr_vals = [autocorrelation(market_totals, lag) for lag in range(max_lag + 1)]

print("Lag\tAutocorrelation")
for lag, val in enumerate(autocorr_vals):
    print(f"{lag}\t{val:.4f}")

overall_autocorr = np.mean(autocorr_vals[1:])
print(f"\nOverall autocorrelation (average over lags 1 to {max_lag}): {overall_autocorr:.4f}")