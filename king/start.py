from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from king.menu import king_menu  # import your existing menu function

# --- /start command ---


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👑 View Igris Menu", callback_data="view_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👹 *The Demon King Watches You* 👹\n\n"
        "💀 Mortal, you dare step into the realm of Igris?\n"
        "Bow before the might of the Demon King and press the button below to continue...",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# --- Button callback ---


async def view_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Directly call the menu function
    await king_menu(update, context)

# --- CommandHandlers for main.py ---
start_handler = CommandHandler("start", start)
menu_button_handler = CallbackQueryHandler(
    view_menu_callback, pattern="^view_menu$")
