import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def king(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚔️👑⚔️\n"
        "*The King has risen!*\n\n"
        "Mortals, witness the might of the realm. Step forward and be seen by your sovereign.\n\n"
        "🌐 [Enter the King’s Realm](https://i-gris.vercel.app/echo)\n\n"
        "The throne is mine, the shadows obey, and the King’s gaze never falters. Tremble mortals! ⚡",
        parse_mode="Markdown"  # <-- Add this
    )

king_shi = CommandHandler("king", king)
