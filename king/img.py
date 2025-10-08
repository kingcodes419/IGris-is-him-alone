# king/img.py
import requests
import re
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

GOOGLE_API_KEY = "AIzaSyCUBpsfAHACYSQ8yR_3L3A0fNp0UxH3pKU"
SEARCH_ENGINE_ID = "f59f665774aaf41bd"   # from Google Custom Search Engine


async def img_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("📸 Usage: /img car |5", parse_mode="Markdown")
        return

    # Split query and number
    match = re.match(r"(.+)\s*\|\s*(\d+)", query)
    if match:
        search_query, limit = match.group(1).strip(), int(match.group(2))
    else:
        search_query, limit = query, 1

    await update.message.reply_text(f"🔍 Searching {search_query} ({limit} pics)...", parse_mode="Markdown")

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": search_query,
            "cx": SEARCH_ENGINE_ID,
            "key": GOOGLE_API_KEY,
            "searchType": "image",
            "num": min(limit, 10)  # Google max 10 per request
        }

        res = requests.get(url, params=params)
        data = res.json()

        if "items" not in data or not data["items"]:
            await update.message.reply_text("❌ No images found.")
            return

        for item in data["items"][:limit]:
            await update.message.reply_photo(photo=item["link"])

    except Exception as e:
        await update.message.reply_text(f"💀 Failed to fetch images: {e}")

# handler to be added in bot.py
img = CommandHandler("img", img_command)
