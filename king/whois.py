import whois
import socket


def run_whois(domain_or_url: str) -> str:
    """
    Returns WHOIS info + resolved IP for a given domain.
    Automatically strips http:// or https:// if present.
    """
    try:
        # Clean domain
        domain = domain_or_url.replace(
            "http://", "").replace("https://", "").split("/")[0]

        # Fetch WHOIS info
        w = whois.whois(domain)
        ip = socket.gethostbyname(domain)

        # Build terminal-style output
        response = f"""
[ IGRIS WHOIS SCAN ]
────────────────────────────
Domain       : {w.domain}
IP Address   : {ip}
Registrar    : {w.registrar}
Creation Date: {w.creation_date}
Expiration   : {w.expiration_date}
Name Servers : {w.name_servers}
Status       : {w.status}
────────────────────────────
Scan Complete ✅
"""
        return response

    except Exception as e:
        return f"[ERROR] Could not fetch info for {domain_or_url}: {e}"
