import logging
from logging_config import configure_logging
from utils import string_to_operator

logger = logging.getLogger(__name__)


def calc(args):
    logger.info("Arguments: %r", args)

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1", exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2", exc_info=e)

    operator_func = string_to_operator(operator)
    result = operator_func(num_1, num_2)

    logger.info("Result: %s", result)
    logger.info("%s %s %s = %s", num_1, operator, num_2, result)


if __name__ == "__main__":
    configure_logging()
    calc(['2', '+', '3'])