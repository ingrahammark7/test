from scipy.stats import pearsonr
from valf1 import (
    nation_age_ratios, nation_age_conflicts,
    year_nation_kills, year_nation_weighted_age,
    print_summary, conflict_year_map
)

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

# Initial state
all_ages = set(age for nation in nation_age_ratios for age in nation_age_ratios[nation])
current_ages = set(all_ages)

all_difficulty_years = set(year_nation_kills.keys())
current_difficulty_years = set(all_difficulty_years)

# Run initial output
print_summary()
print_table(filter_ages=current_ages)
compute_difficulty_factor(filter_years=current_difficulty_years)
print_difficulty_analysis()

# Command loop
while True:
    removed_ages = all_ages - current_ages
    removed_difficulty_years = all_difficulty_years - current_difficulty_years

    print("\nCurrently shown age buckets:", sorted(current_ages) or "(none)")
    print("Removed age buckets:", sorted(removed_ages) or "(none)")
    print("Currently shown difficulty years:", sorted(current_difficulty_years) or "(none)")
    print("Removed difficulty years:", sorted(removed_difficulty_years) or "(none)")

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

    # Refresh output
    print_summary()
    print_table(filter_ages=current_ages)
    compute_difficulty_factor(filter_years=current_difficulty_years)
    print_difficulty_analysis()