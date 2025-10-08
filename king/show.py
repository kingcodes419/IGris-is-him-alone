import os
import re
import wget
import zipfile
from telegram import Update
from telegram.ext import ContextTypes


def sanitize_filename(name: str) -> str:
    """Remove bad characters from folder names"""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)


async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unveil <url>")
        return

    url = context.args[0]
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    safe_name = sanitize_filename(url.replace("://", "_").replace("/", "_"))
    folder_name = os.path.join("websites", safe_name)
    os.makedirs(folder_name, exist_ok=True)
    zip_path = os.path.join("websites", f"{safe_name}.zip")

    try:
        await update.message.reply_text(f"🕸️ Unveiling the source of {url}...")

        # Download the raw HTML source code
        file_path = os.path.join(folder_name, "index.html")
        wget.download(url, out=file_path)

        # Create zip file of the folder
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_name):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, folder_name)
                    zipf.write(full_path, rel_path)

        # Send the zip file back
        if os.path.getsize(zip_path) > 50 * 1024 * 1024:  # 50MB limit
            await update.message.reply_text("⚠️ File too large to send via Telegram.")
        else:
            await update.message.reply_document(document=open(zip_path, "rb"))

        await update.message.reply_text("✅ Source unveiled successfully.")

    except Exception as e:
        await update.message.reply_text(f"💀 Error while unveiling: {e}")
