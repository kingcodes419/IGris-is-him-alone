import os
import yt_dlp
from telegram.ext import CommandHandler

# === /play COMMAND ===


async def play(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("🎵 Tell me the song name, mortal!")
        return

    await update.message.reply_text(f"🎶 Summoning '{query}' from the void...")

    # Remove old song file if it exists
    if os.path.exists("song.mp3"):
        try:
            os.remove("song.mp3")
        except:
            pass

    try:
        ydl_opts = {
            "format": "bestaudio/best",  # auto picks best available format
            "outtmpl": "song.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "ignoreerrors": True,
            "geo_bypass": True,  # skip region locks
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # search for the query
            info = ydl.extract_info(f"ytsearch:{query}", download=True)

            if not info or "entries" not in info or not info["entries"]:
                await update.message.reply_text("❌ Give me something worthy to play , mortal.")
                return

            entry = info["entries"][0]
            title = entry.get("title", "Unknown Song")

        # Check if file exists before sending
        if not os.path.exists("song.mp3"):
            await update.message.reply_text("❌ The audio vanished into the void — try another song.")
            return

        # Send the audio file
        await update.message.reply_audio(audio=open("song.mp3", "rb"), title=title)
        await update.message.reply_text(f"✅ Song delivered, mortal — *{title}*")

        # Cleanup
        os.remove("song.mp3")

    except Exception as e:
        await update.message.reply_text(f"❌ Couldn’t fetch song:\n`{str(e)}`")

# --- ADD HANDLER IN MAIN.PY ---
