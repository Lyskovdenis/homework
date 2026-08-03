from flask import Flask
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from module_29_testing.hw.hw1.models import Client, Parking, ClientParking  # noqa: F401

    return app