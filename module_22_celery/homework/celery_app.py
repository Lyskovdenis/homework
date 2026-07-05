from celery import Celery
from celery.schedules import crontab

# 1. Сначала создаём объект Celery
celery_app = Celery(
    "homework",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "test-newsletter-every-minute": {
        "task": "celery_tasks.send_weekly_newsletter",
        "schedule": crontab(minute="*/1"),
    },
}

# 3. Импортируем модуль с задачами, чтобы они зарегистрировались
import celery_tasks