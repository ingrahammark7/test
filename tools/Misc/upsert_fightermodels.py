import json
import os

INPUT_FILE = "in.json"
MODELS_FILE = "fightermodels.json"
METADATA_FILE = "fighters.json"

# Load existing fighter models
if os.path.exists(MODELS_FILE):
    with open(MODELS_FILE, "r") as f:
        fighter_models = json.load(f)
else:
    fighter_models = {}

# Load existing metadata
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        fighter_metadata = json.load(f)
else:
    fighter_metadata = {}

# Load input file
with open(INPUT_FILE, "r") as f:
    incoming = json.load(f)

# Process and upsert
for name, entry in incoming.items():
    if "model" in entry:
        fighter_models[name] = entry["model"]
        print(f"✅ Upserted model: {name}")
    else:
        print(f"⚠️ No 'model' found for {name}, skipping model upsert.")

    if "meta" in entry:
        fighter_metadata[name] = entry["meta"]
        print(f"📝 Upserted metadata: {name}")
    else:
        print(f"⚠️ No 'meta' found for {name}, skipping metadata upsert.")

# Save both updated files
with open(MODELS_FILE, "w") as f:
    json.dump(fighter_models, f, indent=2)
print(f"\nSaved: {MODELS_FILE}")

with open(METADATA_FILE, "w") as f:
    json.dump(fighter_metadata, f, indent=2)
print(f"Saved: {METADATA_FILE}")