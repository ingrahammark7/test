import os
import json
import numpy as np
from scipy.stats import pearsonr, spearmanr, weibull_min
from sklearn.metrics import r2_score, mutual_info_score
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
import valf3  # assumed present
from valf1 import (
    nation_age_ratios, nation_age_conflicts,
    year_nation_kills, year_nation_weighted_age,
    print_summary, conflict_year_map
)

def get_avg_age_by_side(year, side_nations):
    kills = sum(year_nation_kills[year].get(n, 0) for n in side_nations)
    weighted_age = sum(year_nation_weighted_age[year].get(n, 0) for n in side_nations)
    return (weighted_age / kills) if kills > 0 else 0

# Load year filter from temp.txt
def load_year_filter():
    try:
        with open('temp.txt', 'r') as f:
            lines = f.readlines()
        return set(int(line.strip()) for line in lines if line.strip().isdigit())
    except Exception as e:
        print(f"Could not load year filter from temp.txt: {e}")
        return None

# Weibull function definition
def weibull_func(x, a, b, c):
    # a = scale, b = shape, c = amplitude
    return c * (b / a) * (x / a)**(b - 1) * np.exp(-(x / a)**b)

# Weibull fit and correlation (for diagnostics, optional)
def weibull_fit_and_correlation(age_vals, avg_ratios):
    age_vals = np.array(age_vals)
    avg_ratios = np.array(avg_ratios)

    if len(age_vals) < 3:
        print("Not enough data points for Weibull fit.")
        return None

    try:
        popt, _ = curve_fit(weibull_func, age_vals, avg_ratios, p0=[np.mean(age_vals), 2, max(avg_ratios)])
        a, b, c = popt
        predicted_vals = weibull_func(age_vals, a, b, c)

        r2 = r2_score(avg_ratios, predicted_vals)
        r, p = pearsonr(avg_ratios, predicted_vals)

        print(f"Weibull fit parameters: scale={a:.4f}, shape={b:.4f}, amplitude={c:.4f}")
        print(f"Pearson r: {r:.4f}, p-value: {p:.4f}")
        print(f"R² score: {r2:.4f}")

        return predicted_vals, (r, p, r2)
    except Exception as e:
        print(f"Weibull curve fit failed: {e}")
        return None

