import json
import os

INPUT_FILE = "in.json"
MODELS_FILE = "fightermodels.json"
METADATA_FILE = "fighters.json"

# Load existing
def load_json(path):
    return json.load(open(path)) if os.path.exists(path) else {}

fighter_models = load_json(MODELS_FILE)
fighter_metadata = load_json(METADATA_FILE)

# Load new combined input
try:
    with open(INPUT_FILE, "r") as f:
        incoming = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing error in {INPUT_FILE}: {e}")
    exit(1)

# Process
for name, data in incoming.items():
    # Fallbacks
    model = data.get("model", {
        "body": [[0, 0, 0], [1, 0, 0.1], [3, 0, 0], [1, 0, -0.1]],
        "wing": [[1, -1, 0], [2, 0, 0], [1, 1, 0]],
        "tail": [[2.5, 0, 0], [2.8, 0.2, 0.5], [2.8, -0.2, 0.5]],
        "engine": [[0, -0.2, -0.1], [0, 0.2, -0.1], [-0.5, 0.2, -0.1], [-0.5, -0.2, -0.1]]
    })
    meta = data.get("meta", {
        "gun": "unknown",
        "nation": "unknown",
        "in_service": 1900
    })

    fighter_models[name] = model
    fighter_metadata[name] = meta
    print(f"✔️ {name} added (model {'✓' if 'model' in data else 'stub'}, meta {'✓' if 'meta' in data else 'stub'})")

# Save output
with open(MODELS_FILE, "w") as f:
    json.dump(fighter_models, f, indent=2)
with open(METADATA_FILE, "w") as f:
    json.dump(fighter_metadata, f, indent=2)

print("\n✅ All upserts completed successfully.")