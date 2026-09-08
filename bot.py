import os
import requests
from flask import Flask, request as req

app = Flask(__name__)
T = os.getenv("TELEGRAM_TOKEN")

@app.route("/")
def h():
    return "OK"

@app.route("/webhook", methods=["POST"])
def w():
    try:
        d = req.get_json(force=True)
        c = d["message"]["chat"]["id"]
        t = d["message"]["text"]
        requests.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id": c, "text": f"Echo: {t}"})
    except:
        pass
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
