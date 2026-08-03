from datetime import datetime
from flask import Flask, jsonify, request
from extensions import db
from models import Client, Parking, ClientParking


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.get("/clients")
    def get_clients():
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients]), 200

    @app.get("/clients/<int:client_id>")
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict()), 200

    @app.post("/clients")
    def create_client():
        data = request.get_json()
        client = Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201

    @app.post("/parkings")
    def create_parking():
        data = request.get_json()
        parking = Parking(
            address=data["address"],
            opened=data.get("opened", True),
            count_places=data["count_places"],
            count_available_places=data["count_available_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify(parking.to_dict()), 201

    @app.post("/client_parkings")
    def enter_parking():
        data = request.get_json()
        client = Client.query.get(data["client_id"])
        parking = Parking.query.get(data["parking_id"])

        if not client or not parking:
            return jsonify({"error": "Client or parking not found"}), 404

        if not parking.opened:
            return jsonify({"error": "Parking is closed"}), 400

        if parking.count_available_places <= 0:
            return jsonify({"error": "No available places"}), 400

        existing = ClientParking.query.filter_by(
            client_id=client.id,
            parking_id=parking.id,
            time_out=None
        ).first()
        if existing:
            return jsonify({"error": "Client already parked here"}), 400

        record = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.now(),
            time_out=None,
        )
        parking.count_available_places -= 1
        db.session.add(record)
        db.session.commit()

        return jsonify(record.to_dict()), 201

    @app.delete("/client_parkings")
    def exit_parking():
        data = request.get_json()
        client = Client.query.get(data["client_id"])
        parking = Parking.query.get(data["parking_id"])

        if not client or not parking:
            return jsonify({"error": "Client or parking not found"}), 404

        record = ClientParking.query.filter_by(
            client_id=client.id,
            parking_id=parking.id,
            time_out=None
        ).first()

        if not record:
            return jsonify({"error": "Parking record not found"}), 404

        if not client.credit_card:
            return jsonify({"error": "Client has no credit card"}), 400

        record.time_out = datetime.now()
        parking.count_available_places += 1

        db.session.commit()

        return jsonify({
            "message": "Payment successful",
            "parking_record": record.to_dict(),
        }), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)