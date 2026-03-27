import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN    = os.getenv("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID   = os.getenv("PHONE_NUMBER_ID", "")
VERIFY_TOKEN      = os.getenv("VERIFY_TOKEN", "fluw_secret_2024")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
TEAM_PHONE_NUMBER = os.getenv("TEAM_PHONE_NUMBER", "")

# Dashboard Login
DASHBOARD_USER    = os.getenv("DASHBOARD_USER", "fluw_admin")
DASHBOARD_PASS    = os.getenv("DASHBOARD_PASS", "fluw@2024")
SECRET_KEY        = os.getenv("SECRET_KEY", "fluw-super-secret-key-change-this")
