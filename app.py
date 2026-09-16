from scanner import scan_directory
from database import save_baseline
from monitor import start_monitoring
from db_logger import initialize_database


WATCHED_DIRECTORIES = [
    "watched-files",
    "critical-data",
    "configs"
]


def main():
    initialize_database()

    print("[INFO] Creating initial baseline...")
    

    combined_baseline = {}

    for directory in WATCHED_DIRECTORIES:

        baseline = scan_directory(directory)

        combined_baseline.update(baseline)

    save_baseline(combined_baseline)

    print("[INFO] Baseline created successfully.")

    start_monitoring(WATCHED_DIRECTORIES)


if __name__ == "__main__":
    main()