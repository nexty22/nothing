from flask import Flask, request, jsonify, send_from_directory
import requests, base64

app = Flask(__name__)

TTS_API = "https://tts.fastdevelopers.workers.dev/tts"

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    voice = data.get("voice")

    r = requests.get(TTS_API, params={
        "voice": voice,
        "text": text
    })

    if r.status_code == 200:
        audio = base64.b64encode(r.content).decode("utf-8")
        return jsonify({"success": True, "audio": audio})

    return jsonify({"success": False}), 500
