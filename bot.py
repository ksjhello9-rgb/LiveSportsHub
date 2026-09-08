import os
import requests
from flask import Flask, request as flask_request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    return "Live Sports Hub is alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = flask_request.get_json(force=True)
        if update and "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            if text:
                requests.post(f"{TELEGRAM_API}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": f"⚡ Live Sports Hub Echo: {text}"
                })
    except Exception as e:
        print("Error:", e)
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
