import factory
from faker import Faker
from extensions import db
from models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyFunction(lambda: None if fake.boolean() else fake.credit_card_number())
    car_number = factory.Faker("bothify", text="??###??")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=1, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: fake.random_int(min=0, max=obj.count_places))