import pytest

from extensions import db
from factories import ClientFactory, ParkingFactory
from models import Client, Parking


@pytest.mark.parametrize(
    "method,url",
    [
        ("get", "/clients"),
        ("get", "/clients/1"),
    ],
)
def test_get_methods_return_200(client, method, url):
    response = getattr(client, method)(url)
    assert response.status_code == 200


def test_create_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "Sergey",
            "surname": "Ivanov",
            "credit_card": "9999-8888-7777-6666",
            "car_number": "C999CC77",
        },
    )
    assert response.status_code == 201
    assert response.json["name"] == "Sergey"
    assert response.json["surname"] == "Ivanov"


def test_create_parking(client):
    response = client.post(
        "/parkings",
        json={
            "address": "Arbat 15",
            "opened": True,
            "count_places": 20,
            "count_available_places": 20,
        },
    )
    assert response.status_code == 201
    assert response.json["address"] == "Arbat 15"


@pytest.mark.parking
def test_enter_parking(client, app):
    with app.app_context():
        client_obj = Client.query.filter_by(id=1).first()
        parking_obj = Parking.query.filter_by(id=2).first()

    response = client.post(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    assert response.status_code == 201

    with app.app_context():
        updated_parking = Parking.query.get(parking_obj.id)
        assert updated_parking.count_available_places == 4


@pytest.mark.parking
def test_exit_parking(client, app):
    with app.app_context():
        client_obj = Client.query.filter_by(id=2).first()
        parking_obj = Parking.query.filter_by(id=1).first()

    enter = client.post(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    assert enter.status_code == 201

    response = client.delete(
        "/client_parkings",
        json={"client_id": client_obj.id, "parking_id": parking_obj.id},
    )
    assert response.status_code == 200

    with app.app_context():
        updated_parking = Parking.query.get(parking_obj.id)
        assert updated_parking.count_available_places == 10


def test_enter_closed_parking(client, app):
    with app.app_context():
        parking_obj = Parking.query.filter_by(id=1).first()
        parking_obj.opened = False
        db.session.commit()

    response = client.post(
        "/client_parkings",
        json={"client_id": 1, "parking_id": 1},
    )
    assert response.status_code == 400


def test_create_client_factory(client, app):
    with app.app_context():
        before = Client.query.count()
        obj = ClientFactory()
        payload = {
            "name": obj.name,
            "surname": obj.surname,
            "credit_card": obj.credit_card,
            "car_number": obj.car_number,
        }

    response = client.post("/clients", json=payload)
    assert response.status_code == 201

    with app.app_context():
        after = Client.query.count()
        assert after == before + 1


def test_create_parking_factory(client, app):
    with app.app_context():
        before = Parking.query.count()
        obj = ParkingFactory()
        payload = {
            "address": obj.address,
            "opened": obj.opened,
            "count_places": obj.count_places,
            "count_available_places": obj.count_available_places,
        }

    response = client.post("/parkings", json=payload)
    assert response.status_code == 201

    with app.app_context():
        after = Parking.query.count()
        assert after == before + 1
