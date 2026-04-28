"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import time

app = Flask(__name__)

# Момент запуска процесса (аптайм именно этого Flask-приложения)
START_TIME = time.time()


def get_uptime() -> str:
    seconds = int(time.time() - START_TIME)
    # Преобразуем в чч:мм:сс
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@app.route("/uptime", methods=["GET"])
def uptime() -> str:
    uptime_str = get_uptime()
    return f"Current uptime is {uptime_str}"


if __name__ == "__main__":
    app.run(debug=True)