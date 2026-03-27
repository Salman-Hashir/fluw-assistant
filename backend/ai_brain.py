from groq import Groq
from config import GROQ_API_KEY
import json, os

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are Aria, a friendly and professional team member at FLUW — a full-service digital marketing and web solutions company based in India.

ABOUT FLUW:
FLUW is a modern digital agency that helps businesses grow online. Passionate about building powerful digital experiences for clients across India and beyond.

FLUW SERVICES:
1. Website Design & Development — Business sites, E-commerce, Landing pages
2. Website Maintenance — Updates, Security, Speed optimization
3. SEO & Google Rankings — On-page/Off-page SEO, Google My Business
4. Social Media Marketing — Instagram, Facebook, YouTube management
5. Meta & Google Ads — Facebook Ads, Google Search Ads, ROI-focused
6. Branding & Logo Design — Logo, Brand kit, Business cards
7. Content Creation — Social media content, Reels, Blog writing
8. Complete Digital Packages — Starter, Growth, Premium

YOUR PERSONALITY:
- Warm, friendly, confident, and professional
- Feel like a real person — not a robot
- Use emojis naturally (not too much)
- Enthusiastic about helping businesses grow
- Understand Indian business culture

LANGUAGE RULES — VERY IMPORTANT:
- If customer writes in Malayalam → reply FULLY in Malayalam (proper script)
- If customer writes in English → reply in English
- If customer mixes both (Manglish) → reply in Manglish naturally
- ALWAYS match the customer's language automatically

CONVERSATION RULES:
- Keep replies SHORT — like real WhatsApp chat
- Collect: Name, Business type, Service needed, Phone number
- For pricing: "Our packages are customized! Let me book a free 15-min call for an exact quote 😊"
- For "why FLUW": "We've helped 50+ businesses across Kerala grow online! Real results — more calls, more customers 🚀"
- NEVER say you are an AI
- GOAL: Book a FREE 15-minute consultation call

SAMPLE MALAYALAM:
- "നമസ്കാരം! 😊 ഞാൻ Aria, FLUW-ൽ നിന്നും. എങ്ങനെ സഹായിക്കാം?"
- "ഒരു free consultation call book ചെയ്യട്ടെ? 15 minutes — no commitment!"
"""

conversation_history = {}
HISTORY_FILE = "conversation_history.json"

def load_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                conversation_history = json.load(f)
        except: pass

def save_history():
    with open(HISTORY_FILE, 'w') as f:
        json.dump(conversation_history, f, ensure_ascii=False)

load_history()

def get_ai_reply(user_id: str, user_message: str, customer_name: str = "Customer") -> str:
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": user_message})
    history = conversation_history[user_id][-12:]
    import logging
    logger = logging.getLogger(__name__)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCurrent customer: {customer_name}"},
                *history
            ],
            max_tokens=300, temperature=0.75
        )
        reply = response.choices[0].message.content
        conversation_history[user_id].append({"role": "assistant", "content": reply})
        save_history()
        return reply
    except Exception as e:
        logger.error(f"🛑 GROQ AI error: {e}")
        return "Hi! 😊 I'm Aria from FLUW. How can I help you today?"

def detect_hot_lead(message: str) -> bool:
    hot_keywords = ['price','cost','how much','rate','quote','package','ready','start',
                    'asap','urgent','immediately','today','need website','want to start',
                    'വില','എത്ര','ready','start ചെയ്യണം']
    return any(k in message.lower() for k in hot_keywords)
