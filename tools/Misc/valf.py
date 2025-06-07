import ast
import re

# Load the file
with open("f2.txt") as f:
    try:
        fighter_attrs = ast.literal_eval(f.read())
    except Exception as e:
        print("❌ Error: f2.txt is not a valid Python dictionary.")
        print(f"Details: {e}")
        exit()

# Begin validation
print("Validating f2.txt...\n")

for fighter, attrs in fighter_attrs.items():
    if not isinstance(attrs, dict):
        print(f"❌ {fighter}: Entry is not a dictionary.")
        continue

    gun = attrs.get("gun", None)
    if gun is None:
        print(f"⚠️  {fighter}: Missing 'gun' field.")
    elif not isinstance(gun, str):
        print(f"❌ {fighter}: 'gun' field is not a string.")
    else:
        # Try to extract caliber
        match = re.search(r"(\d{2,3})\s*mm", gun.lower())
        if match:
            print(f"✅ {fighter}: gun = '{gun}' → caliber = {match.group(1)} mm")
        else:
            print(f"⚠️  {fighter}: Gun string '{gun}' does not contain a valid caliber.")

print("\nValidation complete.")