# Telemetry API

Einfache REST-API zum Empfangen und Speichern von Fahrzeug-Telemetriedaten.
Storage-Schicht ist austauschbar: Datei → SQLite → Google Cloud SQL.

## Starten

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Routen

```
GET  /                        → Service-Info
GET  /health                  → {"status": "ok"}
POST /telemetry               → Eintrag speichern
GET  /telemetry               → alle Einträge
GET  /telemetry/<vehicle_id>  → Einträge für ein Fahrzeug
GET  /telemetry?vehicle_id=.. → alternativ als Query-Parameter
```

## Testen

```bash
# Telemetrie senden
curl -X POST http://localhost:8000/telemetry \
     -H "Content-Type: application/json" \
     -d '{"vehicle_id": "VH-001", "sensor": "engine_temp", "value": 87.3, "unit": "°C"}'

curl -X POST http://localhost:8000/telemetry \
     -H "Content-Type: application/json" \
     -d '{"vehicle_id": "VH-001", "sensor": "speed", "value": 112.0, "unit": "km/h"}'

curl -X POST http://localhost:8000/telemetry \
     -H "Content-Type: application/json" \
     -d '{"vehicle_id": "VH-002", "sensor": "battery_voltage", "value": 12.4, "unit": "V"}'

# Abfragen
curl http://localhost:8000/telemetry
curl http://localhost:8000/telemetry/VH-001
```

## Storage-Phasen

In `storage.py` ganz unten die aktive Implementierung wechseln:

| Phase | Implementierung | Zeile in storage.py |
|---|---|---|
| 1 | Datei (`data.json`) | `storage = FileStorage()` |
| 2 | SQLite (`data.db`) | `storage = SQLiteStorage()` |
| 3 | Google Cloud SQL | `storage = CloudSQLStorage()` |
