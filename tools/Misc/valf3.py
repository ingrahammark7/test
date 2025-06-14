import json
from collections import defaultdict
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats import pearsonr

# === Load JSON data ===
with open('F1.json') as f:
    fighter_stats = json.load(f)['fighter_stats']

with open('F2.json') as f:
    aircraft_info = json.load(f)

with open('F3.json') as f:
    conflict_years = json.load(f)

# === Prepare year_nation_kills and year_nation_weighted_age ===
year_nation_kills = defaultdict(lambda: defaultdict(int))
year_nation_weighted_age = defaultdict(lambda: defaultdict(float))

for ac, conflicts in fighter_stats.items():
    ac_info = aircraft_info.get(ac)
    if not ac_info:
        continue
    nation = ac_info.get('nation')
    in_service_year = ac_info.get('in_service')
    if not nation or in_service_year is None:
        continue
    for conflict, stats in conflicts.items():
        year = conflict_years.get(conflict, {}).get('start')
        if not year:
            continue
        kills = stats.get('Kills', 0)
        year_nation_kills[year][nation] += kills
        age = year - in_service_year
        if age < 0:
            age = 0
        year_nation_weighted_age[year][nation] += age * kills

# === Define sides and their nations ===
side_nations = {
    'USA': ['USA'],
    'USSR+France': ['USSR', 'France']
}

nation_to_side = {}
for side, nations in side_nations.items():
    for n in nations:
        nation_to_side[n] = side

# === Compute difficulty factors per year and side ===
difficulty_by_year = {}
for year in sorted(year_nation_kills.keys()):
    total_kills = sum(year_nation_kills[year].values())
    if total_kills == 0:
        continue
    side_ages = {}
    for side, nations in side_nations.items():
        kills = sum(year_nation_kills[year].get(n, 0) for n in nations)
        weighted_age = sum(year_nation_weighted_age[year].get(n, 0) for n in nations)
        side_ages[side] = weighted_age / kills if kills > 0 else 0
    difficulty_by_year[year] = side_ages

# === Build aircraft to side map ===
ac_to_side = {}
for ac, info in aircraft_info.items():
    nation = info.get('nation')
    if nation in nation_to_side:
        ac_to_side[ac] = nation_to_side[nation]

# === Collect kills per aircraft per year (needed for opponent mix) ===
year_ac_kills = defaultdict(lambda: defaultdict(int))  # year -> ac -> kills

for ac, conflicts in fighter_stats.items():
    for conflict, stats in conflicts.items():
        year = conflict_years.get(conflict, {}).get('start')
        if not year:
            continue
        kills = stats.get('Kills', 0)
        year_ac_kills[year][ac] += kills

# === Compute opponent mix helper function ===
def compute_opponent_mix(ac, year):
    ac_side = ac_to_side.get(ac)
    if not ac_side:
        return {}

    opponent_sides = [side for side in side_nations if side != ac_side]
    opponent_acs = [a for a, s in ac_to_side.items() if s in opponent_sides]

    total_opponent_kills = sum(year_ac_kills[year].get(a, 0) for a in opponent_acs)
    if total_opponent_kills == 0:
        return {}

    mix = {}
    for opp_ac in opponent_acs:
        kills = year_ac_kills[year].get(opp_ac, 0)
        if kills > 0:
            mix[opp_ac] = kills / total_opponent_kills
    return mix

# === Build regression model for kill ratio vs difficulty ===
def build_regression_model():
    X = []
    y = []
    for ac, conflicts in fighter_stats.items():
        side = ac_to_side.get(ac)
        if not side:
            continue
        for conflict, stats in conflicts.items():
            year = conflict_years.get(conflict, {}).get('start')
            if not year:
                continue
            difficulty = difficulty_by_year.get(year, {}).get(side)
            if difficulty is None:
                continue
            kills = stats.get('Kills', 0)
            losses = stats.get('Loss', 0)
            if kills == 0 and losses == 0:
                continue
            if losses == 0:
                kill_ratio = kills
            else:
                kill_ratio = kills / losses
            X.append([difficulty])
            y.append(kill_ratio)
    if not X:
        return None
    model = LinearRegression()
    model.fit(X, y)
    return model

# === Load year filter from temp.txt ===
def load_year_filter_from_temp():
    try:
        with open('temp.txt', 'r') as f:
            lines = f.readlines()
            years = set(int(line.strip()) for line in lines if line.strip().isdigit())
            if years:
                return years
    except Exception as e:
        print(f"WARNING: Could not read year filter from temp.txt: {e}")
    return None  # No filter means include all

