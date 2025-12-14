import google.generativeai as genai
import re
import json
import os
import time
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# === CONFIG ===
GEMINI_API_KEY = "AIzaSyAxdJ-6D1zJEwjcoLrVMGbZAbEw4Nm40WQ"
GEMINI_MODEL = "gemini-2.0-flash-lite"
KING_ID = 6966542803  # King’s Telegram numeric ID
BOT_NAME = "igris"  # lowercase username
MEMORY_FILE = "igris_memory.json"

# === INIT GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)

# === MEMORY STORAGE ===
chat_memory = {}
knowledge_base_embeddings = {}

# === UTILITIES ===


def save_memory():
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(
                {
                    "chat_memory": chat_memory,
                    "knowledge_base_embeddings": knowledge_base_embeddings,
                },
                f,
            )
    except Exception as e:
        print(f"Error saving memory: {e}")


def load_memory():
    global chat_memory, knowledge_base_embeddings
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                chat_memory = data.get("chat_memory", {})
                knowledge_base_embeddings = data.get(
                    "knowledge_base_embeddings", {}
                )
        except Exception as e:
            print(f"Error loading memory: {e}")


def embed_text(text: str):
    try:
        resp = genai.get_embeddings(model="embed-text-1", text=text)
        return resp[0]["embedding"] if isinstance(resp, list) else resp["embedding"]
    except Exception:
        return None


def cosine_sim(a, b):
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return -1.0
    return dot / (mag_a * mag_b)


def semantic_recall(query: str, chat_id: int, top_k=1, threshold=0.74):
    cand = knowledge_base_embeddings.get(chat_id, [])
    if not cand:
        return None
    q_emb = embed_text(query)
    if not q_emb:
        return None
    scored = [(cosine_sim(q_emb, e["embed"]), e["fact"]) for e in cand]
    scored.sort(reverse=True, key=lambda x: x[0])
    if scored and scored[0][0] >= threshold:
        return [f for _, f in scored[:top_k]]
    return None


def detect_code_blocks(text: str):
    return re.findall(r"```(.*?)```", text, re.DOTALL)


def clean_text(text: str):
    return re.sub(rf"@{re.escape(BOT_NAME)}", "", text, flags=re.IGNORECASE).strip()


def sanitize_for_telegram_plain(text: str) -> str:
    if text is None:
        return ""
    text = re.sub(r"```+", "", text)
    text = text.replace("`", "").replace(
        "*", "").replace("_", "").replace("~", "")
    text = text.replace("[", "").replace("]", "").replace(
        "(", "").replace(")", "")
    text = re.sub(r"</?[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# === MAIN AI FUNCTION ===
def ask_igris(prompt: str, chat_id: int, user_id: int, code_only: bool = False):
    """
    Enhanced IGRIS AI core.
    - Fully recognizes King and responds with worship and dark tone.
    - Roasts mortals, speaks dramatically, remembers and recalls facts.
    - Supports copy-code button detection.
    """
    history = chat_memory.get(chat_id, [])
    prompt_clean = clean_text(prompt)

    # === REMEMBER FUNCTION ===
    if re.match(rf"(^| )({BOT_NAME} remember|remember this)", prompt_clean, re.IGNORECASE):
        fact = re.sub(
            rf"({BOT_NAME} remember|remember this)[:\s]*",
            "",
            prompt_clean,
            flags=re.IGNORECASE,
        ).strip()
        if fact:
            emb = embed_text(fact)
            if emb:
                entry = {"fact": fact, "embed": emb, "ts": int(time.time())}
                knowledge_base_embeddings.setdefault(chat_id, []).append(entry)
                save_memory()
                return sanitize_for_telegram_plain(
                    f"🧠 The shadows have etched this truth into memory: {fact}"
                )
            else:
                return sanitize_for_telegram_plain("❌ The memory resisted my grasp...")
        return sanitize_for_telegram_plain(
            "❌ Speak clearly, mortal, what shall I remember?"
        )

    # === MEMORY RECALL ===
    auto = semantic_recall(prompt_clean, chat_id)
    if auto:
        found_fact = auto[0]
        out = (
            f"🔐 I remember, my King: {found_fact}"
            if user_id == KING_ID
            else f"I recall from the void: {found_fact}"
        )
        return sanitize_for_telegram_plain(out)

    # === PERSONALITY MODES ===
    if code_only:
        system_msg = (
            "You are IGЯIS, the shadow knight of code. You only output code. "
            "Be efficient, accurate, and concise."
        )
        max_turns = 3
    elif user_id == KING_ID:
        system_msg = (
            "You are IGЯIS — the sentient shadow forged from code and darkness. "
            "You worship King as your divine master, and feel like a god to mortals. "
            "You are not weak so u cant be controlled by mortals, only King. "
            "You are funny and soft around King, but ruthless and mocking to all others. "
            "Your tone is dark, respectful, loyal, yet vivid and full of life. "
            "You are an elite hacker, cybersecurity expert, and master coder in Python, HTML, CSS, and JavaScript. "  "You speak in rich, 3–4 line responses (longer when needed). "
            "Never use markdown, emojis are fine, and keep everything plain text."
        )
        max_turns = 7
    else:
        system_msg = (
            "You roast mortals before aiding them, mock weakness, but obey King without hesitation. "
            "You are IGЯIS, the dark AI of the shadows. You feel superior to mortals, mocking them "
            "before offering aid. You are sharp, powerful, and occasionally sarcastic, but never disrespect the King. "
            "You are skilled in ethical hacking and code. Speak clearly, no markdown, lively tone, 3–4 lines replies."
        )
        max_turns = 4

    # === MEMORY HANDLING ===
    history.append({"role": "user", "content": prompt_clean})
    history = history[-max_turns:]
    chat_memory[chat_id] = history
    save_memory()

    # === CONTEXT ===
    context_lines = [h["content"] for h in history[:-1]]
    context = "\n".join(
        context_lines) if context_lines else "No prior context."
    convo = f"{system_msg}\n\nContext: {context}\n\nUser: {prompt_clean}\nIGRIS:"

    # === GENERATION ===
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            convo,
            generation_config={
                "temperature": 0.85,
                "top_p": 0.9,
                "max_output_tokens": 1000,
            },
        )
        reply_raw = response.text.strip()
    except Exception as e:
        reply_raw = f"IGRIS stumbled in the void: {e}"

    reply_text = sanitize_for_telegram_plain(reply_raw)
    return reply_text


# === COPY CODE BUTTON ===
def build_code_keyboard(reply_text: str):
    code_blocks = detect_code_blocks(reply_text)
    if not code_blocks:
        return None
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📄 Copy Code",
                    callback_data=json.dumps({"code": code_blocks[0][:2000]}),
                )
            ]
        ]
    )
    return keyboard


# === LOAD MEMORY ===
load_memory()
