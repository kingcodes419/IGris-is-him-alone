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


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

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

    app.add_handler(king_handler)
    app.add_handler(play_handler)
    app.add_handler(show_handler)
    app.add_handler(start_handler)
    app.add_handler(menu_button_handler)
    app.add_handler(scanips)
    app.add_handler(summon_igris_handler)
    app.add_handler(king_shi)
    app.add_handler(getips)
    app.add_handler(CommandHandler("url", url_command))
    app.add_handler(CommandHandler("menu", king_menu))
    app.add_handler(img)
    app.add_handler(ping_handler)
    app.add_handler(alive_handler)
    app.add_handler(whois_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_auto_chat))

    print("🤖 Igris is online... [Engine: OpenAI]")
    app.run_polling()


# 🧠 KEEP ALIVE ON RENDER
import os
if os.environ.get("RENDER") == "true":
    import threading
    import http.server
    import socketserver

    def fake_server():
        port = int(os.environ.get("PORT", 10000))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()

    threading.Thread(target=fake_server, daemon=True).start()

if __name__ == "__main__":
    main()
