from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import requests
import asyncio
import os
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from ai_brain import get_ai_reply, detect_hot_lead
from voice_handler import voice_note_to_text, text_to_voice_note, download_whatsapp_media
from booking import save_lead, get_all_leads, update_lead_status
from notifications import send_hot_lead_alert
from config import WHATSAPP_TOKEN, VERIFY_TOKEN, PHONE_NUMBER_ID, DASHBOARD_USER, DASHBOARD_PASS, SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=8)
CORS(app)

# ── Auth Decorator ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def api_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# ── Pages ──────────────────────────────────────────────────────
@app.route('/login')
def login_page():
    if session.get('logged_in'):
        return redirect('/')
    return send_from_directory('../frontend', 'login.html')

@app.route('/login', methods=['POST'])
def do_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if username == DASHBOARD_USER and password == DASHBOARD_PASS:
        session.permanent = True
        session['logged_in'] = True
        session['user'] = username
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
@login_required
def dashboard():
    return send_from_directory('../frontend', 'index.html')

# ── WhatsApp Webhook ───────────────────────────────────────────
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid token', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        entry   = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value   = changes.get('value', {})
        messages = value.get('messages', [])
        if not messages:
            return jsonify({'status': 'no message'}), 200

        message        = messages[0]
        customer_phone = message['from']
        msg_type       = message['type']
        contact_info   = value.get('contacts', [{}])[0]
        customer_name  = contact_info.get('profile', {}).get('name', 'Customer')

        if msg_type == 'text':
            user_text = message['text']['body']
            ai_reply  = get_ai_reply(customer_phone, user_text, customer_name)
            send_whatsapp_text(customer_phone, ai_reply)
            status = 'Hot' if detect_hot_lead(user_text) else 'Warm'
            save_lead(customer_name, customer_phone, user_text, status)
            if status == 'Hot':
                send_hot_lead_alert(customer_name, customer_phone, user_text)

        elif msg_type == 'audio':
            media_id  = message['audio']['id']
            audio_file = download_whatsapp_media(media_id, WHATSAPP_TOKEN)
            user_text  = voice_note_to_text(audio_file)
            ai_reply   = get_ai_reply(customer_phone, user_text, customer_name)
            voice_file = asyncio.run(text_to_voice_note(ai_reply))
            send_whatsapp_voice(customer_phone, voice_file)
            send_whatsapp_text(customer_phone, f"_{ai_reply}_")
            save_lead(customer_name, customer_phone, f"[Voice] {user_text}", 'Warm')

        elif msg_type == 'image':
            caption  = message.get('image', {}).get('caption', 'Sent an image')
            ai_reply = get_ai_reply(customer_phone, f"Customer sent an image: {caption}", customer_name)
            send_whatsapp_text(customer_phone, ai_reply)

    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
    return jsonify({'status': 'ok'}), 200

# ── WhatsApp Helpers ───────────────────────────────────────────
def send_whatsapp_text(to, message):
    url     = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}', 'Content-Type': 'application/json'}
    data    = {'messaging_product': 'whatsapp', 'to': to, 'type': 'text', 'text': {'body': message}}
    try:
        logger.info(f"Attempting to send text to {to}...")
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        logger.info(f"Successfully sent! Meta API Response: {res.json()}")
    except Exception as e:
        logger.error(f"Failed to send text to {to}. Error: {e}")
        if 'res' in locals(): logger.error(f"Meta Graph Details: {res.text}")

def send_whatsapp_voice(to, audio_path):
    try:
        headers    = {'Authorization': f'Bearer {WHATSAPP_TOKEN}'}
        upload_url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/media"
        with open(audio_path, 'rb') as f:
            res = requests.post(upload_url, headers=headers,
                files={'file': ('reply.mp3', f, 'audio/mpeg')},
                data={'messaging_product': 'whatsapp'})
            res.raise_for_status()
        media_id = res.json().get('id')
        if not media_id: return
        url  = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        data = {'messaging_product': 'whatsapp', 'to': to, 'type': 'audio', 'audio': {'id': media_id}}
        r2 = requests.post(url, headers=headers, json=data)
        r2.raise_for_status()
        logger.info(f"Successfully sent voice to {to}")
    except Exception as e:
        logger.error(f"Voice send error: {e}")
        if 'res' in locals(): logger.error(rf"Meta Graphic Details: {res.text}")

# ── API Endpoints ──────────────────────────────────────────────
@app.route('/api/leads', methods=['GET'])
@api_login_required
def api_leads():
    return jsonify(get_all_leads())

@app.route('/api/leads/<phone>/status', methods=['PUT'])
@api_login_required
def api_update_lead(phone):
    update_lead_status(phone, request.json.get('status'))
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
@api_login_required
def api_stats():
    leads     = get_all_leads()
    today     = datetime.now().strftime('%Y-%m-%d')
    return jsonify({
        'total':     len(leads),
        'hot':       sum(1 for l in leads if l.get('status') == 'Hot'),
        'warm':      sum(1 for l in leads if l.get('status') == 'Warm'),
        'converted': sum(1 for l in leads if l.get('status') == 'Converted'),
        'today':     sum(1 for l in leads if l.get('date','').startswith(today))
    })

@app.route('/api/broadcast', methods=['POST'])
@api_login_required
def api_broadcast():
    message = request.json.get('message')
    leads   = get_all_leads()
    sent    = 0
    for lead in leads:
        phone = lead.get('phone')
        if phone:
            send_whatsapp_text(phone, message)
            sent += 1
    return jsonify({'sent': sent})

@app.route('/api/followup/<phone>', methods=['POST'])
@api_login_required
def api_followup(phone):
    name    = request.json.get('name', 'there')
    message = f"Hi {name}! 😊 Aria here from FLUW. Just checking if you had any questions about our services! We'd love to help your business grow online. 🚀"
    send_whatsapp_text(phone, message)
    return jsonify({'success': True})

@app.route('/api/me', methods=['GET'])
@api_login_required
def api_me():
    return jsonify({'user': session.get('user')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
