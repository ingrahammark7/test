import json
import re
from scipy.stats import pearsonr

def load_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} top-level entries from {filename}")
        return data
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return {}

def parse_caliber(gun_str):
    # Extract number before 'mm' ignoring case and spaces
    m = re.search(r'(\d+)\s*mm', gun_str.lower())
    if m:
        return float(m.group(1))
    return None

def main():
    f1_data = load_json_file('f1.json')
    f2_data = load_json_file('f2.json')

    if 'fighter_stats' not in f1_data:
        print("ERROR: 'fighter_stats' key missing in f1.json")
        return

    fighter_stats = f1_data['fighter_stats']

    print(f"fighter_stats keys sample: {list(fighter_stats.keys())[:5]}")
    print(f"fighters_info keys sample: {list(f2_data.keys())[:5]}")

    nation_data = {}
    missing_nation_fighters = []

    print("\nProcessing fighters to extract total kills, gun caliber, and nation...\n")

    for fighter_name, stats in fighter_stats.items():
        fighter_info = f2_data.get(fighter_name)
        if not fighter_info:
            print(f"  WARNING: No fighter info found for '{fighter_name}' in f2.json")
            continue

        gun = fighter_info.get('gun')
        nation = fighter_info.get('nation')

        if not gun:
            print(f"  WARNING: Fighter '{fighter_name}' missing gun info")
            continue

        if not nation:
            print(f"  WARNING: Fighter '{fighter_name}' missing nation info — please update f2.json")
            missing_nation_fighters.append(fighter_name)
            continue

        caliber = parse_caliber(gun)
        if caliber is None:
            print(f"  WARNING: Could not parse caliber from gun '{gun}' for fighter '{fighter_name}'")
            continue

        total_kills = stats.get('Total', {}).get('Kills')
        if total_kills is None:
            print(f"  WARNING: Fighter '{fighter_name}' missing total kills")
            continue

        # Initialize nation container
        if nation not in nation_data:
            nation_data[nation] = {
                'calibers': [],
                'kills': [],
                'details': []
            }

        nation_data[nation]['calibers'].append(caliber)
        nation_data[nation]['kills'].append(total_kills)
        nation_data[nation]['details'].append({
            'fighter': fighter_name,
            'gun': gun,
            'caliber': caliber,
            'kills': total_kills
        })

    if missing_nation_fighters:
        print("\nFighters missing nation info (update f2.json): " + ", ".join(missing_nation_fighters))

    print("\nCorrelation (Kills vs Gun Caliber) by Nation:\n")

    for nation, data in nation_data.items():
        calibers = data['calibers']
        kills = data['kills']

        print(f"Nation: {nation}")
        if len(calibers) < 2:
            print(f"  Not enough data points ({len(calibers)}) to compute correlation.\n")
            continue

        r, p = pearsonr(calibers, kills)
        print(f"  Pearson correlation coefficient: {r:.4f} (p-value: {p:.4g})\n")

        print(f"{'Fighter':15} {'Gun':20} {'Caliber':8} {'Kills':5}")
        print("-" * 55)
        for d in data['details']:
            print(f"{d['fighter']:15} {d['gun']:20} {d['caliber']:8.1f} {d['kills']:5}")
        print()

if __name__ == '__main__':
    main()