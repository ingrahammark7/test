import json
from collections import defaultdict

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

# === Main function to compute and display residual kill ratios ===
def print_residual_kill_tables():
    print("Residual Kill Ratio Tables Per Aircraft\n")

    for ac in sorted(fighter_stats.keys()):
        ac_info = aircraft_info.get(ac, {})
        nation = ac_info.get('nation', 'Unknown')
        in_service = ac_info.get('in_service', '?')
        side = ac_to_side.get(ac)
        if not side:
            continue

        print(f"Aircraft: {ac} (Nation: {nation}, In-Service Year: {in_service})")
        print(f"{'Year':>6} | {'Kills':>5} | {'Losses':>7} | {'Kill Ratio':>10} | {'Difficulty':>10} | {'Residual':>10}")
        print("-" * 80)

        any_data = False
        for conflict, stats in fighter_stats[ac].items():
            year = conflict_years.get(conflict, {}).get('start')
            if not year:
                continue

            kills = stats.get('Kills', 0)
            losses = stats.get('Losses', 0)

            if kills == 0 and losses == 0:
                continue
            if losses == 0:
                kill_ratio = kills  # treat as infinite
            else:
                kill_ratio = kills / losses

            difficulty = difficulty_by_year.get(year, {}).get(side, None)
            if difficulty is None or difficulty == 0:
                residual = kill_ratio
            else:
                residual = kill_ratio / difficulty

            print(f"{year:6} | {kills:5} | {losses:7} | {kill_ratio:10.3f} | {difficulty:10.3f} | {residual:10.3f}")
            any_data = True

        if not any_data:
            print("No valid combat data for this aircraft.")

        print("\n")

# === Run the print function ===
if __name__ == "__main__":
    print_residual_kill_tables()