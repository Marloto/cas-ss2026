# Telemetry Dashboard (Client)

Statisches Web-Frontend für die Telemetry API.
Kein Build-System, kein Framework — reines HTML + JS.

## Voraussetzungen

Telemetry API muss laufen (examples/02-python-webapp).

## Starten

```bash
python -m http.server 8001
```

Dann im Browser: <http://localhost:8001>

## Funktionen

- Tabelle aller Telemetrie-Einträge (automatische Aktualisierung alle 5s)
- Formular zum manuellen Senden eines Eintrags
- Simulation: sendet alle 2s zufällige Sensorwerte für `VH-SIM`

## Cloud-Deployment (später)

Statische Dateien lassen sich ohne Änderungen deployen:

```bash
# Google Cloud Storage (Public Bucket)
gcloud storage cp index.html gs://BUCKET_NAME/

# Cloud Run (mit nginx)
# Firebase Hosting
# AWS S3 + CloudFront
```

API-URL in `index.html` von `http://localhost:8000` auf die Cloud-Run-URL anpassen.
