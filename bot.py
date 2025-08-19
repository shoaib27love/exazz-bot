from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8234777694:AAG3RhP147Y5tpaY1TXzC_270D3B3wH2_Bw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Investment Plan", "👥 Referral Link"],
        ["📥 Deposit", "ℹ️ Help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Welcome to Exazz Bot!\nChoose an option:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()

    # /start command
    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
