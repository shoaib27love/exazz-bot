import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot ka Token
TOKEN = "8234777694:AAG3RhP147Y5tpaY1TXzC_270D3B3wH2_Bw"

# Admin ID (aapki Telegram ID)
ADMIN_ID = 5046658718

# Deposit Address (TRC20)
DEPOSIT_ADDRESS = "TLmkHP3LdQj8xbBPwqyWGpeyxVrT3Ew9PW"

logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 Invest", callback_data="invest")],
        [InlineKeyboardButton("👥 Referral", callback_data="referral")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n\n"
        "This is an Investment Bot.\n\n"
        "👉 Deposit $10 (USDT TRC20) and get $25 after 15 days!",
        reply_markup=reply_markup
    )

# Buttons ka handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "invest":
        await query.edit_message_text(
            text=f"💵 Investment Plan:\n\nDeposit **$10** and Get **$25** after 15 days!\n\n"
                 f"Send USDT (TRC20) to this address:\n`{DEPOSIT_ADDRESS}`\n\n"
                 "After payment, send screenshot to Admin."
        )
    elif query.data == "referral":
        user_id = update.effective_user.id
        ref_link = f"https://t.me/Exazz_bot?start={user_id}"
        await query.edit_message_text(
            text=f"👥 Your Referral Link:\n{ref_link}\n\nInvite friends and earn rewards!"
        )
    elif query.data == "help":
        await query.edit_message_text(
            text="ℹ️ For support, contact Admin."
        )

# Admin panel command
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(
            "⚙️ Admin Panel\n\nCommands:\n"
            "/broadcast <msg> - Send message to all users\n"
            "/users - Show total users"
        )
    else:
        await update.message.reply_text("❌ You are not authorized!")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
