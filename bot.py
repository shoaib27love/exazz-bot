from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import datetime

# === Bot Token ===
TOKEN = "8234777694:AAG3RhP147Y5tpaY1TXzC_270D3B3wH2_Bw"

# === ADMIN ID (aapka Telegram ID) ===
ADMIN_ID = 5046658718

# === In-memory Database ===
user_bonus = {}
user_balances = {}       # user_id -> balance
withdraw_requests = {}   # request_id -> {user_id, method, number, amount}
shown_message = {}       # track which users have seen welcome message

# === Menu Keyboard ===
def main_menu():
    keyboard = [
        ["💰 Investment Plan", "👥 Referral Link"],
        ["📥 Deposit", "🎁 Daily Bonus"],
        ["💰 My Balance", "📤 Withdraw"],
        ["ℹ️ Help", "🏠 Home"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_balances:
        user_balances[user_id] = 0.0  # new user ka balance

    # One-time Welcome Message
    if not shown_message.get(user_id):
        await update.message.reply_text(
            "🎉 Welcome to *Exazz Bot* 🎉\n\n"
            "👉 Here you can invest and earn rewards daily.\n"
            "💰 Claim bonuses, invite friends, and withdraw easily!\n\n"
            "⚠️ Note: Minimum withdrawal is 10 USDT.\n\n"
            "🚀 Let's get started!",
            parse_mode="Markdown"
        )
        shown_message[user_id] = True  # mark as shown

    # Normal Menu
    await update.message.reply_text(
        "👋 Welcome to Exazz Bot!\n\nChoose an option below:",
        reply_markup=main_menu()
    )

# === Help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Help Menu:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "💰 Investment Plan\n"
        "👥 Referral Link\n"
        "📥 Deposit\n"
        "🎁 Daily Bonus\n"
        "💰 My Balance\n"
        "📤 Withdraw"
    )

# === Handle User Messages ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    if text == "💰 Investment Plan":
        await update.message.reply_text("📊 Our Plan: Invest 10 USDT → Get 25 USDT after 15 days.")

    elif text == "👥 Referral Link":
        await update.message.reply_text(f"🔗 Your Referral Link:\nhttps://t.me/Exazz_bot?start={user_id}")

    elif text == "📥 Deposit":
        await update.message.reply_text(
            "💳 Send USDT (TRC20) to this address:\n`TLmkHP3LdQj8xbBPwqyWGpeyxVrT3Ew9PW`\n\n"
            "⚠️ After sending, contact admin with TXID for approval.",
            parse_mode="Markdown"
        )

    elif text == "🎁 Daily Bonus":
        today = datetime.date.today()
        last_claim = user_bonus.get(user_id)

        if last_claim == today:
            await update.message.reply_text("❌ You already claimed your daily bonus today. Come back tomorrow!")
        else:
            user_bonus[user_id] = today
            user_balances[user_id] += 1
            await update.message.reply_text("✅ Congrats! You received 🎁 1 USDT Bonus.")

    elif text == "💰 My Balance":
        balance = user_balances[user_id]
        await update.message.reply_text(f"💰 Your Current Balance: {balance} USDT")

    elif text == "📤 Withdraw":
        keyboard = [["📲 JazzCash", "💳 EasyPaisa"], ["🏠 Home"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📤 Choose withdrawal method:", reply_markup=reply_markup)

    elif text == "📲 JazzCash":
        context.user_data["withdraw_method"] = "JazzCash"
        await update.message.reply_text("📲 Enter your JazzCash number:")

    elif text == "💳 EasyPaisa":
        context.user_data["withdraw_method"] = "EasyPaisa"
        await update.message.reply_text("💳 Enter your EasyPaisa number:")

    elif text.isdigit() and "withdraw_method" in context.user_data:
        method = context.user_data["withdraw_method"]
        number = text
        balance = user_balances[user_id]

        if balance >= 10:  # minimum withdraw 10 USDT
            request_id = len(withdraw_requests) + 1
            withdraw_requests[request_id] = {
                "user_id": user_id,
                "method": method,
                "number": number,
                "amount": balance
            }
            user_balances[user_id] = 0  # reset balance after request

            await update.message.reply_text("✅ Withdrawal request submitted. Waiting for admin approval.")

            # Notify Admin
            buttons = [[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{request_id}")]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📤 Withdraw Request #{request_id}\n\nUser ID: {user_id}\nMethod: {method}\nNumber: {number}\nAmount: {balance} USDT",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("❌ Minimum withdrawal is 10 USDT.")

    elif text == "🏠 Home":
        await update.message.reply_text("🏠 Back to Main Menu", reply_markup=main_menu())

    elif text == "ℹ️ Help":
        await help_command(update, context)

    else:
        await update.message.reply_text("❌ Unknown command. Use the menu or /help")

# === Admin Panel Command ===
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        if not withdraw_requests:
            await update.message.reply_text("📭 No pending withdrawal requests.")
        else:
            for req_id, data in withdraw_requests.items():
                buttons = [[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{req_id}")]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await update.message.reply_text(
                    f"📤 Request #{req_id}\nUser: {data['user_id']}\nMethod: {data['method']}\nNumber: {data['number']}\nAmount: {data['amount']} USDT",
                    reply_markup=reply_markup
                )
    else:
        await update.message.reply_text("❌ You are not authorized to access the admin panel.")

# === Approve Withdraw Callback ===
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    req_id = int(query.data.split("_")[1])
    if req_id in withdraw_requests:
        data = withdraw_requests.pop(req_id)
        user_id = data["user_id"]

        await context.bot.send_message(user_id, "✅ Your withdrawal has been approved! Payment will be processed soon.")
        await query.edit_message_text(f"✅ Request #{req_id} approved successfully!")

# === Main Function ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(approve_request))

    print("✅ Bot is running with Admin Panel...")
    app.run_polling()

if __name__ == "__main__":
    main()

