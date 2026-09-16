from email_alerts import send_email_alert
import logging
import os
from db_logger import log_to_database
from colorama import Fore, Style, init
init(autoreset=True)


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_color(severity):

    if severity == "LOW":
        return Fore.GREEN

    if severity == "MEDIUM":
        return Fore.YELLOW

    if severity == "HIGH":
        return Fore.MAGENTA

    if severity == "CRITICAL":
        return Fore.RED

    return Fore.WHITE


def alert(message, severity):

    full_message = f"[{severity}] {message}"

    color = get_color(severity)

    print(color + full_message + Style.RESET_ALL)
    logging.warning(full_message)

    log_to_database(
    severity,
    message
    )

    send_email_alert(full_message, severity)