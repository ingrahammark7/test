import numpy as np

def run_model(num_investors, num_steps, group_size, start_offset, invert_interval):
    moves = np.array([1 if i % 2 == 0 else -1 for i in range(num_investors)])
    num_pairs_per_group = group_size // 2
    num_groups = num_investors // group_size
    total_pairs = num_groups * num_pairs_per_group
    pair_inverted = np.zeros(total_pairs, dtype=bool)
    group_offset = start_offset
    market_totals = []

    for t in range(num_steps):
        new_moves = moves.copy()

        pairs = []
        for group_start in range(0, num_investors, group_size):
            group_indices = [(group_start + group_offset + i) % num_investors for i in range(group_size)]
            for i in range(0, group_size, 2):
                pairs.append((group_indices[i], group_indices[i+1]))

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

        if (t + 1) % invert_interval == 0:
            moves *= -1

        market_totals.append(moves.sum())
        group_offset = (group_offset + 1) % num_investors

    return np.array(market_totals)

# Parameters
num_investors = 1000
num_steps = 5000
group_size = 20

# Layer configs: vary offsets and inversion intervals to reduce correlation
layer_configs = [
    {'start_offset': 0, 'invert_interval': 3},
    {'start_offset': 5, 'invert_interval': 4},
    {'start_offset': 10, 'invert_interval': 5},
    {'start_offset': 15, 'invert_interval': 6},
]

# Run layers and sum results
combined_totals = np.zeros(num_steps)
for config in layer_configs:
    totals = run_model(num_investors, num_steps, group_size, config['start_offset'], config['invert_interval'])
    combined_totals += totals

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

max_lag = 20
max_lag = min(max_lag, len(combined_totals) - 1)
autocorr_vals = [autocorrelation(combined_totals, lag) for lag in range(max_lag + 1)]

print("Lag\tAutocorrelation")
for lag, val in enumerate(autocorr_vals):
    print(f"{lag}\t{val:.4f}")

overall_autocorr = np.mean(autocorr_vals[1:])
print(f"\nOverall autocorrelation (average over lags 1 to {max_lag}): {overall_autocorr:.4f}")