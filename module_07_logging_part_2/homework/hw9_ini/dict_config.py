import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
    },

    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": "ext://sys.stdout",
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "filename": "logfile.log",
        },
    },

    "loggers": {
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False,
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["consoleHandler"],
    },
}


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)

    logger = logging.getLogger("appLogger")

    logger.debug("Debug message (only в файл).")
    logger.info("Info message (тоже только в файл).")
    logger.warning("Warning message (в файл и в консоль).")
    logger.error("Error message (в файл и в консоль).")