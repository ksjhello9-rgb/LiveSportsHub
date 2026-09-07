import os
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Live Sports Hub Bot is Live and Running!"

# Main Sports Menu with clean in-chat UI
async def show_sports_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏏 Cricket", callback_data="alert_cricket"), InlineKeyboardButton("🎾 Tennis", callback_data="alert_tennis")],
        [InlineKeyboardButton("⚽ Football", callback_data="alert_football"), InlineKeyboardButton("🤼 Kabaddi", callback_data="alert_kabaddi")],
        [InlineKeyboardButton("🏸 Badminton", callback_data="alert_badminton"), InlineKeyboardButton("🏀 Basketball", callback_data="alert_basketball")],
        [InlineKeyboardButton("🏐 Volleyball", callback_data="alert_volleyball"), InlineKeyboardButton("🏎️ Formula 1", callback_data="alert_f1")],
        [InlineKeyboardButton("🏒 Ice Hockey", callback_data="alert_hockey"), InlineKeyboardButton("♟️ Chess", callback_data="alert_chess")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "⚡ *Live Sports Hub*\n\n"
        "Tap your favorite sport below to get instant live scores and match alerts directly in chat! 🏆"
    )
    
    if update.message:
        try:
            await update.message.delete()
        except Exception:
            pass
        
        chat_id = update.effective_chat.id
        if "menu_msg_id" in context.bot_data:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=context.bot_data["menu_msg_id"])
            except Exception:
                pass
                
        sent_msg = await context.bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
        context.bot_data["menu_msg_id"] = sent_msg.message_id

# Handle sports selection with zero typing (Direct automated alerts)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    sport_key = data.replace("alert_", "")
    
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Sports Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    
    alerts_info = {
        "cricket": "🏏 *Cricket Live Hub*\n\n🟢 *Status:* Live Matches Ongoing\n• India vs Australia - 2nd T20\n  *(Score: IND 165/4 (18.2 Overs))* \n• Live Ball-by-Ball & Wicket Alerts Active!",
        "tennis": "🎾 *Tennis Live Hub*\n\n🟢 *Status:* Tournament Finals\n• Novak Djokovic vs Carlos Alcaraz\n  *(Sets: 2-1, Game in Progress)*\n• Break Point & Set Alerts Active!",
        "football": "⚽ *Football Live Hub*\n\n🟢 *Status:* Premier League Live\n• Real Madrid vs Barcelona\n  *(Score: 2 - 1 (78th Min))* \n• Goal & Card Alerts Active!",
        "kabaddi": "🤼 *Kabaddi Live Hub*\n\n🟢 *Status:* Pro Kabaddi League\n• Patna Pirates vs U Mumba\n  *(Score: 32 - 28)*\n• Super Raid & All-Out Alerts Active!",
        "badminton": "🏸 *Badminton Live Hub*\n\n🟢 *Status:* BWF World Tour\n• Viktor Axelsen vs Kunlavut V.\n  *(Game 2: 18-16)*\n• Rally & Match Point Alerts Active!",
        "basketball": "🏀 *Basketball Live Hub*\n\n🟢 *Status:* NBA Live\n• LA Lakers vs Boston Celtics\n  *(Score: 98 - 94 (4th Qtr))* \n• 3-Pointer & Buzzer Alerts Active!",
        "volleyball": "🏐 *Volleyball Live Hub*\n\n🟢 *Status:* FIVB World League\n• Brazil vs Italy\n  *(Sets: 2-2 (14-12))* \n• Set Point Alerts Active!",
        "f1": "🏎️ *Formula 1 Live Hub*\n\n🟢 *Status:* Italian Grand Prix\n• Lap 44 / 53\n• Leader: M. Verstappen\n• Pit Stop & Lap-by-Lap Alerts Active!",
        "hockey": "🏒 *Ice Hockey Live Hub*\n\n🟢 *Status:* NHL Live\n• Toronto Maple Leafs vs Oilers\n  *(Score: 3 - 2 (3rd Period))* \n• Power Play Alerts Active!",
        "chess": "♟️ *Chess Live Hub*\n\n🟢 *Status:* Candidates Tournament\n• Gukesh D vs Magnus Carlsen\n• Move 34. Nf3 (Equal Position)\n• Checkmate Alerts Active!"
    }
    
    alert_text = alerts_info.get(sport_key, "🔔 *Live Alerts Active!*")
    
    await query.message.edit_text(alert_text, reply_markup=reply_markup, parse_mode="Markdown")

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("🏏 Cricket", callback_data="alert_cricket"), InlineKeyboardButton("🎾 Tennis", callback_data="alert_tennis")],
            [InlineKeyboardButton("⚽ Football", callback_data="alert_football"), InlineKeyboardButton("🤼 Kabaddi", callback_data="alert_kabaddi")],
            [InlineKeyboardButton("🏸 Badminton", callback_data="alert_badminton"), InlineKeyboardButton("🏀 Basketball", callback_data="alert_basketball")],
            [InlineKeyboardButton("🏐 Volleyball", callback_data="alert_volleyball"), InlineKeyboardButton("🏎️ Formula 1", callback_data="alert_f1")],
            [InlineKeyboardButton("🏒 Ice Hockey", callback_data="alert_hockey"), InlineKeyboardButton("♟️ Chess", callback_data="alert_chess")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_text = (
            "⚡ *Live Sports Hub*\n\n"
            "Tap your favorite sport below to get instant live scores and match alerts directly in chat! 🏆"
        )
        await query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Please set your TELEGRAM_TOKEN environment variable.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, show_sports_menu))
    application.add_handler(MessageHandler(filters.COMMAND, show_sports_menu))
    
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^alert_"))
    application.add_handler(CallbackQueryHandler(menu_handler, pattern="^back_to_menu$"))

    port = int(os.environ.get("PORT", 5000))
    
    import threading
    threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=port)).start()
    
    print("Bot is starting polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