# === Main function to compute and display residual kill ratios with opponent mix and correlations ===
def print_residual_kill_tables():
    print("Residual Kill Ratio Tables Per Aircraft\n")
    model = build_regression_model()
    year_filter = load_year_filter_from_temp()

    for ac in sorted(fighter_stats.keys()):
        ac_info = aircraft_info.get(ac, {})
        nation = ac_info.get('nation', 'Unknown')
        in_service = ac_info.get('in_service', '?')
        side = ac_to_side.get(ac)
        if not side:
            continue

        print(f"Aircraft: {ac} (Nation: {nation}, In-Service Year: {in_service})")
        header = f"{'Year':>6} | {'Kills':>5} | {'Losses':>7} | {'Kill Ratio':>10} | {'Difficulty':>10} | {'Residual':>10} | Opponent Mix (AC: %)"
        print(header)
        print("-" * len(header))

        residuals_by_year = {}
        opponent_mix_by_year = {}

        any_data = False
        for conflict, stats in fighter_stats[ac].items():
            year = conflict_years.get(conflict, {}).get('start')
            if not year:
                continue
            if year_filter is not None and year not in year_filter:
                continue

            kills = stats.get('Kills', 0)
            losses = stats.get('Loss', 0)
            if kills == 0 and losses == 0:
                continue
            if losses == 0:
                kill_ratio = kills
            else:
                kill_ratio = kills / losses

            difficulty = difficulty_by_year.get(year, {}).get(side)
            expected = model.predict([[difficulty]])[0] if model and difficulty is not None else None
            residual = kill_ratio - expected if expected is not None else None

            diff_str = f"{difficulty:10.3f}" if difficulty is not None else " " * 10
            resid_str = f"{residual:10.3f}" if residual is not None else " " * 10

            mix = compute_opponent_mix(ac, year)
            mix_str = ', '.join(f"{opp_ac}:{pct*100:.1f}%" for opp_ac, pct in sorted(mix.items(), key=lambda x: x[1], reverse=True))

            print(f"{year:6} | {kills:5} | {losses:7} | {kill_ratio:10.3f} | {diff_str} | {resid_str} | {mix_str}")
            any_data = True

            if residual is not None:
                residuals_by_year[year] = residual
                opponent_mix_by_year[year] = mix

        if not any_data:
            print("No valid combat data for this aircraft.\n")
            continue

        all_enemy_acs = set()
        for mix in opponent_mix_by_year.values():
            all_enemy_acs.update(mix.keys())

        if all_enemy_acs:
            print("\nCorrelation Between Residual Kill Ratio and Opponent Aircraft Mix:")
            print("-" * 80)
            for enemy_ac in sorted(all_enemy_acs):
                residual_vals = []
                mix_weights = []
                for year in residuals_by_year:
                    if year in opponent_mix_by_year and enemy_ac in opponent_mix_by_year[year]:
                        residual_vals.append(residuals_by_year[year])
                        mix_weights.append(opponent_mix_by_year[year][enemy_ac])
                if len(residual_vals) < 2:
                    print(f"Enemy Aircraft: {enemy_ac} - Insufficient data for correlation (need >=2 points).")
                    continue
                corr_coef, p_value = pearsonr(residual_vals, mix_weights)
                print(f"Enemy Aircraft: {enemy_ac}")
                print(f"  Correlation coefficient: {corr_coef:.4f}")
                print(f"  P-value: {p_value:.4f}")
                print(f"  Data points: {len(residual_vals)}")
                print("-" * 40)

        # === Simulated residual if 100% of mix is each enemy aircraft ===
        if model:
            print("\nSimulated Residual if 100% Opponent Aircraft:")
            print("-" * 80)
            for enemy_ac in sorted(all_enemy_acs):
                sim_residuals = []
                for year in residuals_by_year:
                    difficulty = difficulty_by_year.get(year, {}).get(side)
                    if difficulty is None:
                        continue
                    expected = model.predict([[difficulty]])[0]
                    if year in opponent_mix_by_year and enemy_ac in opponent_mix_by_year[year]:
                        actual = residuals_by_year[year] + expected
                        sim_kill_ratio = 1.0 * actual + (1.0 - 1.0) * expected
                        sim_residual = sim_kill_ratio - expected
                        sim_residuals.append(sim_residual)
                if sim_residuals:
                    avg_resid = sum(sim_residuals) / len(sim_residuals)
                    print(f"Enemy Aircraft: {enemy_ac:20s} | Simulated Residual: {avg_resid:8.3f} over {len(sim_residuals)} years")

        print("\n")

# === Run the print function ===
if __name__ == "__main__":
    print_residual_kill_tables()
