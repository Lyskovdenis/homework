import json
import re
import time
from typing import Callable, Any


class WSGIApp:
    """
    WSGI-приложение с поддержкой декоратора @route,
    аналогично Flask, но в минимальном виде.
    """

    def __init__(self):
        # Список зарегистрированных маршрутов:
        # (compiled_regex, param_names, handler)
        self._routes: list[tuple[re.Pattern[str], list[str], Callable[..., Any]]] = []

    def route(self, pattern: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Декоратор для регистрации маршрута.
        Поддерживает простые шаблоны вида "/hello" и "/hello/<name>".
        """

        # Преобразуем шаблон "/hello/<name>" в регулярное выражение:
        # - <name> -> захватывающая группа вида (?P<name>[^/]+)
        param_names: list[str] = []

        def _convert_pattern_to_regex(p: str) -> re.Pattern[str]:
            parts = p.strip("/").split("/")
            regex_parts: list[str] = []
            for part in parts:
                if part.startswith("<") and part.endswith(">"):
                    param_name = part[1:-1]
                    param_names.append(param_name)
                    # одна часть пути, без "/"
                    regex_parts.append(f"(?P<{param_name}>[^/]+)")
                else:
                    # обычный сегмент URL
                    regex_parts.append(re.escape(part))
            regex = "^/" + "/".join(regex_parts) + "$"
            return re.compile(regex)

        compiled = _convert_pattern_to_regex(pattern)

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # Регистрируем маршрут
            self._routes.append((compiled, param_names.copy(), func))
            return func

        return decorator

    def __call__(self, environ: dict, start_response: Callable) -> list[bytes]:
        """
        Реализация WSGI-интерфейса:
        - environ: данные о запросе (в том числе REQUEST_URI / PATH_INFO)
        - start_response: функция для отправки статуса и заголовков
        Возвращает итератор (список байтов) с телом ответа.
        """
        # Cервер может положить путь в PATH_INFO
        path = environ.get("PATH_INFO") or environ.get("REQUEST_URI") or "/"

        # Пытаемся найти подходящий маршрут
        for regex, param_names, handler in self._routes:
            match = regex.match(path)
            if match:
                # Есть совпадение: вытаскиваем именованные параметры
                kwargs = {name: match.group(name) for name in param_names}
                try:
                    payload = handler(**kwargs)
                    body = json.dumps(payload, indent=4)
                    status = "200 OK"
                except Exception as exc:
                    # На всякий случай отлавливаем ошибки в обработчиках
                    body = json.dumps(
                        {"error": "Internal Server Error", "details": str(exc)},
                        indent=4,
                    )
                    status = "500 Internal Server Error"

                headers = [
                    ("Content-Type", "application/json; charset=utf-8"),
                    ("Content-Length", str(len(body.encode("utf-8")))),
                ]
                start_response(status, headers)
                return [body.encode("utf-8")]

        # Если ни один маршрут не подошёл — 404
        body = json.dumps({"error": "Not found"}, indent=4)
        status = "404 Not Found"
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body.encode("utf-8")))),
        ]
        start_response(status, headers)
        return [body.encode("utf-8")]


# Создаём экземпляр приложения — WSGI-приложение
app = WSGIApp()


# Декларативно объявляем эндпоинты, как во Flask

@app.route("/hello")
def say_hello() -> dict:
    return {"response": "Hello, world!"}


@app.route("/hello/<name>")
def say_hello_with_name(name: str) -> dict:
    return {"response": f"Hello, {name}!"}


@app.route("/long_task")
def long_task() -> dict:
    time.sleep(300)
    return {"message": "We did it!"}