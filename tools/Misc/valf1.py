import json
from collections import defaultdict
from scipy.stats import pearsonr

# Load your JSON files (assumes they are in the same directory)
with open('f1.json') as f1_file:
    data_f1 = json.load(f1_file)
with open('f2.json') as f2_file:
    data_f2 = json.load(f2_file)
with open('f3.json') as f3_file:
    data_f3 = json.load(f3_file)

fighter_stats = data_f1['fighter_stats']
conflicts = data_f3

# Map conflict name to start year for quick lookup
conflict_year_map = {}
for cname, cdata in conflicts.items():
    start = cdata.get('start')
    if start is not None:
        conflict_year_map[cname] = start

# Helper function: get nation of a fighter
def get_nation(fighter):
    info = data_f2.get(fighter, {})
    return info.get('nation')

# Collect kill ratios by nation and age
nation_age_ratios = defaultdict(lambda: defaultdict(list))
nation_age_conflicts = defaultdict(lambda: defaultdict(set))

# Yearly kills and weighted age sums for difficulty factor
year_nation_kills = defaultdict(lambda: defaultdict(float))
year_nation_weighted_age = defaultdict(lambda: defaultdict(float))

# Debug counters
total_pairs = 0
skipped_no_in_service = 0
skipped_no_conflict_year = 0
skipped_zero_kills_losses = 0
skipped_negative_age = 0
matched_pairs = 0

for fighter, conflicts_data in fighter_stats.items():
    in_service = data_f2.get(fighter, {}).get('in_service')
    nation = get_nation(fighter)
    if in_service is None or nation is None:
        skipped_no_in_service += 1
        continue
    for conflict_name, stats in conflicts_data.items():
        if conflict_name == "Total":
            continue  # Skip totals
        start_year = conflict_year_map.get(conflict_name)
        if start_year is None:
            skipped_no_conflict_year += 1
            continue
        kills = stats.get('Kills', 0)
        losses = stats.get('Loss', 0)
        total_pairs += 1
        if kills == 0 and losses == 0:
            skipped_zero_kills_losses += 1
            continue
        age = start_year - in_service
        if age < 0:
            skipped_negative_age += 1
            continue
        kill_ratio = kills / losses if losses > 0 else kills
        if kill_ratio == 0:
            continue
        matched_pairs += 1
        nation_age_ratios[nation][age].append(kill_ratio)
        if len(nation_age_conflicts[nation][age]) < 3:
            nation_age_conflicts[nation][age].add(conflict_name)

        # Track kills and weighted age sums for difficulty factor
        year_nation_kills[start_year][nation] += kills
        year_nation_weighted_age[start_year][nation] += kills * age

def print_summary():
    print(f"Total (fighter, conflict) pairs: {total_pairs}")
    print(f"Skipped no in_service or nation: {skipped_no_in_service}")
    print(f"Skipped no conflict year: {skipped_no_conflict_year}")
    print(f"Skipped zero kills or losses: {skipped_zero_kills_losses}")
    print(f"Skipped negative age: {skipped_negative_age}")
    print(f"Matched pairs: {matched_pairs}")
    print()