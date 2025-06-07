import re
from math import sqrt

# Helper function to safely load Python dicts from files
def load_dict_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Use eval since file is a python dict string; be careful in real apps
    data = eval(content)
    return data

# Improved caliber parser to accept '20mm' or '20 mm'
def parse_caliber(gun_str):
    if not gun_str or not isinstance(gun_str, str):
        return None
    m = re.search(r'(\d+(?:\.\d+)?)\s*mm', gun_str.lower())
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None

# Pearson correlation coefficient calculation
def pearson_corr(x, y):
    n = len(x)
    if n < 2:
        return None
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator_x = sqrt(sum((xi - mean_x) ** 2 for xi in x))
    denominator_y = sqrt(sum((yi - mean_y) ** 2 for yi in y))
    if denominator_x == 0 or denominator_y == 0:
        return None
    return numerator / (denominator_x * denominator_y)

def main():
    # Load fighter stats and fighter info
    print("Loading file: f1.txt")
    fighter_stats_data = load_dict_from_file("f1.txt")
    print(f"Loaded {len(fighter_stats_data.get('fighter_stats', {}))} fighters from f1.txt")

    print("Loading file: f2.txt")
    fighters_info = load_dict_from_file("f2.txt")
    print(f"Loaded {len(fighters_info)} fighters info from f2.txt")

    # Keys samples for debug
    print(f"fighter_stats keys sample: {list(fighter_stats_data.get('fighter_stats', {}).keys())[:5]}")
    print(f"fighters keys sample: {list(fighters_info.keys())[:5]}")

    kills_list = []
    caliber_list = []
    details = []

    print("\nProcessing fighters to extract kills and gun caliber...\n")

    for fighter_name, stats in fighter_stats_data.get('fighter_stats', {}).items():
        fighter_info = fighters_info.get(fighter_name)
        if not fighter_info:
            print(f"  No fighter info found for '{fighter_name}' in f2.txt")
            continue
        gun = fighter_info.get('gun')
        if not gun:
            print(f"  Fighter '{fighter_name}' has no 'gun' field in f2.txt")
            continue

        caliber = parse_caliber(gun)
        if caliber is None:
            print(f"  Could not parse caliber from gun '{gun}' for fighter '{fighter_name}'")
            continue

        # Sum kills from all conflicts under fighter_stats[fighter_name]
        total_kills = 0
        for conflict, conflict_stats in stats.items():
            if conflict == "Total":
                # Use total if available (safer, less prone to summation errors)
                total_kills = conflict_stats.get("Kills", 0)
                break
        else:
            # If no Total, sum manually
            for conflict_stats in stats.values():
                total_kills += conflict_stats.get("Kills", 0)

        kills_list.append(total_kills)
        caliber_list.append(caliber)
        details.append((fighter_name, gun, caliber, total_kills))

    print(f"Total valid data points: {len(kills_list)}\n")

    if len(kills_list) < 2:
        print("Not enough data points to compute correlation.")
        return

    r = pearson_corr(kills_list, caliber_list)
    if r is None:
        print("Could not compute correlation (division by zero).")
        return

    print(f"Pearson correlation coefficient (Kills vs Gun Caliber): {r:.4f}\n")

    # Print table header
    print(f"{'Fighter':<15} {'Gun':<20} {'Caliber':<8} {'Kills':<5}")
    print("-" * 55)
    for fighter_name, gun, caliber, total_kills in details:
        print(f"{fighter_name:<15} {gun:<20} {caliber:<8.1f} {total_kills:<5}")

if __name__ == "__main__":
    main()