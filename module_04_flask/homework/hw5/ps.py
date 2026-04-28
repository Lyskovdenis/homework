"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    # Считываем все параметры ?arg=...
    args = request.args.getlist("arg")  # /ps?arg=a&arg=u&arg=x -> ["a", "u", "x"]

    # Формируем команду: ["ps", "a", "u", "x"]
    cmd = ["ps"] + args

    # Запускаем ps с указанными аргументами
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )

    # Возвращаем stdout команды ps
    return result.stdout


if __name__ == "__main__":
    app.run(debug=True)