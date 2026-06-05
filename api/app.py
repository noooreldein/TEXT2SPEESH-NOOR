import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# ===== الإعدادات =====
FISH_AUDIO_API_KEY = os.environ.get("FISH_AUDIO_KEY", "1a72e8e0eed64d7a939cfef7e50aa73b")
FISH_AUDIO_URL = "https://api.fish.audio/v1/tts"

# ===== حقوقك =====
MY_OWNER = "@n_7_3_a"
MY_CHANNEL = "https://t.me/n_7_3_a_2"
MY_NAME = "Noor"

@app.route("/")
def home():
    return {
        "status": "running",
        "api": "Fish Audio TTS by Noor",
        "usage": "/tts?text=مرحباً&voice=default",
        "voices": "default, ar-001, ar-002 (حسب المتاح)",
        "owner": MY_OWNER,
        "channel": MY_CHANNEL,
        "developer": MY_NAME
    }

@app.route("/tts", methods=["GET"])
def tts():
    text = request.args.get("text", "")
    voice = request.args.get("voice", "default")

    if not text:
        return {"status": "error", "message": "استخدم ?text=نص_عربي"}, 400

    headers = {
        "Authorization": FISH_AUDIO_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice": voice
    }

    try:
        resp = requests.post(FISH_AUDIO_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

    # إعادة الصوت مباشرة
    return Response(resp.content, mimetype="audio/mpeg")

# ===== للتشغيل المحلي =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
