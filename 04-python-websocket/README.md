# Live Telemetry – WebSocket

Echtzeit-Streaming von Fahrzeug-Telemetriedaten über WebSockets.  
Der Server pusht jede Sekunde einen zufälligen Sensorwert an alle verbundenen Clients.

## Starten

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

## Clients

**Python-Client** (Terminal):
```bash
python client.py
```

**Browser-Client**: `client.html` direkt im Browser öffnen, dann auf *Verbinden* klicken.

## Architektur

```
server.py
  ├── producer()   – erzeugt jede Sekunde einen Telemetrie-Eintrag
  ├── broadcast()  – sendet an alle verbundenen WebSocket-Clients
  └── handler()    – verwaltet einzelne Client-Verbindungen
```

## Protokoll

Server → Client (JSON, 1×/s):
```json
{
  "vehicle_id": "VH-001",
  "sensor":     "engine_temp",
  "value":      87.3,
  "unit":       "°C",
  "timestamp":  "2026-04-21T10:00:00Z"
}
```

Client → Server (optional):
```json
{ "action": "ping" }
```

Server antwortet mit `{ "action": "pong" }`.

## Vergleich REST vs. WebSocket

| Kriterium        | REST (02)          | WebSocket (03)       |
|------------------|--------------------|----------------------|
| Verbindung       | kurzlebig, stateless | persistent, stateful |
| Datenfluss       | Request → Response | bidirektional        |
| Push vom Server  | nicht möglich      | nativ                |
| Overhead         | HTTP-Header je Request | einmaliger Handshake |
| Einsatz          | CRUD, Abfragen     | Live-Daten, Chat     |
