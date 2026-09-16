import os
import hashlib


def load_ignore_rules():

    try:

        with open("ignore_rules.txt", "r") as file:

            return [
                line.strip()
                for line in file.readlines()
                if line.strip()
            ]

    except Exception as e:

        print(f"[IGNORE RULE ERROR] {e}")

        return []


IGNORE_RULES = load_ignore_rules()


def should_ignore(file_path):

    for rule in IGNORE_RULES:

        if file_path.endswith(rule):

            return True

    return False


def generate_hash(file_path):

    try:

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):

                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as e:

        print(f"[HASH ERROR] {e}")

        return None


def scan_directory(directory):

    baseline = {}

    try:

        for root, dirs, files in os.walk(directory):

            for file in files:

                file_path = os.path.join(root, file)

                if should_ignore(file_path):
                    continue

                file_hash = generate_hash(file_path)

                if file_hash:

                    baseline[file_path] = file_hash

    except Exception as e:

        print(f"[SCAN ERROR] {e}")

    return baseline