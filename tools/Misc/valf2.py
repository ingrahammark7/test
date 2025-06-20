import os
import json
from scipy.stats import pearsonr
import valf3  # your helper module (assumed present)
from valf1 import (
    nation_age_ratios, nation_age_conflicts,
    year_nation_kills, year_nation_weighted_age,
    print_summary, conflict_year_map
)

# --- Ensure JSON files exist with defaults ---

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

# Filenames and their default content
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
    print("Difficulty factors by year and side (weighted average aircraft age):")
    side_nations = {
        'USA': ['USA'],
        'USSR+France': ['USSR', 'France']
    }

    years = sorted(year_nation_kills.keys())
    if filter_years is not None:
        years = [y for y in years if y in filter_years]

    global difficulty_by_year
    difficulty_by_year = {}

    for year in years:
        total_kills = sum(year_nation_kills[year].values())
        if total_kills == 0:
            continue

        side_ages = {}
        for side, nations in side_nations.items():
            kills = sum(year_nation_kills[year].get(n, 0) for n in nations)
            weighted_age = sum(year_nation_weighted_age[year].get(n, 0) for n in nations)
            side_ages[side] = weighted_age / kills if kills > 0 else 0

        difficulty_by_year[year] = side_ages

        print(f"Year {year}:")
        for side in side_nations:
            print(f"  {side} Difficulty Factor (Avg Aircraft Age): {side_ages[side]:.2f}")
    print()

def print_table(filter_ages=None):
    for nation, age_data in nation_age_ratios.items():
        print(f"Nation: {nation} Age-to-Average Kill Ratio Buckets:")
        ages = sorted(age_data.keys())
        avg_ratios = []
        age_vals = []
        for age in ages:
            if filter_ages is not None and age not in filter_ages:
                continue
            ratios = age_data[age]
            avg_ratio = sum(ratios) / len(ratios)
            age_vals.append(age)
            avg_ratios.append(avg_ratio)
            conflicts_sample = ', '.join(sorted(nation_age_conflicts[nation][age]))
            print(f"  Age {age}: Avg Ratio {avg_ratio:.2f} (Conflicts: {conflicts_sample})")
        if len(age_vals) > 1:
            r, p = pearsonr(age_vals, avg_ratios)
            print(f"Pearson r: {r:.4f}")
            print(f"P-value: {p:.4f}")
        else:
            print("Not enough data for correlation.")
        print()

def print_difficulty_analysis():
    print("Comparative Difficulty Analysis:")
    print("Year | Diff (USSR+France - USA) | Ratio (USSR+France / USA) | USA Kill Ratio | USSR+France Kill Ratio")
    print("-" * 85)
    valid_years = [y for y in difficulty_by_year if all(s in difficulty_by_year[y] and difficulty_by_year[y][s] > 0 for s in ['USA', 'USSR+France'])]

    usa_ratios = []
    ussr_ratios = []
    diffs = []
    ratios = []

    for year in sorted(valid_years):
        d_usa = difficulty_by_year[year]['USA']
        d_comm = difficulty_by_year[year]['USSR+France']
        diff = d_comm - d_usa
        ratio = d_comm / d_usa if d_usa > 0 else 0

        usa_kills = year_nation_kills[year].get('USA', 0)
        comm_kills = sum(year_nation_kills[year].get(n, 0) for n in ['USSR', 'France'])
        total_kills = usa_kills + comm_kills
        usa_ratio = usa_kills / total_kills if total_kills else 0
        comm_ratio = comm_kills / total_kills if total_kills else 0

        print(f"{year} | {diff:24.2f} | {ratio:25.2f} | {usa_ratio:.3f}         | {comm_ratio:.3f}")

        diffs.append(diff)
        ratios.append(ratio)
        usa_ratios.append(usa_ratio)
        ussr_ratios.append(comm_ratio)

    def regress(x, y, label):
        if len(x) > 1:
            r, p = pearsonr(x, y)
            print(f"{label} Pearson r: {r:.4f}, p = {p:.4f}")
        else:
            print(f"{label}: Not enough data for regression.")

    print()
    regress(diffs, usa_ratios, "USA vs Diff")
    regress(ratios, usa_ratios, "USA vs Ratio")
    regress(diffs, ussr_ratios, "USSR+France vs Diff")
    regress(ratios, ussr_ratios, "USSR+France vs Ratio")

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

# --- Write current difficulty years to temp.txt ---

def write_temp_file():
    try:
        with open('temp.txt', 'w') as f:
            for year in sorted(current_difficulty_years):
                f.write(f"{year}\n")
    except Exception as e:
        print(f"Failed to write temp.txt: {e}")

# --- Initial data state sets ---

all_ages = set(age for nation in nation_age_ratios for age in nation_age_ratios[nation])
current_ages = set(all_ages)

all_difficulty_years = set(year_nation_kills.keys())
current_difficulty_years = set(all_difficulty_years)

# --- Initial output ---

print_summary()
print_table(filter_ages=current_ages)
compute_difficulty_factor(filter_years=current_difficulty_years)
print_difficulty_analysis()
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
    print_difficulty_analysis()
    print_aircraft_residual_kill_tables(filter_years=current_difficulty_years)
    write_temp_file()
