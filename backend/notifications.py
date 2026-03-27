import requests, logging
from datetime import datetime
from config import WHATSAPP_TOKEN, PHONE_NUMBER_ID, TEAM_PHONE_NUMBER
logger = logging.getLogger(__name__)

def send_whatsapp_text(to, message):
    url     = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}', 'Content-Type': 'application/json'}
    data    = {'messaging_product': 'whatsapp', 'to': to, 'type': 'text', 'text': {'body': message}}
    try: requests.post(url, headers=headers, json=data)
    except Exception as e: logger.error(f"Send error: {e}")

def send_hot_lead_alert(name, phone, message):
    if not TEAM_PHONE_NUMBER: return
    alert = f"🔥 *HOT LEAD — FLUW*\n\n👤 {name}\n📱 {phone}\n💬 {message}\n⏰ {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\nReply NOW! ⚡"
    send_whatsapp_text(TEAM_PHONE_NUMBER, alert)
