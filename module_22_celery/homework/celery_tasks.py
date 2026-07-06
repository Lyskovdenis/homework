from typing import Optional
from pathlib import Path

from email.mime.text import MIMEText
import smtplib

from celery import group

from celery_app import celery_app
from config import SMTP_USER, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT
from image import blur_image


SUBSCRIBERS_FILE = Path(__file__).with_name("subscribers.txt")


def _load_subscribers() -> set[str]:
    try:
        with SUBSCRIBERS_FILE.open("r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


@celery_app.task
def blur_image_task(src_filename: str, dst_filename: Optional[str] = None):
    blur_image(src_filename, dst_filename)
    if dst_filename is None:
        dst_filename = f"blur_{src_filename}"
    return dst_filename


@celery_app.task
def send_email_task(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    return f"Email sent to {to_email}"


@celery_app.task
def send_weekly_newsletter():
    """
    Еженедельная рассылка всем подписчикам.
    Сейчас вызывается каждую минуту для теста (см. beat_schedule).
    """
    subscribers = _load_subscribers()

    subject = "Новости сервиса обработки изображений"
    body = (
        "Спасибо, что пользуетесь нашим сервисом! "
        "Напоминаем, что вы можете загружать изображения для обработки."
    )

    tasks = [
        send_email_task.s(email, subject, body)
        for email in subscribers
    ]
    if tasks:
        group(tasks).apply_async()

    return f"Sent newsletter to {len(subscribers)} subscribers"