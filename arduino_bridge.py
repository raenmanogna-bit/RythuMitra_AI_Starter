import json
import time
from unicodedata import name
import serial
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# ESP32 connection
ARDUINO_PORT = "COM10"
BAUD_RATE = 9600

latest_data = {
    "soilReading": None,
    "soilStatus": "Waiting for ESP32",
    "irrigationRequest": "OFF",
    "safetyTimeout": False,
    "connected": False
}


def read_arduino():
    global latest_data

    while True:
        try:
            with serial.Serial(
                ARDUINO_PORT, BAUD_RATE, timeout=2
            ) as board:
                print(f"Connected to ESP32 on {ARDUINO_PORT}")
                time.sleep(2)

                while True:
                    line = board.readline().decode(
                        "utf-8", errors="ignore"
                    ).strip()

                    if not line:
                        continue

                    print("ESP32:", line)

                    reading = None
                    status = "UNKNOWN"
                    irrigation = "OFF"
                    timeout = False

                    # Format 1: Soil sensor test
                    # Soil sensor raw value: 1234
                    if "Soil sensor raw value:" in line:
                        try:
                            reading = int(line.split(":")[-1].strip())
                        except ValueError:
                            continue

                    # Format 2: Detailed irrigation output
                    # Average soil reading: 669 | Soil status: DRY |
                    # Irrigation request: OFF | SAFETY TIMEOUT
                    elif "Average soil reading:" in line:
                        try:
                            parts = line.split("|")
                            reading = int(
                                parts[0].split(":")[1].strip()
                            )

                            for part in parts[1:]:
                                part = part.strip()

                                if "Soil status:" in part:
                                    status = part.split(":")[1].strip()

                                elif "Irrigation request:" in part:
                                    irrigation = part.split(":")[1].strip()

                                if "SAFETY TIMEOUT" in part:
                                    timeout = True
                        except (ValueError, IndexError):
                            continue
                    else:
                        continue

                    if status == "UNKNOWN":
                        status = (
                            "DRY" if reading > 2000 else "WET"
                        )

                    latest_data = {
                        "soilReading": reading,
                        "soilStatus": status,
                        "irrigationRequest": irrigation,
                        "safetyTimeout": timeout,
                        "connected": True
                    }

        except (serial.SerialException, OSError) as error:
            latest_data["connected"] = False
            print("ESP32 connection error:", error)
            print("Retrying in 3 seconds...")
            time.sleep(3)


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/status":
            body = json.dumps(latest_data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    Thread(target=read_arduino, daemon=True).start()

    server = HTTPServer(("127.0.0.1", 8000), DashboardHandler)
    print("Bridge ready at http://127.0.0.1:8000/api/status")
    server.serve_forever()