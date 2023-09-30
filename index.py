import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data (replace with a database in a real implementation)
with open("doctors.json", "r") as file:
    doctors = json.load(file)
appointments = []


# Landing Page
@app.route("/")
def ld():
    return "Welcome to Out-Patient slot booking!!"


# List Doctors
@app.route("/doctors", methods=["GET"])
def list_doctors():
    return jsonify(doctors)


# Doctor Detail
@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def doctor_detail(doctor_id):
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if doctor:
        return jsonify(doctor)
    return jsonify({"message": "Doctor not found"}), 404


# Appointment Booking
@app.route("/appointments", methods=["POST", "GET"])
def book_appointment():
    if request.method == "POST":
        data = request.json
        doctor_id = data.get("doctor_id")
        week_day = data.get("week_day")
        appointment_time = data.get("appointment_time")

        doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
        if not doctor:
            return jsonify({"message": "Doctor not found"}), 404

        for slot in doctor["available_slots"]:
            if (
                slot["week_day"] == week_day
                and slot["time"] == appointment_time
                and slot["available_patients"] < slot["max_patients"]
            ):
                slot["available_patients"] -= 1
                appointment = {
                    "doctor_id": doctor_id,
                    "week_day": week_day,
                    "appointment_time": appointment_time,
                    "status": "confirmed",
                }
                appointments.append(appointment)
                return jsonify(appointment), 201

        return jsonify({"message": "Appointment slot not available"}), 400
    else:
        return jsonify(appointments)


if __name__ == "__main__":
    app.run(debug=True)
