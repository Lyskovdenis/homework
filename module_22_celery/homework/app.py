from flask import Flask, request, jsonify, abort

from pathlib import Path

from celery import group
from celery.result import GroupResult

from celery_tasks import blur_image_task

app = Flask(__name__)

# Хранилище групп задач в памяти процесса Flask
GROUPS: dict[str, GroupResult] = {}

# Файл для хранения подписчиков (общий для Flask и Celery)
SUBSCRIBERS_FILE = Path(__file__).with_name("subscribers.txt")


def _load_subscribers() -> set[str]:
    try:
        with SUBSCRIBERS_FILE.open("r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


def _save_subscribers(subscribers: set[str]) -> None:
    with SUBSCRIBERS_FILE.open("w", encoding="utf-8") as f:
        for email in subscribers:
            f.write(email + "\n")


@app.post("/blur")
def blur_endpoint():
    """
    Ставит в очередь обработку переданных изображений.
    Ожидает JSON:
    {
      "images": ["img1.jpg", "img2.jpg"],
      "email": "user@example.com"
    }
    Возвращает ID группы задач.
    """
    data = request.get_json(silent=True) or {}
    images = data.get("images")
    email = data.get("email")

    if not images or not isinstance(images, list):
        abort(400, description="images must be a non-empty list")
    if not email:
        abort(400, description="email is required")

    blur_jobs = [blur_image_task.s(src) for src in images]
    group_result: GroupResult = group(blur_jobs).apply_async()

    GROUPS[group_result.id] = group_result

    return jsonify({"group_id": group_result.id}), 202


@app.get("/status/<group_id>")
def status_endpoint(group_id: str):
    """
    Возвращает прогресс и статус группы задач по её ID.
    """
    group_result = GROUPS.get(group_id)
    if group_result is None:
        abort(404, description="Group not found")

    total = len(group_result.results)
    completed = sum(1 for r in group_result.results if r.ready())
    status = "completed" if group_result.ready() else "processing"

    return jsonify({
        "group_id": group_id,
        "total_tasks": total,
        "completed_tasks": completed,
        "status": status,
    })


@app.post("/subscribe")
def subscribe_endpoint():
    """
    Подписка на еженедельную рассылку.
    Ожидает JSON: {"email": "..."}.
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    if not email:
        abort(400, description="email is required")

    subscribers = _load_subscribers()
    subscribers.add(email)
    _save_subscribers(subscribers)

    return jsonify({"message": "Subscribed", "email": email})


@app.post("/unsubscribe")
def unsubscribe_endpoint():
    """
    Отписка от рассылки.
    Ожидает JSON: {"email": "..."}.
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    if not email:
        abort(400, description="email is required")

    subscribers = _load_subscribers()
    subscribers.discard(email)
    _save_subscribers(subscribers)

    return jsonify({"message": "Unsubscribed", "email": email})


if __name__ == "__main__":
    app.run(debug=True)