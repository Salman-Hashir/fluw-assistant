import json, os
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
LEADS_FILE = "leads.json"

def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f: return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, 'w') as f: json.dump(leads, f, indent=2, ensure_ascii=False)

def save_lead(name, phone, requirement, status='Warm', source='WhatsApp'):
    leads = load_leads()
    for lead in leads:
        if lead.get('phone') == phone:
            lead['last_message'] = requirement
            lead['last_seen']    = datetime.now().strftime('%Y-%m-%d %H:%M')
            if status == 'Hot': lead['status'] = 'Hot'
            save_leads(leads); return
    leads.append({'id': len(leads)+1, 'name': name, 'phone': phone,
        'requirement': requirement, 'status': status, 'source': source,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'last_message': requirement})
    save_leads(leads)

def get_all_leads():
    return sorted(load_leads(), key=lambda x: x.get('date',''), reverse=True)

def update_lead_status(phone, new_status):
    leads = load_leads()
    for lead in leads:
        if lead.get('phone') == phone:
            lead['status']  = new_status
            lead['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M'); break
    save_leads(leads)
