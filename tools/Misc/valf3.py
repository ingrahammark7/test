import json
from collections import defaultdict
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

# === Prepare aircraft kill stats by year for residual calculation ===
# For each aircraft and year, get kills and compute opponent mix and residual kill ratio

# First, gather kills per aircraft per year (using conflict start years)
ac_year_kills = defaultdict(lambda: defaultdict(int))
# Also collect opponent kills per year for mix calculation
year_total_kills = defaultdict(int)

# To build opponent mix, find all aircraft that fought in same year but on opposite side

# Helper: nation -> side
nation_to_side = {}
for side, nations in side_nations.items():
    for n in nations:
        nation_to_side[n] = side

# Collect kills and opponent kills per year
for ac, conflicts in fighter_stats.items():
    ac_info = aircraft_info.get(ac)
    if not ac_info:
        continue
    nation = ac_info.get('nation')
    side = nation_to_side.get(nation)
    if not side:
        continue
    for conflict, stats in conflicts.items():
        year = conflict_years.get(conflict, {}).get('start')
        if not year:
            continue
        kills = stats.get('Kills', 0)
        if kills == 0:
            continue
        ac_year_kills[ac][year] += kills
        year_total_kills[year] += kills

# For each year, build total opponent kills per aircraft per year to calculate mix
# Opponents are aircraft whose nation is on the other side

# First build mapping of aircraft to side for quick lookup
ac_to_side = {}
for ac, info in aircraft_info.items():
    nation = info.get('nation')
    if nation in nation_to_side:
        ac_to_side[ac] = nation_to_side[nation]

# Build opponent kills per year (opponent aircraft kills in same year)
year_ac_kills = defaultdict(lambda: defaultdict(int))
for ac, years in ac_year_kills.items():
    for year, kills in years.items():
        year_ac_kills[year][ac] = kills

# Now for each aircraft and year, compute opponent mix (percentage of opponent kills by opponent aircraft)
def compute_opponent_mix(ac, year):
    ac_side = ac_to_side.get(ac)
    if not ac_side:
        return {}
    opponent_side = None
    for side in side_nations:
        if side != ac_side:
            opponent_side = side
            break
    if opponent_side is None:
        return {}

    # Sum opponent kills in that year by opponent aircraft
    opponent_acs = [a for a, s in ac_to_side.items() if s == opponent_side]
    total_opponent_kills = sum(year_ac_kills[year].get(a, 0) for a in opponent_acs)
    if total_opponent_kills == 0:
        return {}

    mix = {}
    for opp_ac in opponent_acs:
        kills = year_ac_kills[year].get(opp_ac, 0)
        if kills > 0:
            mix[opp_ac] = kills / total_opponent_kills
    return mix

# Compute residual kill ratios:
# residual = actual kill ratio adjusted by difficulty factor for that year and side

# First compute kill ratio per aircraft per year:
# kill ratio = kills of ac in year / total kills of that side in year

# Need total kills per side per year
year_side_kills = defaultdict(lambda: defaultdict(int))
for year, nations_kills in year_nation_kills.items():
    for nation, kills in nations_kills.items():
        side = nation_to_side.get(nation)
        if side:
            year_side_kills[year][side] += kills

# Now calculate residual kill ratio:
# Residual = kill ratio / difficulty factor (to partial out difficulty effect)
# (If difficulty factor = average aircraft age, we invert or scale accordingly)
# Here, higher average aircraft age means higher difficulty, so residual = kill_ratio / difficulty

# --- Main function to print tables ---

def print_residual_kill_tables():
    print("Residual Kill Ratio Tables Per Aircraft\n")

    for ac in sorted(ac_year_kills.keys()):
        ac_info = aircraft_info.get(ac, {})
        nation = ac_info.get('nation', 'Unknown')
        in_service = ac_info.get('in_service', '?')
        print(f"Aircraft: {ac} (Nation: {nation}, In-Service Year: {in_service})")
        print(f"{'Year':>6} | {'Kills':>5} | {'Kill Ratio':>10} | {'Difficulty':>10} | {'Residual':>10} | Opponent Mix (Aircraft:%)")
        print("-" * 90)
        for year in sorted(ac_year_kills[ac].keys()):
            kills = ac_year_kills[ac][year]
            side = ac_to_side.get(ac)
            if not side:
                continue
            total_side_kills = year_side_kills[year].get(side, 0)
            if total_side_kills == 0:
                continue
            kill_ratio = kills / total_side_kills
            difficulty = difficulty_by_year.get(year, {}).get(side, None)
            if not difficulty or difficulty == 0:
                residual = kill_ratio
            else:
                residual = kill_ratio / difficulty

            # Opponent mix string
            mix = compute_opponent_mix(ac, year)
            mix_str = ', '.join(f"{opp_ac}:{pct*100:.1f}%" for opp_ac, pct in sorted(mix.items(), key=lambda x: x[1], reverse=True))

            print(f"{year:6} | {kills:5} | {kill_ratio:10.4f} | {difficulty:10.3f} | {residual:10.4f} | {mix_str}")

        print("\n")

# === Run the print function ===
if __name__ == "__main__":
    print_residual_kill_tables()