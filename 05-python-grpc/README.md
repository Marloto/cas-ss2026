# Telemetry – gRPC

Fahrzeug-Telemetrie über gRPC mit zwei RPC-Typen:

| RPC | Typ | Beschreibung |
|-----|-----|--------------|
| `SendReading` | Unary | Client sendet einen Messwert, Server antwortet mit Ack |
| `StreamReadings` | Server-Streaming | Server pusht kontinuierlich Messwerte |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Stubs generieren

Aus der `.proto`-Datei werden zwei Python-Dateien erzeugt:

```bash
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    telemetry.proto
```

Erzeugt: `telemetry_pb2.py` (Messages) und `telemetry_pb2_grpc.py` (Service-Stubs).

## Starten

```bash
# Terminal 1
python server.py

# Terminal 2
python client.py
```

## Protokoll (telemetry.proto)

```
TelemetryService
  ├── SendReading(TelemetryReading) → Ack          # Unary
  └── StreamReadings(StreamRequest) → stream ...   # Server-Streaming
```

## Vergleich REST / WebSocket / gRPC

| Kriterium        | REST (02)        | WebSocket (04)       | gRPC (05)               |
|------------------|------------------|----------------------|-------------------------|
| Transport        | HTTP/1.1         | TCP (WS-Framing)     | HTTP/2                  |
| Schema           | keins (JSON)     | keins (JSON)         | Protobuf (`.proto`)     |
| Typsicherheit    | —                | —                    | stark typisiert         |
| Streaming        | —                | bidirektional        | uni- & bidirektional    |
| Code-Generierung | —                | —                    | ja (Stubs)              |
| Einsatz          | Public APIs      | Live-UIs, Chat       | Microservices, intern   |
