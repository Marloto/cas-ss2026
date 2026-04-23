import asyncio
import json
import websockets


async def main() -> None:
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        print(f"Connected to {uri}")
        async for message in ws:
            data = json.loads(message)
            print(f"[{data['timestamp']}] {data['vehicle_id']} "
                  f"{data['sensor']}: {data['value']} {data['unit']}")


if __name__ == "__main__":
    asyncio.run(main())
