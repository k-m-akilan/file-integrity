import os
import shutil


BACKUP_FOLDER = "backups"


os.makedirs(BACKUP_FOLDER, exist_ok=True)


def backup_file(file_path):

    try:

        if not os.path.exists(file_path):
            return

        filename = os.path.basename(file_path)

        backup_path = os.path.join(
            BACKUP_FOLDER,
            filename + ".bak"
        )

        shutil.copy2(file_path, backup_path)

        print(f"[BACKUP] Backup created: {backup_path}")

    except Exception as e:

        print(f"[BACKUP ERROR] {e}")


def recover_file(file_path):

    try:

        filename = os.path.basename(file_path)

        backup_path = os.path.join(
            BACKUP_FOLDER,
            filename + ".bak"
        )

        if not os.path.exists(backup_path):

            print("[RECOVERY ERROR] No backup found.")

            return

        shutil.copy2(backup_path, file_path)

        print(f"[RECOVERY] File restored: {file_path}")

    except Exception as e:

        print(f"[RECOVERY ERROR] {e}")