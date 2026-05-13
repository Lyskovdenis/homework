import logging
import logging.config
import logging.handlers
import sys
from pathlib import Path


# --- Класс фильтра ---
class ASCIIFilter(logging.Filter):
    """Фильтр, пропускающий только сообщения, состоящие из ASCII-символов."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().isascii()


# --- Конфигурация логирования ---
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(levelname)s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "filters": {
        "ascii_only": {
            "()": "__main__.ASCIIFilter"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
            "filters": ["ascii_only"]
        },
        "level_file_handler": {
            "()": "__main__.LevelFileHandler",
            "base_name": "calc",
            "level": "DEBUG",
            "formatter": "standard",
            "filters": ["ascii_only"]
        }
    },
    "root": {
        "handlers": ["stdout", "level_file_handler"],
        "level": "DEBUG"
    }
}


class LevelFileHandler(logging.Handler):
    def __init__(self, base_name: str = "calc"):
        super().__init__()
        self.base_name = base_name
        self._handlers: dict[int, logging.FileHandler] = {}

    def _get_handler_for_level(self, levelno: int) -> logging.FileHandler:
        if levelno in self._handlers: return self._handlers[levelno]
        level_name = logging.getLevelName(levelno).lower()
        filename = f"{self.base_name}_{level_name}.log"
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
        if self.formatter: fh.setFormatter(self.formatter)
        self._handlers[levelno] = fh
        return fh

    def emit(self, record: logging.LogRecord) -> None:
        try:
            handler = self._get_handler_for_level(record.levelno)
            handler.emit(record)
        except Exception:
            self.handleError(record)

    def setFormatter(self, fmt: logging.Formatter) -> None:
        super().setFormatter(fmt)
        for h in self._handlers.values(): h.setFormatter(fmt)


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("test_logger")

    print("--- Тестирование ASCII фильтра ---")

    # Это сообщение должно пройти фильтр
    logger.info("This is a valid ASCII message.")

    # Эти сообщения содержат не-ASCII и должны быть отфильтрованы
    logger.info("Это сообщение содержит кириллицу и не должно появиться.")
    logger.warning("Special symbols: ÎŒØ∏‡°⁄·°€")

    # Это сообщение снова должно пройти
    logger.error("Error 404: Access denied.")

    print("\nПроверьте консоль выше: должны отобразиться только английские сообщения.")