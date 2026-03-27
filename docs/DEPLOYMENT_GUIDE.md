# FLUW AI Assistant v2 — Complete Deployment Guide
## 100% Free | Secure Login | Fully Responsive

---

## 📋 WHAT'S NEW IN V2
- ✅ Secure login page (username + password)
- ✅ Session-based authentication (Flask)
- ✅ Fully responsive — Phone, Tablet, PC
- ✅ All API endpoints protected
- ✅ Auto-redirect to login if not authenticated

---

## 🔐 DEFAULT LOGIN CREDENTIALS
```
Username: fluw_admin
Password: fluw@2024
```
⚠️ CHANGE THESE before deploying! Set your own in environment variables.

---

## STEP 1 — GET GROQ API KEY (Free)
1. Go to https://groq.com → Sign up free
2. Dashboard → API Keys → Create Key → Name: "FLUW"
3. Copy key (starts with gsk_...)
📊 Free limit: 14,400 requests/day

---

## STEP 2 — WHATSAPP CLOUD API (Free)
1. Go to https://developers.facebook.com
2. My Apps → Create App → Business → WhatsApp → Set up
3. WhatsApp → API Setup → Copy:
   - Access Token → WHATSAPP_TOKEN
   - Phone Number ID → PHONE_NUMBER_ID
📊 Free limit: 1,000 conversations/month

---

## STEP 3 — PUSH TO GITHUB
1. Create private repo at github.com
2. Upload entire fluw-assistant folder
3. Confirm structure:
   fluw-assistant/
   ├── backend/
   │   ├── main.py
   │   ├── ai_brain.py
   │   ├── voice_handler.py
   │   ├── booking.py
   │   ├── notifications.py
   │   ├── config.py
   │   ├── requirements.txt
   │   └── .env.example
   ├── frontend/
   │   ├── index.html    (dashboard)
   │   └── login.html    (login page)
   ├── Procfile
   ├── render.yaml
   └── README.md

---

## STEP 4 — DEPLOY ON RENDER.COM (Free)
1. Go to render.com → Sign in with GitHub
2. New + → Web Service → Connect your repo
3. Settings:
   - Build Command: pip install -r backend/requirements.txt
   - Start Command: gunicorn --chdir backend main:app
   - Plan: FREE
4. Click Advanced → Add these environment variables:

   WHATSAPP_TOKEN      = (from Step 2)
   PHONE_NUMBER_ID     = (from Step 2)
   VERIFY_TOKEN        = fluw_secret_2024
   GROQ_API_KEY        = (from Step 1)
   TEAM_PHONE_NUMBER   = 91XXXXXXXXXX
   DASHBOARD_USER      = fluw_admin
   DASHBOARD_PASS      = YourStrongPassword123
   SECRET_KEY          = any-long-random-string-here

5. Click "Create Web Service"
6. Wait 3-5 min → Copy your URL

---

## STEP 5 — CONNECT WHATSAPP WEBHOOK
1. Meta Developer Console → WhatsApp → Configuration
2. Webhook URL: https://YOUR-APP.onrender.com/webhook
3. Verify Token: fluw_secret_2024
4. Subscribe to: messages
5. Save

---

## STEP 6 — KEEP AWAKE 24/7 (Free)
Render free tier sleeps after 15 min inactivity.

Fix with UptimeRobot (free):
1. Go to uptimerobot.com → Sign up free
2. Add New Monitor → HTTP(s)
3. URL: https://YOUR-APP.onrender.com
4. Interval: Every 5 minutes
5. Save ✅

Your bot now runs 24/7 for ₹0!

---

## STEP 7 — ACCESS YOUR DASHBOARD
Open: https://YOUR-APP.onrender.com
Login with your username and password.

Dashboard features:
- 📊 Live stats (total, hot, warm, converted leads)
- 👥 All leads table with search & filter
- 📢 Broadcast messages to all leads
- 🤖 Airah AI capabilities view
- ⚙️ Setup guide built-in

---

## 🔐 CHANGING YOUR PASSWORD
Update these environment variables in Render dashboard:
- DASHBOARD_USER = your_username
- DASHBOARD_PASS = your_new_password
- SECRET_KEY     = new-random-secret-string

Then click "Save Changes" → App will restart with new credentials.

---

## 📱 RESPONSIVE SUPPORT
The dashboard works perfectly on:
- 📱 Mobile phones (320px+)
- 📟 Tablets (768px+)
- 💻 Laptops & PCs (1024px+)

---

## 🔧 TROUBLESHOOTING

Bot not replying?
→ Check Render logs for errors
→ Verify all env vars are set
→ Check webhook is subscribed to "messages"

Login not working?
→ Check DASHBOARD_USER and DASHBOARD_PASS env vars
→ Redeploy after updating env vars

Session expiring too fast?
→ Session lasts 8 hours by default
→ Modify timedelta in main.py if needed

Malayalam voice not clear?
→ Change model = whisper.load_model("small") in voice_handler.py
→ Redeploy

---

## 💰 TOTAL MONTHLY COST: ₹0

| Service        | Free Limit              |
|----------------|-------------------------|
| Groq API       | 14,400 requests/day     |
| WhatsApp API   | 1,000 conversations/mo  |
| Render.com     | 750 hours/month         |
| UptimeRobot    | 50 monitors free        |
| GitHub         | Unlimited private repos |

---

Built for FLUW Digital Agency 🚀
