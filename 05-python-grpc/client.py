import time
import grpc
import telemetry_pb2
import telemetry_pb2_grpc


def send_reading(stub: telemetry_pb2_grpc.TelemetryServiceStub) -> None:
    reading = telemetry_pb2.TelemetryReading(
        vehicle_id="VH-001",
        sensor="engine_temp",
        value=87.3,
        unit="°C",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )
    ack = stub.SendReading(reading)
    print(f"SendReading  →  ok={ack.ok}  id={ack.id}")


def stream_readings(stub: telemetry_pb2_grpc.TelemetryServiceStub, vehicle_id: str = "") -> None:
    req = telemetry_pb2.StreamRequest(vehicle_id=vehicle_id)
    print(f"StreamReadings (filter='{vehicle_id or 'all'}')  — Ctrl-C zum Beenden")
    for reading in stub.StreamReadings(req):
        print(f"  [{reading.timestamp}]  {reading.vehicle_id}  "
              f"{reading.sensor}: {reading.value} {reading.unit}")


def main() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = telemetry_pb2_grpc.TelemetryServiceStub(channel)

        send_reading(stub)
        print()
        stream_readings(stub, vehicle_id="VH-001")


if __name__ == "__main__":
    main()
