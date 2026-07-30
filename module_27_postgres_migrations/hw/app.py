import random

import requests
from flask import Flask, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import scoped_session

from database import Base, SessionLocal, engine
from models import Coffee, User

app = Flask(__name__)
db = scoped_session(SessionLocal)
seeded = False


def seed_data():
    global seeded
    if seeded:
        return

    Base.metadata.create_all(bind=engine)

    coffee_exists = db.query(Coffee).first()
    user_exists = db.query(User).first()
    if coffee_exists or user_exists:
        seeded = True
        return

    coffee_resp = requests.get("https://dummyjson.com/products/search?q=coffee", timeout=10)
    coffee_resp.raise_for_status()
    coffee_data = coffee_resp.json()["products"][0]

    coffee = Coffee(
        title=coffee_data["title"],
        category=coffee_data.get("category"),
        description=coffee_data.get("description"),
        reviews=[review["comment"] for review in coffee_data.get("reviews", []) if review.get("comment")],
    )
    db.add(coffee)
    db.flush()

    users_resp = requests.get("https://dummyjson.com/users", timeout=10)
    users_resp.raise_for_status()
    users_data = users_resp.json()["users"]

    for _ in range(10):
        u = random.choice(users_data)
        user = User(
            name=u.get("firstName", "Unknown"),
            has_sale=random.choice([True, False]),
            address=u.get("address", {}),
            coffee_id=coffee.id,
        )
        db.add(user)

    db.commit()
    seeded = True


@app.route("/users", methods=["POST"])
def add_user():
    coffee = db.query(Coffee).order_by(func.random()).first()
    if coffee is None:
        return jsonify({"error": "No coffee found"}), 404

    data = request.get_json(silent=True) or {}
    user = User(
        name=data.get("name", "New User"),
        has_sale=data.get("has_sale", False),
        address=data.get("address", {"country": "Unknown"}),
        coffee_id=coffee.id,
    )
    db.add(user)
    db.commit()

    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "has_sale": user.has_sale,
            "address": user.address,
            "coffee": {
                "id": coffee.id,
                "title": coffee.title,
                "category": coffee.category,
                "description": coffee.description,
                "reviews": coffee.reviews,
            },
        }
    ), 201


@app.route("/coffee/search", methods=["GET"])
def search_coffee():
    title = request.args.get("title", "").strip()

    if not title:
        return jsonify([])

    results = (
        db.query(Coffee)
        .filter(
            func.to_tsvector("english", Coffee.title).op("@@")(
                func.plainto_tsquery("english", title)
            )
        )
        .all()
    )

    return jsonify(
        [
            {
                "id": c.id,
                "title": c.title,
                "category": c.category,
                "description": c.description,
                "reviews": c.reviews,
            }
            for c in results
        ]
    )


@app.route("/coffee/reviews/unique", methods=["GET"])
def unique_reviews():
    rows = db.query(Coffee.reviews).all()
    unique = set()

    for (reviews,) in rows:
        if reviews:
            unique.update(reviews)

    return jsonify(sorted(unique))


@app.route("/users/by-country", methods=["GET"])
def users_by_country():
    country = request.args.get("country", "").strip()
    if not country:
        return jsonify([])

    users = db.query(User).filter(User.address["country"].as_string() == country).all()
    return jsonify(
        [
            {
                "id": u.id,
                "name": u.name,
                "has_sale": u.has_sale,
                "address": u.address,
                "coffee_id": u.coffee_id,
            }
            for u in users
        ]
    )


def init_app():
    seed_data()


init_app()