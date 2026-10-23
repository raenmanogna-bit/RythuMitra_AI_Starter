🌱 Rythu Mitra AI: Smart Agriculture Monitoring System 🚜
Rythu Mitra AI is an integrated hardware and software solution designed to assist rural farmers with precise crop management. Developed during the AI BOTS Hackathon 2026, the system bridges physical analog sensors with a digital web dashboard to automate irrigation and provide real-time, data-backed farming advice.

✨ Key Features
🌍 Multilingual AI Assistant: Breaks the language barrier! The conversational AI interface supports 5 languages (English, Telugu, Hindi, Tamil, and Kannada), allowing farmers to ask questions like "నా పొలంలో నీళ్లు ఎప్పుడు పెట్టాలి?" or "क्या मुझे अब पानी देना चाहिए?" and get instant help.

💧 Smart IoT Telemetry: Arduino-based analog signal conditioning for real-time soil moisture and environmental monitoring.

⚙️ Automated Actuation: 12V relay-driven pump simulation for closed-loop, automated irrigation control based on live field conditions.

📊 Real-Time Dashboard: An interactive web interface displaying live sensor data, pump status, weather forecasts, and market price estimates.

🛠️ Tech Stack
Hardware:

🔌 Arduino Uno (Microcontroller)

🌡️ Analog Soil Moisture Sensor, DHT11 (Temp/Humidity), LDR (Light)

🚰 12V Relay Module & Water Pump (Simulation)

Software:

Embedded: C++ (sketch.ino)

Backend Middleware: Python (arduino_bridge.py for Serial communication)

AI Server: Python / Flask (ai_server.py for API endpoints and NLP engine)

Frontend: HTML5, CSS3, JavaScript (index.html)

📂 Project Structure
sketch.ino - The embedded C++ code that runs on the Arduino to read analog sensors and trigger the relay.

arduino_bridge.py - Python script that listens to the Arduino's COM port and bridges the serial data to the web server.

ai_server.py - The main Python backend that processes the AI chatbot requests in 5 languages.

index.html - The frontend UI dashboard for the farmer.

diagram.json / wokwi.toml - Circuit simulation files.

🚀 How to Run Locally
Upload Hardware Code: Flash sketch.ino to your Arduino using the Arduino IDE.

Start the Bridge: Run python arduino_bridge.py in your terminal to start capturing serial data.

Start the AI Server: Run python ai_server.py in a separate terminal to start the backend API.

Open the Dashboard: Double-click index.html in your browser to view the real-time interface and interact with the multilingual chatbot!

Built with ❤️ by Team Tech Titans for the AI BOTS Hackathon 2026.
