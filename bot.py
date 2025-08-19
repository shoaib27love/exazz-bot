from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# === Aapka Bot Token ===
TOKEN = "8234777694:AAG3RhP147Y5tpaY1TXzC_270D3B3wH2_Bw"

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Investment Plan", "👥 Referral Link"],
        ["📥 Deposit", "ℹ️ Help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Welcome to Exazz Bot!\n\nChoose an option below:",
        reply_markup=reply_markup
    )

# === Help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Help Menu:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "💰 Investment Plan\n"
        "👥 Referral Link\n"
        "📥 Deposit"
    )

# === Message Handler (buttons handle karega) ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Investment Plan":
        await update.message.reply_text("📊 Our Plan: Invest 10 USDT → Get 25 USDT after 15 days.")
    elif text == "👥 Referral Link":
        user_id = update.message.from_user.id
        await update.message.reply_text(f"🔗 Your Referral Link:\nhttps://t.me/Exazz_bot?start={user_id}")
    elif text == "📥 Deposit":
        await update.message.reply_text("💳 Send USDT (TRC20) to this address:\n`TLmkHP3LdQj8xbBPwqyWGpeyxVrT3Ew9PW`")
    elif text == "ℹ️ Help":
        await help_command(update, context)
    else:
        await update.message.reply_text("❌ Unknown command. Use the menu or /help")

# === Main Function ===
def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
