import requests
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

CATBOX_API = "https://catbox.moe/user/api.php"

# -------- Function to upload --------
def upload_to_catbox(file_path: str):
    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        data = {"reqtype": "fileupload"}
        r = requests.post(CATBOX_API, data=data, files=files)
        return r.text.strip()  # Direct URL

# -------- Command: /url --------
async def url_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("⚠️ Reply to an image with /url, mortal.")
        return

    # Get the highest resolution photo
    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    # Save temp file
    file_path = f"temp_{photo.file_id}.jpg"
    await file.download_to_drive(file_path)

    try:
        url = upload_to_catbox(file_path)
        await update.message.reply_text(f"✅ Uploaded: {url}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {e}")

# -------- Add Handler -------
url = (CommandHandler("url", url_command))