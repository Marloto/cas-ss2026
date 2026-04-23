import asyncio
import json
import random
import time
import websockets
from websockets.server import WebSocketServerProtocol

CLIENTS: set[WebSocketServerProtocol] = set()

VEHICLES = ["VH-001", "VH-002", "VH-003"]
SENSORS = {
    "engine_temp": (70.0, 110.0, "°C"),
    "speed":       (0.0,  180.0, "km/h"),
    "battery":     (11.8,  14.4, "V"),
    "rpm":         (700.0, 6500.0, "rpm"),
}


def generate_reading() -> dict:
    sensor, (lo, hi, unit) = random.choice(list(SENSORS.items()))
    return {
        "vehicle_id": random.choice(VEHICLES),
        "sensor":     sensor,
        "value":      round(random.uniform(lo, hi), 1),
        "unit":       unit,
        "timestamp":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


async def broadcast(message: str) -> None:
    if CLIENTS:
        await asyncio.gather(*[c.send(message) for c in CLIENTS])


async def producer() -> None:
    while True:
        await asyncio.sleep(1)
        reading = generate_reading()
        await broadcast(json.dumps(reading))


async def handler(ws: WebSocketServerProtocol) -> None:
    CLIENTS.add(ws)
    print(f"+ client connected  ({len(CLIENTS)} total)")
    try:
        async for message in ws:
            try:
                cmd = json.loads(message)
                if cmd.get("action") == "ping":
                    await ws.send(json.dumps({"action": "pong"}))
            except json.JSONDecodeError:
                pass
    finally:
        CLIENTS.discard(ws)
        print(f"- client disconnected ({len(CLIENTS)} total)")


async def main() -> None:
    asyncio.create_task(producer())
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.get_event_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
