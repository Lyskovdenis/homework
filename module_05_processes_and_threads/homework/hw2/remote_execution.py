"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
import subprocess

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"      # любой непустой ключ
app.config["WTF_CSRF_ENABLED"] = False       # отключаем CSRF для форм


class CodeForm(FlaskForm):
    code = StringField(
        "code",
        validators=[
            DataRequired(message="Code is required"),
            Length(min=1, max=10_000),
        ],
    )
    timeout = IntegerField(
        "timeout",
        validators=[
            DataRequired(message="Timeout is required"),
            NumberRange(min=1, max=30, message="Timeout must be between 1 and 30"),
        ],
    )


def run_python_code_in_subproccess(code: str, timeout: int):
    """
    Запускает код в отдельном процессе:
    prlimit --nproc=1:1 python -c "<code>"
    Возвращает (stdout, stderr, timed_out: bool).
    """
    # Ограничение ресурсов через prlimit и запуск python -c
    cmd = [
        "prlimit",
        "--nproc=1:1",
        "python",
        "-c",
        code,
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,  # Критично для безопасности: никакого shell=True
    )

    try:
        stdout, stderr = proc.communicate(timeout=timeout)  # секунд
        return stdout, stderr, False
    except subprocess.TimeoutExpired:
        # Не уложились по времени
        proc.kill()
        stdout, stderr = proc.communicate()
        return stdout, stderr, True


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if not form.validate_on_submit():
        # Некорректные данные формы
        return {"errors": form.errors}, 400

    code = form.code.data
    timeout = form.timeout.data

    stdout, stderr, timed_out = run_python_code_in_subproccess(code, timeout)

    if timed_out:
        # Сообщение о том, что не уложились в отведённое время
        return (
            f"Execution did not finish in {timeout} seconds.\n"
            f"Stdout:\n{stdout}\nStderr:\n{stderr}",
            408,
        )

    # Успешное выполнение
    # Для простоты вернём stdout+stderr в одном ответе
    return f"Stdout:\n{stdout}\nStderr:\n{stderr}", 200

if __name__ == '__main__':
    app.run(debug=True)
