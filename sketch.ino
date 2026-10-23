#include <Arduino.h>

const int MOISTURE_PIN = 34; // Analog pin for potentiometer
const int PUMP_PIN = 2;      // Digital pin for pump LED
const int ESTOP_PIN = 12;    // Digital pin for emergency stop button

bool pumpStatus = false;
bool emergencyStop = false;

void setup() {
  Serial.begin(115200);
  pinMode(PUMP_PIN, OUTPUT);
  
  // Use internal pullup for the button so we don't need an external resistor
  pinMode(ESTOP_PIN, INPUT_PULLUP); 
  
  digitalWrite(PUMP_PIN, LOW);
  Serial.println("RythuMitra ESP32 Edge Controller Initialized.");
}

void loop() {
  // 1. Read sensors
  int rawMoisture = analogRead(MOISTURE_PIN);
  
  // Convert 12-bit ADC (0-4095) to a percentage (100% is dry, 0% is wet for this simulation)
  int moisturePercent = map(rawMoisture, 0, 4095, 0, 100);
  
  // Read button (LOW means pressed because of INPUT_PULLUP)
  bool buttonPressed = (digitalRead(ESTOP_PIN) == LOW);

  // 2. Safety Loop: Emergency Stop overrides everything
  if (buttonPressed) {
    emergencyStop = true;
    pumpStatus = false;
    Serial.println("ALERT: EMERGENCY STOP ENGAGED!");
  }

  // 3. Automation Logic (Only runs if no emergency stop is active)
  if (!emergencyStop) {
    if (moisturePercent < 35 && !pumpStatus) {
      pumpStatus = true; // Soil is too dry, turn pump ON
    } else if (moisturePercent >= 55 && pumpStatus) {
      pumpStatus = false; // Soil is wet enough, turn pump OFF
    }
  }

  // 4. Actuate Hardware
  digitalWrite(PUMP_PIN, pumpStatus ? HIGH : LOW);

  // 5. Output Telemetry (Your backend will eventually read this via Serial/MQTT)
  Serial.print("Moisture: ");
  Serial.print(moisturePercent);
  Serial.print("% | Pump: ");
  Serial.print(pumpStatus ? "ON" : "OFF");
  Serial.print(" | E-Stop: ");
  Serial.println(emergencyStop ? "ACTIVE" : "CLEAR");

  delay(1000); // 1-second interval
}