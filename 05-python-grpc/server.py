import random
import time
import uuid
from concurrent import futures

import grpc
import telemetry_pb2
import telemetry_pb2_grpc

VEHICLES = ["VH-001", "VH-002", "VH-003"]
SENSORS = {
    "engine_temp": (70.0, 110.0, "°C"),
    "speed":       (0.0,  180.0, "km/h"),
    "battery":     (11.8,  14.4, "V"),
    "rpm":         (700.0, 6500.0, "rpm"),
}


def _random_reading(vehicle_id: str = "") -> telemetry_pb2.TelemetryReading:
    sensor, (lo, hi, unit) = random.choice(list(SENSORS.items()))
    return telemetry_pb2.TelemetryReading(
        vehicle_id=vehicle_id or random.choice(VEHICLES),
        sensor=sensor,
        value=round(random.uniform(lo, hi), 1),
        unit=unit,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


class TelemetryServicer(telemetry_pb2_grpc.TelemetryServiceServicer):

    def SendReading(self, request, context):
        print(f"  recv  {request.vehicle_id}  {request.sensor}={request.value}{request.unit}")
        return telemetry_pb2.Ack(ok=True, id=str(uuid.uuid4()))

    def StreamReadings(self, request, context):
        vehicle_filter = request.vehicle_id
        print(f"  stream start  filter='{vehicle_filter or 'all'}'")
        try:
            while context.is_active():
                reading = _random_reading(vehicle_filter)
                yield reading
                time.sleep(1)
        finally:
            print("  stream end")


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    telemetry_pb2_grpc.add_TelemetryServiceServicer_to_server(TelemetryServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
