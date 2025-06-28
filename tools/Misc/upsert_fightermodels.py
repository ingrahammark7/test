import json

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def upsert_models_and_meta(fm_path, fmeta_path, in_path):
    fightermodels = load_json(fm_path)
    fighters_meta = load_json(fmeta_path)
    in_data = load_json(in_path)

    # Upsert fightermodels
    for model_name, model_data in in_data.items():
        if model_name == "meta":
            continue  # skip meta key in models
        if model_name in fightermodels:
            # Merge dictionaries; deep merge armor and subsystems if present
            for key, value in model_data.items():
                if isinstance(value, dict) and key in fightermodels[model_name]:
                    fightermodels[model_name][key].update(value)
                else:
                    fightermodels[model_name][key] = value
        else:
            fightermodels[model_name] = model_data

    # Upsert fighters meta if present
    if "meta" in in_data:
        for model_name, meta_data in in_data["meta"].items():
            if model_name in fighters_meta:
                fighters_meta[model_name].update(meta_data)
            else:
                fighters_meta[model_name] = meta_data

    save_json(fm_path, fightermodels)
    save_json(fmeta_path, fighters_meta)
    print(f"Upsert complete: {fm_path} and {fmeta_path}")

if __name__ == "__main__":
    upsert_models_and_meta('fightermodels.json', 'fighters.json', 'in.json')