from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode
import json
import os
import asyncio


# ==================================================
# BOT TOKEN
# ==================================================

TOKEN = "8772299501:AAF0a-tMhE1IvlTSx66VWsywzqrlKOMFghY"


# ==================================================
# ADMIN
# ==================================================

ADMIN_USERNAME = "Jin_woo_28"


# ==================================================
# USER DATABASE
# ==================================================

USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return set()

    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)

        return set(data)

    except Exception:
        return set()


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(list(users), f)


def add_user(user_id):
    users = load_users()

    if user_id not in users:
        users.add(user_id)
        save_users(users)


# ==================================================
# WELCOME MESSAGE
# ==================================================

def welcome_text(user, member_count):

    name = user.full_name
    username = f"@{user.username}" if user.username else "Not Set"

    return f"""
✨ <b>WELCOME TO COMRADE</b> ✨

👤 <b>Name</b>           : {name}
🆔 <b>Username</b>       : {username}
👥 <b>Group Members</b>  : {member_count}

🎉 <b>অভিনন্দন, {name}!</b>

💎 আমাদের <b>Comrade Support Group</b>-এ
আপনাকে স্বাগতম!

⚡ প্রয়োজনীয় Bot ব্যবহার করতে
নিচের Button থেকে নির্বাচন করুন।

🛡️ <b>COMRADE TEAM</b>

━━━━━━━━━━━━━━━━━━
🤝 Together We Grow
━━━━━━━━━━━━━━━━━━
"""


# ==================================================
# BUTTONS
# ==================================================

def welcome_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "🤖 COMRADE BOT",
                url="https://t.me/Comrade_sms_bot"
            ),
            InlineKeyboardButton(
                "🔵 COMRADE OTP",
                url="https://t.me/Comrade_sms_OTP"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ==================================================
# /START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user:
        return

    # User database-এ save
    add_user(user.id)

    print(
        f"👤 User: {user.full_name} | "
        f"ID: {user.id} | "
        f"Username: @{user.username if user.username else 'None'}"
    )

    # Member count
    member_count = 0

    try:
        member_count = await context.bot.get_chat_member_count(
            update.effective_chat.id
        )
    except Exception:
        pass

    text = welcome_text(user, member_count)
    buttons = welcome_buttons()

    # Profile photo
    try:
        photos = await context.bot.get_user_profile_photos(
            user.id,
            limit=1
        )

        if photos.total_count > 0:

            photo = photos.photos[0][-1].file_id

            await update.message.reply_photo(
                photo=photo,
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=buttons
            )

            return

    except Exception:
        pass

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=buttons
    )


# ==================================================
# NEW MEMBER JOIN
# ==================================================

async def new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if not update.message.new_chat_members:
        return

    for user in update.message.new_chat_members:

        if user.is_bot:
            continue

        # User save
        add_user(user.id)

        print(
            f"🆕 New Member: {user.full_name} | "
            f"ID: {user.id}"
        )

        # Member count
        try:
            member_count = await context.bot.get_chat_member_count(
                update.effective_chat.id
            )
        except Exception:
            member_count = 0

        text = welcome_text(user, member_count)
        buttons = welcome_buttons()

        # Profile photo
        try:
            photos = await context.bot.get_user_profile_photos(
                user.id,
                limit=1
            )

            if photos.total_count > 0:

                photo = photos.photos[0][-1].file_id

                await update.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=buttons
                )

                continue

        except Exception:
            pass

        await update.message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons
        )


# ==================================================
# /BROADCAST
# ==================================================

async def broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not user:
        return

    # শুধু Admin ব্যবহার করতে পারবে
    if not user.username:
        await update.message.reply_text(
            "⛔ Admin access denied."
        )
        return

    if user.username.lower() != ADMIN_USERNAME.lower():

        await update.message.reply_text(
            "⛔ এই Command শুধুমাত্র Admin-এর জন্য।"
        )

        return

    # Reply message আছে কিনা
    replied_message = update.message.reply_to_message

    # /broadcast এর পরে সরাসরি text
    command_text = update.message.text or ""

    users = load_users()

    if not users:

        await update.message.reply_text(
            "⚠️ এখনো কোনো registered user পাওয়া যায়নি।"
        )

        return

    # ------------------------------------------
    # Broadcast message নির্বাচন
    # ------------------------------------------

    if replied_message is None:

        parts = command_text.split(" ", 1)

        if len(parts) < 2:

            await update.message.reply_text(
                "📢 Broadcast করার নিয়ম:\n\n"
                "কোনো Message-এর উপর Reply করে "
                "/broadcast লিখুন।\n\n"
                "অথবা সরাসরি:\n"
                "/broadcast তোমার মেসেজ"
            )

            return

        message_text = parts[1]

    else:

        message_text = None

    await update.message.reply_text(
        f"📢 <b>BROADCAST STARTED</b>\n\n"
        f"👥 Total Users: <b>{len(users)}</b>\n"
        f"⏳ Sending...",
        parse_mode=ParseMode.HTML
    )

    success = 0
    failed = 0

    # ------------------------------------------
    # Send Broadcast
    # ------------------------------------------

    for user_id in users:

        try:

            if replied_message:

                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=update.effective_chat.id,
                    message_id=replied_message.message_id
                )

            else:

                await context.bot.send_message(
                    chat_id=user_id,
                    text=message_text
                )

            success += 1

            # Telegram rate limit কমানোর জন্য
            await asyncio.sleep(0.05)

        except Exception as e:

            failed += 1

            print(
                f"❌ Broadcast failed "
                f"User {user_id}: {e}"
            )

    # ------------------------------------------
    # Broadcast Result
    # ------------------------------------------

    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━\n"
        "📢 <b>BROADCAST COMPLETE</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"✅ Sent: <b>{success}</b>\n"
        f"❌ Failed: <b>{failed}</b>\n"
        f"👥 Total: <b>{len(users)}</b>\n\n"
        "🛡️ <b>COMRADE TEAM</b>",
        parse_mode=ParseMode.HTML
    )


# ==================================================
# TELEGRAM COMMAND MENU
# ==================================================

async def set_commands(application):

    commands = [
        BotCommand(
            "start",
            "Welcome message"
        ),
        BotCommand(
            "broadcast",
            "Admin broadcast"
        ),
    ]

    await application.bot.set_my_commands(
        commands
    )


# ==================================================
# MAIN
# ==================================================

def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(set_commands)
        .build()
    )

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # /broadcast
    app.add_handler(
        CommandHandler(
            "broadcast",
            broadcast
        )
    )

    # New member
    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            new_member
        )
    )

    print(
        "🔥 COMRADE WELCOME + BROADCAST BOT is running..."
    )

    app.run_polling()


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":
    main()