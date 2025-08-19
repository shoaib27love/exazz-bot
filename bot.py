import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 Bot Config
BOT_TOKEN = "8234777694:AAG3RhP147Y5tpaY1TXzC_270D3B3wH2_Bw"
ADMIN_ID = 5046658718
CHANNEL_LINK = "https://t.me/+2VWp09FHP5c3ZmRk"

# User data memory
users = {}
withdraw_requests = []

logging.basicConfig(level=logging.INFO)

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users[user.id] = {"balance": 0, "referrals": 0, "deposits": [], "withdrawals": []}

    keyboard = [
        [InlineKeyboardButton("💰 Investment Plans", callback_data="plans")],
        [InlineKeyboardButton("🎁 Daily Bonus", callback_data="bonus"),
         InlineKeyboardButton("👤 My Balance", callback_data="balance")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw"),
         InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("👥 Refer & Earn", callback_data="refer"),
         InlineKeyboardButton("📖 How It Works", callback_data="how")],
        [InlineKeyboardButton("📜 Transactions History", callback_data="history")],
        [InlineKeyboardButton("📩 Support", callback_data="support"),
         InlineKeyboardButton("🏆 Top Investors", callback_data="top")],
        [InlineKeyboardButton("❓ FAQs", callback_data="faq"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("🌍 Join Our Channel", url=CHANNEL_LINK)]
    ]
    await update.message.reply_text(
        f"👋 Welcome *{user.first_name}*!\n\n"
        "🚀 This is an earning & investment bot.\n"
        "💎 Explore the menu below:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON HANDLERS ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "plans":
        await query.edit_message_text("💰 *Investment Plans*\n\n👉 Invest $10 and get $22 after 15 days!", parse_mode="Markdown")
    elif query.data == "bonus":
        await query.edit_message_text("🎁 You received your daily bonus: +$0.5")
        users[query.from_user.id]["balance"] += 0.5
    elif query.data == "balance":
        bal = users[query.from_user.id]["balance"]
        await query.edit_message_text(f"👤 Your Balance: *${bal}*", parse_mode="Markdown")
    elif query.data == "withdraw":
        await query.edit_message_text("💵 Withdraw Options:\n1. JazzCash\n2. Easypaisa\n3. USDT (TRC20)")
    elif query.data == "stats":
        total_users = len(users)
        await query.edit_message_text(f"📊 Stats:\n👥 Total Users: {total_users}")
    elif query.data == "refer":
        await query.edit_message_text("👥 Refer & Earn:\nInvite friends using your referral link to earn rewards!")
    elif query.data == "how":
        await query.edit_message_text("📖 *How It Works*\n\n1. Invest money\n2. Wait 15 days\n3. Get profits\n4. Withdraw easily", parse_mode="Markdown")
    elif query.data == "history":
        await query.edit_message_text("📜 Your Transactions:\n\nNo transactions yet.")
    elif query.data == "support":
        await query.edit_message_text("📩 Contact Admin: @Exazz_bot")
    elif query.data == "top":
        await query.edit_message_text("🏆 Top Investors:\n\nFeature coming soon...")
    elif query.data == "faq":
        await query.edit_message_text("❓ *FAQs*\n\nQ: Minimum deposit?\nA: $10\n\nQ: Withdrawal time?\nA: 24 hours", parse_mode="Markdown")
    elif query.data == "settings":
        await query.edit_message_text("⚙️ Settings:\nUpdate your info soon.")

# ---------------- ADMIN PANEL ----------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized to access the Admin Panel.")
        return

    keyboard = [
        [InlineKeyboardButton("📜 View Withdraw Requests", callback_data="view_withdrawals")],
        [InlineKeyboardButton("✅ Approve All", callback_data="approve_all")]
    ]
    await update.message.reply_text("⚙️ Admin Panel", reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "view_withdrawals":
        if not withdraw_requests:
            await query.edit_message_text("📜 No withdrawal requests.")
        else:
            text = "📜 Withdrawal Requests:\n\n"
            for r in withdraw_requests:
                text += f"👤 {r['user']} | 💵 ${r['amount']}\n"
            await query.edit_message_text(text)
    elif query.data == "approve_all":
        withdraw_requests.clear()
        await query.edit_message_text("✅ All withdrawal requests approved!")

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CallbackQueryHandler(admin_handler, pattern="^view_withdrawals|approve_all$"))

    app.run_polling()

if __name__ == "__main__":
    main()
