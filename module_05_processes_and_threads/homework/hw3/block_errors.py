"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection[Type[BaseException]]) -> None:
        # Сохраняем типы ошибок как кортеж для issubclass
        self._errors: tuple[Type[BaseException], ...] = tuple(errors)

    def __enter__(self) -> None:
        # Ничего возвращать не нужно, менеджер сам по себе не используется
        return None

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[True] | None:
        # Если исключения не было — ничего не подавляем
        if exc_type is None:
            return None

        # Если тип исключения — подкласс одного из переданных, подавляем его
        if issubclass(exc_type, self._errors):
            return True  # вернуть True → сообщить интерпретатору, что исключение обработано

        # Неожиданный тип — не подавляем, исключение уйдёт выше
        return None