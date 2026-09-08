import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.environ.get("PORT", 5000))

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🏏 Cricket", callback_data="alert_cricket"), InlineKeyboardButton("🎾 Tennis", callback_data="alert_tennis")],
        [InlineKeyboardButton("⚽ Football", callback_data="alert_football"), InlineKeyboardButton("🤼 Kabaddi", callback_data="alert_kabaddi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚡ *Live Sports Hub*\n\nTap your favorite sport below to get instant live scores!", reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    sport = query.data.replace("alert_", "")
    await query.message.edit_text(f"🟢 *Live Updates Active for {sport.upper()}!*\n\nFetching live scores...", parse_mode="Markdown")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_webhook(listen="0.0.0.0", port=PORT, webhook_url=f"https://livesportshub.onrender.com/{TOKEN}")

if __name__ == '__main__':
    main()