def build_combined_regression_model():
    age_vals = []
    avg_ratios = []

    for nation, age_data in nation_age_ratios.items():
        for age, ratios in age_data.items():
            relevant_conflicts = nation_age_conflicts[nation].get(age, [])
            conflict_years = {conflict_year_map.get(conf, -1) for conf in relevant_conflicts}
            if not conflict_years.intersection(current_difficulty_years):
                continue
            if not ratios:
                continue
            avg = sum(ratios) / len(ratios)
            age_vals.append(age)
            avg_ratios.append(avg)

    if len(age_vals) < 3:
        print("Not enough data points for combined model.")
        return None

    age_vals = np.array(age_vals)
    avg_ratios = np.array(avg_ratios)

    # Fit Weibull
    try:
        popt, _ = curve_fit(weibull_func, age_vals, avg_ratios,
                            p0=[np.mean(age_vals), 2, max(avg_ratios)])
        a, b, c = popt
        weibull_pred = weibull_func(age_vals, a, b, c)
    except Exception as e:
        print(f"Weibull fit failed: {e}")
        return None

    residuals = avg_ratios - weibull_pred

    # Residual models
    quad_model = np.poly1d(np.polyfit(age_vals, residuals, deg=2))
    quad_pred = quad_model(age_vals)

    try:
        def cubic_func(x, a, b, c, d):
            return a*x**3 + b*x**2 + c*x + d
        cubic_params, _ = curve_fit(cubic_func, age_vals, residuals)
        cubic_pred = cubic_func(age_vals, *cubic_params)
    except Exception:
        cubic_pred = None

    try:
        window = 3
        padded = np.pad(residuals, (window//2, window//2), mode='edge')
        kernel_pred = np.convolve(padded, np.ones(window)/window, mode='valid')
        # Ensure kernel_pred has the same length
        if len(kernel_pred) != len(residuals):
            kernel_pred = kernel_pred[:len(residuals)]
    except Exception:
        kernel_pred = None

    # Assemble features
    features = [quad_pred]
    if cubic_pred is not None:
        features.append(cubic_pred)
    if kernel_pred is not None and len(kernel_pred) == len(residuals):
        features.append(kernel_pred)

    try:
        X = np.column_stack(features)
        y = residuals
        model = LinearRegression()
        model.fit(X, y)
    except Exception as e:
        print(f"Regression fitting failed: {e}")
        return None

    # Final prediction function
    def combined_predict(age_input):
        age_input = np.array(age_input)

        if age_input.ndim == 0:
            age_input = age_input.reshape(1)
        elif age_input.ndim > 1:
            age_input = age_input.ravel()

        w = weibull_func(age_input, a, b, c)
        quad_feat = quad_model(age_input)

        feat_stack = [quad_feat]

        if cubic_pred is not None:
            feat_stack.append(cubic_func(age_input, *cubic_params))

        if kernel_pred is not None:
            smoothed_input = np.pad(quad_feat, (window//2, window//2), mode='edge')
            smoothed = np.convolve(smoothed_input, np.ones(window)/window, mode='valid')
            smoothed = smoothed[:len(age_input)]
            feat_stack.append(smoothed)

        try:
            X_input = np.column_stack(feat_stack)
            r = model.predict(X_input)
        except Exception as e:
            print(f"Prediction error: {e}")
            r = np.zeros_like(w)

        return w + r

    return combined_predict

# --- New function to write difficulty factors to temp1.txt ---
def write_difficulty_to_temp1():
    if(os.path.exists('temp1.txt')):
    	os.remove('temp1.txt')
    try:
        with open('temp1.txt', 'w') as f:
            for year, sides in difficulty_by_year.items():
                for side, diff_val in sides.items():
                    f.write(f"{year},{side},{diff_val}\n")
    except Exception as e:
        print(f"Failed to write difficulty to temp1.txt: {e}")

# Ensure JSON files exist with defaults
def ensure_json_file(filename, default_data):
    if not os.path.exists(filename):
        print(f"File '{filename}' not found. Creating with default content.")
        try:
            with open(filename, 'w') as f:
                json.dump(default_data, f, indent=2)
        except Exception as e:
            print(f"ERROR: Could not create '{filename}': {e}")
            exit(1)
    else:
        print(f"File '{filename}' exists.")

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR: JSON decode error in '{filename}', resetting to empty dict.")
        with open(filename, 'w') as f:
            json.dump({}, f)
        return {}
    except Exception as e:
        print(f"ERROR: Unexpected error loading '{filename}': {e}")
        exit(1)

# Files and defaults
files_and_defaults = {
    'F1.json': {},
    'F2.json': {},
    'F3.json': {},
    'opponent_mix_weights.json': {}
}

for filename, default in files_and_defaults.items():
    ensure_json_file(filename, default)

fighter_stats = load_json('F1.json')
aircraft_metadata = load_json('F2.json')
conflict_years = load_json('F3.json')
opponent_mix_weights = load_json('opponent_mix_weights.json')

def get_conflict_start_year(conflict_name):
    entry = conflict_years.get(conflict_name)
    if entry and 'start' in entry:
        return entry['start']
    return None

def get_aircraft_side(aircraft):
    meta = aircraft_metadata.get(aircraft, {})
    nation = meta.get('nation', 'Unknown')
    if nation == 'USA':
        return 'USA'
    elif nation in ('USSR', 'France'):
        return 'USSR+France'
    else:
        return 'Other'

difficulty_by_year = {}

def compute_difficulty_factor(filter_years=None):
    global difficulty_by_year
    print("Difficulty factors by year and side (model-based expected kill ratio):")

    model = build_combined_regression_model()
    if model is None:
        print("Failed to build combined regression model.")
        return

    side_groups = {
        'USA': ['USA'],
        'USSR+France': ['USSR', 'France']
    }

    years = sorted(year_nation_kills.keys())
    if filter_years is not None:
        years = [y for y in years if y in filter_years]

    difficulty_by_year = {}

    for year in years:
        total_kills = sum(year_nation_kills[year].values())
        if total_kills == 0:
            continue

        side_features = {}
        for side, nations in side_groups.items():
            avg_age = get_avg_age_by_side(year, nations)
            side_features[side] = avg_age

        if any(side_features[s] == 0 for s in side_groups):
            continue

        # Compute age difference
        age_diff = side_features['USSR+France'] - side_features['USA']

        side_outputs = {}
        for side in side_groups:
            input_features = np.array([[side_features[side], age_diff]])
            expected_ratio = model(input_features)[0]
            side_outputs[side] = expected_ratio

        difficulty_by_year[year] = side_outputs

        print(f"Year {year}:")
        for side in side_groups:
            print(f"  {side} Difficulty Factor (Model-Expected Kill Ratio): {side_outputs[side]:.2f}")
    print()

    # Write difficulty factors for valf3 to read
    write_difficulty_to_temp1()

# Manual Gaussian kernel smoother (optional)
def gaussian_kernel_smooth(x, y, bandwidth=1.0):
    smoothed_y = []
    n = len(x)
    for i in range(n):
        weights = []
        weighted_vals = []
        for j in range(n):
            dist = x[i] - x[j]
            w = np.exp(-(dist**2) / (2 * bandwidth**2))
            weights.append(w)
            weighted_vals.append(w * y[j])
        smoothed_y.append(sum(weighted_vals) / sum(weights))
    return np.array(smoothed_y)

def print_table(filter_ages=None):
    for nation, age_data in nation_age_ratios.items():
        print(f"Nation: {nation} Age-to-Average Kill Ratio Buckets:")
        ages = sorted(age_data.keys())
        avg_ratios = []
        age_vals = []
        for age in ages:
            conflicts = nation_age_conflicts[nation].get(age, [])
            conflict_years = {conflict_year_map.get(conf, -1) for conf in conflicts}
            if not conflict_years.intersection(current_difficulty_years):
                continue
            if filter_ages is not None and age not in filter_ages:
                continue
            ratios = age_data[age]
            avg_ratio = sum(ratios) / len(ratios)
            age_vals.append(age)
            avg_ratios.append(avg_ratio)
            conflicts_sample = ', '.join(sorted(nation_age_conflicts[nation][age]))
            print(f"  Age {age}: Avg Ratio {avg_ratio:.2f} (Conflicts: {conflicts_sample})")

        if len(age_vals) > 1:
            print("\nCorrelations and Curve Fits:")
            r, p = pearsonr(age_vals, avg_ratios)
            print(f"  Pearson r: {r:.4f}, p= {p:.4f}")
            weibull_fit_and_correlation(np.array(ages), np.array(avg_ratios))
            rho, sp_p = spearmanr(age_vals, avg_ratios)
            print(f"  Spearman ρ: {rho:.4f}, p = {sp_p:.4f}")

            coeffs = np.polyfit(age_vals, avg_ratios, deg=2)
            poly_model = np.poly1d(coeffs)
            quad_pred = poly_model(np.array(age_vals))
            r2_quad = r2_score(avg_ratios, quad_pred)
            print(f"  Quadratic fit R²: {r2_quad:.4f}")

            try:
                def nonlinear_model(x, a, b, c, d):
                    return a*x**3 + b*x**2 + c*x + d

                popt, _ = curve_fit(nonlinear_model, age_vals, avg_ratios)
                cubic_pred = nonlinear_model(np.array(age_vals), *popt)
                r2_cubic = r2_score(avg_ratios, cubic_pred)
                print(f"  Nonlinear cubic fit R²: {r2_cubic:.4f}")
            except Exception as e:
                cubic_pred = None
                r2_cubic = float('-inf')
                print(f"  Nonlinear cubic fit failed: {e}")

            try:
                window = 3
                padded = np.pad(avg_ratios, (window//2, window//2), mode='edge')
                kernel_pred = np.convolve(padded, np.ones(window)/window, mode='valid')
                r2_kernel = r2_score(avg_ratios, kernel_pred)
                print("  Kernel smoothing: Computed successfully.")
                print(f"  Kernel smoothing R²: {r2_kernel:.4f}")
            except Exception as e:
                kernel_pred = None
                r2_kernel = float('-inf')
                print(f"  Kernel smoothing failed: {e}")

            try:
                mi = mutual_info_score(np.digitize(age_vals, bins=10), np.digitize(avg_ratios, bins=10))
                print(f"  Mutual Information Score: {mi:.4f}")
            except Exception as e:
                print(f"  Mutual Information failed: {e}")

            try:
                shape, loc, scale = weibull_min.fit(avg_ratios, floc=0)
                print(f"  Weibull shape: {shape:.4f}, scale: {scale:.4f}")
            except Exception as e:
                print(f"  Weibull fit failed: {e}")

            try:
                features_raw = []
                if quad_pred is not None:
                    features_raw.append(quad_pred)
                if cubic_pred is not None:
                    features_raw.append(cubic_pred)
                if kernel_pred is not None:
                    features_raw.append(kernel_pred)

                if len(features_raw) < 2:
                    print("  Not enough regression models for combined multivariate regression.")
                else:
                    # Model WITHOUT Weibull (direct)
                    X_raw = np.column_stack(features_raw)
                    y_raw = np.array(avg_ratios)

                    direct_model = LinearRegression()
                    direct_model.fit(X_raw, y_raw)
                    y_direct_pred = direct_model.predict(X_raw)
                    direct_r2 = r2_score(y_raw, y_direct_pred)
                    print(f"  Combined Regression R² (No Weibull): {direct_r2:.4f}")

                    # Model WITH Weibull (residual modeling)
                    combined_model = build_combined_regression_model()
                    if combined_model:
                        combined_pred = combined_model(np.array(age_vals))
                        combined_r2 = r2_score(avg_ratios, combined_pred)
                        print(f"  Combined Regression R² (Weibull + Residual): {combined_r2:.4f}")
                    else:
                        print("  Combined model (Weibull + residuals) failed.")
            except Exception as e:
                print(f"  Combined regression evaluation failed: {e}")
        else:
            print("Not enough data for correlation.")
        print()

def print_aircraft_residual_kill_tables(filter_years=None):
    print("\nResidual Kill Ratio Tables by Aircraft (kills normalized by difficulty factor):\n")
    for aircraft, conflicts in fighter_stats.items():
        kills_by_year = {}
        for conflict_name, stats in conflicts.items():
            start_year = get_conflict_start_year(conflict_name)
            if start_year is None:
                continue
            if filter_years is not None and start_year not in filter_years:
                continue
            kills = stats.get('Kills', 0)
            kills_by_year[start_year] = kills_by_year.get(start_year, 0) + kills

        if not kills_by_year:
            continue

        side = get_aircraft_side(aircraft)

        print(f"Aircraft: {aircraft}")
        print(f"{'Year':<6} {'Kills':<6} {'Difficulty':<10} {'Residual':<10} Opponent Mix")
        print("-" * 80)

        for year in sorted(kills_by_year.keys()):
            kills = kills_by_year[year]
            difficulty = difficulty_by_year.get(year, {}).get(side, None)
            if difficulty is None or difficulty == 0:
                difficulty = 1

            residual = kills / difficulty

            opp_mix = opponent_mix_weights.get(str(year), {})
            opp_mix_str = ", ".join(f"{ac}: {w*100:.0f}%" for ac, w in opp_mix.items()) if opp_mix else "N/A"

            print(f"{year:<6} {kills:<6} {difficulty:<10.2f} {residual:<10.2f} {opp_mix_str}")

        print()

def write_temp_file():
    if(os.path.exists('temp.txt')):
    	os.remove('temp.txt')
    try:
        with open('temp.txt', 'w') as f:
            for year in sorted(difficulty_by_year.keys()):
                f.write(f"{year}\n")
    except Exception as e:
        print(f"Failed to write temp.txt: {e}")

# --- Initial data state sets ---

all_ages = set(age for nation in nation_age_ratios for age in nation_age_ratios[nation])
current_ages = set(all_ages)

all_difficulty_years = set(year_nation_kills.keys())
loaded_years = load_year_filter()
if loaded_years is not None:
    current_difficulty_years = loaded_years
else:
    current_difficulty_years = set(all_difficulty_years)

# --- Initial output ---

print_summary()
print_table(filter_ages=current_ages)
compute_difficulty_factor(filter_years=current_difficulty_years)
print_aircraft_residual_kill_tables(filter_years=current_difficulty_years)
write_temp_file()

# --- Interactive command loop ---

while True:
    removed_ages = all_ages - current_ages
    removed_difficulty_years = all_difficulty_years - current_difficulty_years

    print("\nCurrently shown age buckets:", sorted(current_ages) or "(none)")
    print("Removed age buckets:", sorted(removed_ages) or "(none)")
    print("Currently shown difficulty years:", sorted(current_difficulty_years) or "(none)")
    print("Removed difficulty years:", sorted(removed_difficulty_years) or "(none)")

    valf3.print_residual_kill_tables()

    user_input = input(
        "\nEnter command:\n"
        "  'add <ages>' or 'remove <ages>' (e.g., 'add 4,7')\n"
        "  'adddif <years>' or 'removedif <years>'\n"
        "  Press Enter to quit: "
    ).strip().lower()

    if not user_input:
        print("Exiting.")
        break

    parts = user_input.split(maxsplit=1)
    if len(parts) != 2 or parts[0] not in ('add', 'remove', 'adddif', 'removedif'):
        print("Invalid command.")
        continue

    try:
        values = set(int(x.strip()) for x in parts[1].split(','))
    except ValueError:
        print("Invalid input: must be integers separated by commas.")
        continue

    if parts[0] == 'add':
        current_ages.update(values)
    elif parts[0] == 'remove':
        current_ages.difference_update(values)
    elif parts[0] == 'adddif':
        current_difficulty_years.update(values)
    elif parts[0] == 'removedif':
        current_difficulty_years.difference_update(values)

    # Refresh outputs and temp.txt
    print_summary()
    print_table(filter_ages=current_ages)
    compute_difficulty_factor(filter_years=current_difficulty_years)
    print_aircraft_residual_kill_tables(filter_years=current_difficulty_years)
    write_temp_file()