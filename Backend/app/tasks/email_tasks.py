import smtplib
from email.message import EmailMessage

from app.core.celery_app import celery_app
from app.core.config import settings


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def send_welcome_email(self, to_email: str, username: str):
    if not settings.SMTP_USER:
        print(f"[EMAIL SIMULATION] To: {to_email} | Welcome {username}!")
        return "simulated"

    msg = EmailMessage()
    msg["Subject"] = "Welcome to Student Management App"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email
    msg.set_content(
        f"Hi {username},\n\n"
        "Your account has been created successfully.\n\n"
        "Thanks,\nStudent Management Team"
    )

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)

    return f"sent to {to_email}"