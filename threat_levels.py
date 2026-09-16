import os


CRITICAL_EXTENSIONS = [
    ".conf",
    ".config",
    ".ini",
    ".env"
]


def get_severity(event_type, file_path):

    extension = os.path.splitext(file_path)[1].lower()

    filename = os.path.basename(file_path).lower()

    if event_type == "deleted":

        if extension in CRITICAL_EXTENSIONS:
            return "CRITICAL"

        return "HIGH"

    if event_type == "modified":

        if extension in CRITICAL_EXTENSIONS:
            return "HIGH"

        if "secret" in filename:
            return "HIGH"

        return "MEDIUM"

    if event_type == "created":

        if extension in CRITICAL_EXTENSIONS:
            return "MEDIUM"

        return "LOW"

    return "LOW"