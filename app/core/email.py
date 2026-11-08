"""
Email sending helpers.
"""
from email.message import EmailMessage
import smtplib

from app.core.config import settings


def send_verification_email(recipient_email: str, verification_code: str, full_name: str | None = None) -> bool:
    """Send an account verification code using SMTP.

    Returns True when the message is sent and False when email is not configured.
    """
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
        return False

    sender = settings.MAIL_FROM or settings.MAIL_USERNAME
    message = EmailMessage()
    message["Subject"] = "Your StudyWise AI verification code"
    message["From"] = sender
    message["To"] = recipient_email

    greeting = f"Hi {full_name}," if full_name else "Hi there,"
    message.set_content(
        f"""{greeting}

Thanks for registering for StudyWise AI.

Your verification code is:

{verification_code}

Open StudyWise AI, paste this code into the verification box, and click Verify email code.

If you did not create this account, you can ignore this email.
"""
    )

    if settings.MAIL_PORT == 465:
        server = smtplib.SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_PORT, timeout=20)
    else:
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT, timeout=20)

    with server:
        server.ehlo()
        if settings.MAIL_PORT != 465:
            server.starttls()
            server.ehlo()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(message)

    return True