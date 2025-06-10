import json
from collections import defaultdict
from scipy.stats import linregress

# === Load JSON data ===
with open('F1.json') as f:
    fighter_stats = json.load(f)['fighter_stats']

with open('F2.json') as f:
    aircraft_info = json.load(f)

with open('F3.json') as f:
    conflict_years = json.load(f)

# === Prepare nation and age-based difficulty data ===
year_nation_kills = defaultdict(lambda: defaultdict(int))
year_nation_weighted_age = defaultdict(lambda: defaultdict(float))

for ac, conflicts in fighter_stats.items():
    ac_info = aircraft_info.get(ac)
    if not ac_info:
        continue
    nation = ac_info.get('nation')
    in_service = ac_info.get('in_service')
    if not nation or in_service is None:
        continue
    for conflict, stats in conflicts.items():
        year = conflict_years.get(conflict, {}).get('start')
        if not year:
            continue
        kills = stats.get('Kills', 0)
        age = max(0, year - in_service)
        year_nation_kills[year][nation] += kills
        year_nation_weighted_age[year][nation] += kills * age

# === Define sides and their nations ===
side_nations = {
    'USA': ['USA'],
    'USSR+France': ['USSR', 'France']
}
nation_to_side = {nation: side for side, nations in side_nations.items() for nation in nations}

# === Compute difficulty by year and side ===
difficulty_by_year = defaultdict(dict)
for year in sorted(year_nation_kills):
    for side, nations in side_nations.items():
        kills = sum(year_nation_kills[year].get(n, 0) for n in nations)
        weighted_age = sum(year_nation_weighted_age[year].get(n, 0) for n in nations)
        if kills > 0:
            difficulty_by_year[year][side] = weighted_age / kills

# === Compute kills per aircraft per year ===
ac_year_kills = defaultdict(lambda: defaultdict(int))
year_total_kills = defaultdict(int)
year_side_kills = defaultdict(lambda: defaultdict(int))

for ac, conflicts in fighter_stats.items():
    ac_info = aircraft_info.get(ac)
    nation = ac_info.get('nation') if ac_info else None
    side = nation_to_side.get(nation)
    if not side:
        continue
    for conflict, stats in conflicts.items():
        year = conflict_years.get(conflict, {}).get('start')
        if not year:
            continue
        kills = stats.get('Kills', 0)
        ac_year_kills[ac][year] += kills
        year_total_kills[year] += kills
        year_side_kills[year][side] += kills

# === Map aircraft to side ===
ac_to_side = {
    ac: nation_to_side.get(info['nation'])
    for ac, info in aircraft_info.items()
    if info.get('nation') in nation_to_side
}

# === Prepare data for regression: (difficulty → kill ratio) per side ===
regression_data = defaultdict(list)  # side → list of (difficulty, kill ratio)

for ac, year_kills in ac_year_kills.items():
    side = ac_to_side.get(ac)
    if not side:
        continue
    for year, kills in year_kills.items():
        total_kills = year_side_kills[year].get(side, 0)
        if total_kills == 0:
            continue
        kill_ratio = kills / total_kills
        difficulty = difficulty_by_year.get(year, {}).get(side)
        if difficulty is not None:
            regression_data[side].append((difficulty, kill_ratio))

# === Fit linear regression per side ===
side_models = {}
for side, data in regression_data.items():
    x_vals, y_vals = zip(*data)
    slope, intercept, *_ = linregress(x_vals, y_vals)
    side_models[side] = (slope, intercept)

# === Build year_ac_kills for opponent mix ===
year_ac_kills = defaultdict(lambda: defaultdict(int))
for ac, years in ac_year_kills.items():
    for year, kills in years.items():
        year_ac_kills[year][ac] = kills

# === Opponent mix function ===
def compute_opponent_mix(ac, year):
    ac_side = ac_to_side.get(ac)
    if not ac_side:
        return {}
    opponent_side = next(s for s in side_nations if s != ac_side)
    opponent_acs = [a for a, s in ac_to_side.items() if s == opponent_side]
    total_opp_kills = sum(year_ac_kills[year].get(a, 0) for a in opponent_acs)
    if total_opp_kills == 0:
        return {}
    mix = {
        a: year_ac_kills[year][a] / total_opp_kills
        for a in opponent_acs if year_ac_kills[year][a] > 0
    }
    return mix

# === Print residual table ===
def print_residual_kill_tables():
    print("Residual Kill Ratio Tables Per Aircraft\n")
    for ac in sorted(ac_year_kills.keys()):
        ac_info = aircraft_info.get(ac, {})
        nation = ac_info.get('nation', 'Unknown')
        in_service = ac_info.get('in_service', '?')
        print(f"Aircraft: {ac} (Nation: {nation}, In-Service Year: {in_service})")
        print(f"{'Year':>6} | {'Kills':>5} | {'Kill Ratio':>10} | {'Predicted':>10} | {'Residual':>10} | Opponent Mix (Aircraft:%)")
        print("-" * 100)

        side = ac_to_side.get(ac)
        if not side or side not in side_models:
            continue
        slope, intercept = side_models[side]

        for year in sorted(ac_year_kills[ac].keys()):
            kills = ac_year_kills[ac][year]
            total_side_k = year_side_kills[year].get(side, 0)
            if total_side_k == 0:
                continue
            kill_ratio = kills / total_side_k
            difficulty = difficulty_by_year.get(year, {}).get(side)
            if difficulty is None:
                continue
            predicted = slope * difficulty + intercept
            residual = kill_ratio - predicted

            mix = compute_opponent_mix(ac, year)
            mix_str = ', '.join(f"{opp_ac}:{pct*100:.1f}%" for opp_ac, pct in sorted(mix.items(), key=lambda x: x[1], reverse=True))
            print(f"{year:6} | {kills:5} | {kill_ratio:10.4f} | {predicted:10.4f} | {residual:10.4f} | {mix_str}")
        print()

# === Run ===
if __name__ == "__main__":
    print_residual_kill_tables()