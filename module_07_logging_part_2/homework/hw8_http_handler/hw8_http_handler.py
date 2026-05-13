import logging
import logging.config
import threading
import time

import requests


# ---------- 1. Кастомный HTTP‑обработчик, отправляющий JSON на server.py ----------

class CentralizedHTTPHandler(logging.Handler):
    def __init__(self, host: str, url: str, method: str = "POST"):
        super().__init__()
        self.host = host
        self.url = url
        self.method = method.upper()

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        return {
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "created": record.created,
            "service": record.name,
        }

    def emit(self, record):
        try:
            data = self.mapLogRecord(record)
            full_url = f"http://{self.host}{self.url}"
            requests.post(full_url, json=data, timeout=2)
        except Exception:
            self.handleError(record)


# ---------- 2. dict‑конфиг логирования ----------

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "central_server": {
            # Создаём наш кастомный handler через вызов конструктора
            "()": "__main__.CentralizedHTTPHandler",
            "host": "127.0.0.1:5000",
            "url": "/log",
            "method": "POST",
            "level": "DEBUG",
        },
    },
    "loggers": {
        # Приглушаем лишние логи внешних библиотек
        "urllib3": {"level": "WARNING"},
        "werkzeug": {"level": "WARNING"},
    },
    "root": {
        "handlers": ["stdout", "central_server"],
        "level": "DEBUG",
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


# ---------- 3. Имитация работы нескольких сервисов ----------

def simulate_services():
    """
    Пишем несколько логов от разных "сервисов".
    Они уйдут и в stdout, и на server.py → logs.jsonl.
    """
    service_a = logging.getLogger("Service_Alpha")
    service_b = logging.getLogger("Service_Beta")

    print("--- Имитация отправки логов ---")
    service_a.info("Alpha: system start-up sequence initiated.")
    service_a.error("Alpha: connection lost to database node 2.")
    service_b.warning("Beta: high memory usage detected.")
    service_b.debug(
        "Beta: this DEBUG не уйдёт в stdout (level INFO), "
        "но уйдёт на центральный сервер."
    )


if __name__ == "__main__":
    # Настраиваем логирование
    setup_logging()

    # Даём немного времени, чтобы ты успел запустить server.py
    time.sleep(1)

    simulate_services()

    # Небольшая пауза, чтобы HTTP‑запросы успели уйти
    time.sleep(1)

    print(
        "\nЛоги отправлены на центральный сервер."
        "\nОткрой http://127.0.0.1:5000/logs, чтобы их посмотреть."
    )