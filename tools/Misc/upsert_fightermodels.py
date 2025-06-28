import json
import os

INPUT_FILE = "in.json"
TARGET_FILE = "fightermodels.json"

# Load existing fighter models (if file exists)
if os.path.exists(TARGET_FILE):
    with open(TARGET_FILE, "r") as f:
        existing_models = json.load(f)
else:
    existing_models = {}

# Load new input data
with open(INPUT_FILE, "r") as f:
    new_models = json.load(f)

# Upsert new models into existing ones
for key, value in new_models.items():
    existing_models[key] = value
    print(f"Upserted model: {key}")

# Save updated models
with open(TARGET_FILE, "w") as f:
    json.dump(existing_models, f, indent=2)

print("fightermodels.json updated.")