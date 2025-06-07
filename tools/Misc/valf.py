import json
import os

def load_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"✅ Loaded {filename} with {len(data)} top-level entries.")
        return data
    except Exception as e:
        print(f"❌ Failed to load {filename}: {e}")
        return None

def debug_f1(data):
    print("\n=== Debugging f1.json ===")
    print(f"Type of data: {type(data)}")
    print(f"Number of top-level keys: {len(data)}")
    keys = list(data.keys())
    print(f"Sample keys: {keys[:5]}")
    
    if "fighter_stats" in data:
        fs = data["fighter_stats"]
        print(f"Key: 'fighter_stats' -> Type: {type(fs)}")
        print(f"  Number of keys: {len(fs)}")
        print(f"  Sample fighter keys: {list(fs.keys())[:5]}")
    else:
        print("WARNING: Missing 'fighter_stats' key in f1.json")

def debug_f2(data):
    print("\n=== Debugging f2.json ===")
    print(f"Type of data: {type(data)}")
    print(f"Number of top-level keys: {len(data)}")
    keys = list(data.keys())
    print(f"Sample fighter keys: {keys[:5]}")

    # Check structure for first 3 fighters
    for fighter in keys[:3]:
        info = data.get(fighter, {})
        print(f"Key: '{fighter}' -> Type: {type(info)}")
        print(f"  Number of keys: {len(info)}")
        print(f"  Sample subkeys: {list(info.keys())}")

def debug_f3(data):
    print("\n=== Debugging f3.json ===")
    print(f"Type of data: {type(data)}")
    print(f"Number of top-level keys: {len(data)}")
    keys = list(data.keys())
    print(f"Sample war/conflict keys: {keys[:5]}")

    # Check structure for first 3 conflicts
    for conflict in keys[:3]:
        info = data.get(conflict, {})
        print(f"Key: '{conflict}' -> Type: {type(info)}")
        print(f"  Number of keys: {len(info)}")
        print(f"  Sample subkeys: {list(info.keys())}")

def validate_fighter_in_service(f1_stats, f2_info):
    print("\n=== Validating fighters for 'in_service' info ===")
    valid_fighters = []
    missing_fighters = []
    missing_in_service = []
    
    for fighter in f1_stats.keys():
        if fighter not in f2_info:
            print(f"WARNING: Fighter '{fighter}' not found in f2.json")
            missing_fighters.append(fighter)
            continue
        info = f2_info[fighter]
        if "in_service" not in info:
            print(f"WARNING: Fighter '{fighter}' missing 'in_service' key")
            missing_in_service.append(fighter)
            continue
        in_service_year = info["in_service"]
        print(f"Fighter '{fighter}' in service since {in_service_year}")
        valid_fighters.append((fighter, in_service_year))
        
    print(f"\nTotal fighters in f1.json: {len(f1_stats)}")
    print(f"Missing in f2.json: {len(missing_fighters)} fighters")
    print(f"Missing 'in_service' key: {len(missing_in_service)} fighters")
    print(f"Valid fighters with in_service year: {len(valid_fighters)}")
    
    return valid_fighters

def validate_war_dates(war_dates):
    print("\n=== Validating war/conflict date entries ===")
    missing_start = []
    missing_end = []
    valid_conflicts = []
    
    for conflict, dates in war_dates.items():
        if not isinstance(dates, dict):
            print(f"WARNING: Conflict '{conflict}' has unexpected type {type(dates)}")
            continue
        if "start" not in dates:
            missing_start.append(conflict)
        if "end" not in dates:
            missing_end.append(conflict)
        if "start" in dates and "end" in dates:
            valid_conflicts.append(conflict)
        print(f"Conflict '{conflict}': start = {dates.get('start')}, end = {dates.get('end')}")
    
    print(f"\nTotal conflicts: {len(war_dates)}")
    print(f"Conflicts missing 'start': {len(missing_start)}")
    print(f"Conflicts missing 'end': {len(missing_end)}")
    print(f"Conflicts with valid start/end: {len(valid_conflicts)}")
    return valid_conflicts

def main():
    # Load files from current directory
    f1 = load_json("f1.json")
    f2 = load_json("f2.json")
    f3 = load_json("f3.json")
    
    if not (f1 and f2 and f3):
        print("ERROR: One or more files failed to load, exiting.")
        return
    
    # Debug each json
    debug_f1(f1)
    debug_f2(f2)
    debug_f3(f3)
    
    # Validate fighter 'in_service'
    fighter_stats = f1.get("fighter_stats", {})
    valid_fighters = validate_fighter_in_service(fighter_stats, f2)
    
    # Validate war dates
    valid_conflicts = validate_war_dates(f3)
    
    print("\n=== Summary ===")
    print(f"Fighters with valid 'in_service': {len(valid_fighters)}")
    print(f"Conflicts with valid dates: {len(valid_conflicts)}")

if __name__ == "__main__":
    main()