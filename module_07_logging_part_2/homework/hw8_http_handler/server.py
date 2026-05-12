# server.py
import json
from flask import Flask, request, Response

app = Flask(__name__)

LOG_FILE = "logs.jsonl"  # по строке JSON на лог


@app.route('/log', methods=['POST'])
def log():
    """
    Принимаем лог и записываем его в файл.
    Ожидаем JSON в теле запроса.
    """
    data = request.get_json(silent=True)
    if data is None:
        return Response("Bad JSON or missing Content-Type: application/json", status=400)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.write("\n")

    return Response("Log saved", status=201)


@app.route('/logs', methods=['GET'])
def logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    content = "".join(lines) if lines else "No logs yet"
    html = f"<pre>{content}</pre>"
    return Response(html, status=200, mimetype="text/html")


if __name__ == '__main__':
    app.run(debug=True)