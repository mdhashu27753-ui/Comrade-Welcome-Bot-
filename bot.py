from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from html import escape

# =========================
# CONFIG
# =========================

TOKEN = "8772299501:AAF0a-tMhE1IvlTSx66VWsywzqrlKOMFghY"

# Test Group
GROUP_ID = "@test_group_10t"

# Admin username — @ ছাড়া
ADMIN_USERNAME = "Jin_woo_28"

# Bot usernames — @ ছাড়া
COMRADE_BOT = "Comrade_sms_bot"
COMRADE_OTP = "Comrade_sms_OTP"


# =========================
# BUTTONS
# =========================

def buttons():
    keyboard = [
        [
            InlineKeyboardButton(
                "🤖 COMRADE BOT",
                url=f"https://t.me/{COMRADE_BOT}"
            ),
            InlineKeyboardButton(
                "🔵 COMRADE OTP",
                url=f"https://t.me/{COMRADE_OTP}"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# =========================
# WELCOME MESSAGE
# =========================

def welcome_text(name):
    return (
        "╭━━━━━━━━━━━━━━━━━━╮\n"
        "✨ <b>WELCOME TO COMRADE</b> ✨\n"
        "╰━━━━━━━━━━━━━━━━━━╯\n\n"
        f"🎉 <b>অভিনন্দন, {escape(name)}!</b>\n\n"
        "💎 আমাদের Comrade Support Group-এ\n"
        "আপনাকে স্বাগতম।\n\n"
        "⚡ প্রয়োজনীয় Bot ব্যবহার করতে নিচের\n"
        "Button থেকে নির্বাচন করুন।\n\n"
        "🛡️ <b>COMRADE TEAM</b>"
    )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "বন্ধু"

    await update.message.reply_text(
        welcome_text(name),
        parse_mode="HTML",
        reply_markup=buttons()
    )


# =========================
# NEW MEMBER WELCOME
# =========================

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        if member.is_bot:
            continue

        name = member.first_name or "বন্ধু"

        await update.message.reply_text(
            welcome_text(name),
            parse_mode="HTML",
            reply_markup=buttons()
        )


# =========================
# BROADCAST
# =========================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user or (user.username or "").lower() != ADMIN_USERNAME.lower():
        await update.message.reply_text(
            "⛔ এই Command শুধুমাত্র Admin ব্যবহার করতে পারবেন।"
        )
        return

    await update.message.reply_text(
        "📢 <b>BROADCAST MODE</b>\n\n"
        "এখন যে Message / Photo / Video / File / Audio পাঠাবে,\n"
        "সেটা Test Group-এ পাঠানো হবে।\n\n"
        "❌ বন্ধ করতে /cancel লিখো।",
        parse_mode="HTML"
    )


# =========================
# ADMIN CONTENT → GROUP
# =========================

async def admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user or (user.username or "").lower() != ADMIN_USERNAME.lower():
        return

    message = update.message

    try:

        if message.text:

            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=message.text,
                reply_markup=buttons()
            )

        elif message.photo:

            await context.bot.send_photo(
                chat_id=GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=message.caption or "",
                reply_markup=buttons()
            )

        elif message.video:

            await context.bot.send_video(
                chat_id=GROUP_ID,
                video=message.video.file_id,
                caption=message.caption or "",
                reply_markup=buttons()
            )

        elif message.document:

            await context.bot.send_document(
                chat_id=GROUP_ID,
                document=message.document.file_id,
                caption=message.caption or "",
                reply_markup=buttons()
            )

        elif message.audio:

            await context.bot.send_audio(
                chat_id=GROUP_ID,
                audio=message.audio.file_id,
                caption=message.caption or "",
                reply_markup=buttons()
            )

        else:
            await update.message.reply_text(
                "⚠️ এই ধরনের ফাইল এখনো সাপোর্ট করা হয়নি।"
            )
            return

        await update.message.reply_text(
            "✅ <b>POST SENT</b>\n\n"
            "📡 Test Group-এ সফলভাবে পাঠানো হয়েছে।",
            parse_mode="HTML"
        )

    except Exception as error:

        print("ERROR:", error)

        await update.message.reply_text(
            "❌ Group-এ পাঠানো যায়নি।\n\n"
            "চেক করো:\n"
            "• Bot Group-এর Admin কিনা\n"
            "• GROUP_ID ঠিক আছে কিনা"
        )


# =========================
# CANCEL
# =========================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user:
        if (update.effective_user.username or "").lower() == ADMIN_USERNAME.lower():

            await update.message.reply_text(
                "❌ Broadcast বন্ধ করা হয়েছে।"
            )


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(CommandHandler("cancel", cancel))

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            new_member
        )
    )

    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            admin_message
        )
    )

    print("🔥 COMRADE BOT is running...")

    app.run_polling()


if __name__ == "__main__":
    main()