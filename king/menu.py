import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)
from king.igris import ask_igris  # Import your AI brain function here

# === VIDEO / MENU CONFIG ===
VIDEO_URL = "https://files.catbox.moe/4wf1bl.mp4"

# === MENU FUNCTION ===


async def king_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Demon King menu with video link + summon button"""
    keyboard = [
        [InlineKeyboardButton("⚔️ Summon Igris", callback_data="arise")],
        [InlineKeyboardButton(
            "📢 Join Channel", url="https://t.me/YourChannel")],
        [InlineKeyboardButton("📬 Contact K I N G",
                              url="https://t.me/IamKing419")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    menu_titles = [
        "👑 *📜 The Summons of Igris*",
        "🔥 *Throne of Igris*",
        "⚔️ *Igris’ Shadow Realm*",
        "💀 *Dominion of the Demon King*",
        "🛡️ *Igris, Eternal Sentinel*",
    ]

    message = update.message or update.callback_query.message

    caption_text = f"""
{random.choice(menu_titles)}

🖤 *Whispers of the Abyss:*
- /ping - Check bot responsiveness
- /play - Play music
- /img - Download images
- /url - Convert images to URL
- /alive - Check if bot is alive
- /echo - Hear the Echo of the King

☠️ *Dark Incantations:*
- /getip - Summon Mortal's Secrets
- /scan - Reveal the Shadow Realm
- /king - Bow to the King
- /whois - Expose the true name carved in a soul’s fate.
- /unveil - Expose the weak codes of any webs.
King shall unleash more soon enough...

👹 *Note:* Use commands wisely, mortal. The King watches all.
"""

    await message.reply_video(
        video=VIDEO_URL,
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

# === SUMMON CALLBACK (ARISE) ===


async def summon_igris_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """When 'Summon Igris' is clicked"""
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user_id = query.from_user.id

    # Step 1: Show cinematic typing delay
    await query.message.reply_chat_action("typing")
    await asyncio.sleep(1.5)
    await query.message.reply_text("🖤 Arise...")

    # Step 2: Ask the AI to respond as if user said "arise"
    ai_reply = ask_igris("arise", chat_id=chat_id, user_id=user_id)

    # Step 3: Send Igris' AI-generated response
    await query.message.reply_text(ai_reply)

# === HANDLERS ===
