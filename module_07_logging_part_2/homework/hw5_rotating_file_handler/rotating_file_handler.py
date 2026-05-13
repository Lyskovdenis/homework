import logging
import logging.config
import logging.handlers
import sys
from pathlib import Path

# --- Эмуляция файла конфигурации ---
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
        "utils_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": "utils.log",
            "when": "h",
            "interval": 1,
            "backupCount": 10,
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "utils": {
            "handlers": ["utils_handler"],
            "level": "INFO",
            "propagate": False
        },
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
        if levelno in self._handlers:
            return self._handlers[levelno]
        level_name = logging.getLevelName(levelno).lower()
        filename = f"{self.base_name}_{level_name}.log"
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
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
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)

if __name__ == "__main__":
    # Логгер для расчетов (root)
    calc_logger = get_logger("calc_app")
    calc_logger.debug("Этот дебаг попадет в консоль и calc_debug.log")

    # Логгер utils
    utils_logger = logging.getLogger("utils")
    utils_logger.info("Это сообщение INFO для utils.log")
    utils_logger.debug("Это сообщение DEBUG не попадет в utils.log (уровень INFO)")
    utils_logger.error("Это сообщение ERROR для utils.log")