from pathlib import Path
import json


def save_json_to_raw(data, filename):
    # Compute the project root (two levels up from current file, e.g., file_manager.py)
    project_root = Path(__file__).resolve().parents[1]

    # Construct full path to data/raw/
    raw_data_path = project_root / "data" / "raw" / filename

    # Ensure the raw directory exists
    raw_data_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the JSON file
    with open(raw_data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Saving raw data to:", raw_data_path)


def load_json_from_raw(filename):
    # Compute the project root (two levels up from current file, e.g., file_manager.py)
    project_root = Path(__file__).resolve().parents[1]

    # Construct full path to data/raw/
    raw_data_path = project_root / "data" / "raw" / filename

    # Read the JSON file
    with open(raw_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Loading raw data from:", raw_data_path)

    return data


def save_json_to_processed(data, filename):
    # Compute the project root (two levels up from current file, e.g., file_manager.py)
    project_root = Path(__file__).resolve().parents[1]

    # Construct full path to data/processed/
    processed_data_path = project_root / "data" / "processed" / filename

    # Ensure the processed directory exists
    processed_data_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the JSON file
    with open(processed_data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Saving processed data to:", processed_data_path)


def load_json_from_processed(filename):
    # Compute the project root (two levels up from current file, e.g., file_manager.py)
    project_root = Path(__file__).resolve().parents[1]

    # Construct full path to data/processed/
    processed_data_path = project_root / "data" / "processed" / filename

    # Read the JSON file
    with open(processed_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Loading processed data from:", processed_data_path)

    return data
