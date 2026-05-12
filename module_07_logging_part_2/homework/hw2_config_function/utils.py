from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging

logger = logging.getLogger(__name__)  # имя логгера = "utils" [web:372]

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic operator as string
    """
    if not isinstance(value, str):
        logger.error("Wrong operator type: %r (%s)", value, type(value))
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error("Wrong operator value: %r", value)
        raise ValueError("wrong operator value")

    logger.debug("Operator %r mapped to %r", value, OPERATORS[value])
    return OPERATORS[value]