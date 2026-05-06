from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from storage import storage

app = Flask(__name__)
CORS(app)

# Datenaustauschformate?
# -> JSON, wie sieht es aus?
# -> XML
# -> Plaintext
# -> YAML
# -> 
# Beispiel JSON
# - Key-Values für die Werte, z.B. "foo": 123
# - Objects als eine Hauptstruktur mit {...}, 
#   können auch nested sein
# - Arrays / Listen als zweite Hauptstruktur mit [...]
# z.B.: [1,2,3], {"foo": 123}, [{"foo": 123}], {"bar": {"foo": 123}}
# - wenn man z.B. Positionsdaten abbildet:
#   {"longitute": 12.234, "latitude": 42.123}
#   Übertragen bzw. Dargestellt als String
#   zzgl. Overhead für Attribute, Strukturen usw.
# - Protocol Buffer (Google, gRPC)
@app.route("/")
def index():
    return jsonify({
        "service": "Telemetry API",
        "endpoints": [
            "GET /health", 
            "POST /telemetry", 
            "GET /telemetry", 
            "GET /telemetry/<vehicle_id>"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/telemetry", methods=["POST"])
def ingest():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON-Body erforderlich"}), 400

    required = {"vehicle_id", "sensor", "value"}
    missing = required - data.keys()
    if missing:
        return jsonify({"error": f"Fehlende Felder: {', '.join(missing)}"}), 400

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vehicle_id": data["vehicle_id"],
        "sensor":     data["sensor"],
        "value":      data["value"],
        "unit":       data.get("unit"),
    }
    saved = storage.add(entry)
    return jsonify(saved), 201


@app.route("/telemetry", methods=["GET"])
def list_all():
    vehicle_id = request.args.get("vehicle_id")
    return jsonify(storage.all(vehicle_id=vehicle_id))


@app.route("/telemetry/<vehicle_id>", methods=["GET"])
def list_by_vehicle(vehicle_id):
    return jsonify(storage.all(vehicle_id=vehicle_id))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=8000)
