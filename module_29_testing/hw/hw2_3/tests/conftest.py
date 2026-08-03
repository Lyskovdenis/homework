import pytest
from app import create_app
from extensions import db
from models import Client, Parking, ClientParking


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        client1 = Client(
            name="Ivan",
            surname="Petrov",
            credit_card="1111-2222-3333-4444",
            car_number="A123BC77",
        )
        parking1 = Parking(
            address="Lenina 10",
            opened=True,
            count_places=10,
            count_available_places=10,
        )

        client2 = Client(
            name="Petr",
            surname="Sidorov",
            credit_card="5555-6666-7777-8888",
            car_number="B777BB77",
        )
        parking2 = Parking(
            address="Tverskaya 1",
            opened=True,
            count_places=5,
            count_available_places=5,
        )

        db.session.add_all([client1, parking1, client2, parking2])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db