"""
Storage-Schicht — austauschbar je nach Phase:

  Phase 1 (lokal):  FileStorage    — JSON auf die Festplatte
  Phase 2 (lokal):  SQLiteStorage  — relationale DB, kein Server nötig
  Phase 3 (Cloud):  CloudSQLStorage — Google Cloud SQL via Connector

Aktive Implementierung ganz unten wechseln: storage = ...
"""

import json
import os
import sqlite3


# ---------------------------------------------------------------------------
# Phase 1: Dateisystem
# ---------------------------------------------------------------------------

class FileStorage:
    def __init__(self, path="data.json"):
        self.path = path

    def all(self, vehicle_id=None):
        entries = self._load()
        if vehicle_id:
            entries = [e for e in entries if e.get("vehicle_id") == vehicle_id]
        return entries

    def add(self, entry):
        entries = self._load()
        entries.append(entry)
        with open(self.path, "w") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return entry

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return []


# ---------------------------------------------------------------------------
# Phase 2: SQLite
# ---------------------------------------------------------------------------

class SQLiteStorage:
    def __init__(self, db="data.db"):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                vehicle_id TEXT   NOT NULL,
                sensor    TEXT    NOT NULL,
                value     REAL    NOT NULL,
                unit      TEXT
            )
        """)
        self.conn.commit()

    def all(self, vehicle_id=None):
        if vehicle_id:
            rows = self.conn.execute(
                "SELECT id, timestamp, vehicle_id, sensor, value, unit "
                "FROM telemetry WHERE vehicle_id = ? ORDER BY timestamp DESC",
                (vehicle_id,)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, timestamp, vehicle_id, sensor, value, unit "
                "FROM telemetry ORDER BY timestamp DESC"
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def add(self, entry):
        self.conn.execute(
            "INSERT INTO telemetry (timestamp, vehicle_id, sensor, value, unit) "
            "VALUES (?, ?, ?, ?, ?)",
            (entry["timestamp"], entry["vehicle_id"],
             entry["sensor"], entry["value"], entry.get("unit"))
        )
        self.conn.commit()
        return entry

    def _row_to_dict(self, row):
        return {
            "id": row[0], "timestamp": row[1], "vehicle_id": row[2],
            "sensor": row[3], "value": row[4], "unit": row[5],
        }


# ---------------------------------------------------------------------------
# Phase 3: Google Cloud SQL  (Connector + SQLAlchemy)
# ---------------------------------------------------------------------------

# from google.cloud.sql.connector import Connector
# import sqlalchemy
#
# class CloudSQLStorage:
#     def __init__(self):
#         connector = Connector()
#         def getconn():
#             return connector.connect(
#                 "PROJECT:REGION:INSTANCE",
#                 "pg8000", user="...", password="...", db="telemetry"
#             )
#         self.engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
#         with self.engine.connect() as c:
#             c.execute(sqlalchemy.text("""
#                 CREATE TABLE IF NOT EXISTS telemetry (
#                     id SERIAL PRIMARY KEY, timestamp TIMESTAMPTZ,
#                     vehicle_id TEXT, sensor TEXT, value FLOAT, unit TEXT
#                 )
#             """))
#
#     def all(self, vehicle_id=None): ...
#     def add(self, entry): ...


# ---------------------------------------------------------------------------
# Aktive Implementierung — hier wechseln
# ---------------------------------------------------------------------------

storage = FileStorage()
# storage = SQLiteStorage()
# storage = CloudSQLStorage()
