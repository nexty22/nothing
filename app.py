from flask import Flask, render_template, request, send_file
import requests, base64, io

app = Flask(__name__)

TTS_API = "https://tts.fastdevelopers.workers.dev/tts"

@app.route("/", methods=["GET", "POST"])
def index():
    audio_base64 = None

    if request.method == "POST":
        text = request.form["text"]
        voice = request.form["voice"]

        r = requests.get(TTS_API, params={
            "voice": voice,
            "text": text
        })

        if r.status_code == 200:
            audio_base64 = base64.b64encode(r.content).decode("utf-8")

    return render_template("index.html", audio=audio_base64)

@app.route("/download", methods=["POST"])
def download():
    audio_b64 = request.form["audio"]
    audio_bytes = base64.b64decode(audio_b64)

    return send_file(
        io.BytesIO(audio_bytes),
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="NEXTY_AI.mp3"
    )

if __name__ == "__main__":
    app.run()
