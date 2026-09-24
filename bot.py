# -*- coding: utf-8 -*-

import json
import os
import html

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)


# =========================================================
#                    BOT CONFIG
# =========================================================

TOKEN = "8966531097:AAGtfafInd05YusUOeetONDdgISJjZSOGlM"

OWNER_USERNAME = "Jin_woo_28"

GROUP_ID = "@Comrade_Support_team"

COMRADE_BOT_USERNAME = "Comrade_sms_bot"
COMRADE_OTP_USERNAME = "Comrade_sms_OTP"

ADMINS_FILE = "admins.json"
WELCOME_FILE = "welcome.json"


# =========================================================
#                DEFAULT ADMINS
# =========================================================

DEFAULT_ADMINS = [
    "Chill2929",
    "oggy_39",
    "polash980",
]


# =========================================================
#                DEFAULT WELCOME MESSAGE
# =========================================================

DEFAULT_WELCOME = """💎 COMRADE WELCOME

অভিনন্দন {name}! 🎉

আপনাকে স্বাগতম
COMRADE SUPPORT GROUP-এ। 🤝

যেকোনো সাহায্য বা সমস্যার জন্য
আমাদের সাথে যোগাযোগ করুন।

⚡ Active থাকুন
💎 COMRADE ADMIN TEAM"""


# =========================================================
#                  CONVERSATION STATES
# =========================================================

ADD_ADMIN = 1
REMOVE_ADMIN = 2
EDIT_WELCOME = 3
BROADCAST = 4


# =========================================================
#                 FILE FUNCTIONS
# =========================================================

