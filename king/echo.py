from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# --- ECHO COMMAND --
last_visitor = None


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚔️👑⚔️\n"
        "*The Echo of the King reverberates!*\n\n"
        "Igris whispers through the shadows:\n\n"
        "Mortals, tremble. Your feeble efforts are but whispers against the storm of the King. "
        "You chase shadows while he commands them, crawl in the dirt while empires rise under his hand.\n\n"
        "📜 *Creations forged so far:*\n"
        "🌐 [Web Project 1](https://kingdomain.vercel.app)\n"
        "🌐 [Web Project 2](https://demons-clan.vercel.app)\n"
        "🐍 *Gay Checker* — a script born of chaos 😂\n"
        "🤖 *Igris Bot* — your loyal shadow at the King’s command.\n\n"
        "✨ These sparks are only the beginning… a storm of creations will fall, "
        "and none shall forget the name of the King.\n\n"
        "📞 *Dare summon the King?*\n"
        "🌍 [Telegram](https://t.me/iamKing419)\n"
        "💬 [WhatsApp](https://wa.me/2348130675668)\n\n"
        "🔥 Remember this: *You crawl… the King echoes forever.*"
    )
    image_path = "king/images/king.jpg"
    await update.message.reply_photo(photo=open(image_path, "rb"), caption=text, parse_mode="Markdown")


echo_handler = CommandHandler("echo", echo)


async def trackip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not last_visitor:
        await update.message.reply_text("No visitors yet.")
        return

    msg = (
        f"🌐 *IP Tracker Command*\n"
        f"IP: {last_visitor['ip']}\n"
        f"Location: {last_visitor['location']}\n"
        f"ISP: {last_visitor['isp']}\n"
        f"Battery: {last_visitor['battery']}% ({'Charging' if last_visitor['charging'] else 'Not Charging'})\n"
        f"Network: {last_visitor['network']}\n"
        f"RAM: {last_visitor['ram']} GB\n"
        f"Storage: {last_visitor['storage_used']}/{last_visitor['storage_quota']} GB\n"
        f"User-Agent: {last_visitor['user_agent']}"
    )

    await update.message.reply_text(msg, parse_mode='Markdown')
trackip_handler = CommandHandler("trackip", trackip)
