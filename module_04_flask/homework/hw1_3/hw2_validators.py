"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""

from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Валидатор-декоратор для проверки длины числа в IntegerField.

    Использование:
        phone = IntegerField(validators=[InputRequired(), number_length(10, 10)])
    """

    if message is None:
        if min == max:
            default_message = f"Длина числа должна быть ровно {min} символов"
        else:
            default_message = f"Длина числа должна быть от {min} до {max} символов"
    else:
        default_message = message

    def _number_length(form: FlaskForm, field: Field):
        data = field.data

        # Если поле пустое — пусть решает другой валидатор (DataRequired/InputRequired)
        if data is None:
            return

        # Преобразуем в строку, считаем длину
        s = str(data)
        length = len(s)

        if length < min or length > max:
            raise ValidationError(default_message)

    return _number_length


class NumberLength:
    """
    Класс-валидатор для проверки длины числа в IntegerField.

    Использование:
        phone = IntegerField(validators=[InputRequired(), NumberLength(10, 10)])
    """

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        if message is None:
            if min == max:
                self.message = f"Длина числа должна быть ровно {min} символов"
            else:
                self.message = f"Длина числа должна быть от {min} до {max} символов"
        else:
            self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        data = field.data

        if data is None:
            return

        s = str(data)
        length = len(s)

        if length < self.min or length > self.max:
            raise ValidationError(self.message)

