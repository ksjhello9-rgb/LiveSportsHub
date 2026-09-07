import os
import threading
from flask import Flask, render_template_string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = "8939692755:AAFwzR3H4BQv2qjDlGmcqqKj6eAEkxai7lo"

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Sports Hub</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            background: linear-gradient(135deg, #064e3b, #022c22);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 20px;
            text-align: center;
            margin: 0;
            min-height: 100vh;
        }
        h2 { color: #4ade80; margin-bottom: 5px; font-size: 24px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        p { color: #cbd5e1; font-size: 14px; margin-bottom: 20px; }
        .container { max-width: 400px; margin: 0 auto; }
        .sports-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .sport-btn {
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid #10b981;
            padding: 12px;
            border-radius: 12px;
            color: #ffffff;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            text-align: center;
        }
        .sport-btn:active {
            transform: scale(0.95);
            background-color: #10b981;
            color: #064e3b;
        }
        .active-view {
            margin-top: 20px;
            background: rgba(15, 23, 42, 0.95);
            padding: 20px;
            border-radius: 16px;
            display: none;
            border: 1px solid #10b981;
            text-align: left;
        }
        input {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            box-sizing: border-box;
            border-radius: 8px;
            border: 1px solid #334155;
            background: #022c22;
            color: white;
            font-size: 15px;
        }
        .submit-btn {
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 12px;
            margin-top: 15px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
        }
        .back-btn {
            background-color: #ef4444;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚡ Live Sports Hub</h2>
        <p>Select your favorite sport to track live alerts</p>
        
        <div id="sportGrid" class="sports-grid">
            <button class="sport-btn" onclick="selectSport('Cricket')">🏏 Cricket</button>
            <button class="sport-btn" onclick="selectSport('Tennis')">🎾 Tennis</button>
            <button class="sport-btn" onclick="selectSport('Football')">⚽ Football</button>
            <button class="sport-btn" onclick="selectSport('Kabaddi')">🔴 Kabaddi</button>
            <button class="sport-btn" onclick="selectSport('Badminton')">🏸 Badminton</button>
            <button class="sport-btn" onclick="selectSport('Basketball')">🏀 Basketball</button>
            <button class="sport-btn" onclick="selectSport('Volleyball')">🏐 Volleyball</button>
            <button class="sport-btn" onclick="selectSport('Formula 1')">🏎️ Formula 1</button>
            <button class="sport-btn" onclick="selectSport('Ice Hockey')">🏒 Ice Hockey</button>
            <button class="sport-btn" onclick="selectSport('Chess')">♟️ Chess</button>
        </div>

        <div id="sportView" class="active-view">
            <h3 id="selectedTitle" style="color: #4ade80; margin-top: 0;">Track Sport</h3>
            <p style="margin-bottom: 5px; font-size: 13px;">Enter Team / Player / Series name:</p>
            <input type="text" id="trackInput" placeholder="e.g. India, RCB, Nadal...">
            <button class="submit-btn" onclick="startTracking()">Set Live Alert</button>
            <button class="submit-btn back-btn" onclick="goBack()">Back to Sports Hub</button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();
        let currentSport = "";

        function selectSport(sportName) {
            currentSport = sportName;
            document.getElementById("sportGrid").style.display = "none";
            document.getElementById("selectedTitle").innerText = "Track " + sportName;
            document.getElementById("sportView").style.display = "block";
        }

        function goBack() {
            document.getElementById("sportView").style.display = "none";
            document.getElementById("sportGrid").style.display = "grid";
            document.getElementById("trackInput").value = "";
        }

        function startTracking() {
            let val = document.getElementById("trackInput").value.trim();
            if(!val) {
                alert("Please enter a name to track!");
                return;
            }
            alert("Alert set successfully for " + currentSport + " (" + val + ")! You will receive live updates.");
            goBack();
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
  return render_template_string(HTML_TEMPLATE)


def run_flask():
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
  web_app_url = os.getenv("WEB_APP_URL", "https://livesportshub.onrender.com")

  keyboard = [[
      InlineKeyboardButton(
          "🚀 Open Live Sports Hub", web_app=WebAppInfo(url=web_app_url)
      )
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)

  if update.message:
    await update.message.reply_text(
        "👋 Welcome to Live Sports Hub!\n\nTap the button below to launch the"
        " ultimate multi-sport tracking hub inside Telegram: 🏆",
        reply_markup=reply_markup,
    )


def main():
  t = threading.Thread(target=run_flask)
  t.start()

  bot_app = Application.builder().token(BOT_TOKEN).build()
  bot_app.add_handler(CommandHandler("start", send_welcome))
  bot_app.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), send_welcome)
  )

  print("Live Sports Hub is running perfectly...")
  bot_app.run_polling()


if __name__ == "__main__":
  main()
