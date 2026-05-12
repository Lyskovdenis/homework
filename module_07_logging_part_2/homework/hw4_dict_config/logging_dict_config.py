import logging
import logging.config
import sys
from pathlib import Path

# --- Эмуляция отдельного файла конфигурации logging_config.py ---
# В реальном проекте это должен быть отдельный .py файл
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "level_file_handler": {
            "()": "__main__.LevelFileHandler",
            "base_name": "calc",
            "level": "DEBUG",
            "formatter": "standard"
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "level_file_handler"],
            "level": "DEBUG",
            "propagate": False
        },
    }
}
# -----------------------------------------------------------

class LevelFileHandler(logging.Handler):
    """
    Пишет логи в разные файлы в зависимости от уровня.
    """
    def __init__(self, base_name: str = "calc"):
        super().__init__()
        self.base_name = base_name
        self._handlers: dict[int, logging.FileHandler] = {}

    def _get_handler_for_level(self, levelno: int) -> logging.FileHandler:
        if levelno in self._handlers:
            return self._handlers[levelno]

        level_name = logging.getLevelName(levelno).lower()
        filename = f"{self.base_name}_{level_name}.log"
        path = Path(filename)

        fh = logging.FileHandler(path, mode="a", encoding="utf-8")
        if self.formatter is not None:
            fh.setFormatter(self.formatter)

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
        for h in self._handlers.values():
            h.setFormatter(fmt)


def get_logger(name: str) -> logging.Logger:
    # Применяем декларативную конфигурацию
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)

    logger.debug("debug message")
    logger.info("info message")
    logger.error("error message")