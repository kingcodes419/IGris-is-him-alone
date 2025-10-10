from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)
import re
import os
from threading import Thread
from flask import Flask

from king.menu import king_menu, summon_igris_callback
from king.scan import scanip
from king.getip import getip
from king.echo import echo
from king.king import king
from king.ping import ping, alive
from king.play import play
from king.show import show
from king.url import url_command
from king.img import img
from king.start import start, view_menu_callback
from king.whois import run_whois
from king.igris import ask_igris

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = "8254458626:AAHwhFEuRKs9OS2YLgCsWFneUsaI8UThMfw"
KING_ID = 6966542803
BOT_USERNAME = "@igris_MDbot"


# ---------------- WHOIS COMMAND ----------------
async def whois_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /whois <domain>")
        return

    domain = context.args[0]
    info = run_whois(domain)
    await update.message.reply_text(info)


# ---------------- AI AUTO-CHAT ----------------
async def ai_auto_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    msg_lower = message.lower()

    code_only = False
    if (
        ("code" in msg_lower and (
            "start" in msg_lower or "make" in msg_lower or "create" in msg_lower))
        and ("python" in msg_lower or "code" in msg_lower)
    ):
        code_only = True

    if update.effective_chat.type == "private":
        reply = ask_igris(message, chat_id, user_id, code_only=code_only)
        await send_copyable_message(update, reply)
        return

    is_reply_to_bot = update.message.reply_to_message and \
        update.message.reply_to_message.from_user.username == BOT_USERNAME.strip("@")
    mentioned = "igris" in msg_lower or "arise" in msg_lower

    if is_reply_to_bot or mentioned:
        reply = ask_igris(message, chat_id, user_id, code_only=code_only)
        await send_copyable_message(update, reply)


async def send_copyable_message(update: Update, text: str):
    markup = None
    code_match = re.search(r"```(.*?)```", text, re.DOTALL)
    if code_match:
        code_only = code_match.group(1).strip()
        button = InlineKeyboardButton(
            "📋 Copy Code", switch_inline_query_current_chat=code_only)
        markup = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)


# ---------------- KEEP ALIVE ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "🛡️ Igris Sentinel is awake — Render ping successful 👑"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()


# ---------------- MAIN ----------------
def main():
    keep_alive()  # ✅ keep the service alive on Render

    app_bot = Application.builder().token(TELEGRAM_TOKEN).build()

    summon_igris_handler = CallbackQueryHandler(summon_igris_callback, pattern="^arise$")
    ping_handler = CommandHandler("ping", ping)
    show_handler = CommandHandler("unveil", show)
    alive_handler = CommandHandler("alive", alive)
    king_handler = CommandHandler("echo", echo)
    king_shi = CommandHandler("king", king)
    scanips = CommandHandler("scan", scanip)
    getips = CommandHandler("getip", getip)
    start_handler = CommandHandler("start", start)
    menu_button_handler = CallbackQueryHandler(view_menu_callback, pattern="^view_menu$")
    whois_handler = CommandHandler("whois", whois_command)
    play_handler = CommandHandler("play", play)

    app_bot.add_handler(king_handler)
    app_bot.add_handler(play_handler)
    app_bot.add_handler(show_handler)
    app_bot.add_handler(start_handler)
    app_bot.add_handler(menu_button_handler)
    app_bot.add_handler(scanips)
    app_bot.add_handler(summon_igris_handler)
    app_bot.add_handler(king_shi)
    app_bot.add_handler(getips)
    app_bot.add_handler(CommandHandler("url", url_command))
    app_bot.add_handler(CommandHandler("menu", king_menu))
    app_bot.add_handler(img)
    app_bot.add_handler(ping_handler)
    app_bot.add_handler(alive_handler)
    app_bot.add_handler(whois_handler)
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_auto_chat))

    print("🤖 Igris is online... [Engine: OpenAI]")
    app_bot.run_polling()


if __name__ == "__main__":
    main()
