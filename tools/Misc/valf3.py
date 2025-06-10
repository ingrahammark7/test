# valf3.py

import valf1  # runs data loading and populates data structures
import valf2  # contains print_summary, print_age_buckets, print_difficulty_factors, print_comparative_analysis, etc.

def main():
    valf2.print_summary()

    # Initialize age buckets and difficulty years from valf2's current data
    # Defensive: If keys missing, use empty list
    age_buckets = sorted(valf2.nation_age_ratios.get('USA', {}).keys())
    difficulty_years = sorted(valf2.year_nation_kills.keys())

    valf2.print_age_buckets(age_buckets)
    valf2.print_difficulty_factors(difficulty_years)
    valf2.print_comparative_analysis()

    while True:
        cmd = input(
            "Enter command:\n"
            "  'add <ages>' or 'remove <ages>' (e.g., 'add 4,7')\n"
            "  'adddif <years>' or 'removedif <years>'\n"
            "  Press Enter to quit: "
        ).strip()

        if not cmd:
            break

        parts = cmd.split(maxsplit=1)
        if len(parts) != 2:
            print("Invalid command format")
            continue

        action, values = parts
        # Parse values as integers safely
        try:
            values_list = [int(v.strip()) for v in values.split(',') if v.strip().isdigit()]
        except ValueError:
            print("Please provide comma-separated integers for ages/years")
            continue

        if action == "add":
            for v in values_list:
                if v not in age_buckets:
                    age_buckets.append(v)
            age_buckets.sort()
            valf2.print_age_buckets(age_buckets)

        elif action == "remove":
            age_buckets = [v for v in age_buckets if v not in values_list]
            valf2.print_age_buckets(age_buckets)

        elif action == "adddif":
            for v in values_list:
                if v not in difficulty_years:
                    difficulty_years.append(v)
            difficulty_years.sort()
            valf2.print_difficulty_factors(difficulty_years)

        elif action == "removedif":
            difficulty_years = [v for v in difficulty_years if v not in values_list]
            valf2.print_difficulty_factors(difficulty_years)

        else:
            print(f"Unknown command '{action}'")

        valf2.print_comparative_analysis()

if __name__ == "__main__":
    main()