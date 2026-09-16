import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_ADDRESS = "Your Mail address"
EMAIL_PASSWORD = "Your Google app password"

TO_EMAIL = "RECIPIENT_EMAIL_ADDRESS"


def send_email_alert(message, severity):

    try:

        subject = f"FIM Security Alert - {severity}"

        body = f"""
File Integrity Monitoring Alert

Severity: {severity}

Details:
{message}
"""

        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("[INFO] Email alert sent successfully.")

    except Exception as e:

        print(f"[EMAIL ERROR] {e}")
