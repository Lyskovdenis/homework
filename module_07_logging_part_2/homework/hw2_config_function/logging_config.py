import logging
import sys


def configure_logging(level=logging.DEBUG):
    fmt = "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"

    logging.basicConfig(
        level=level,
        stream=sys.stdout,          # stdout, как требует задание
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
    )