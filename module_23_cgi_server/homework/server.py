from wsgiref.simple_server import make_server
from routes import app  # твоё WSGI-приложение

if __name__ == "__main__":
    with make_server("127.0.0.1", 8000, app) as server:
        print("Serving WSGI app on http://127.0.0.1:8000 ...")
        server.serve_forever()