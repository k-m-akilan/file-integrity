import json
import os

BASELINE_FILE = "data/baseline.json"


def save_baseline(data):

    os.makedirs("data", exist_ok=True)

    with open(BASELINE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_baseline():

    if not os.path.exists(BASELINE_FILE):
        return {}

    with open(BASELINE_FILE, "r") as file:
        return json.load(file)