# RythuMitra AI — Starter Prototype

## What this first milestone includes
- Responsive single-file dashboard
- Language selector: Telugu, Hindi, Tamil, Kannada, English
- Simulated soil-moisture readings and automatic/manual demo pump state
- Sample FairPrice net-return calculator
- Demonstration chat interface
- Leaf-photo preview (not disease diagnosis)

## Run it
1. Extract `RythuMitra_AI_Starter.zip` to a folder.
2. Open `index.html` in Chrome or Edge.
3. The dashboard works without npm, Node.js, or internet access for the local demo.

## Important status
This is **Milestone 1: front-end simulation**.
- Soil readings and pump status are simulated; no ESP32 is connected.
- Chat answers are predefined examples; no live AI service is connected.
- FairPrice uses editable sample values; no live market data is connected.
- The leaf-photo panel only previews the image; it does not diagnose disease.
- Voice input depends on browser speech recognition support and may need internet/browser services.

## Controls
- `Simulate new reading`: changes the simulated moisture value.
- `Automatic mode`: applies the demo rule (start below 35%, stop at/above 55%).
- `Manual mode`: switches to manual simulation. Click the ON/OFF pump status text to toggle it.
- `Red stop button` / physical emergency stop will be implemented with the ESP32 in the hardware milestone. This website simulation is not a safety controller.
- FairPrice: edit quantity, prices and costs, then compare estimated net returns.

## Next milestone
Connect a real ESP32 to the website using a small backend and a defined HTTP or MQTT message format. Then replace demo chat replies with a real AI endpoint, add verified market-data retrieval, and only then integrate/test a suitable leaf-image model.

## Safety
Do not connect a real borewell motor directly to an ESP32. Use a low-voltage demonstration pump for this project. Real motor installations require appropriately rated protection and qualified electrical installation.
