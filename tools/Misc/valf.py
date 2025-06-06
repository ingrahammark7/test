import json
from collections import defaultdict
from scipy.stats import pearsonr

# Load your JSON files (replace with actual file paths or variables)
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

# Helper: get nation of fighter
def get_nation(fighter):
    info = data_f2.get(fighter, {})
    return info.get('nation')

# Collect data: {nation: {age_bucket: [ratios]}} and store conflict samples per bucket
nation_age_ratios = defaultdict(lambda: defaultdict(list))
nation_age_conflicts = defaultdict(lambda: defaultdict(set))

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

def print_summary():
    print(f"Total (fighter, conflict) pairs: {total_pairs}")
    print(f"Skipped no in_service or nation: {skipped_no_in_service}")
    print(f"Skipped no conflict year: {skipped_no_conflict_year}")
    print(f"Skipped zero kills or losses: {skipped_zero_kills_losses}")
    print(f"Skipped negative age: {skipped_negative_age}")
    print(f"Matched pairs: {matched_pairs}")
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
        # Compute correlation if enough data
        if len(age_vals) > 1:
            r, p = pearsonr(age_vals, avg_ratios)
            print(f"Pearson r: {r:.4f}")
            print(f"P-value: {p:.4f}")
        else:
            print("Not enough data for correlation.")
        print()

print_summary()
print_table()

all_ages = set(age for nation in nation_age_ratios for age in nation_age_ratios[nation])
current_ages = all_ages.copy()

while True:
    removed_ages = all_ages - current_ages
    print(f"Currently shown age buckets: {', '.join(map(str, sorted(current_ages))) if current_ages else '(none)'}")
    print(f"Removed age buckets: {', '.join(map(str, sorted(removed_ages))) if removed_ages else '(none)'}")

    user_input = input(
        "Enter command to 'add' or 'remove' age buckets (e.g. 'add 4,7' or 'remove 13'),\n"
        "or press Enter to quit: ").strip().lower()

    if not user_input:
        print("Exiting.")
        break

    parts = user_input.split(maxsplit=1)
    if len(parts) != 2 or parts[0] not in ('add', 'remove'):
        print("Invalid command. Use 'add <ages>' or 'remove <ages>'.")
        continue

    cmd, ages_part = parts
    try:
        ages_to_change = set(int(x.strip()) for x in ages_part.split(','))
    except ValueError:
        print("Invalid age values; please enter comma-separated integers.")
        continue

    if cmd == 'add':
        current_ages.update(ages_to_change)
    elif cmd == 'remove':
        current_ages.difference_update(ages_to_change)

    print_summary()
    print_table(filter_ages=current_ages)