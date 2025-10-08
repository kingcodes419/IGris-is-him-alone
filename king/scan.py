from telegram import Update
from telegram.ext import ContextTypes
import requests
import nmap
import random

# ---------------- King ID ----------------
KING_ID = 6966542803  # Replace with your Telegram ID

# ---------------- King Lines ----------------
KING_LINES = [
    "Mortals quake at your gaze! ⚡",
    "The shadows whisper of your supremacy… 🛡️",
    "Even the mightiest tremble before the King 👑",
    "Pathetic mortals can only watch as you strike! 🗡️",
    "Your subjects await your command, weaklings tremble! 🏰"
]

# ---------------- Mortal Mock Lines ----------------
MORTAL_LINES = [
    "Ah, a mortal dares to scan… weaklings tremble ⚡",
    "Behold your results, pathetic mortal 🗡️",
    "Your device shivers under my gaze 🛡️",
    "Even your firewall looks scared 😏",
    "Mortals can only pretend to understand these numbers 🏰"
]

# ---------------- Mortal Fun End Lines ----------------
MORTAL_END_LINES = [
    "Better luck next time, mortal 😎",
    "Go back to your tiny lair 🏚️",
    "Your network will never escape the King 👑",
    "The shadows still laugh at your weakness ⚡",
    "Mortals, be gone! 🗡️"
]


async def scanip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ---------------- Check for IP ----------------
    if not context.args:
        lines = [
            "⚠️ O Mortal, you dare summon powers without providing a target? Example: /scan 8.8.8.8",
            "⚠️ Weakling! Speak the IP to behold its secrets. Example: /scan 8.8.8.8",
            "⚠️ Mortals tremble, yet you forgot the IP! Try: /scan 8.8.8.8",
            "⚠️ Foolish mortal! The King awaits an IP to unleash your shame: /scan 8.8.8.8"
        ]
        await update.message.reply_text(random.choice(lines))
        return

    ip = context.args[0]
    is_king = update.effective_user.id == KING_ID

    # ---------------- Initial Reply ----------------
    if is_king:
        await update.message.reply_text(f"🔍 By the decree of the King, scanning `{ip}`... 🛡️")
    else:
        await update.message.reply_text(f"Scanning `{ip}`... {random.choice(MORTAL_LINES)}")

    # ---------------- Geo Info ----------------
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if geo.get("status") == "success":
            city = geo.get("city", "Unknown")
            region = geo.get("regionName", "Unknown")
            country = geo.get("country", "Unknown")
            country_code = geo.get("countryCode", "Unknown")
            lat = geo.get("lat", "Unknown")
            lon = geo.get("lon", "Unknown")
            isp = geo.get("isp", "Unknown")
            org = geo.get("org", "Unknown")
            asn = geo.get("as", "Unknown")
        else:
            city = region = country = country_code = lat = lon = isp = org = asn = "Unknown"
    except Exception:
        city = region = country = country_code = lat = lon = isp = org = asn = "Unknown"

    # ---------------- Nmap Scan ----------------
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-Pn -T4 -F')
        open_ports = []
        if ip in nm.all_hosts():
            for proto in nm[ip].all_protocols():
                for port in nm[ip][proto].keys():
                    if nm[ip][proto][port]['state'] == 'open':
                        open_ports.append(f"{port}/{proto}")
        open_ports_text = ", ".join(
            open_ports) if open_ports else "No open ports found"
    except Exception:
        open_ports_text = "Nmap scan failed"

    # ---------------- Build Message ----------------
    if is_king:
        line = random.choice(KING_LINES)
        msg = (
            f"👑 *King’s Sentinel Report*\n"
            f"{line}\n\n"
            f"🌐 *Target IP:* `{ip}`\n"
            f"🏙️ City: {city}\n"
            f"🗺️ State/Region: {region}\n"
            f"🌍 Country: {country} ({country_code})\n"
            f"📍 Latitude/Longitude: {lat}, {lon}\n"
            f"🏢 ISP: {isp}\n"
            f"🏰 Organization: {org}\n"
            f"🛡️ ASN: {asn}\n"
            f"⚔️ Open Ports: {open_ports_text}\n"
        )
    else:
        line = random.choice(MORTAL_LINES)
        end_line = random.choice(MORTAL_END_LINES)
        msg = (
            f"🌐 *IP Scan Result* 🔎\n"
            f"{line}\n\n"
            f"IP: `{ip}`\n"
            f"City: {city}\n"
            f"State/Region: {region}\n"
            f"Country: {country} ({country_code})\n"
            f"Latitude/Longitude: {lat}, {lon}\n"
            f"ISP: {isp}\n"
            f"Organization: {org}\n"
            f"ASN: {asn}\n"
            f"Open Ports: {open_ports_text}\n\n"
            f"{end_line}"
        )

    await update.message.reply_text(msg, parse_mode="Markdown")
