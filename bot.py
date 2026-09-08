import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🏏 Cricket", callback_data="alert_cricket"), InlineKeyboardButton("🎾 Tennis", callback_data="alert_tennis")],
        [InlineKeyboardButton("⚽ Football", callback_data="alert_football"), InlineKeyboardButton("🤼 Kabaddi", callback_data="alert_kabaddi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "⚡ *Live Sports Hub*\n\nTap your favorite sport below to get instant live scores!"
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    sport = query.data.replace("alert_", "")
    await query.message.edit_text(f"🟢 *Live Updates Active for {sport.upper()}!*\n\nFetching live scores...", parse_mode="Markdown")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))

@app.route('/')
def index():
    return "Live Sports Hub Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        
        async def process():
            await telegram_app.initialize()
            await telegram_app.process_update(update)
            
        asyncio.run(process())
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return 'OK'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
