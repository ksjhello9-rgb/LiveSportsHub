import os
import requests
from flask import Flask, request as flask_request

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    return "Live Sports Hub is alive!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = flask_request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        if text == "/start":
            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "⚡ *Live Sports Hub*\n\nWelcome! Your bot is fully active.",
                "parse_mode": "Markdown"
            })
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
