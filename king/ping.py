import time
import random
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# --- PING COMMAND ---


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    message = await update.message.reply_text("⚔️ Igris prepares to strike...")
    end_time = time.time()
    latency = (end_time - start_time) * 1000

    responses = [
        f"⚔️ Igris strikes in {latency:.2f} ms — swift and precise.",
        f"🔥 The blade sings in {latency:.2f} ms.",
        f"🛡️ The realm obeys in {latency:.2f} ms, my liege.",
        f"👑 Shadows answer your call in {latency:.2f} ms.",
        f"⚔️ Loyalty delivered in {latency:.2f} ms — for the Monarch!",
    ]

    await message.edit_text(random.choice(responses))

ping_handler = CommandHandler("ping", ping)

# --- ALIVE COMMAND ---


async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    responses = [
        "👑 Igris kneels before you, King. The shadows stir at your command.",
        "⚔️ Ever vigilant, Igris stands ready to fight at your side.",
        "🔥 From the abyss I rise, awaiting your next order, Monarch.",
        "🛡️ My loyalty is eternal, King. The realm is safe under my watch.",
        "👤 Igris, your shadow knight, breathes unbroken — alive and awaiting battle.",
    ]

    await update.message.reply_text(random.choice(responses))

alive_handler = CommandHandler("alive", alive)
