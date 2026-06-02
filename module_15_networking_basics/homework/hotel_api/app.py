from flask import Flask, jsonify, request
from .database import init_db
from .business_logic import add_room_service, get_rooms_service, booking_room_service

app = Flask(__name__)

init_db()


@app.route('/room')
def get_rooms():
    rooms = get_rooms_service()
    available_rooms = [room for room in rooms if not room.booked]

    rooms_data = [
        {
            "roomId": room.room_id,
            "floor": room.floor,
            "guestNum": room.guest_num,
            "beds": room.beds,
            "price": room.price
        }
        for room in available_rooms
    ]
    return jsonify({"rooms": rooms_data}), 200


@app.route('/add-room', methods=['POST'])
def add_room():
    data = request.get_json() or {}
    floor = data.get("floor", 1)
    guest_num = data.get("guestNum", 1)
    beds = data.get("beds", 1)
    price = data.get("price", 1000)

    add_room_service(floor=floor, guest_num=guest_num, beds=beds, price=price)

    rooms = get_rooms_service()
    rooms_data = [
        {
            "roomId": r.room_id,
            "floor": r.floor,
            "guestNum": r.guest_num,
            "beds": r.beds,
            "price": r.price
        }
        for r in rooms if not r.booked
    ]
    return jsonify({"rooms": rooms_data}), 200


@app.route('/booking', methods=['POST'])
def booking():
    data = request.get_json() or {}
    room_id = data.get("roomId")

    if room_id is None:
        return jsonify({"error": "roomId required"}), 400

    success, status_code = booking_room_service(room_id)

    if success:
        return jsonify({"message": "Room booked successfully"}), 200
    else:
        return jsonify({"error": "Room already booked"}), status_code