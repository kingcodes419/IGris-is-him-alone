import os
import yt_dlp
from telegram.ext import CommandHandler

async def play(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("🎵 Tell me the song name, mortal!")
        return

    await update.message.reply_text(f"🎶 Summoning '{query}' from the void...")

    if os.path.exists("song.mp3"):
        try:
            os.remove("song.mp3")
        except:
            pass

    try:
        cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "ignoreerrors": True,
            "geo_bypass": True,
            "cookiefile": cookies_file,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)

            if not info or "entries" not in info or not info["entries"]:
                await update.message.reply_text("❌ No results found, mortal.")
                return

            entry = info["entries"][0]
            title = entry.get("title", "Unknown Song")

        if not os.path.exists("song.mp3"):
            await update.message.reply_text("❌ YouTube blocked the download — try again later.")
            return

        await update.message.reply_audio(audio=open("song.mp3", "rb"), title=title)
        await update.message.reply_text(f"✅ Song delivered, mortal — *{title}*")

        os.remove("song.mp3")

    except Exception as e:
        await update.message.reply_text(f"❌ Couldn’t fetch song:\n`{str(e)}`")