def load_admins():
    """Load admins from admins.json."""

    if not os.path.exists(ADMINS_FILE):
        data = {
            "admins": DEFAULT_ADMINS
        }

        save_json(ADMINS_FILE, data)
        return DEFAULT_ADMINS.copy()

    try:
        with open(ADMINS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        admins = data.get("admins", [])

        if not isinstance(admins, list):
            return DEFAULT_ADMINS.copy()

        return admins

    except Exception:
        return DEFAULT_ADMINS.copy()


def save_admins(admins):
    """Save admins to admins.json."""

    data = {
        "admins": admins
    }

    save_json(ADMINS_FILE, data)


def load_welcome():
    """Load welcome message."""

    if not os.path.exists(WELCOME_FILE):
        save_welcome(DEFAULT_WELCOME)
        return DEFAULT_WELCOME

    try:
        with open(WELCOME_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        message = data.get("welcome", DEFAULT_WELCOME)

        if not isinstance(message, str) or not message.strip():
            return DEFAULT_WELCOME

        return message

    except Exception:
        return DEFAULT_WELCOME


def save_welcome(message):
    """Save welcome message."""

    data = {
        "welcome": message
    }

    save_json(WELCOME_FILE, data)


def save_json(filename, data):
    """Save JSON safely."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )
    except Exception as e:
        print(f"JSON SAVE ERROR: {e}")


# =========================================================
#                    USER CHECK
# =========================================================

def normalize_username(username):
    if not username:
        return ""

    return username.replace("@", "").strip().lower()


def is_owner(user):
    if not user:
        return False

    username = normalize_username(user.username)

    return username == normalize_username(OWNER_USERNAME)


def is_admin(user):
    if not user:
        return False

    username = normalize_username(user.username)

    if username == normalize_username(OWNER_USERNAME):
        return True

    admins = load_admins()

    return username in [
        normalize_username(admin)
        for admin in admins
    ]


# =========================================================
#                    KEYBOARDS
# =========================================================

def get_welcome_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "🤎 COMRADE BOT",
                url=f"https://t.me/{COMRADE_BOT_USERNAME}"
            ),
            InlineKeyboardButton(
                "🔵 COMRADE OTP",
                url=f"https://t.me/{COMRADE_OTP_USERNAME}"
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_owner_panel():

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add Admin",
                callback_data="owner:add_admin"
            ),
            InlineKeyboardButton(
                "➖ Remove Admin",
                callback_data="owner:remove_admin"
            ),
        ],
        [
            InlineKeyboardButton(
                "📋 Admin List",
                callback_data="owner:admins"
            ),
        ],
        [
            InlineKeyboardButton(
                "✏️ Edit Welcome",
                callback_data="owner:edit_welcome"
            ),
            InlineKeyboardButton(
                "👀 Preview Welcome",
                callback_data="owner:preview_welcome"
            ),
        ],
        [
            InlineKeyboardButton(
                "📢 Send Broadcast",
                callback_data="broadcast:start"
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_admin_panel():

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Send Broadcast",
                callback_data="broadcast:start"
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="panel:back"
                )
            ]
        ]
    )


def get_cancel_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="action:cancel"
                )
            ]
        ]
    )


# =========================================================
#                 OWNER / ADMIN PANEL
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not user:
        return

    # Owner
    if is_owner(user):

        await update.message.reply_text(
            "👑 <b>COMRADE OWNER PANEL</b>\n\n"
            "স্বাগতম Owner! 💎\n\n"
            "নিচের Button থেকে একটি Action নির্বাচন করুন।",
            parse_mode="HTML",
            reply_markup=get_owner_panel()
        )

        return

    # Admin
    if is_admin(user):

        await update.message.reply_text(
            "🛡️ <b>COMRADE ADMIN PANEL</b>\n\n"
            "আপনার Admin Access সক্রিয় আছে।\n\n"
            "নিচের Button ব্যবহার করুন।",
            parse_mode="HTML",
            reply_markup=get_admin_panel()
        )

        return

    # Normal user
    message = load_welcome()

    message = message.replace(
        "{name}",
        user.full_name
    )

    await update.message.reply_text(
        message,
        reply_markup=get_welcome_keyboard()
    )


# =========================================================
#                OWNER BUTTON HANDLER
# =========================================================

async def owner_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    user = update.effective_user

    await query.answer()

    if not is_owner(user):
        await query.answer(
            "❌ শুধুমাত্র Owner এই Action ব্যবহার করতে পারবেন।",
            show_alert=True
        )
        return ConversationHandler.END

    action = query.data

    # ---------------- ADD ADMIN ----------------

    if action == "owner:add_admin":

        await query.message.reply_text(
            "➕ <b>Add Admin</b>\n\n"
            "যে Username-কে Admin করতে চান সেটি পাঠান।\n\n"
            "উদাহরণ:\n"
            "<code>username</code>\n"
            "অথবা\n"
            "<code>@username</code>",
            parse_mode="HTML",
            reply_markup=get_cancel_button()
        )

        return ADD_ADMIN

    # ---------------- REMOVE ADMIN ----------------

    if action == "owner:remove_admin":

        admins = load_admins()

        if not admins:

            await query.message.reply_text(
                "📋 বর্তমানে কোনো Admin নেই।",
                reply_markup=get_back_button()
            )

            return ConversationHandler.END

        text = "➖ <b>Remove Admin</b>\n\n"
        text += "যে Admin-কে Remove করতে চান তার Username পাঠান।\n\n"
        text += "বর্তমান Admin:\n\n"

        for index, admin in enumerate(admins, 1):
            text += f"{index}. @{admin}\n"

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=get_cancel_button()
        )

        return REMOVE_ADMIN

    # ---------------- ADMIN LIST ----------------

    if action == "owner:admins":

        admins = load_admins()

        text = "📋 <b>COMRADE ADMIN LIST</b>\n\n"
        text += f"👑 Owner: @{OWNER_USERNAME}\n\n"

        if admins:
            for index, admin in enumerate(admins, 1):
                text += f"🛡️ {index}. @{admin}\n"
        else:
            text += "কোনো additional admin নেই।"

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=get_back_button()
        )

        return ConversationHandler.END

    # ---------------- EDIT WELCOME ----------------

    if action == "owner:edit_welcome":

        current = load_welcome()

        text = (
            "✏️ <b>EDIT WELCOME MESSAGE</b>\n\n"
            "নতুন Welcome Message পাঠান।\n\n"
            "👤 নতুন মেম্বারের নাম বসাতে:\n"
            "<code>{name}</code>\n\n"
            "উদাহরণ:\n"
            "<code>💎 স্বাগতম {name}! 🎉</code>\n\n"
            "বর্তমান Message:\n\n"
            f"{html.escape(current)}"
        )

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=get_cancel_button()
        )

        return EDIT_WELCOME

    # ---------------- PREVIEW ----------------

    if action == "owner:preview_welcome":

        welcome = load_welcome()

        preview = welcome.replace(
            "{name}",
            "COMRADE USER"
        )

        await query.message.reply_text(
            "👀 <b>WELCOME PREVIEW</b>\n\n"
            + html.escape(preview),
            parse_mode="HTML",
            reply_markup=get_back_button()
        )

        return ConversationHandler.END

    return ConversationHandler.END


# =========================================================
#                    ADD ADMIN
# =========================================================

async def add_admin_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_owner(user):
        return ConversationHandler.END

    username = normalize_username(
        update.message.text
    )

    if not username:
        await update.message.reply_text(
            "❌ Username সঠিক নয়। আবার পাঠান।",
            reply_markup=get_cancel_button()
        )

        return ADD_ADMIN

    if username == normalize_username(OWNER_USERNAME):

        await update.message.reply_text(
            "❌ Owner-কে Admin হিসেবে Add করার প্রয়োজন নেই।",
            reply_markup=get_back_button()
        )

        return ConversationHandler.END

    admins = load_admins()

    normalized_admins = [
        normalize_username(admin)
        for admin in admins
    ]

    if username in normalized_admins:

        await update.message.reply_text(
            f"⚠️ @{username} ইতিমধ্যেই Admin।",
            reply_markup=get_back_button()
        )

        return ConversationHandler.END

    admins.append(username)

    save_admins(admins)

    await update.message.reply_text(
        f"✅ <b>Admin Added Successfully!</b>\n\n"
        f"🛡️ Username: @{username}",
        parse_mode="HTML",
        reply_markup=get_back_button()
    )

    return ConversationHandler.END


# =========================================================
#                  REMOVE ADMIN
# =========================================================

async def remove_admin_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_owner(user):
        return ConversationHandler.END

    username = normalize_username(
        update.message.text
    )

    admins = load_admins()

    found = None

    for admin in admins:
        if normalize_username(admin) == username:
            found = admin
            break

    if found is None:

        await update.message.reply_text(
            f"❌ @{username} Admin List-এ নেই।",
            reply_markup=get_back_button()
        )

        return ConversationHandler.END

    admins.remove(found)

    save_admins(admins)

    await update.message.reply_text(
        f"✅ <b>Admin Removed!</b>\n\n"
        f"👤 @{username}",
        parse_mode="HTML",
        reply_markup=get_back_button()
    )

    return ConversationHandler.END


# =========================================================
#                EDIT WELCOME TEXT
# =========================================================

async def edit_welcome_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_owner(user):
        return ConversationHandler.END

    new_message = update.message.text

    if not new_message.strip():

        await update.message.reply_text(
            "❌ Welcome Message খালি রাখা যাবে না।",
            reply_markup=get_cancel_button()
        )

        return EDIT_WELCOME

    if len(new_message) > 4000:

        await update.message.reply_text(
            "❌ Message অনেক বড়। সর্বোচ্চ 4000 characters ব্যবহার করুন।",
            reply_markup=get_cancel_button()
        )

        return EDIT_WELCOME

    save_welcome(new_message)

    await update.message.reply_text(
        "✅ <b>Welcome Message Updated!</b>\n\n"
        "এখন থেকে নতুন Member Join করলে "
        "এই নতুন Message automatically যাবে।\n\n"
        "👤 <code>{name}</code> ব্যবহার করলে "
        "নতুন Member-এর নাম বসবে।",
        parse_mode="HTML",
        reply_markup=get_back_button()
    )

    return ConversationHandler.END


# =========================================================
#                  CANCEL ACTION
# =========================================================

async def cancel_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "❌ Action Cancelled.",
            reply_markup=get_back_button()
        )

    return ConversationHandler.END


async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "❌ Action Cancelled.",
        reply_markup=get_back_button()
    )

    return ConversationHandler.END


# =========================================================
#                  BACK TO PANEL
# =========================================================

async def back_to_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    user = update.effective_user

    await query.answer()

    if is_owner(user):

        await query.message.reply_text(
            "👑 <b>COMRADE OWNER PANEL</b>",
            parse_mode="HTML",
            reply_markup=get_owner_panel()
        )

    elif is_admin(user):

        await query.message.reply_text(
            "🛡️ <b>COMRADE ADMIN PANEL</b>",
            parse_mode="HTML",
            reply_markup=get_admin_panel()
        )

    else:

        await query.message.reply_text(
            "❌ Access Denied."
        )

    return ConversationHandler.END


# =========================================================
#                   BROADCAST
# =========================================================

async def start_broadcast(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user):

        if update.callback_query:
            await update.callback_query.answer(
                "❌ আপনার Broadcast Permission নেই।",
                show_alert=True
            )

        return ConversationHandler.END

    if update.callback_query:

        query = update.callback_query
        await query.answer()

        await query.message.reply_text(
            "📢 <b>BROADCAST MODE</b>\n\n"
            "যে Message / Photo / Video / File Group-এ পাঠাতে চান "
            "সেটি এখন পাঠান।\n\n"
            "একটি Message পাঠালেই সেটি Group-এ যাবে।\n\n"
            "❌ বন্ধ করতে Cancel চাপুন।",
            parse_mode="HTML",
            reply_markup=get_cancel_button()
        )

    else:

        await update.message.reply_text(
            "📢 <b>BROADCAST MODE</b>\n\n"
            "যে Message / Photo / Video / File Group-এ পাঠাতে চান "
            "সেটি এখন পাঠান।",
            parse_mode="HTML",
            reply_markup=get_cancel_button()
        )

    return BROADCAST


# =========================================================
#              BROADCAST FRAME
# =========================================================

def create_broadcast_frame(text):

    return (
        "╔════════════════════════════╗\n"
        "║      🏆 COMRADE সুখবর      ║\n"
        "╠════════════════════════════╣\n"
        "║                            ║\n"
        f"{text}\n"
        "║                            ║\n"
        "╠════════════════════════════╣\n"
        "║      💎 COMRADE TEAM       ║\n"
        "╚════════════════════════════╝"
    )


# =========================================================
#               BROADCAST MESSAGE
# =========================================================

async def broadcast_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user):
        return ConversationHandler.END

    message = update.message

    try:

        # ---------------- TEXT ----------------

        if message.text:

            framed = create_broadcast_frame(
                message.text
            )

            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=framed
            )

        # ---------------- PHOTO ----------------

        elif message.photo:

            caption = message.caption or ""

            if caption:
                caption = create_broadcast_frame(caption)

            await context.bot.send_photo(
                chat_id=GROUP_ID,
                photo=message.photo[-1].file_id,
                caption=caption if caption else None
            )

        # ---------------- VIDEO ----------------

        elif message.video:

            caption = message.caption or ""

            if caption:
                caption = create_broadcast_frame(caption)

            await context.bot.send_video(
                chat_id=GROUP_ID,
                video=message.video.file_id,
                caption=caption if caption else None
            )

        # ---------------- DOCUMENT ----------------

        elif message.document:

            caption = message.caption or ""

            if caption:
                caption = create_broadcast_frame(caption)

            await context.bot.send_document(
                chat_id=GROUP_ID,
                document=message.document.file_id,
                caption=caption if caption else None
            )

        # ---------------- AUDIO ----------------

        elif message.audio:

            caption = message.caption or ""

            if caption:
                caption = create_broadcast_frame(caption)

            await context.bot.send_audio(
                chat_id=GROUP_ID,
                audio=message.audio.file_id,
                caption=caption if caption else None
            )

        # ---------------- VOICE ----------------

        elif message.voice:

            await context.bot.send_voice(
                chat_id=GROUP_ID,
                voice=message.voice.file_id
            )

        # ---------------- STICKER ----------------

        elif message.sticker:

            await context.bot.send_sticker(
                chat_id=GROUP_ID,
                sticker=message.sticker.file_id
            )

        # ---------------- ANIMATION/GIF ----------------

        elif message.animation:

            caption = message.caption or ""

            if caption:
                caption = create_broadcast_frame(caption)

            await context.bot.send_animation(
                chat_id=GROUP_ID,
                animation=message.animation.file_id,
                caption=caption if caption else None
            )

        else:

            await update.message.reply_text(
                "❌ এই ধরনের Message Broadcast করা এখনো supported নয়।",
                reply_markup=get_back_button()
            )

            return ConversationHandler.END

        await update.message.reply_text(
            "✅ <b>Broadcast Sent Successfully!</b>\n\n"
            "📢 Group-এ আপনার Broadcast পাঠানো হয়েছে।",
            parse_mode="HTML",
            reply_markup=get_back_button()
        )

    except Exception as e:

        print(f"BROADCAST ERROR: {e}")

        await update.message.reply_text(
            "❌ Broadcast পাঠানো যায়নি।\n\n"
            "Group ID, Bot Permission এবং Bot Admin status check করুন.",
            reply_markup=get_back_button()
        )

    return ConversationHandler.END


# =========================================================
#                AUTOMATIC WELCOME
# =========================================================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    new_members = update.message.new_chat_members

    if not new_members:
        return

    welcome_template = load_welcome()

    for member in new_members:

        # Bot হলে Welcome দেবে না
        if member.is_bot:
            continue

        member_name = member.full_name

        # {name} replace
        welcome_text = welcome_template.replace(
            "{name}",
            member_name
        )

        try:

            await update.message.reply_text(
                welcome_text,
                reply_markup=get_welcome_keyboard()
            )

        except Exception as e:

            print(f"WELCOME ERROR: {e}")


# =========================================================
#                    COMMAND PANEL
# =========================================================

async def panel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user):

        await update.message.reply_text(
            "❌ আপনার Admin Permission নেই।"
        )

        return

    if is_owner(user):

        await update.message.reply_text(
            "👑 <b>COMRADE OWNER PANEL</b>",
            parse_mode="HTML",
            reply_markup=get_owner_panel()
        )

    else:

        await update.message.reply_text(
            "🛡️ <b>COMRADE ADMIN PANEL</b>",
            parse_mode="HTML",
            reply_markup=get_admin_panel()
        )


# =========================================================
#                   ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print(
        "ERROR:",
        context.error
    )


# =========================================================
#                       MAIN
# =========================================================

def main():

    print("====================================")
    print("       COMRADE SUKHOBOR BOT")
    print("====================================")
    print("Bot is starting...")
    print("Owner:", OWNER_USERNAME)
    print("Group:", GROUP_ID)

    # Create files if missing
    load_admins()
    load_welcome()

    # Build application
    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # =====================================================
    # OWNER / ADMIN CONVERSATION
    # =====================================================

    owner_conversation = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                owner_button,
                pattern=r"^owner:"
            ),

            CallbackQueryHandler(
                start_broadcast,
                pattern=r"^broadcast:start$"
            ),

            CommandHandler(
                "broadcast",
                start_broadcast
            ),
        ],

        states={

            ADD_ADMIN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    add_admin_text
                ),
            ],

            REMOVE_ADMIN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    remove_admin_text
                ),
            ],

            EDIT_WELCOME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_welcome_text
                ),
            ],

            BROADCAST: [
                MessageHandler(
                    filters.ALL & ~filters.COMMAND,
                    broadcast_message
                ),
            ],
        },

        fallbacks=[
            CallbackQueryHandler(
                cancel_action,
                pattern=r"^action:cancel$"
            ),

            CommandHandler(
                "cancel",
                cancel_command
            ),
        ],

        allow_reentry=True,
    )

    application.add_handler(
        owner_conversation
    )

    # =====================================================
    # PANEL
    # =====================================================

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "panel",
            panel_command
        )
    )

    # =====================================================
    # BACK BUTTON
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            back_to_panel,
            pattern=r"^panel:back$"
        )
    )

    # =====================================================
    # CANCEL BUTTON
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            cancel_action,
            pattern=r"^action:cancel$"
        )
    )

    # =====================================================
    # AUTOMATIC WELCOME
    # =====================================================

    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )

    # =====================================================
    # ERROR HANDLER
    # =====================================================

    application.add_error_handler(
        error_handler
    )

    # =====================================================
    # START BOT
    # =====================================================

    print("Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
#                    RUN
# =========================================================

if __name__ == "__main__":
    main()