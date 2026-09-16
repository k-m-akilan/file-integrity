import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from scanner import (
    generate_hash,
    should_ignore
)

from database import (
    load_baseline,
    save_baseline
)

from alerts import alert

from recovery import (
    backup_file,
    recover_file
)

from threat_levels import get_severity


class FileMonitorHandler(FileSystemEventHandler):

    def __init__(self):

        self.baseline = load_baseline()

    def on_modified(self, event):

        try:

            if event.is_directory:
                return

            file_path = event.src_path

            if should_ignore(file_path):
                return

            backup_file(file_path)

            current_hash = generate_hash(file_path)

            old_hash = self.baseline.get(file_path)

            if current_hash and old_hash:

                if current_hash != old_hash:

                    severity = get_severity(
                        "modified",
                        file_path
                    )

                    alert(
                        f"File modified: {file_path}",
                        severity
                    )

                    self.baseline[file_path] = current_hash

                    save_baseline(self.baseline)

        except Exception as e:

            print(f"[ERROR] {e}")

    def on_created(self, event):

        try:

            if event.is_directory:
                return

            file_path = event.src_path

            if should_ignore(file_path):
                return

            current_hash = generate_hash(file_path)

            self.baseline[file_path] = current_hash

            save_baseline(self.baseline)

            severity = get_severity(
                "created",
                file_path
            )

            alert(
                f"New file created: {file_path}",
                severity
            )

        except Exception as e:

            print(f"[ERROR] {e}")

    def on_deleted(self, event):

        try:

            if event.is_directory:
                return

            file_path = event.src_path

            if should_ignore(file_path):
                return

            if file_path in self.baseline:

                del self.baseline[file_path]

                save_baseline(self.baseline)

            severity = get_severity(
                "deleted",
                file_path
            )

            alert(
                f"File deleted: {file_path}",
                severity
            )

            recover_file(file_path)

        except Exception as e:

            print(f"[ERROR] {e}")


def start_monitoring(paths):

    event_handler = FileMonitorHandler()

    observer = Observer()

    for path in paths:

        observer.schedule(
            event_handler,
            path,
            recursive=True
        )

        print(f"[INFO] Monitoring started on: {path}")

    observer.start()

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        print("\n[INFO] Monitoring stopped.")

        observer.stop()

    observer.join()
