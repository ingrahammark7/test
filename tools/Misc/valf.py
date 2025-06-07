import json
from scipy.stats import pearsonr

with open('f1.json') as f1_file, open('f2.json') as f2_file, open('f3.json') as f3_file:
    data_f1 = json.load(f1_file)['fighter_stats']
    data_f2 = json.load(f2_file)
    data_f3 = json.load(f3_file)

# Map conflict name -> start year
conflict_years = {}
for name, details in data_f3.items():
    start = details.get('start')
    if start is not None:
        conflict_years[name] = start

# Map fighter -> in_service year and nation
fighter_info = {}
for fighter, info in data_f2.items():
    in_service = info.get('in_service')
    nation = info.get('nation')
    if in_service is not None and nation is not None:
        fighter_info[fighter] = {'in_service': in_service, 'nation': nation}

# Data structures
overall_age_buckets = {}
nation_age_buckets = {}

total_pairs = 0
skipped_no_in_service = 0
skipped_no_conflict_year = 0
skipped_zero_kills_losses = 0
skipped_negative_age = 0
matched_pairs = 0
skipped_no_nation = 0

for fighter_name, conflicts in data_f1.items():
    if fighter_name not in fighter_info:
        skipped_no_in_service += 1
        continue
    in_service_year = fighter_info[fighter_name]['in_service']
    nation = fighter_info[fighter_name]['nation']

    for conflict_name, stats in conflicts.items():
        if conflict_name == 'Total':
            continue
        total_pairs += 1
        if conflict_name not in conflict_years:
            skipped_no_conflict_year += 1
            continue
        start_year = conflict_years[conflict_name]

        kills = stats.get('Kills', 0)
        losses = stats.get('Loss', 0)

        if kills == 0 or losses == 0:
            skipped_zero_kills_losses += 1
            continue

        age = start_year - in_service_year
        if age < 0:
            skipped_negative_age += 1
            continue

        if not nation:
            skipped_no_nation += 1
            continue

        matched_pairs += 1

        ratio = kills / losses

        # Add to overall buckets
        overall_age_buckets.setdefault(age, []).append(ratio)

        # Add to nation buckets
        nation_age_buckets.setdefault(nation, {}).setdefault(age, []).append(ratio)

print(f"Total (fighter, conflict) pairs: {total_pairs}")
print(f"Skipped no in_service or nation: {skipped_no_in_service + skipped_no_nation}")
print(f"Skipped no conflict year: {skipped_no_conflict_year}")
print(f"Skipped zero kills or losses: {skipped_zero_kills_losses}")
print(f"Skipped negative age: {skipped_negative_age}")
print(f"Matched pairs: {matched_pairs}")

def print_correlation(age_buckets, label):
    if not age_buckets:
        print(f"No data for {label}")
        return
    avg_kill_ratio_per_age = {age: sum(ratios)/len(ratios) for age, ratios in age_buckets.items()}
    print(f"\n{label} Age-to-Average Kill Ratio Buckets:")
    for age in sorted(avg_kill_ratio_per_age.keys()):
        print(f"  Age {age}: Avg Ratio {avg_kill_ratio_per_age[age]:.2f}")
    if len(avg_kill_ratio_per_age) >= 2:
        ages = list(avg_kill_ratio_per_age.keys())
        avg_ratios = [avg_kill_ratio_per_age[a] for a in ages]
        r, p = pearsonr(ages, avg_ratios)
        print(f"Pearson r: {r:.4f}")
        print(f"P-value: {p:.4f}")
    else:
        print("Not enough data to compute correlation.")

# Print overall correlation
print_correlation(overall_age_buckets, "Overall")

# Print per nation
for nation, buckets in nation_age_buckets.items():
    print_correlation(buckets, f"Nation: {nation}")