
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
ARDUINO_URL = "http://127.0.0.1:8000/api/status"
MODEL = "qwen2.5:3b"

FARMING_INSTRUCTIONS = """
You are RythuMitra AI, a practical farming assistant for Indian farmers.

Help with crops, irrigation, soil health, fertilizer guidance, weather
precautions, livestock basics, government schemes and farm economics.

Use the farmer's requested language. Give clear, simple advice.
Never invent live weather, market prices, or scheme eligibility.
A raw soil sensor reading is not a moisture percentage and does not
measure soil nutrients. Interpret DRY/WET using the supplied sensor
status, but explain that watering decisions also depend on the crop,
growth stage, soil type and recent rainfall.

Never claim to operate a physical pump. The irrigation request is not
proof that a pump is running. Do not override hardware safety logic.
For serious crop disease or livestock health concerns, recommend
qualified agricultural or veterinary advice.
"""

def get_sensor_context():
    try:
        response = requests.get(ARDUINO_URL, timeout=3)
        response.raise_for_status()
        data = response.json()

        if (
            not data.get("connected")
            or data.get("soilReading") is None
        ):
            return (
                "Arduino status: unavailable or no valid reading. "
                "Do not assume the soil is dry or wet."
            )

        return (
            "CURRENT ARDUINO SENSOR DATA:\n"
            f"Raw soil sensor reading: {data.get('soilReading')}\n"
            f"Reported soil status: {data.get('soilStatus', 'UNKNOWN')}\n"
            f"Irrigation request: {data.get('irrigationRequest', 'UNKNOWN')}\n"
            f"Safety timeout active: {bool(data.get('safetyTimeout', False))}\n"
            "The irrigation request does not confirm actual pump operation."
        )

    except (requests.RequestException, ValueError) as exc:
        print("Arduino context unavailable:", type(exc).__name__)
        return (
            "Arduino status: unavailable. Do not invent sensor readings. "
            "Give general advice and tell the farmer that live sensor "
            "data could not be retrieved."
        )


@app.get("/")
def home():
    return jsonify({
        "service": "RythuMitra AI",
        "status": "running",
        "engine": "Ollama local AI"
    })


@app.get("/api/health")
def health():
    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags", timeout=3
        )
        response.raise_for_status()
        models = response.json().get("models", [])
        available = any(
            item.get("name", "").split(":")[0] == MODEL.split(":")[0]
            for item in models
        )
        return jsonify({
            "status": "running",
            "engine": "Ollama",
            "model": MODEL,
            "model_available": available
        })
    except requests.RequestException:
        return jsonify({
            "status": "waiting",
            "engine": "Ollama",
            "error": "Ollama is not responding."
        }), 503


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    language = str(data.get("language", "English")).strip()

    if not message:
        return jsonify({"error": "Please enter a farming question."}), 400

    if len(message) > 4000:
        return jsonify({"error": "Keep your question under 4000 characters."}), 400

    sensor_context = get_sensor_context()

    prompt = (
        FARMING_INSTRUCTIONS
        + f"\nRespond in this language: {language}."
        + "\n\nUse this sensor context when relevant:\n"
        + sensor_context
        + "\n\nFarmer's question:\n"
        + message
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": FARMING_INSTRUCTIONS
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "options": {"num_predict": 300}
            },
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        answer = result.get("message", {}).get("content", "").strip()

        if not answer:
            return jsonify({"error": "The local model returned no answer."}), 502

        sensor_available = "CURRENT ARDUINO SENSOR DATA:" in sensor_context

        return jsonify({
            "answer": answer,
            "sensor_context_available": sensor_available,
            "sensor_context": sensor_context,
            "source": (
                "Local AI with live Arduino context"
                if sensor_available
                else "Local AI; live sensor data unavailable"
            )
        })

    except requests.Timeout:
        return jsonify({
            "error": "The local model took too long to respond."
        }), 504
    except requests.RequestException as exc:
        print("Ollama request failed:", type(exc).__name__, str(exc))
        return jsonify({
            "error": "Cannot reach Ollama. Check that it is running and the model is installed."
        }), 502


if __name__ == "__main__":
    print("RythuMitra AI: http://127.0.0.1:8001")
    print("Model:", MODEL)
    app.run(host="127.0.0.1", port=8001, debug=False)
